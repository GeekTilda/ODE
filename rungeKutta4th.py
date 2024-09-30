from decimal import Decimal, getcontext
import math

def rungeKutta4th(f, x0, y0, u0, h, xend, tol):
    n = int((xend - x0) / h)  # Antal steg

    x = x0
    y = y0
    u = u0

    for i in range(n):
        # Steg i Runge-Kutta algoritmen
        k1 = f(x, y, u)
        k2 = f(x + h/2, y + h*k1[0]/2, u + h*k1[1]/2)
        k3 = f(x + h/2, y + h*k2[0]/2, u + h*k2[1]/2)
        k4 = f(x + h, y + h*k3[0], u + h*k3[1])

        # Uppdatera y och u (y = position, u = hastighet)
        y_new = y + h*(k1[0] + 2*k2[0] + 2*k3[0] + k4[0]) / 6
        u_new = u + h*(k1[1] + 2*k2[1] + 2*k3[1] + k4[1]) / 6

        x = x + h
        y = y_new
        u = u_new

        # Kontrollera när y passerar 0 för att få π
        if y_new < 0:
            if abs(2*x - Decimal(math.pi)) < tol:
                print(2*x)
                return 2*x
            else:
                h = h/2
