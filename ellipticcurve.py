from mathutils import MathUtils

class PointNotOnCurveException(Exception):
    '''Raise when the point is not on the curve'''


class EllipticCurve(object):

    # Courbes standardisées
    available_curves = [(1, 3),
                        (1, 442)]

    # Modulos standardisés correspondants
    corresponding_modulus = [   17,
                                509]

    # Points standardisés correspondants
    corresponding_points = [(3, 4),
                            (4, 1)]

    # First curve in array is the default one
    def __init__(self):
        self.a = self.available_curves[0][0]
        self.b = self.available_curves[0][1]
        self.setField(self.corresponding_modulus[0])
        self.init_point = self.corresponding_points[0]
        self.point_order = self.find_point_order(self.init_point)

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


    def askCurveToUse(self):
        print("-------------------------------------")
        
        for curve_index in range(len(self.available_curves)):
            self.a = self.available_curves[curve_index][0]
            self.b = self.available_curves[curve_index][1]
            print(str(curve_index+1) + ": " + str(self))

        try:
            choosen_curve = int(input("Which curve do you want to use ? [default 1] : "))

            if choosen_curve < 1 or choosen_curve > len(self.available_curves):
                raise ValueError("Choosen curve doesn't exist.")

            choosen_curve -= 1 # Replace dans le tableau

        except ValueError:
            print("Invalid curve id. Default will be used.")
            choosen_curve = 1

        self.a = self.available_curves[choosen_curve][0]
        self.b = self.available_curves[choosen_curve][1]
        self.setField(self.corresponding_modulus[choosen_curve])
        self.init_point = self.corresponding_points[choosen_curve]
        self.point_order = self.find_point_order(self.init_point)
