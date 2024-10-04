import numpy as np
from matplotlib import pyplot as plt
from rungeKutta import rungeKutta

def main():
    
    x0 = -1
    y0 = -1
    h = 0.1
    n = 40
    x,y = rungeKutta(dudx3,x0,y0,h,n)   # Uppg.3

    #plt.plot(x, y)
    #plt.show()
    
    N = 81
    x0 = 0
    y0 = N/100
    h = 0.01
    n = 1240    # "Explodes at" 125 :)
    x,y = rungeKutta(dudx4,x0,y0,h,n)   #Uppg. 4
    
    plt.plot(x, y)
    plt.show()
    
    N = 81
    x0 = 0
    y0 = N
    xend = 512    # 2^k : 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024 (Overflow for matplotlib)
    h = 0.1
    n = int(xend/h)
    x,y = rungeKutta(dudx5,x0,y0,h,n)   # Uppg. 5
    #print(y[-1])

    #plt.plot(x, y)
    #plt.show()


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


### CALLING MAIN 


main()
