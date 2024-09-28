import numpy as np
from matplotlib import pyplot as plt
from rungeKutta import rungeKutta
from rungeKutta2nd import rungeKutta2nd

def main():
    """
    x0 = -1
    y0 = -1
    h = 0.1
    n = 40
    x,y = rungeKutta(dudx3,x0,y0,h,n)   # Uppg.3
    """

    """
    N = 81
    x0 = 0
    y0 = N/100
    h = 0.01
    n = 123    # Smäller vid 125 :)
    x,y = rungeKutta(dudx4,x0,y0,h,n)   #Uppg. 4
    """
    """
    N = 81
    x0 = 0
    y0 = N
    xend = 512    # 2^k : 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024 (Overflow for matplotlib)
    h = 0.01
    n = int(xend/h)
    x,y = rungeKutta(dudx5,x0,y0,h,n)   # Uppg. 5
    """

    x0 = np.pi / 2
    y0 = 0
    u0 = -1
    h = 0.001   # Varying h so get closer and closer to pi 
    xend = np.pi
    n = int(xend/h)
    x,y,u = rungeKutta2nd(dudx6,x0,y0,u0,h,n)   # Uppg. 6 OBS OBS OBS INTE KLAR

    plt.plot(x, y)
    plt.show()
    print(y[-1])    # Only for uppg. 5 & 6

### DIFFERENTIAL EQUATIONS 

def dudx3(x, y):
    dydx = np.sqrt(abs(y))  # 3 : differential equation y' = sqrt(|y|)
    return dydx

def dudx4(x, y):
    dydx = y*y  # 4 : differential equation y' = y^2
    return dydx

def dudx5(x, y):
    dydx = y    # 5 : differential equation y' = y
    return dydx 

def dudx6(x, y, u):
    dydx = u    # u = y'
    dudx = -y   # 6 : differential equation y'' = -y    <=>    u' = y'' = -y
    return dydx, dudx


### CALLING MAIN 

main()
