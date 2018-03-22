from MathUtils import MathUtils

class PointNotOnCurveException(Exception):
    '''Raise when the point is not on the curve'''
    

class EllipticCurve(object):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return "y² = x³ + " + str(self.a) + "x + " + str(self.b)

    def getCoef(self):
        return self.a, self.b

    def setField(self, p):
        self.Fp = p

    def getField(self):
        return self.Fp

    def isPointValid(self, point):

        if point == None:   # Point à l'infini
            return True     # Le point est forcément valide

        return point[1]**2 % self.Fp == (point[0]**3 + self.a * point[0] + self.b) % self.Fp # Vérifie que le point est sur la courbe


    def addPoints(self, p1, p2):

        if not self.isPointValid(p1) or not self.isPointValid(p2):
            raise PointNotOnCurveException("Point not on the curve.")

        if p1 == None:  # Si p1 est le point à l'infini...
            return p2   # ...alors on renvoie l'autre point
        if p2 == None:  # Si p2 est le point à l'infini...
            return p1   # ...alors on renvoie l'autre point

        if p1 == p2: # 2P
            if p1[1] == 0:
                return None # Point à l'infini

            λ = ( 3 * (p2[0] ** 2) + self.a ) * MathUtils.modinv( (2 * p2[1]) % self.Fp, self.Fp)

        else: # P + Q
            if p1[0] == p2[0]:
                return None # Point à l'infini

            λ = (p2[1] - p1[1]) * MathUtils.modinv((p2[0] - p1[0]) % self.Fp, self.Fp)

        λ %= self.Fp
        x = λ ** 2 - p2[0] - p1[0]
        y = λ * (p1[0] - x) - p1[1]

        return (x % self.Fp, y % self.Fp)


    def fast_exp(self, n, point):

        if not self.isPointValid(point):
            raise PointNotOnCurveException("Point not on the curve.")

        P = None # point à l'infini

        if n < 0:
            n = -n
            point = MathUtils.symetric(point)

        while n != 0:
            if n%2 == 1:
                P = self.addPoints(P, point)

            n = n // 2
            point = self.addPoints(point, point)

        return P


    def find_point_order(self, point):

        current = point
        order = 1

        while current != None: # Tant que ca n'est pas le point à l'infini...
            current = self.addPoints(current, point)
            order += 1

        return order
