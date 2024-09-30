import math
from decimal import Decimal, getcontext

getcontext().prec = 25

x0 = Decimal(0)
y0 = Decimal(1)
u0 = Decimal(0)
h = Decimal(0.001)
tol = Decimal(1e-20)

xPrev = x0
yPrev = y0
uPrev = u0

# Definiera funktionen som representerar systemet y'' = -y
def dudx6(x, y, u):
    dydx = u    # u = y'
    dudx = -y   # y'' = -y
    return dydx, dudx

while (True):
    x = xPrev
    y = yPrev
    u = uPrev
    while(True):
        # Steg i Runge-Kutta algoritmen
        k1 = dudx6(x, y, u)
        k2 = dudx6(x + h/2, y + h*k1[0]/2, u + h*k1[1]/2)
        k3 = dudx6(x + h/2, y + h*k2[0]/2, u + h*k2[1]/2)
        k4 = dudx6(x + h, y + h*k3[0], u + h*k3[1])

        xPrev = x
        yPrev = y
        uPrev = u

        # Uppdatera x, y och u
        x = x + h
        y = y + h*(k1[0] + 2*k2[0] + 2*k3[0] + k4[0]) / 6
        u = u + h*(k1[1] + 2*k2[1] + 2*k3[1] + k4[1]) / 6

        # Kontrollera när y passerar 0 för att få π
        if y < 0:
            print(2*x)
            if abs(2*x - Decimal(math.pi)) < tol:
                print(2*x)
                break
            else:
                h = h/2
                break

'''
3.14159265358979323846
'''