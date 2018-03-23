from ellipticcurve import EllipticCurve
import hashlib
import pickle
from random import *

class DiffieHellman(EllipticCurve):

    def __init__(self):
        super().__init__()
        self.__initDiffieHellmanParameters()


    def __initDiffieHellmanParameters(self):
        self.dh_random = randint(0, self.point_order-1)
        self.dh_param = self.fast_exp(self.dh_random, self.init_point)


    def getParameterToSend(self):
        return self.dh_param


    def askCurveToUse(self):
        super().askCurveToUse()
        self.__initDiffieHellmanParameters()


    # Permet d'utiliser le paramètre envoyé par la personne avec qui on souhaite échanger afin de générer la clé secrète
    def completeDiffieHellmanExchange(self, B):
        self.secret_key = self.fast_exp(self.dh_random, B)
        print("sha1(secret_key) = " + hashlib.sha1(pickle.dumps(self.secret_key)).hexdigest())
