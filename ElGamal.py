from EllipticCurve import EllipticCurve
from random import *

class ElGamal(object):

    def __init__(self):

        pass

    def __initParameters(self):
        self.privateKeyA = randint(1, self.find_point_order())#trouver le poitn P au préalable
        self.publicKeyA = fast_exp(self.privateKey, )#Pareil ajouter le point P
        self.message = #M doit appartenir au groupe engendré par P

    def encrypt(self):
        self.privateKeyB = randint(1, self.find_point_order())
        self.c1 = fast_exp(self.privateKeyB, )#Pareil le point P
        self.c2 =
        pass

    def decrypt(self):
        pass
