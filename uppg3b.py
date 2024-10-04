import numpy as np
from matplotlib import pyplot as plt

def main():
    x0 = -1
    y0 = -1 + 1e-6  # Starting with epsilon-disturbance
    h = 0.0000001
    n = 1000000000

    x, y, num = rungeKuttaWithStop(dudx3, x0, y0, h, n)  # Uppg.3
    print(num)
    
    plt.plot(x, y)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Numerisk lösning av y' = sqrt(|y|)")
    plt.show()


### DIFFERENTIAL EQUATION (Uppg. 3)

def dudx3(x, y):
    dydx = np.sqrt(abs(y))  # 3 : differential equation y' = sqrt(|y|)
    return dydx


### MODIFIED RUNGE-KUTTA 

def rungeKuttaWithStop(f, x0, y0, h, n):
    num = 0
    x = [x0]
    y = [y0]

    for i in range(n):
        k1 = h * f(x[i], y[i])
        k2 = h * f(x[i] + h/2, y[i] + k1/2)
        k3 = h * f(x[i] + h/2, y[i] + k2/2)
        k4 = h * f(x[i] + h, y[i] + k3)

        xNext = x[i] + h
        yNext = y[i] + (k1 + 2*k2 + 2*k3 + k4) / 6

        x.append(xNext)
        y.append(yNext)

        # If we got stuck at |y| <= 10^-6
        if abs(yNext) <= 1e-6:
            num = num + 1
            print(f"Lösningen fastnar vid y ≈ 0 när x ≈ {xNext}")
        if yNext > 1e-6:
            break

    return x, y, num

### CALLING MAIN

main()