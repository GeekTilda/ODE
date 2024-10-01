import math
from decimal import Decimal, getcontext


getcontext().prec = 50  # How many decimals we want


x = Decimal(0)
y = Decimal(1)
u = Decimal(0)
h = Decimal(0.01)
tol = Decimal(1e-20)


# Represents the system y'' = -y
def dudx6(y, u):
    dydx = u    # y' = u
    dudx = -y   # y'' = -y
    return dydx, dudx


while True:
    # Saving our previous solution
    #xPrev = x
    #yPrev = y
    #uPrev = u

    # Runge-Kutta algorithm
    k1 = dudx6(y, u)
    k2 = dudx6(y + h * k1[0] / 2, u + h * k1[1] / 2)
    k3 = dudx6(y + h * k2[0] / 2, u + h * k2[1] / 2)
    k4 = dudx6(y + h * k3[0], u + h * k3[1])

    # Updating x, y and u
    x = x + h
    y = y + h * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6
    u = u + h * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6

    # Checking when y passes 0
    if y < 0:
        approxPi = 2 * (x - h)
        print(approxPi)
        print(abs(approxPi - Decimal(math.pi)))

        if abs(approxPi - Decimal(math.pi)) < tol:
            print("Converged result: ", approxPi,"±",abs(approxPi - Decimal(math.pi)))
            break
        
        # Returning to old values
        x = x - h
        y = y - h * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6
        u = u - h * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6

        # Making our steps 1/2 as big
        h /= 2
        continue

'''
3.141592653589793115997963
'''