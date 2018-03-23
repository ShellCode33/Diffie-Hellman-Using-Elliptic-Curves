#!/usr/bin/python3
# -*- coding: utf-8 -*-

from socket import *
from diffiehellman import DiffieHellman
import pickle

BUFFER_SIZE = 4096

if __name__ == "__main__":

    dh = DiffieHellman()
    dh.askCurveToUse()

    s = socket(AF_INET, SOCK_STREAM)
    s.connect(("localhost", 1337))
    s.send(pickle.dumps(dh.getParameterToSend()))
    dh_parameter = pickle.loads(s.recv(BUFFER_SIZE))
    print("Received parameter: ", dh_parameter)
    dh.completeDiffieHellmanExchange(dh_parameter) # Attention au pickle.loads() qui peut entrainer une vulnérabilité, utilisé ici tel quel pour l'exemple
    s.close()
