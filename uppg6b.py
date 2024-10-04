import math
from decimal import Decimal, getcontext

getcontext().prec = 100 

x = Decimal(0)
y = Decimal(1)
u = Decimal(0)
h = Decimal(0.01)
tol = Decimal(1e-20)

# Looking for the zero-crossing close to 318π
targetZeroCrossings = 318
zeroCrossings = 0  # Counter

# Our differential equation y'' = -y
def dudx6(y, u):
    dydx = Decimal(u)    # y' = u
    dudx = -Decimal(y)   # y'' = -y
    return dydx, dudx

# Previous y to know which zero-crossing we are at
prevY = y

while True:
    # Runge-Kutta-algorithm
    k1 = dudx6(Decimal(y), Decimal(u))
    k2 = dudx6(Decimal(y) + Decimal(h) * Decimal(k1[0]) / Decimal(2), Decimal(u) + Decimal(h) * Decimal(k1[1]) / Decimal(2))
    k3 = dudx6(Decimal(y) + Decimal(h) * Decimal(k2[0]) / Decimal(2), Decimal(u) + Decimal(h) * Decimal(k2[1]) / Decimal(2))
    k4 = dudx6(Decimal(y) + Decimal(h) * Decimal(k3[0]), Decimal(u) + Decimal(h) * Decimal(k3[1]))

    # Updating x, y och u
    x = Decimal(x) + Decimal(h)
    y = Decimal(y) + Decimal(h) * (Decimal(k1[0]) + Decimal(2) * Decimal(k2[0]) + Decimal(2) * Decimal(k3[0]) + Decimal(k4[0])) / Decimal(6)
    u = Decimal(u) + Decimal(h) * (Decimal(k1[1]) + Decimal(2) * Decimal(k2[1]) + Decimal(2) * Decimal(k3[1]) + Decimal(k4[1])) / Decimal(6)

    # Controlling crossing
    if prevY > 0 and y < 0 or y > 0 and prevY < 0:  # If we pass zero 
        zeroCrossings += 1
        print(f"Nollgenomgång nummer {zeroCrossings} vid x ≈ {x}")

        if zeroCrossings >= 315:
            h = 0.00001

        # Zero crossings close to 318π
        if zeroCrossings >= targetZeroCrossings:
            approxPi = ((Decimal(x) - Decimal(h)))/Decimal(318)  # Approximation of 318π
            exactPi = Decimal(math.pi)  # Exakt value for 318π
            print(f"Uppskattat värde för roten vid 318π: {approxPi} ± {abs(approxPi - exactPi)}")
            break

    # Updating previous y
    prevY = y
