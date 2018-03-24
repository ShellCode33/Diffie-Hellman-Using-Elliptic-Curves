# -*- coding: utf-8 -*-


class MathUtils(object):

    @staticmethod
    def egcd(a, b):
        """
        Extended Euclidean algorithm
        :param a
        :param b
        """
        if a == 0:
            return b, 0, 1
        else:
            g, y, x = MathUtils.egcd(b % a, a)
            return g, x - (b // a) * y, y

    @staticmethod
    def modinv(a, m):
        """
        Modular inverse calculation
        :param a: the number we want to inverse
        :param m: the modulus
        """
        g, x, y = MathUtils.egcd(a, m)
        if g != 1:
            print("a: " + str(a) + " ; m: " + str(m) + " ; g: " + str(g))
            raise Exception('Modular inverse does not exist')
        else:
            return x % m

    @staticmethod
    def symetric(point):
        """
        :param point
        :return: Symetric of the point
        """
        return point[0], -point[1]

    @staticmethod
    def numberToBase(num, base):
        """
        Convert a number into digits list of specified base
        :param num
        :param base
        :return: a list of digits
        """
        if num == 0:
            return [0]
        digits = []
        while num:
            digits.append(int(num % base))
            num //= base
        return digits[::-1]

    @staticmethod
    def baseToNumber(digits, base):
        """
        Convert a list of digits into a number of specified base
        :param digits
        :param base
        :return: a number
        """
        if len(digits) == 1:
            return digits[0]
        else:
            return digits[-1] + base * MathUtils.baseToNumber(digits[:-1], base)
