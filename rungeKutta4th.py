# rungeKutta4th.py

from decimal import Decimal

def rungeKutta4th(f, x0, y0, u0, h, n):
    """
    Argument:
    - f: Systemet av differentialekvationer som ska lösas, dvs en funktion som returnerar derivator.
    - x0, y0, u0: Startvärden för x, y och y' (initial conditions).
    - h: Steglängd.
    - n: Antal steg att ta.
    """
    
    # Initialisera listor för x, y och u
    x = [Decimal(x0)]
    y = [Decimal(y0)]
    u = [Decimal(u0)]

    for i in range(n):
        # Beräkna k1, k2, k3 och k4
        k1_y, k1_u = f(x[i], y[i], u[i])
        k2_y, k2_u = f(x[i] + h/2, y[i] + k1_y * h / 2, u[i] + k1_u * h / 2)
        k3_y, k3_u = f(x[i] + h/2, y[i] + k2_y * h / 2, u[i] + k2_u * h / 2)
        k4_y, k4_u = f(x[i] + h, y[i] + k3_y * h, u[i] + k3_u * h)
        
        # Uppdatera värden
        x.append(x[i] + h)
        y.append(y[i] + (k1_y + 2 * k2_y + 2 * k3_y + k4_y) * h / 6)
        u.append(u[i] + (k1_u + 2 * k2_u + 2 * k3_u + k4_u) * h / 6)
    
    return x, y, u
