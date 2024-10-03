
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
    h = 0.001
    n = 1240    # "Explodes at" 125 :)
    x,y = rungeKutta(dudx4,x0,y0,h,n)   #Uppg. 4
    
    plt.plot(x, y)
    plt.show()
    
    N = 81
    x0 = 0
    y0 = N
    xend = 512    # 2^k : 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024 (Overflow for matplotlib)
    h = 0.01
    n = int(xend/h)
    x,y = rungeKutta(dudx5,x0,y0,h,n)   # Uppg. 5
    print(y[-1])

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

'''
import numpy as np
from matplotlib import pyplot as plt

def main():
    x0 = -1
    y0 = -1 + 1e-6  # Starta med epsilon-störning
    h = 0.001  # Mindre steglängd för noggrannare resultat
    n = 400000  # Antal steg

    # Lös uppgift 3 och kontrollera när lösningen fastnar
    x, y = rungeKutta_with_stop(dudx3, x0, y0, h, n)  # Uppg.3
    
    plt.plot(x, y)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Numerisk lösning av y' = sqrt(|y|)")
    plt.show()


### DIFFERENTIAL EQUATION (Uppg. 3)

def dudx3(x, y):
    dydx = np.sqrt(abs(y))  # 3 : differential equation y' = sqrt(|y|)
    return dydx


### MODIFIERAD RUNGE-KUTTA MED STOPPKRITERIUM

def rungeKutta_with_stop(f, x0, y0, h, n):
    x = [x0]
    y = [y0]

    for i in range(n):
        k1 = h * f(x[i], y[i])
        k2 = h * f(x[i] + h/2, y[i] + k1/2)
        k3 = h * f(x[i] + h/2, y[i] + k2/2)
        k4 = h * f(x[i] + h, y[i] + k3)

        x_next = x[i] + h
        y_next = y[i] + (k1 + 2*k2 + 2*k3 + k4) / 6

        # Lägg till nästa värde i listorna
        x.append(x_next)
        y.append(y_next)

        # Kontrollera om y har fastnat (|y| <= 10^-6)
        if abs(y_next) <= 1e-6:
            print(f"Lösningen fastnar vid y ≈ 0 när x ≈ {x_next}")
            break  # Avsluta loopen när lösningen når stoppkriteriet

    return x, y

### KALLA MAIN-FUNKTIONEN

main()
'''