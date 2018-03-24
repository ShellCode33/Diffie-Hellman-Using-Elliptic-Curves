#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

os.chdir(os.path.dirname(os.path.realpath(__file__)))  # Set working directory to the script location
sys.path.append('..')  # Add parent directory to the path in order to import modules

from socket import *
from algorithms.diffiehellman import DiffieHellman
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

    dh = DiffieHellman()
    dh.askCurveToUse()
    data = conn.recv(BUFFER_SIZE)
    # Attention au pickle.loads() qui peut entrainer une vulnérabilité, utilisé ici tel quel pour l'exemple
    dh_parameter = pickle.loads(data)
    print("DH remote parameter: ", dh_parameter)
    dh.completeDiffieHellmanExchange(dh_parameter)
    conn.send(pickle.dumps(dh.getParameterToSend()))

    conn.close()
    s.close()
