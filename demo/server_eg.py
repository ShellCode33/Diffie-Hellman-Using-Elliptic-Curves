#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, os
os.chdir(os.path.dirname(os.path.realpath(__file__))) # Set working directory to the script location
sys.path.append('..') # Add parent directory to the path in order to import modules

from socket import *
from algorithms.elgamal import ElGamal
import pickle

BUFFER_SIZE = 4096

if __name__ == "__main__":

    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(("localhost", 1337))
    s.listen(1)

    print("Waiting for client...")
    conn, addr = s.accept()
    print("Client connected.")

    eg = ElGamal()
    eg.askCurveToUse()
    print("Sending public key to client...")

    # On envoie la clé publique au client, ATTENTION : l'authentification n'est pas garantie !! Un MITM est possible.
    # C'est juste pour l'exemple, pour montrer que le chiffrement/déchiffrement fonctionne
    conn.send(pickle.dumps(eg.getPublicKey()))

    cipher = pickle.loads(conn.recv(BUFFER_SIZE))
    print("Cipher received: " + str(cipher))
    plaintext = eg.decrypt(cipher)
    print("Received: " + str(plaintext))

    conn.close()
    s.close()
