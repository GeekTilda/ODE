import math
from decimal import Decimal, getcontext

getcontext().prec = 100  # Ökad precision för långa intervall

x = Decimal(0)
y = Decimal(1)
u = Decimal(0)
h = Decimal(0.01)  # Steglängd
tol = Decimal(1e-20)

# Vi letar efter nollgenomgången nära 318π
target_zero_crossings = 318
zero_crossings = 0  # Räknare för antalet nollgenomgångar

# Definiera systemet y'' = -y
def dudx6(y, u):
    dydx = Decimal(u)    # y' = u
    dudx = -Decimal(y)   # y'' = -y
    return dydx, dudx

# Tidigare värde på y för att hålla koll på nollgenomgångar
prev_y = y

while True:
    # Runge-Kutta-algoritm
    k1 = dudx6(Decimal(y), Decimal(u))
    k2 = dudx6(Decimal(y) + Decimal(h) * Decimal(k1[0]) / Decimal(2), Decimal(u) + Decimal(h) * Decimal(k1[1]) / Decimal(2))
    k3 = dudx6(Decimal(y) + Decimal(h) * Decimal(k2[0]) / Decimal(2), Decimal(u) + Decimal(h) * Decimal(k2[1]) / Decimal(2))
    k4 = dudx6(Decimal(y) + Decimal(h) * Decimal(k3[0]), Decimal(u) + Decimal(h) * Decimal(k3[1]))

    # Uppdatera x, y och u
    x = Decimal(x) + Decimal(h)
    y = Decimal(y) + Decimal(h) * (Decimal(k1[0]) + Decimal(2) * Decimal(k2[0]) + Decimal(2) * Decimal(k3[0]) + Decimal(k4[0])) / Decimal(6)
    u = Decimal(u) + Decimal(h) * (Decimal(k1[1]) + Decimal(2) * Decimal(k2[1]) + Decimal(2) * Decimal(k3[1]) + Decimal(k4[1])) / Decimal(6)

    # Kontrollera nollgenomgång
    if prev_y > 0 and y < 0 or y > 0 and prev_y < 0:  # Om vi passerar 0 från positiv till negativ eller tvärt om
        zero_crossings += 1
        print(f"Nollgenomgång nummer {zero_crossings} vid x ≈ {x}")

        if zero_crossings >= 315:
            h = 0.00001

        #print(f"Uträknat x ≈ {x}, bör vara ")

        # När vi når nollgenomgången nära 318π
        if zero_crossings >= target_zero_crossings:
            approxPi = ((Decimal(x) - Decimal(h)))/Decimal(318)  # Approximation av 318π
            exact_pi = Decimal(math.pi)  # Exakta värdet för 318π
            print(f"Uppskattat värde för roten vid 318π: {approxPi} ± {abs(approxPi - exact_pi)}")
            break

    # Uppdatera prev_y för att hålla koll på nollgenomgångarna
    prev_y = y
