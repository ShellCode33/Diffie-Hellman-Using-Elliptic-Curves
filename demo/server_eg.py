#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

os.chdir(os.path.dirname(os.path.realpath(__file__)))  # Set working directory to the script location
sys.path.append('..')  # Add parent directory to the path in order to import modules

from socket import *
from algorithms.elgamal import ElGamal
import pickle

BUFFER_SIZE = 4096

if __name__ == "__main__":

    # Creates the socket and listen to incomming connections
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(("localhost", 1337))
    s.listen(1)

    print("Waiting for client...")
    conn, addr = s.accept()
    print("Client connected.")

    # Initialises ElGamal class and asks to the user which curve he wants to use
    eg = ElGamal()
    eg.askCurveToUse()
    print("Sending public key to client...")

    # Sends the public key. In this example, the server is not authentificated,
    # MITM is possible and the public key could be hijacked.
    conn.send(pickle.dumps(eg.getPublicKey()))

    # Receives cipher sent by the client.
    # Be careful with pickle.loads() it can lead to serious security issues. This is only an example.
    cipher = pickle.loads(conn.recv(BUFFER_SIZE))
    print("Cipher received: " + str(cipher))

    # Decrypt cipher and print it
    plaintext = eg.decrypt(cipher)
    print("Received: " + str(plaintext))

    conn.close()
    s.close()
