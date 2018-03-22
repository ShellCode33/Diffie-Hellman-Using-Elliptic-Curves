class MathUtils(object):
    # From https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = MathUtils.egcd(b % a, a)
            return (g, x - (b // a) * y, y)


    def modinv(a, m):
        g, x, y = MathUtils.egcd(a, m)
        if g != 1:
            print("a: " + str(a) + " ; m: " + str(m) + " ; g: " + str(g))
            raise Exception('Modular inverse does not exist')
        else:
            return x % m


    def symetric(point):
        return (point[0], -point[1])
