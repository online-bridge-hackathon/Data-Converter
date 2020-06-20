from common import LHO, RHO, PARTNER, SIDE
import re


def rotate(player):
    index = "SWNE".index(player)
    return "SWNE"[index:] + "SWNE"[:index]

def dump_hand(hand):
    return ".".join(
        "".join(
            card[1]
            for card in sorted(
                (card for card in hand if card[0] == suit),
                key=lambda card: ("CDHS".index(card[0]), "23456789TJQKA".index(card[1])),
                reverse=True
            )
        ) for suit in "SHDC"
    )

def dump_deal(hands, first="S"):
    return first + ":" + " ".join(
        dump_hand(hands[direction]) for direction in rotate(first)
    )

def dump_auction(auction):
    calls = []

    for i, call in enumerate(auction):
        if i % 4 == 0:
            calls.append([])
        calls[-1].append(call[0])

    return "\n".join(
        " ".join(
            call for call in line
        ) for line in calls
    )


def dump_play(plays, first):
    tricks = []

    for i, play in enumerate(plays):
        if i % 4 == 0:
            tricks.append(dict(S="-", W="-", N="-", E="-"))

        tricks[-1][play[0]] = play[1]

    rotated = rotate(first)
    return "\n".join(
        " ".join(trick[player] for player in rotated) for trick in tricks
    )


def dump_board(board):
    contract = board["contract"]
    leader = LHO[board["declarer"]]
    risk = contract["risk"] if contract["risk"] else ""
    play_state = CardPlayState()
    play_state.reset(board["deal"], board["declarer"], contract["denomination"][0])
    for card in board["play"]:
        play_state.play(card)

    return "".join([
        '[Dealer "', board["dealer"], '"]\n',
        '[Vulnerable "', board["vulnerable"], '"]\n',
        '[Deal "', dump_deal(board["deal"], board["dealer"]), '"]\n',
        '[Declarer "', board["declarer"], '"]\n',
        '[Contract "', str(contract["level"]), contract["denomination"], risk, '"]\n',
        '[Result "', str(board["result"]) if board["result"] is not None else "", '"]\n',
        '[Auction "', board["dealer"], '"]\n',
        dump_auction(board["auction"]), "\n" if len(board["auction"]) > 0 else "",
        '[Play "', leader, '"]\n',
        dump_play(play_state.plays, leader)
    ])


def parse_pbn(s):
    s = re.sub(r"{[^}]*}(\r?\n)?", "", s)

    data = []

    for board in re.split(r"\r?\n\s*\r?\n", s):
        if board:
            try:
                data.append(parse_board(board))
            except:
                continue

    for (i, (strings, _)) in enumerate(data):
        for tag in strings:
            if strings[tag] == "#" and i > 0:
                strings[tag] = data[i - 1][0][tag]

    return data


def parse_board(s):
    strings = dict()
    blocks = dict()

    for line in s.splitlines():
        if line[0] == "[" and not line.startswith("[Note "):
            tag, string = line.strip("[]").split(" ", 1)
            strings[tag] = string.strip('"')
        elif line[0] != "%":
            blocks.setdefault(tag, [])
            blocks[tag].append(line)

    return strings, blocks


def parse_deal(s):
    deal = dict(S=[], W=[], N=[], E=[])

    for player, hand in zip(rotate(s[0]), s[2:].split(" ")):
        if hand != "-":
            for suit, ranks in zip("SHDC", hand.split(".")):
                for rank in ranks:
                    deal[player].append(suit + rank)

    return deal


def parse_play(lines, first):
    tricks = []

    for line in lines:
        trick = dict()
        player = first

        for item in line.split():
            if item[0] in "=^":
                continue

            if item[0] in "CDHS":
                trick[player] = item

            player = dict(zip("SWNE", "WNES"))[player]

        if trick:
            tricks.append(trick)

        if len(trick) < 4:
            break

    return tricks


def parse_auction(lines):
    calls = []
    alerts = dict()

    for line in lines:
        if line[0] == "[":
            string = line.strip("[]").split(" ", 1)[1]
            key, alert = string.strip('"').split(":", 1)
            alerts[key] = alert
        else:
            for item in line.split():
                if item[0] == "=":
                    calls[-1] = calls[-1][0], item.strip("=")
                elif item != "-":
                    call = item.capitalize() if item.capitalize() == "Pass" else item
                    if call == "AP":
                        calls.extend([("Pass", None)] * 3)
                    else:
                        calls.append((call, None))

    return [(call, alerts[key] if key else "") for (call, key) in calls]


def parse_contract(s):
    m = re.match(r"([1-7])([SHDC]|NT)(XX?)?", s)
    return dict(level=int(m.group(1)), denomination=m.group(2), risk=m.group(3)) if m else None

def parse_pbn_string(pbn_string):
    """
    Convert a pbn string to a list of dictionaries. Does not currently copy all possible
    information that can be found in a pbn.
    """

    boards = []
    for strings, blocks in parse_pbn(pbn_string):
        if "Contract" in strings and strings["Contract"].capitalize() != "Pass":
            boards.append({
                "event": strings.get("Event"),
                "board": strings.get("Board"),
                "dealer": strings.get("Dealer"),
                "vulnerable": strings.get("Vulnerable"),
                "deal": parse_deal(strings["Deal"]) if "Deal" in strings else None,
                "declarer": strings.get("Declarer"),
                "contract": (
                    parse_contract(strings["Contract"]) if "Contract" in strings else None
                ),
                "result": strings.get("Result"),
                "auction": (
                    parse_auction(blocks["Auction"]) if "Auction" in blocks else []
                ),
                "play": (
                    parse_play(blocks["Play"], strings["Play"]) if "Play" in blocks else []
                )
            })

    return boards
