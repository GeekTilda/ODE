from decimal import Decimal

def rungeKutta4th(f, x0, y0, u0, h, n):
    # Starta alla värden som Decimal
    x = [Decimal(x0)]
    y = [Decimal(y0)]
    u = [Decimal(u0)]
    h = Decimal(h)  # Steglängd som Decimal

    for i in range(n):
        k1 = f(x[i], y[i], u[i])
        k2 = f(x[i] + h/2, y[i] + k1[0]*h/2, u[i] + k1[1]*h/2)
        k3 = f(x[i] + h/2, y[i] + k2[0]*h/2, u[i] + k2[1]*h/2)
        k4 = f(x[i] + h, y[i] + k3[0]*h, u[i] + k3[1]*h)
        
        x.append(x[i] + h)
        y.append(y[i] + (k1[0] + 2*k2[0] + 2*k3[0] + k4[0]) / 6)
        u.append(u[i] + (k1[1] + 2*k2[1] + 2*k3[1] + k4[1]) / 6)
    
    return x, y, u
