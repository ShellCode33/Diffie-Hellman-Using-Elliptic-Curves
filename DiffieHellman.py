from EllipticCurve import EllipticCurve
import hashlib
import pickle
from random import *

class DiffieHellman(object):

    # Courbes standardisées
    available_curves = [EllipticCurve(1, 3),
                        EllipticCurve(1, 442)]

    # Modulos standardisés correspondants
    corresponding_modulus = [   17,
                                509]

    # Points standardisés correspondants
    corresponding_points = [(3, 4),
                            (4, 1)]


    def __init__(self):
        self.curve = self.available_curves[0]
        self.curve.setField(self.corresponding_modulus[0])
        self.point = self.corresponding_points[0]
        self.point_order = self.curve.find_point_order(self.point)
        self.__initDiffieHellmanParameters()


    def __initDiffieHellmanParameters(self):
        self.a = randint(0, self.point_order-1)
        self.A = self.curve.fast_exp(self.a, self.point)


    def getParameterToSend(self):
        return self.A


    def askCurveToUse(self):
        print("-------------------------------------")
        for curve_index in range(len(self.available_curves)):
            print(str(curve_index+1) + ": " + str(self.available_curves[curve_index]))

        try:
            choosen_curve = int(input("Which curve do you want to use ? [default 1] : "))

            if choosen_curve < 1 or choosen_curve > len(self.available_curves):
                raise ValueError("Choosen curve doesn't exist.")

            choosen_curve -= 1 # Replace dans le tableau

        except ValueError:
            print("Invalid curve id. Default will be used.")
            choosen_curve = 1

        self.curve = self.available_curves[choosen_curve]
        self.curve.setField(self.corresponding_modulus[choosen_curve])
        self.point = self.corresponding_points[choosen_curve]
        self.point_order = self.curve.find_point_order(self.point)
        self.__initDiffieHellmanParameters()


    # Permet d'utiliser le paramètre envoyé par la personne avec qui on souhaite échanger afin de générer la clé secrète
    def completeDiffieHellmanExchange(self, B):
        self.secret_key = self.curve.fast_exp(self.a, B)
        print("sha1(secret_key) = " + hashlib.sha1(pickle.dumps(self.secret_key)).hexdigest())
