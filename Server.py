#!/usr/bin/python3
# -*- coding: utf-8 -*-

from socket import *
from DiffieHellman import DiffieHellman
import pickle

BUFFER_SIZE = 4096

if __name__ == "__main__":

    dh = DiffieHellman()
    dh.askCurveToUse()

    s = socket(AF_INET, SOCK_STREAM)
    s.bind(("localhost", 1337))
    s.listen(1)

    conn, addr = s.accept()

    print("Client connected.")

    data = conn.recv(BUFFER_SIZE)
    if not data: exit()
    dh_parameter = pickle.loads(data)
    print("Received parameter: ", dh_parameter)
    dh.completeDiffieHellmanExchange(dh_parameter) # Attention au pickle.loads() qui peut entrainer une vulnérabilité, utilisé ici tel quel pour l'exemple
    conn.send(pickle.dumps(dh.getParameterToSend()))

    conn.close()
    s.close()
