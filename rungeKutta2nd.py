def rungeKutta2nd(f, x0, y0, u0, h, n):
    # f is our function                     (function)
    # x0 is our starting value for x        (int)
    # y0 is our staring value for y         (int)
    # u0 is our starting value for y'       (int)
    # h is our step-size                    (int)
    # n is the amount steps we want to take (int)

    x = [x0]
    y = [y0]
    u = [u0]

    for i in range(n):
        k1 = f(x[i]*h, y[i]*h, u[i]*h)
        k2 = f(x[i]*h + h*h/2, y[i]*h + k1[0]*h/2, u[i]*h + k1[1]*h/2)
        k3 = f(x[i]*h + h*h/2, y[i]*h + k2[0]*h/2, u[i]*h + k2[1]*h/2)
        k4 = f(x[i]*h + h*h, y[i]*h + k3[0]*h, u[i]*h + k3[1]*h)
        
        x.append(x[i] + h)
        y.append(y[i] + (k1[0] + 2*k2[0] + 2*k3[0] + k4[0])/6)
        u.append(u[i] + (k1[1] + 2*k2[1] + 2*k3[1] + k4[1])/6)
    
    return x, y, u