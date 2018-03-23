from ellipticcurve import EllipticCurve

class ElGamal(EllipticCurve):

    def __init__(self):
        super().__init__()
        #TODO : convert msg to msg point
        pass

    def __initElGamalParameters(self):
        self.private_key = randint(1, self.point_order-1)#trouver le poitn P au préalable
        self.public_key = self.fast_exp(self.private_key, self.init_point)#Pareil ajouter le point P


    def setRemotePublicKey(self, public_key):
        self.remote_public_key = public_key


    def encrypt(self, msg):
        self.coef_k = randint(1, self.point_order)
        self.c1 = self.fast_exp(self.coef_k, self.init_point)#Pareil le point P
        self.c2 = self.addPoints(msg, self.fast_exp(self.coef_k, self.remote_public_key))
        return self.c1, self.c2


    def decrypt(self, cipher):
        self.decrypt_step_one = self.fast_exp(cipher[0], self.private_key)
        self.decrypted_message = self.addPoints(cipher[1], MathUtils.symetric(self.decrypt_step_one))
        return self.decrypted_message


    def askCurveToUse(self):
        super().askCurveToUse()
        self.__initElGamalParameters()
