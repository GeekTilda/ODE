import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Konstanter
G = 6.67430e-11  # Gravitationskonstanten, m^3 kg^-1 s^-2
M_sun = 1.989e30  # Solens massa, kg

# Initialvärden
x0 = 1.496e11  # Startavstånd från solen i meter (cirka 1 AU)
y0 = 0  # Börjar på y = 0
vx0 = 0  # Startar med hastighet i y-riktningen
vy0 = 29780  # Cirkulär omloppshastighet för jorden runt solen, m/s

# Tidssteg och simuleringstid
dt = 60 * 60  # 1 timme i sekunder
total_time = 365.25 * 24 * 60 * 60  # 1 år i sekunder

def acceleration(x, y):
    r = np.sqrt(x**2 + y**2)
    ax = -G * M_sun * x / r**3
    ay = -G * M_sun * y / r**3
    return ax, ay

def euler_method(x0, y0, vx0, vy0, dt, total_time):
    # Antal tidssteg
    n_steps = int(total_time / dt)
    
    # Initialisera listor för att lagra position och hastighet
    x = np.zeros(n_steps)
    y = np.zeros(n_steps)
    vx = np.zeros(n_steps)
    vy = np.zeros(n_steps)
    
    # Sätt initialvärden
    x[0], y[0], vx[0], vy[0] = x0, y0, vx0, vy0
    
    # Simulera rörelsen
    for i in range(1, n_steps):
        ax, ay = acceleration(x[i-1], y[i-1])
        vx[i] = vx[i-1] + ax * dt
        vy[i] = vy[i-1] + ay * dt
        x[i] = x[i-1] + vx[i-1] * dt
        y[i] = y[i-1] + vy[i-1] * dt
    
    return x, y

def symplectic_euler_method(x0, y0, vx0, vy0, dt, total_time):
    # Antal tidssteg
    n_steps = int(total_time / dt)
    
    # Initialisera listor för att lagra position och hastighet
    x = np.zeros(n_steps)
    y = np.zeros(n_steps)
    vx = np.zeros(n_steps)
    vy = np.zeros(n_steps)
    
    # Sätt initialvärden
    x[0], y[0], vx[0], vy[0] = x0, y0, vx0, vy0
    
    # Simulera rörelsen
    for i in range(1, n_steps):
        ax, ay = acceleration(x[i-1], y[i-1])
        vx[i] = vx[i-1] + ax * dt
        vy[i] = vy[i-1] + ay * dt
        x[i] = x[i-1] + vx[i] * dt
        y[i] = y[i-1] + vy[i] * dt
    
    return x, y

# Kör simuleringarna
x_euler, y_euler = euler_method(x0, y0, vx0, vy0, dt, total_time)
x_symplectic, y_symplectic = symplectic_euler_method(x0, y0, vx0, vy0, dt, total_time)

# Plotta banorna
plt.figure(figsize=(10, 5))

# Euler
plt.subplot(1, 2, 1)
plt.plot(x_euler, y_euler)
plt.title("Euler-metoden")
plt.xlabel("x-position (m)")
plt.ylabel("y-position (m)")
plt.axis('equal')

# Symplektisk Euler
plt.subplot(1, 2, 2)
plt.plot(x_symplectic, y_symplectic)
plt.title("Symplektisk Euler-metod")
plt.xlabel("x-position (m)")
plt.ylabel("y-position (m)")
plt.axis('equal')

plt.tight_layout()
plt.show()
