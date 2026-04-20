
#!/usr/bin/env python3
from pwn import *
import re
import socket
import time

HOST = "154.57.164.82"
PORT = 30840

r = remote(HOST, PORT)

# Start game
r.recvuntil(b"> ")
r.sendline(b"1")

def solve_round():
    players = {}
    
    while True:
        line = r.recvline().decode()

        # Player dice line
        if "Player" in line and ":" in line:
            parts = line.strip().split(":")
            player_id = int(parts[0].split()[1])
            dices = list(map(int, parts[1].strip().split()))
            players[player_id] = sum(dices)

        # Question reached
        if "Who wins this round?" in line:
            break

    # skip menu lines (1. Player1 etc.)
    for _ in range(len(players)):
        r.recvline()

    r.recvuntil(b"> ")

    # find winner (max sum, if tie → highest player id)
    max_score = max(players.values())
    winners = [p for p, s in players.items() if s == max_score]
    answer = max(winners)

    r.sendline(str(answer).encode())

    resp = r.recvline().decode()
    return "Correct" in resp


# Play all rounds
for i in range(100):
    if not solve_round():
        print("Failed at round", i)
        exit()

# Print flag
print(r.recvall().decode())
