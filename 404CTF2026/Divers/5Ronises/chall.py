from time import time
from random import randint, seed
from hashlib import sha256
from functools import reduce
import os

def set_seed():
    seed(int(time()))

def matmul(A, B):
    Bt = list(zip(*B))
    return [[sum(a * b for a, b in zip(row, col)) for col in Bt] for row in A]

def genere_nombre_super_secret(n):
    A = [[randint(0, pow(2, 64)) for _ in range(n)] for _ in range(n)]
    
    for i in range(pow(2, 10)):
        A = matmul(A, A)
        A = [[y % pow(2, 64) for y in x] for x in A]

    base = reduce(lambda x, y: x ^ y, [reduce(lambda x, y: x ^ y, row) for row in A])

    hashed = sha256(hex(base).encode()).hexdigest()
    return int(hashed, 16)

def main():
    set_seed()

    print("On va jouer à un jeu. Devine mon nombre secret et je te donne le flag !")
    guess = input("> ")

    secret = genere_nombre_super_secret(8)
    if int(guess) == secret:
        print(f"Wow ! Voici le flag : {os.getenv("FLAG", "404CTF{Fake_Flag}")}")
    else:
        print(f"Et non, mon nombre c'était : {secret}")

if __name__ == "__main__":
    main()