from decimal import Decimal

def rungeKutta4th(f, x0, y0, u0, h, xend, tol):
    while (True):
        n = int(xend / h)  # Antal steg

        x = []
        y = []
        u = []

        for i in range(n):
            x.append(x0 + h*i)
            y.append(y0 + h*i)
            u.append(u0 + h*i)

        for i in range(n):
            k1 = f(x[i], y[i], u[i])
            k2 = f(x[i] + h/2, y[i] + k1[0]*h/2, u[i] + k1[1]*h/2)
            k3 = f(x[i] + h/2, y[i] + k2[0]*h/2, u[i] + k2[1]*h/2)
            k4 = f(x[i] + h, y[i] + k3[0]*h, u[i] + k3[1]*h)
    
            y[0] = float(k4[0]) - 3.14159265358979323846
            print(y[0])

            if  y[0] < 0:
                if abs(y[0]) < tol:
                    print(y[0])
                    return y[0]
                else:
                    h = h/2