#!/usr/bin/python3
# -*- coding: utf-8 -*-

from socket import *
from diffiehellman import DiffieHellman
from elgamal import ElGamal
import pickle

BUFFER_SIZE = 4096

if __name__ == "__main__":

    s = socket(AF_INET, SOCK_STREAM)
    s.connect(("localhost", 1337))

    # dh = DiffieHellman()
    # dh.askCurveToUse()
    # s.send(pickle.dumps(dh.getParameterToSend()))
    # dh_parameter = pickle.loads(s.recv(BUFFER_SIZE))
    # print("Received parameter: ", dh_parameter)
    # dh.completeDiffieHellmanExchange(dh_parameter) # Attention au pickle.loads() qui peut entrainer une vulnérabilité, utilisé ici tel quel pour l'exemple

    eg = ElGamal()
    eg.askCurveToUse()
    public_key = pickle.loads(s.recv(BUFFER_SIZE))
    eg.setRemotePublicKey(public_key) # On envoie la clé publique au client, ATTENTION : l'authentification n'est pas garantie !! Un MITM est possible. C'est juste pour l'exemple, pour montrer que le chiffrement/déchiffrement fonctionne
    print("Received public key of server")
    cipher = eg.encrypt((3, 4))
    print("Sending encrypted message to server...")
    s.send(pickle.dumps(cipher))

    s.close()
