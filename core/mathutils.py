# -*- coding: utf-8 -*-


class MathUtils(object):

    @staticmethod
    def egcd(a, b):
        if a == 0:
            return b, 0, 1
        else:
            g, y, x = MathUtils.egcd(b % a, a)
            return g, x - (b // a) * y, y

    @staticmethod
    def modinv(a, m):
        g, x, y = MathUtils.egcd(a, m)
        if g != 1:
            print("a: " + str(a) + " ; m: " + str(m) + " ; g: " + str(g))
            raise Exception('Modular inverse does not exist')
        else:
            return x % m

    @staticmethod
    def symetric(point):
        return point[0], -point[1]

    @staticmethod
    def numberToBase(num, base):
        if num == 0:
            return [0]
        digits = []
        while num:
            digits.append(int(num % base))
            num //= base
        return digits[::-1]

    @staticmethod
    def baseToNumber(digits, base):
        if len(digits) == 1:
            return digits[0]
        else:
            return digits[-1] + base * MathUtils.baseToNumber(digits[:-1], base)
