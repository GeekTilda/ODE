import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Konstanter
G = 6.67430e-11  # Gravitationskonstanten, m^3 kg^-1 s^-2
M_sun = 1.989e30  # Solens massa, kg
M_earth = 5.972e24  # Jordens massa, kg
earth_radius = 6.371e6  # Jordens radie i meter

# Initialvärden
x0 = 1.496e11  # Startavstånd från solen i meter (1 AU)
y0 = 0  # Börjar på y = 0
vx0 = 0  # Startar med hastighet i y-riktningen
vy0 = 29780  # Cirkulär omloppshastighet för jorden runt solen, m/s

# Tidssteg och simuleringstid
dt = 60 * 60  # 1 timme i sekunder
total_time = 5 * 365.25 * 24 * 60 * 60  # 5 år i sekunder

def acceleration(x, y):
    r = np.sqrt(x**2 + y**2)
    ax = -G * M_sun * x / r**3
    ay = -G * M_sun * y / r**3
    return ax, ay

def euler_method(x0, y0, vx0, vy0, dt, total_time):
    n_steps = int(total_time / dt)
    x = np.zeros(n_steps)
    y = np.zeros(n_steps)
    vx = np.zeros(n_steps)
    vy = np.zeros(n_steps)
    
    x[0], y[0], vx[0], vy[0] = x0, y0, vx0, vy0
    
    for i in range(1, n_steps):
        ax, ay = acceleration(x[i-1], y[i-1])
        vx[i] = vx[i-1] + ax * dt
        vy[i] = vy[i-1] + ay * dt
        x[i] = x[i-1] + vx[i-1] * dt
        y[i] = y[i-1] + vy[i-1] * dt
    
    return x, y

def symplectic_euler_method(x0, y0, vx0, vy0, dt, total_time):
    n_steps = int(total_time / dt)
    
    x = np.zeros(n_steps)
    y = np.zeros(n_steps)
    vx = np.zeros(n_steps)
    vy = np.zeros(n_steps)
    
    x[0], y[0], vx[0], vy[0] = x0, y0, vx0, vy0
    
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
plt.figure(figsize=(12, 6))

# Euler
plt.subplot(1, 2, 1)
plt.plot(x_euler, y_euler, label='Bana', linewidth=0.5)  # Justera linjetjockleken
plt.scatter(x_euler[0], y_euler[0], color='blue', s=earth_radius*1e-6, label='Jorden')  # Plotta planeten
plt.title("Euler-metoden")
plt.xlabel("x-position (m)")
plt.ylabel("y-position (m)")
plt.axis('equal')
plt.gca().add_artist(plt.Circle((0, 0), 6.96e9, color='yellow', label='Solen'))  # Rita solen
plt.legend(loc='upper right')  # Flytta legend till övre högra hörnet

# Symplektisk Euler
plt.subplot(1, 2, 2)
plt.plot(x_symplectic, y_symplectic, label='Bana', linewidth=0.5)  # Justera linjetjockleken
plt.scatter(x_symplectic[0], y_symplectic[0], color='blue', s=earth_radius*1e-6, label='Jorden')  # Plotta planeten
plt.title("Symplektisk Euler-metod")
plt.xlabel("x-position (m)")
plt.ylabel("y-position (m)")
plt.axis('equal')
plt.gca().add_artist(plt.Circle((0, 0), 6.96e9, color='yellow', label='Solen'))  # Rita solen
plt.legend(loc='upper right')  # Flytta legend till övre högra hörnet

plt.tight_layout()
plt.show()

import numpy as np
import matplotlib.pyplot as plt

# Beräkna total energi
def total_energy(x, y, vx, vy):
    kinetic_energy = 0.5 * M_earth * (vx**2 + vy**2)
    potential_energy = -G * M_sun * M_earth / np.sqrt(x**2 + y**2)
    return kinetic_energy + potential_energy

# Använd energifunktionerna
energies_euler = total_energy(x_euler, y_euler, np.zeros_like(x_euler), np.zeros_like(y_euler))
energies_symplectic = total_energy(x_symplectic, y_symplectic, np.zeros_like(x_symplectic), np.zeros_like(y_symplectic))

# Plotta energin
plt.figure(figsize=(12, 6))
plt.plot(energies_euler, label='Total energi (Euler)', color='blue')
plt.plot(energies_symplectic, label='Total energi (Symplektisk)', color='orange')
plt.title('Total energi över tid')
plt.xlabel('Tidssteg')
plt.ylabel('Energi (Joules)')
plt.legend()
plt.grid()
plt.show()
