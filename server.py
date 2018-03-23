#!/usr/bin/python3
# -*- coding: utf-8 -*-

from socket import *
from diffiehellman import DiffieHellman
from elgamal import ElGamal
import pickle

BUFFER_SIZE = 4096

if __name__ == "__main__":

    s = socket(AF_INET, SOCK_STREAM)
    s.bind(("localhost", 1337))
    s.listen(1)

    print("Waiting for client...")
    conn, addr = s.accept()
    print("Client connected.")

    # dh = DiffieHellman()
    # dh.askCurveToUse()
    # data = conn.recv(BUFFER_SIZE)
    # if not data: exit()
    # dh_parameter = pickle.loads(data)
    # print("DH remote parameter: ", dh_parameter)
    # dh.completeDiffieHellmanExchange(dh_parameter) # Attention au pickle.loads() qui peut entrainer une vulnérabilité, utilisé ici tel quel pour l'exemple
    # conn.send(pickle.dumps(dh.getParameterToSend()))


    eg = ElGamal()
    eg.askCurveToUse()
    print("Sending public key to client...")
    conn.send(pickle.dumps(eg.getPublicKey())) # On envoie la clé publique au client, ATTENTION : l'authentification n'est pas garantie !! Un MITM est possible. C'est juste pour l'exemple, pour montrer que le chiffrement/déchiffrement fonctionne
    cipher = pickle.loads(conn.recv(BUFFER_SIZE))
    print("Cipher received: " + str(cipher))
    plaintext = eg.decrypt(cipher)
    print("Received: " + str(plaintext))

    conn.close()
    s.close()
