# -*- coding: utf-8 -*-

from core.ellipticcurve import EllipticCurve
import hashlib
import pickle
from random import *


class DiffieHellman(EllipticCurve):

    def __init__(self):
        super(DiffieHellman, self).__init__()
        self.__initDiffieHellmanParameters()

    def __initDiffieHellmanParameters(self):
        """
        This method creates the Diffie Hellman parameters
        """
        self.dh_random = randint(0, self.point_order - 1)
        self.dh_param = self.fast_exp(self.dh_random, self.init_point)

    def getParameterToSend(self):
        """
        Getter
        :return: Diffie Hellman parameter to be sent over the network
        """
        return self.dh_param

    def askCurveToUse(self):
        """
        Overriding EllipticCurve's method in order to init ElGamal parameters after
        """
        super(DiffieHellman, self).askCurveToUse()
        self.__initDiffieHellmanParameters()

    def completeDiffieHellmanExchange(self, B):
        """
        Completes the DH exchange and calculate the secret key thanks to the parameter B
        :param B: sent over the network by the person you're communicating with
        """
        secret_key = self.fast_exp(self.dh_random, B)
        print("sha1(secret_key) = " + hashlib.sha1(pickle.dumps(secret_key)).hexdigest())
