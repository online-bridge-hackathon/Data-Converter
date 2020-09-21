#!/usr/bin/env python3.8

import json
from sys import argv
from re import sub

# deal supplied as an argument for conversion
I = int(argv[1], 16)

output = argv[2]

# Total number of possible deals = 52!/(13!)^4
K = int("0xAD55E315634DDA658BF49200",16)

# initialising suits and card counts
N, E, S, W = 13, 13, 13, 13
C = 52

# cards = A K Q J T 9 8 7 6 5 4 3 2
cards="AKQJT98765432"

# suits [spades, hearts, diamonds, clubs]
suits = [[(52-4*i) for i in range(13)], [(51-4*i) for i in range(13)], [(50-4*i) for i in range(13)], [(49-4*i) for i in range(13)]]

# initialise the suits
suits[0].insert(0,"S")
suits[1].insert(0,"H")
suits[2].insert(0,"D")
suits[3].insert(0,"C")

# initialise the seats: north, east, south, west
seats = [["N"], ["E"], ["S"], ["W"]]

# initialize the deck which is SA, HA, DA, CA, SK, HK, DK, CK, SQ, .... etc
deck = ["" for i in range(52)]

#
# Algorithm as explained by Richard Pavlicek
# http://www.rpbridge.net/7z68.htm
#
# map the UUID into the deck, where the SA position (0) is replaced by the seat that holds it
# Example = ["N", "E", "E", "S", "W", .....etc]
for C in range(52, 0, -1):
    X = K*N/C
    # is this card Norths?
    if I < K*N/C and N > 0:
        X = K*N/C
        # print("C=",C ,"; N=",N, "K*N/C=", X)
        N = N-1
        K = X
        deck[C-1]="N"
        seats[0].append(C)
    # ...Easts?
    elif I < K*(N+E)/C and E > 0:
        I = I - K*N/C
        X = K*E/C
        # print("C=",C ,"; E=",E, "K*E/C=", X)
        E = E-1
        K = X
        deck[C-1]="E"
        seats[1].append(C)
    # ...South's?
    elif I < K*(N+E+S)/C and S > 0:
        I = I - K*(N+E)/C
        X = K*S/C
        # print("C=",C ,"; S=",S, "K*S/C=", X)
        S = S-1
        K = X
        deck[C-1]="S"
        seats[2].append(C)
    # ...West's?
    elif I < K*(N+E+S+W)/C and W > 0:
        I = I - K*(N+E+S)/C
        X = K*W/C
        # print("C=",C ,"; W=",W, "K*W/C=", X)
        W = W-1
        K = X
        deck[C-1]="W"
        seats[3].append(C)

    else:
        print(".")  # not needed if the elif cases are done correctly

# formats
# single string
#   N:.AT87.A852.943.Q6 E:.QJ.KJ93.QJ7.J752 S:.K6432.4.KT652.83 W:.95.QT76.A8.AKT94
# key/value
B = {}

# Human (readable)
B["human"] = {}
# PBN
B["pbn"] = {}
B["pbn"][0] = "Deal"
# RBN (Richard's Bridge Notation) - http://www.rpbridge.net/7a12.htm
B["rbn"] = {}
B["rbn"][0] = "H"
# LIN
B["lin"] = {}
# B["lin"][0] = "H"


# cycle the seats
A = ["" for i in range(4)]
# special array for LIN as they have suit names before 
L = ["" for i in range(4)]

for k in range(4):
    suit = ["" for i in range(4)]
    # suits
    A[k] = ''.join([seats[k][0],":"])
    for j in range(4):
        suit[j]=""
        for i in range(1,14):
            try:
                suit[j] += cards[suits[j].index(seats[k][i])-1]
            except ValueError:
                a = ""
        A[k] = A[k] + "." + suit[j]
        L[k] = L[k] + suits[j][0] + suit[j]
    B["human"][seats[k][0]] = sub(r'^.{3}','',A[k])
    B["pbn"][seats[k][0]] = sub(r'^.{3}','',A[k])
    B["lin"][seats[k][0]] = L[k]

B["pbn"][1] = ''.join(["N:",B["pbn"]["N"],' ',B["pbn"]["E"],' ',B["pbn"]["S"],' ',B["pbn"]["N"]])
B["rbn"][1] = ''.join(["N:",B["pbn"]["N"],':',B["pbn"]["E"],':',B["pbn"]["S"],':',B["pbn"]["N"]])
B["lin"][1] = ','.join([B["lin"]["S"],B["lin"]["W"],B["lin"]["N"],B["lin"]["E"]])

# print formats

b = ""
if output == "human":
    b = B["human"]
elif output == "pbn":
    b = {B["pbn"][0]:B["pbn"][1]}
elif output == "rbn":
    b = {B["rbn"][0]:B["rbn"][1]}
elif output == "lin":
    b = {"md":B["lin"][1]}

print({
    'statusCode': 200,
    'body': json.dumps(b)
})