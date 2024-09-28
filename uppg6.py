import numpy as np
from decimal import Decimal, getcontext

# Ställ in precisionen för Decimal
getcontext().prec = 50

# Definiera funktionen som representerar systemet
def dudx6(x, y, u):
    dydx = u    # u = y'
    dudx = -y   # y'' = -y
    return dydx, dudx

# Initialvillkor
x0 = Decimal(0)  # Startpunkt
y0 = Decimal(1)  # y(0) = 1
u0 = Decimal(0)  # y'(0) = 0
h = Decimal(0.000001)  # Värde för steglängd
xend = Decimal(7.9)  # Sökning upp till t = 7.9
n = int(xend / h)  # Antal steg

# Euler's metod
def euler_method(f, x0, y0, u0, h, n):
    x = [x0]
    y = [y0]
    u = [u0]

    for i in range(n):
        dydx, dudx = f(x[i], y[i], u[i])
        y_next = y[i] + dydx * h
        u_next = u[i] + dudx * h
        x_next = x[i] + h

        x.append(x_next)
        y.append(y_next)
        u.append(u_next)

    return x, y, u

# Använd Euler's metod för att lösa differentialekvationen
x, y, u = euler_method(dudx6, x0, y0, u0, h, n)

# Funktion för att hitta nollstället
def func(t):
    index = int(t / h)
    if index < len(y):
        return y[index]
    return Decimal(0)

# Bättre approximation av derivatan med centrala differenser
def derivative_func(t):
    index = int(t / h)
    if index > 0 and index < len(y) - 1:
        return (y[index + 1] - y[index - 1]) / (2 * h)
    return Decimal(0)

# Bisection-metoden
def bisection_method(a, b, max_iterations=200000, tolerance=1e-20):
    if func(a) * func(b) >= 0:
        print("Tecknen för f(a) och f(b) måste vara olika.")
        return None
    
    for _ in range(max_iterations):
        c = (a + b) / 2
        f_c = func(c)
        
        if abs(f_c) < tolerance:
            return c
        
        if func(a) * f_c < 0:
            b = c
        else:
            a = c

    print("Maximala iterationer nådda utan konvergens.")
    return (a + b) / 2

# Justera toleransen temporärt
temporary_tolerance = 1e-6  # Temporär högre tolerans för de första iterationerna

# Newton-Raphsons metod med temporär högre tolerans
def newton_method_with_temp_tolerance(initial_guess, max_iterations=200000):
    x_n = Decimal(initial_guess)

    for iteration in range(max_iterations):
        f_x_n = func(x_n)
        f_prime_x_n = derivative_func(x_n)

        if f_prime_x_n == 0:
            print("Derivatan är noll, ingen lösning.")
            return None

        # Dynamisk justering av steglängden
        step_size = f_x_n / f_prime_x_n
        adjusted_step_size = step_size if abs(step_size) < Decimal(0.01) else step_size * Decimal(0.5)

        x_n1 = x_n - adjusted_step_size

        # Skriv ut med hög precision
        print(f"Iteration {iteration}: x_n={x_n:.25f}, f(x_n)={f_x_n:.25f}, f'(x_n)={f_prime_x_n:.25f}, adjusted_step_size={adjusted_step_size:.25f}")

        # Använd tillfällig tolerans under de första 50 iterationerna
        if iteration < 50 and abs(f_x_n) < temporary_tolerance:
            return x_n1
        
        if abs(f_x_n) < temporary_tolerance:
            return x_n1
        
        x_n = x_n1

    print("Maximala iterationer nådda utan konvergens.")
    return x_n


# Använd bisection-metoden för att hitta ett nollställe först
a = Decimal(4.6)  # Justera detta intervall
b = Decimal(4.72)

t_zero_bisection = bisection_method(a, b)

# Använd t_zero_bisection för att starta Newtons metod
if t_zero_bisection is not None:
    initial_guess = t_zero_bisection
    t_zero_newton = newton_method_with_temp_tolerance(initial_guess)

    # Använd t_zero_newton för att uppskatta π
    if t_zero_newton is not None:
        pi_approx_newton = (t_zero_newton * Decimal(2)) / Decimal(3)
        print(f"Uppskattat värde av π: {pi_approx_newton:.25f}")
        print("Rätt värde av π:       3.14159265358979323846")
        print("Differens: ", (float(pi_approx_newton) - 3.14159265358979323846))
    else:
        print("Kunde inte hitta nollstället med Newtons metod.")
else:
    print("Kunde inte hitta nollstället med bisection-metoden.")
