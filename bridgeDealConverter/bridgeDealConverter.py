#!/usr/bin/env python3.8

import sys, json, re


I = int(sys.argv[1], 16)
K = int("0xAD55E315634DDA658BF49200",16)

N, E, S, W = 13, 13, 13, 13
C = 52

# cards = A K Q J T 9 8 7 6 5 4 3 2
cards="AKQJT98765432"

# suits [spades, hearts, diamonds, clubs]
suits = [[(52-4*i) for i in range(13)], [(51-4*i) for i in range(13)], [(50-4*i) for i in range(13)], 
[(49-4*i) for i in range(13)]]

suits[0].insert(0,"S")
suits[1].insert(0,"H")
suits[2].insert(0,"C")
suits[3].insert(0,"D")

# north, east, south, west
seats = [["N"], ["E"], ["S"], ["W"]]

deck = ["" for i in range(52)]

for C in range(52, 0, -1):
    X = K*N/C

    if I < K*N/C and N > 0:
        X = K*N/C
        # print("C=",C ,"; N=",N, "K*N/C=", X)
        N = N-1
        K = X
        deck[C-1]="N"
        seats[0].append(C)
 
    elif I < K*(N+E)/C and E > 0:
        I = I - K*N/C
        X = K*E/C
        # print("C=",C ,"; E=",E, "K*E/C=", X)
        E = E-1
        K = X
        deck[C-1]="E"
        seats[1].append(C)
        
    elif I < K*(N+E+S)/C and S > 0:
        I = I - K*(N+E)/C
        X = K*S/C
        # print("C=",C ,"; S=",S, "K*S/C=", X)
        S = S-1
        K = X
        deck[C-1]="S"
        seats[2].append(C)

    elif I < K*(N+E+S+W)/C and W > 0:
        I = I - K*(N+E+S)/C
        X = K*W/C
        # print("C=",C ,"; W=",W, "K*W/C=", X)
        W = W-1
        K = X
        deck[C-1]="W"
        seats[3].append(C)

    else:
        print(".")
        
# formats
# single string
#   N:.AT87.A852.943.Q6 E:.QJ.KJ93.QJ7.J752 S:.K6432.4.KT652.83 W:.95.QT76.A8.AKT94
# key/value
#     

# oneliner
# cycle the seats
A = ["" for i in range(4)]
B = {}
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
    #print(A[k])
    B[seats[k][0]] = re.sub(r'^.{3}','',A[k]) 
 
# print(*A)
print(json.dumps(B))
