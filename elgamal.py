from ellipticcurve import EllipticCurve

class ElGamal(EllipticCurve):

    def __init__(self):

        pass

    def __initElGamalParameters(self, M):
        self.private_Key_A = randint(1, self.find_point_order(M)-1)#trouver le poitn P au préalable
        self.public_Key_A = self.fast_exp(self.private_Key_A, M)#Pareil ajouter le point P
        self.message = self.fast_exp(randint(1, self.find_point_order(M)-1), M)#M doit appartenir au groupe engendré par P

    def encrypt(self, M):
        self.private_Key_B = randint(1, self.find_point_order())
        self.c1 = self.fast_exp(self.private_Key_B, )#Pareil le point P
        self.c2 = self.addPoints(M, self.fast_exp(self.private_Key_B, self.public_Key_A))
        self.encrypted_message = self.addPoints(self.c1, self.c2)
        return self.encrypted_message

    def decrypt(self, M):
        self.decrypt_step_one = self.fast_exp(self.private_Key_B, self.public_Key_A)
        self.decrypted_message = self.addPoints(self.c1, self.decrypt_step_one)
        return self.decrypted_message

    def askCurveToUse(self):
        super().askCurveToUse()
        self.__initElGamalParameters()

    def completeElGamal(self, M):
        self.askCurveToUse()
        self.
