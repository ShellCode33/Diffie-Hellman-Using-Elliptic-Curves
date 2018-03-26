#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

os.chdir(os.path.dirname(os.path.realpath(__file__)))  # Set working directory to the script location
sys.path.append('..')  # Add parent directory to the path in order to import modules

from socket import *
from algorithms.dsa import DSA
import pickle
import hashlib

BUFFER_SIZE = 4096

if __name__ == "__main__":

    # Creates the socket and listen to incomming connections
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(("localhost", 1337))
    s.listen(1)

    # Initialises DSA class and asks to the user which curve he wants to use
    dsa = DSA("Hello world!")
    dsa.askCurveToUse()
    signature = dsa.sign()

    print("Waiting for client...")
    conn, addr = s.accept()
    print("Client connected.")

    # Send the public key and the signature
    # Sends the public key. In this example, the server is not authentificated,
    # MITM is possible and the public key could be hijacked.
    conn.send(pickle.dumps(dsa.public_key))
    print("Public key is sent.")
    conn.send(pickle.dumps(signature))
    print("Signature is sent.")

    conn.close()
    s.close()
