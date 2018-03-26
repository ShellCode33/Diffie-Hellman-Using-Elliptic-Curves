# -*- coding: utf-8 -*-

from core.mathutils import MathUtils
from random import *


class PointNotOnCurveException(Exception):
    """Raise when the point is not on the curve"""


class EllipticCurve(object):
    # Elliptic Curves examples :
    # http://www.secg.org/sec2-v2.pdf
    # https://www.legifrance.gouv.fr/affichTexte.do?cidTexte=JORFTEXT000024668816

    # Standard curves
    available_curves = [(1, 3),
                        (0xF1FD178C0B3AD58F10126DE8CE42435B3961ADBCABC8CA6DE8FCF353D86E9C00,
                         0xEE353FCA5428A9300D4ABA754A44C00FDFEC0C9AE4B1A1803075ED967B7BB73F)]

    # Corresponding standard modulus
    corresponding_modulus = [17,
                             0xF1FD178C0B3AD58F10126DE8CE42435B3961ADBCABC8CA6DE8FCF353D86E9C03]

    # Corresponding standard points
    corresponding_points = [(3, 4),
                            (0xB6B3D4C356C139EB31183D4749D423958C27D2DCAF98B70164C97A2DD98F5CFF,
                             0x6142E0F7C8B204911F9271F0F3ECEF8C2701C307E8E4C9E183115A1554062CFB)]

    # Corresponding standard points orders
    corresponding_orders = [17,
                            0xF1FD178C0B3AD58F10126DE8CE42435B53DC67E140D2BF941FFDD459C6D655E1]

    def __init__(self):
        """
        The first curve in array is the default one, you can use the method askCurveToUse() in order to choose the
        curve you want to use.
        """
        self.a = self.available_curves[0][0]
        self.b = self.available_curves[0][1]
        self.Fp = self.corresponding_modulus[0]
        self.init_point = self.corresponding_points[0]
        # self.point_order = self.find_point_order(self.init_point)
        self.point_order = self.corresponding_orders[0]
        self.__gen_keys()

    def __str__(self):
        return "y² = x³ + " + str(self.a) + "x + " + str(self.b)

    def isPointValid(self, point):
        """
        Check either a point is valid or not

        :param point: the point to check
        :return: True or False
        """
        if point is None:  # point at infinity
            return True  # This point is a valid one

        # Checks that the point is on the curve
        return point[1] ** 2 % self.Fp == (point[0] ** 3 + self.a * point[0] + self.b) % self.Fp

    def addPoints(self, p1, p2):
        """
        Add two point on the curve mod Fp

        :param p1: first point
        :param p2: second point
        """
        if not self.isPointValid(p1) or not self.isPointValid(p2):
            raise PointNotOnCurveException("Point not on the curve.")

        if p1 is None:  # If p1 is the point at infinity...
            return p2  # ...then we return the other point
        if p2 is None:  # If p2 is the point at infinity...
            return p1  # ...then we return the other point

        if p1 == p2:  # 2P
            if p1[1] == 0:
                return None  # point at infinity

            lmbda = (3 * (p2[0] ** 2) + self.a) * MathUtils.modinv((2 * p2[1]) % self.Fp, self.Fp)

        else:  # P + Q
            if p1[0] == p2[0]:
                return None  # point at infinity

            lmbda = (p2[1] - p1[1]) * MathUtils.modinv((p2[0] - p1[0]) % self.Fp, self.Fp)

        lmbda %= self.Fp
        x = lmbda ** 2 - p2[0] - p1[0]
        y = lmbda * (p1[0] - x) - p1[1]

        return x % self.Fp, y % self.Fp

    def fast_exp(self, n, point):
        """
        Fast algorithm to multiply n times the point

        :param n:
        :param point:
        :return: result point of the multiplication
        """
        if not self.isPointValid(point):
            raise PointNotOnCurveException("Point not on the curve.")

        P = None  # point at infinity

        if n < 0:
            n = -n
            point = MathUtils.symetric(point)

        while n != 0:
            if n % 2 == 1:
                P = self.addPoints(P, point)

            n = n // 2
            point = self.addPoints(point, point)

        return P

    def __gen_keys(self):
        """
        This method creates the public and private key
        """
        self.private_key = randint(1, self.point_order - 1)
        self.public_key = self.fast_exp(self.private_key, self.init_point)

    def find_point_order(self, point):
        """
        Find the point order, this method is very slow with big numbers. The best way to do is to hardcode its value

        :param point:
        :return: the point order
        """
        current = point
        order = 1

        while current is not None:  # While this is not the point at infinity...
            current = self.addPoints(current, point)
            order += 1

        return order

    def askCurveToUse(self):
        """
        This method will ask the user which of the standard curves he wants to use
        """
        print("-------------------------------------")

        for curve_index in range(len(self.available_curves)):
            self.a = self.available_curves[curve_index][0]
            self.b = self.available_curves[curve_index][1]
            print(str(curve_index + 1) + ": " + str(self))

        try:
            choosen_curve = int(input("Which curve do you want to use ? [default 1] : "))

            if choosen_curve < 1 or choosen_curve > len(self.available_curves):
                raise ValueError("Choosen curve doesn't exist.")

            choosen_curve -= 1  # Shift to list index

        except ValueError:
            print("Invalid curve id. Default will be used.")
            choosen_curve = 0

        self.a = self.available_curves[choosen_curve][0]
        self.b = self.available_curves[choosen_curve][1]
        self.Fp = self.corresponding_modulus[choosen_curve]
        self.init_point = self.corresponding_points[choosen_curve]
        # self.point_order = self.find_point_order(self.init_point)
        self.point_order = self.corresponding_orders[choosen_curve]
        self.__gen_keys()  # We regenerate the keys according to the new parameters
