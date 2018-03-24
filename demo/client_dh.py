#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

os.chdir(os.path.dirname(os.path.realpath(__file__)))  # Set working directory to the script location
sys.path.append('..')  # Add parent directory to the path in order to import modules

from socket import *
from algorithms.diffiehellman import DiffieHellman
import pickle
import hashlib

BUFFER_SIZE = 4096

if __name__ == "__main__":

    # Creates the socket in order to connect to the server
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(("localhost", 1337))

    # Initialises DiffieHellman class and asks to the user which curve he wants to use
    dh = DiffieHellman()
    dh.askCurveToUse()

    # Sends the DH parameter to the server
    s.send(pickle.dumps(dh.getParameterToSend()))

    # Receives server's DH parameter
    # Be careful with pickle.loads() it can lead to serious security issues. This is only an example.
    dh_parameter = pickle.loads(s.recv(BUFFER_SIZE))
    print("Received parameter: ", dh_parameter)

    # Computes the dh parameter received and outputs the secret key
    secret_key = dh.completeDiffieHellmanExchange(dh_parameter)
    print("sha1(secret_key) = " + hashlib.sha1(pickle.dumps(secret_key)).hexdigest())

    s.close()
