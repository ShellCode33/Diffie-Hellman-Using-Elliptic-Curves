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
    s.connect(("localhost", 1337))

    eg = ElGamal()
    eg.askCurveToUse()
    public_key = pickle.loads(s.recv(BUFFER_SIZE))

    # On recoit la clé publique du client, ATTENTION : l'authentification n'est pas garantie !! Un MITM est possible.
    # C'est juste pour l'exemple, pour montrer que le chiffrement/déchiffrement fonctionne
    eg.setRemotePublicKey(public_key)

    print("Received public key of server")
    cipher = eg.encrypt("Salut ca va ? Moi ca va très bien ma foi ! Je fais aller :) Nickel.")
    print("Sending encrypted message to server...")
    s.send(pickle.dumps(cipher))

    s.close()
