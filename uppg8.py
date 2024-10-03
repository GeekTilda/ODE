import numpy as np
import matplotlib.pyplot as plt

# Konstant
G = 6.67430e-11  # Gravitationskonstant
MSun = 1.989e30  # Solens massa
MJupiter = 1.898e27  # Jupiters massa
MEarth = 5.972e24  # Jordens massa
AU = 1.496e11  # 1 AU i meter

# Initiala positioner och hastigheter
x_sun, y_sun = 0, 0  # Solens position
x_jupiter, y_jupiter = 5.2 * AU, 0  # Jupiters position
vx_jupiter, vy_jupiter = 0, 13000  # Jupiters hastighet (ca 13 km/s)
x_earth, y_earth = AU, 0  # Jordens position
vx_earth, vy_earth = 0, 29780  # Jordens hastighet

# Rymdskeppets initiala värden
x0 = x_earth + 1e7  # Lite utanför jordens position
y0 = 1e6  # Lite ovanför x-axeln
vx0 = 0  # Start hastighet
vy0 = 4.3e4  # Initiera hastighet för att simuleras

# Tidssteg och total tid
dt = 60 * 60  # 1 timme i sekunder
totalTime = 10 * 365.25 * 24 * 60 * 60  # 5 år i sekunder

def acceleration(x, y, x_target, y_target, mass_target):
    r = np.sqrt((x - x_target)**2 + (y - y_target)**2)
    ax = -G * mass_target * (x - x_target) / r**3
    ay = -G * mass_target * (y - y_target) / r**3
    return ax, ay

# Euler-Bakåt metod med rörliga kroppar
def eulerBackwardMethod(x0, y0, vx0, vy0, dt, totalTime, MSun, MJupiter, x_jupiter, y_jupiter, vx_jupiter, vy_jupiter):
    nSteps = int(totalTime / dt)
    x = np.zeros(nSteps)
    y = np.zeros(nSteps)
    vx = np.zeros(nSteps)
    vy = np.zeros(nSteps)
    
    # Jupiters position och hastighet
    x_jup = x_jupiter
    y_jup = y_jupiter
    vx_jup = vx_jupiter
    vy_jup = vy_jupiter

    # Skapa arrayer för Jupiters positioner
    x_jupiter_array = np.zeros(nSteps)
    y_jupiter_array = np.zeros(nSteps)

    # Initialisering av positioner och hastigheter
    x[0], y[0], vx[0], vy[0] = x0, y0, vx0, vy0
    x_jupiter_array[0], y_jupiter_array[0] = x_jup, y_jup

    # Simulera rörelse
    for i in range(1, nSteps):
        # Beräkna accelerationen för Jupiters position
        ax_jup, ay_jup = acceleration(x_jup, y_jup, x_sun, y_sun, MSun)

        # Uppdatera Jupiters hastighet och position
        vx_jup += ax_jup * dt
        vy_jup += ay_jup * dt
        x_jup += vx_jup * dt
        y_jup += vy_jup * dt

        # Spara Jupiters position i arrays
        x_jupiter_array[i] = x_jup
        y_jupiter_array[i] = y_jup

        # Beräkna accelerationen för rymdskeppet baserat på både solen och Jupiter
        ax_earth, ay_earth = acceleration(x[i-1], y[i-1], x_sun, y_sun, MSun)
        ax_ship_jup, ay_ship_jup = acceleration(x[i-1], y[i-1], x_jup, y_jup, MJupiter)

        # Total acceleration på rymdskeppet
        total_ax = ax_earth + ax_ship_jup
        total_ay = ay_earth + ay_ship_jup

        # Uppdatera hastigheter (implicit)
        vx[i] = vx[i-1] + total_ax * dt
        vy[i] = vy[i-1] + total_ay * dt

        # Uppdatera positioner för rymdskeppet
        x[i] = x[i-1] + vx[i] * dt
        y[i] = y[i-1] + vy[i] * dt
    
    return x, y, x_jupiter_array, y_jupiter_array

# Simulera rörelsen
x_trajectory, y_trajectory, x_jupiter_trajectory, y_jupiter_trajectory = eulerBackwardMethod(
    x0, y0, vx0, vy0, dt, totalTime, MSun, MJupiter, x_jupiter, y_jupiter, vx_jupiter, vy_jupiter
)

# Plotta banorna
plt.figure(figsize=(10, 10))
plt.plot(x_trajectory, y_trajectory, label='Rymdskeppets bana', linewidth=0.5)
plt.plot(x_jupiter_trajectory, y_jupiter_trajectory, color='orange', label='Jupiters bana', linewidth=0.5)
plt.scatter(x_earth, y_earth, color='blue', s=50, label='Jorden')
plt.scatter(x_jupiter_trajectory[-1], y_jupiter_trajectory[-1], color='orange', s=100, label='Jupiter (slutposition)')
plt.scatter(x_sun, y_sun, color='yellow', s=200, label='Solen')
plt.title("Rymdskeppets rörelse nära Jupiter med rörliga kroppar (Euler-Bakåt)")
plt.xlabel("x-position (m)")
plt.ylabel("y-position (m)")
plt.axis('equal')
plt.legend()
plt.grid()
plt.show()
