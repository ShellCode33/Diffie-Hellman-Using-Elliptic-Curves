from ellipticcurve import EllipticCurve

class ElGamal(EllipticCurve):

    def __init__(self, msg):
        #TODO : convert msg to msg point
        pass

    def __initElGamalParameters(self, msg_point):
        self.private_key = randint(1, self.point_order(msg_point)-1)#trouver le poitn P au préalable
        self.private_key = self.fast_exp(self.private_key, msg_point)#Pareil ajouter le point P
        self.message = self.fast_exp(randint(1, self.point_order(msg_poin)-1), msg_point)#M doit appartenir au groupe engendré par P

    def encrypt(self, msg_point):
        self.coef_k = randint(1, self.point_order(msg_point))
        self.c1 = self.fast_exp(self.coef_k, )#Pareil le point P
        self.c2 = self.addPoints(msg_point, self.fast_exp(self.coef_k, self.private_key))
        self.encrypted_message = self.addPoints(self.c1, self.c2)
        return self.encrypted_message

    def decrypt(self, msg_point):
        self.decrypt_step_one = self.fast_exp(self.coef_k, self.private_key)
        self.decrypted_message = self.addPoints(self.c1, self.decrypt_step_one)
        return self.decrypted_message

    def askCurveToUse(self):
        super().askCurveToUse()
        self.__initElGamalParameters()

    def completeElGamal(self, msg_point):
        self.askCurveToUse()
        self.
