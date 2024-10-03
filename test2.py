import math
from decimal import Decimal, getcontext

getcontext().prec = 100  # Öka precisionen för större intervall

x = Decimal(0)
y = Decimal(1)
u = Decimal(0)
h = Decimal(0.001)  # Steglängden
tol = Decimal(1e-20)
targetPi = Decimal(318 * math.pi)  # För att hitta roten vid 318π ≈ 1000

# Systemet y'' = -y
def dudx6(y, u):
    dydx = Decimal(u)    # y' = u
    dudx = -Decimal(y)   # y'' = -y
    return dydx, dudx

while True:
    # Runge-Kutta algoritm
    k1 = dudx6(Decimal(y), Decimal(u))
    k2 = dudx6(Decimal(y) + Decimal(h) * Decimal(k1[0]) / Decimal(2), Decimal(u) + Decimal(h) * Decimal(k1[1]) / Decimal(2))
    k3 = dudx6(Decimal(y) + Decimal(h) * Decimal(k2[0]) / Decimal(2), Decimal(u) + Decimal(h) * Decimal(k2[1]) / Decimal(2))
    k4 = dudx6(Decimal(y) + Decimal(h) * Decimal(k3[0]), Decimal(u) + Decimal(h) * Decimal(k3[1]))

    # Uppdatera x, y och u
    x = Decimal(x) + Decimal(h)
    y = Decimal(y) + Decimal(h) * (Decimal(k1[0]) + Decimal(2) * Decimal(k2[0]) + Decimal(2) * Decimal(k3[0]) + Decimal(k4[0])) / Decimal(6)
    u = Decimal(u) + Decimal(h) * (Decimal(k1[1]) + Decimal(2) * Decimal(k2[1]) + Decimal(2) * Decimal(k3[1]) + Decimal(k4[1])) / Decimal(6)

    # Kontrollera om y passerar 0 och vi är nära 318π
    if y < 0 and abs(x - targetPi) < Decimal(1e-5):
        approxPi = Decimal(2) * (Decimal(x) - Decimal(h))
        print(approxPi)
        print("Resultat för roten vid 318π:", approxPi, "±", abs(approxPi - Decimal(318 * math.pi)))
        break

    # Gör steg mindre om vi är nära roten
    if y < 0:
        # Återställ gamla värden
        x = Decimal(x) - Decimal(h)
        y = Decimal(y) - Decimal(h) * (Decimal(k1[0]) + Decimal(2) * Decimal(k2[0]) + Decimal(2) * Decimal(k3[0]) + Decimal(k4[0])) / Decimal(6)
        u = Decimal(u) - Decimal(h) * (Decimal(k1[1]) + Decimal(2) * Decimal(k2[1]) + Decimal(2) * Decimal(k3[1]) + Decimal(k4[1])) / Decimal(6)

        # Gör steglängden h mindre
        h /= Decimal(2)
        continue
