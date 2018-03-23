from mathutils import MathUtils

class PointNotOnCurveException(Exception):
    '''Raise when the point is not on the curve'''


class EllipticCurve(object):

    # Recommanded EC : http://www.secg.org/sec2-v2.pdf

    # Courbes standardisées
    available_curves = [(1, 3), # custom
                        (0xF1FD178C0B3AD58F10126DE8CE42435B3961ADBCABC8CA6DE8FCF353D86E9C00, 0xEE353FCA5428A9300D4ABA754A44C00FDFEC0C9AE4B1A1803075ED967B7BB73F)] # https://www.legifrance.gouv.fr/affichTexte.do?cidTexte=JORFTEXT000024668816

    # Modulos standardisés correspondants
    corresponding_modulus = [17,
                            0xF1FD178C0B3AD58F10126DE8CE42435B3961ADBCABC8CA6DE8FCF353D86E9C03]

    # Points standardisés correspondants
    corresponding_points = [(3, 4),
                            (0xB6B3D4C356C139EB31183D4749D423958C27D2DCAF98B70164C97A2DD98F5CFF, 0x6142E0F7C8B204911F9271F0F3ECEF8C2701C307E8E4C9E183115A1554062CFB)]

    # Ordres des points standardisés
    corresponding_orders = [17,
                            0xF1FD178C0B3AD58F10126DE8CE42435B53DC67E140D2BF941FFDD459C6D655E1]

    # First curve in array is the default one
    def __init__(self):
        self.a = self.available_curves[0][0]
        self.b = self.available_curves[0][1]
        self.setField(self.corresponding_modulus[0])
        self.init_point = self.corresponding_points[0]
        #self.point_order = self.find_point_order(self.init_point)
        self.point_order = self.corresponding_orders[0]

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
            choosen_curve = 0

        self.a = self.available_curves[choosen_curve][0]
        self.b = self.available_curves[choosen_curve][1]
        self.setField(self.corresponding_modulus[choosen_curve])
        self.init_point = self.corresponding_points[choosen_curve]
        #self.point_order = self.find_point_order(self.init_point)
        self.point_order = self.corresponding_orders[choosen_curve]
