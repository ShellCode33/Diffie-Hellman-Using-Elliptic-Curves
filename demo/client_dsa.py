#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

os.chdir(os.path.dirname(os.path.realpath(__file__)))  # Set working directory to the script location
sys.path.append('..')  # Add parent directory to the path in order to import modules

from socket import *
from algorithms.dsa import DSA
import pickle

BUFFER_SIZE = 4096

if __name__ == "__main__":

    # Initialises DSA class and asks to the user which curve he wants to use
    dsa = DSA("Hello world!")
    dsa.askCurveToUse()

    # Creates the socket in order to connect to the server
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(("localhost", 1337))

    # Be careful with pickle.loads() it can lead to serious security issues. This is only an example.
    # Receives the public key. In this example, the server is not authentificated,
    # MITM is possible and the public key could be hijacked.
    public_key = pickle.loads(s.recv(BUFFER_SIZE))
    print("Received public key: ", public_key)
    dsa.setRemotePublicKey(public_key)

    data = s.recv(BUFFER_SIZE)
    signature = pickle.loads(data)
    print("Received signature: " + str(signature))
    print("Is the signature valid : " + str(dsa.checkSignature(signature)))

    s.close()
