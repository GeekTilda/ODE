def rungeKutta(f, x0, y0, h, n):
    # f is our function                     (function)
    # x0 is our starting value for x        (int)
    # y0 is our staring value for y         (int)
    # h is our step-size                    (int)
    # n is the amount steps we want to take (int)

    x = [x0]
    y = [y0]

    for i in range(n):
        k1 = h * f(x[i], y[i])
        k2 = h * f(x[i] + h/2, y[i] + k1/2)
        k3 = h * f(x[i] + h/2, y[i] + k2/2)
        k4 = h * f(x[i] + h, y[i] + k3)

        x.append(x[i] + h)
        y.append(y[i] + (k1 + 2*k2 + 2*k3 + k4)/6)
    
    return x, y