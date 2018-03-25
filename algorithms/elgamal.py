# -*- coding: utf-8 -*-

from core.ellipticcurve import EllipticCurve
from core.mathutils import MathUtils
from random import *


class ElGamal(EllipticCurve):

    def __init__(self):
        """
        The remote public key has to be set manually using the setRemotePublicKey method.
        """
        super(ElGamal, self).__init__()
        self.remote_public_key = None
        self.__gen_keys()

    def setRemotePublicKey(self, public_key):
        """
        Public Key Setter

        :param public_key: Public key of the person we're communicating with
        """
        self.remote_public_key = public_key

    def getPublicKey(self):
        """
        Public Key Getter

        :return: self.public_key
        """
        return self.public_key

    # https://www.sciencedirect.com/science/article/pii/S1877050915013332
    def convertMessageToPointsOnCurve(self, msg):
        """
        This method turns a message into points on the curve that can be encrypted

        :param msg: The string to encrypt
        :return: The list of points representing the message
        """
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

        # this list looks like [x, y, x, y, x, y]
        return groups_big_int

    def encrypt(self, msg):
        """
        The encryption method

        :param msg: The string you want to cipher
        :return: the encrypted string
        """
        msg_points = self.convertMessageToPointsOnCurve(msg)
        msg_point = (msg_points[0], msg_points[1])
        coef_k = randint(1, self.point_order - 1)
        c1 = self.fast_exp(coef_k, self.init_point)
        c2 = self.addPoints(msg_point, self.fast_exp(coef_k, self.remote_public_key))
        return c1, c2

    def decrypt(self, cipher):
        """
        The decryption method

        :param cipher: The cipher you want to recover
        :return: The decrypted message
        """
        decrypt_step_one = self.fast_exp(self.private_key, cipher[0])
        decrypted_message = self.addPoints(cipher[1], MathUtils.symetric(decrypt_step_one))
        return decrypted_message

    def askCurveToUse(self):
        """
        Overriding EllipticCurve's method in order to init ElGamal parameters after
        """
        super(ElGamal, self).askCurveToUse()
        self.__gen_keys()
