from decimal import Decimal, getcontext


getcontext().prec = 50  # How many decimals we want


x = Decimal(0)
y = Decimal(1)
u = Decimal(0)
h = Decimal(0.000001)
tol = Decimal(1e-20)


# Represents the system y'' = -y
def dudx6(y, u):
    dydx = Decimal(u)    # y' = u
    dudx = -Decimal(y)   # y'' = -y
    return dydx, dudx


while True:
    # Saving our previous solution
    #xPrev = x
    #yPrev = y
    #uPrev = u

    # Runge-Kutta algorithm
    k1 = dudx6(Decimal(y), Decimal(u))
    k2 = dudx6(Decimal(y) + Decimal(h) * Decimal(k1[0]) / Decimal(2), Decimal(u) + Decimal(h) * Decimal(k1[1]) / Decimal(2))
    k3 = dudx6(Decimal(y) + Decimal(h) * Decimal(k2[0]) / Decimal(2), Decimal(u) + Decimal(h) * Decimal(k2[1]) / Decimal(2))
    k4 = dudx6(Decimal(y) + Decimal(h) * Decimal(k3[0]), Decimal(u) + Decimal(h) * Decimal(k3[1]))

    # Updating x, y and u
    x = Decimal(x) + Decimal(h)
    y = Decimal(y) + Decimal(h) * (Decimal(k1[0]) + Decimal(2) * Decimal(k2[0]) + Decimal(2) * Decimal(k3[0]) + Decimal(k4[0])) / Decimal(6)
    u = Decimal(u) + Decimal(h) * (Decimal(k1[1]) + Decimal(2) * Decimal(k2[1]) + Decimal(2) * Decimal(k3[1]) + Decimal(k4[1])) / Decimal(6)

    # Checking when y passes 0
    if y < 0:
        approxPi = Decimal(2) * (Decimal(x) - Decimal(h))

        if abs(Decimal(approxPi) - Decimal("3.14159265358979323846")) < tol:
            print("Converged result: ", approxPi,"±",abs(approxPi - Decimal("3.14159265358979323846")))
            break
        
        # Returning to old values
        x = Decimal(x) - Decimal(h)
        y = Decimal(y) - Decimal(h) * (Decimal(k1[0]) + Decimal(2) * Decimal(k2[0]) + Decimal(2) * Decimal(k3[0]) + Decimal(k4[0])) / Decimal(6)
        u = Decimal(u) - Decimal(h) * (Decimal(k1[1]) + Decimal(2) * Decimal(k2[1]) + Decimal(2) * Decimal(k3[1]) + Decimal(k4[1])) / Decimal(6)

        # Making our steps 1/2 as big
        h /= Decimal(2)
        continue