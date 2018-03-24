# -*- coding: utf-8 -*-

from core.ellipticcurve import EllipticCurve
from core.mathutils import MathUtils
from random import *


class ElGamal(EllipticCurve):

    def __init__(self):
        super(ElGamal, self).__init__()
        self.remote_public_key = None
        self.__initElGamalParameters()

    def __initElGamalParameters(self):
        self.private_key = randint(1, self.point_order - 1)  # trouver le poitn P au préalable
        self.public_key = self.fast_exp(self.private_key, self.init_point)  # Pareil ajouter le point P

    def setRemotePublicKey(self, public_key):
        self.remote_public_key = public_key

    def getPublicKey(self):
        return self.public_key

    # https://www.sciencedirect.com/science/article/pii/S1877050915013332
    def convertMessageToPointOnCurve(self, msg):
        group_size = len(MathUtils.numberToBase(self.Fp, 65536)) - 1
        groups = []

        # Partionning ascii values
        msg_bytes = msg.encode()
        group = []
        i = 0
        while i < len(msg_bytes):
            group.append(msg_bytes[i])
            i += 1

            if i % group_size == 0:
                groups.append(group)
                group = []

        if len(group) > 0:
            groups.append(group)

        # Convert each group to one big base 65536 number
        groups_big_int = []

        for group in groups:
            groups_big_int.append(MathUtils.baseToNumber(group, 65536))

        # Pad with 32 if the number of groups is odd
        if len(groups_big_int) % 2 == 1:
            groups_big_int.append(32)

        return groups_big_int

    def encrypt(self, msg):
        msg_point = self.convertMessageToPointOnCurve(msg)
        msg_point = (msg_point[0], msg_point[1])
        coef_k = randint(1, self.point_order - 1)
        c1 = self.fast_exp(coef_k, self.init_point)
        c2 = self.addPoints(msg_point, self.fast_exp(coef_k, self.remote_public_key))
        return c1, c2

    def decrypt(self, cipher):
        decrypt_step_one = self.fast_exp(self.private_key, cipher[0])
        decrypted_message = self.addPoints(cipher[1], MathUtils.symetric(decrypt_step_one))
        return decrypted_message

    def askCurveToUse(self):
        super(ElGamal, self).askCurveToUse()
        self.__initElGamalParameters()
