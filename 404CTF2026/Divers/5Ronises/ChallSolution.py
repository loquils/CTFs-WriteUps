from time import time
from random import randint, seed
from hashlib import sha256
from functools import reduce
import os
import socket

def set_seed(times):
    seed(int(times))

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

def genere_nombre_super_secret2(n):
    A = [[randint(0, pow(2, 64)) for _ in range(n)] for _ in range(n)]
    
    for i in range(pow(2, 10)):
        A = matmul(A, A)
        A = [[y % pow(2, 64) for y in x] for x in A]

    base = reduce(lambda x, y: x ^ y, [reduce(lambda x, y: x ^ y, row) for row in A])

    hashed = sha256(hex(base).encode()).hexdigest()
    return int(hashed, 16)

def main():
    #Open the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("challenge.404ctf.fr", 10200))

    #Get the timestamp when we asked the connection to the server.
    timesLoad = int(time())
    #Define the seed with the same timestamp as the server.
    set_seed(timesLoad)

    #Generate the number.
    secret = genere_nombre_super_secret(8)

    data = s.recv(1024)
    print("Received:", repr(data))

    print("Our number : " + str(secret))
    s.sendall((str(secret) + "\n").encode())

    data = s.recv(1024)
    print("Received:", repr(data))

    print("Connection closed.")
    s.close()


if __name__ == "__main__":
    main()