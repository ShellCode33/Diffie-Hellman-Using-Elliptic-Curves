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

    # Creates the socket in order to connect to the server
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(("localhost", 1337))

    # Initialises ElGamal class and asks to the user which curve he wants to use
    eg = ElGamal()
    eg.askCurveToUse()

    # Receives server's public key
    # Be careful with pickle.loads() it can lead to serious security issues. This is only an example.
    public_key = pickle.loads(s.recv(BUFFER_SIZE))

    # Sets the remote public key we've just received. In this example, the server is not authentificated,
    # MITM is possible and the public key could be hijacked.
    eg.setRemotePublicKey(public_key)

    print("Server's public key received.")
    cipher = eg.encrypt("Salut ca va ? Moi ca va très bien ma foi ! Je fais aller :) Nickel.")

    print("Sending encrypted message to server...")
    s.send(pickle.dumps(cipher))

    s.close()
