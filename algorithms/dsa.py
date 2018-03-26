# -*- coding: utf-8 -*-

from core.ellipticcurve import EllipticCurve
from core.mathutils import MathUtils
import hashlib
from random import *


class WrongSignatureException(Exception):
    """Raise when the signature is wrong"""


class DSA(EllipticCurve):

    def __init__(self, msg):
        super(DSA, self).__init__()
        self.msg = msg
        self.remote_public_key = None

    def setRemotePublicKey(self, public_key):
        """
        Public Key Setter

        :param public_key: Public key of the person we're communicating with
        """
        self.remote_public_key = public_key

    def sign(self):
        """
        Signs a message
        :return: a point corresponding to the signature
        """
        coef_k = randint(1, self.point_order-1)
        kP = self.fast_exp(coef_k, self.init_point)
        u = kP[0] % self.point_order
        v = int(hashlib.sha256(self.msg.encode()).hexdigest(), 16) + self.private_key * u
        v = (v * MathUtils.modinv(coef_k, self.point_order)) % self.point_order

        if u == 0 or v == 0:
            return self.sign()

        return u, v

    def checkSignature(self, u_v):
        """
        Checks that the signature is valid

        :param u_v: point which represents the signature
        :return: True or False depending on the signature's validity
        """
        if u_v[0] < 1 or u_v[0] > self.point_order-1 or u_v[1] < 1 or u_v[1] > self.point_order-1:
            raise WrongSignatureException("Wrooooonnggggg")

        kP = int(hashlib.sha256(self.msg.encode()).hexdigest(), 16) * MathUtils.modinv(u_v[1], self.point_order)
        kP = self.fast_exp(kP, self.init_point)
        kQ = u_v[0] * MathUtils.modinv(u_v[1], self.point_order)
        kQ = self.fast_exp(kQ, self.remote_public_key)
        kP = self.addPoints(kP, kQ)

        if u_v[0] != kP[0] % self.point_order:
            raise WrongSignatureException("Wrooooonnggggg")

        if self.remote_public_key is None or not self.isPointValid(self.remote_public_key):
            raise WrongSignatureException("Wrooooonnggggg")

        if self.fast_exp(self.point_order, self.remote_public_key) is not None:
            raise WrongSignatureException("Wrooooonnggggg")

        return True


