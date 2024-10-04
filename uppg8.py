import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11  # Gravitational constant
MSun = 1.989e30  # Mass of the Sun
MJupiter = 1.898e27  # Mass of Jupiter
AU = 1.496e11  # 1 AU in meters

# Initial positions and velocities
x_sun, y_sun = 0, 0  # Sun's position
x_jupiter, y_jupiter = 5.2 * AU, 0  # Jupiter's position
vx_jupiter, vy_jupiter = 0, 13000  # Jupiter's velocity (about 13 km/s)
x_earth, y_earth = AU, 0  # Earth's position
vx_earth, vy_earth = 0, 29780  # Earth's velocity

# Rocketship's initial values
x0 = x_earth + 1e7  # Slightly outside Earth's position
y0 = 1e6  # Slightly above the x-axis
vx0 = 10000  # Initial velocity towards Jupiter (adjusted)
vy0 = 10000  # Initial velocity to simulate slingshot effect

# Time step and total time
dt = 60 * 60  # 1 hour in seconds
totalTime = 2 * 365.25 * 24 * 60 * 60  # 10 years in seconds

def acceleration(x, y, x_target, y_target, mass_target):
    r = np.sqrt((x - x_target)**2 + (y - y_target)**2)
    ax = -G * mass_target * (x - x_target) / r**3
    ay = -G * mass_target * (y - y_target) / r**3
    return ax, ay

# Euler-Backward method with moving bodies
def eulerBackwardMethod(x0, y0, vx0, vy0, dt, totalTime, MSun, MJupiter, x_jupiter, y_jupiter, vx_jupiter, vy_jupiter):
    nSteps = int(totalTime / dt)
    x = np.zeros(nSteps)
    y = np.zeros(nSteps)
    vx = np.zeros(nSteps)
    vy = np.zeros(nSteps)
    
    # Jupiter's position and velocity
    x_jup = x_jupiter
    y_jup = y_jupiter
    vx_jup = vx_jupiter
    vy_jup = vy_jupiter

    # Create arrays for Jupiter's positions
    x_jupiter_array = np.zeros(nSteps)
    y_jupiter_array = np.zeros(nSteps)

    # Initialization of positions and velocities
    x[0], y[0], vx[0], vy[0] = x0, y0, vx0, vy0
    x_jupiter_array[0], y_jupiter_array[0] = x_jup, y_jup

    # Simulate motion
    for i in range(1, nSteps):
        # Calculate acceleration based on Sun's position
        ax_sun, ay_sun = acceleration(x_jup, y_jup, x_sun, y_sun, MSun)

        # Update Jupiter's velocity and position
        vx_jup += ax_sun * dt
        vy_jup += ay_sun * dt
        x_jup += vx_jup * dt
        y_jup += vy_jup * dt

        # Save Jupiter's position in arrays
        x_jupiter_array[i] = x_jup
        y_jupiter_array[i] = y_jup

        # Calculate acceleration for the rocketship based on both the Sun and Jupiter
        ax_ship_sun, ay_ship_sun = acceleration(x[i-1], y[i-1], x_sun, y_sun, MSun)
        ax_ship_jup, ay_ship_jup = acceleration(x[i-1], y[i-1], x_jup, y_jup, MJupiter)

        # Total acceleration on the rocketship
        total_ax = - ax_ship_sun + ax_ship_jup
        total_ay = - ay_ship_sun + ay_ship_jup

        # Update velocities (implicit)
        vx[i] = vx[i-1] + total_ax * dt
        vy[i] = vy[i-1] + total_ay * dt

        # Update positions for the rocketship
        x[i] = x[i-1] + vx[i] * dt
        y[i] = y[i-1] + vy[i] * dt
    
    return x, y, x_jupiter_array, y_jupiter_array

# Simulate the motion
x_trajectory, y_trajectory, x_jupiter_trajectory, y_jupiter_trajectory = eulerBackwardMethod(
    x0, y0, vx0, vy0, dt, totalTime, MSun, MJupiter, x_jupiter, y_jupiter, vx_jupiter, vy_jupiter
)

# Plot the trajectories
plt.figure(figsize=(10, 10))
plt.plot(x_trajectory, y_trajectory, label='Rocketship trajectory', linewidth=0.5)
plt.plot(x_jupiter_trajectory, y_jupiter_trajectory, color='orange', label='Jupiter trajectory', linewidth=0.5)
plt.scatter(x_earth, y_earth, color='blue', s=50, label='Earth')
plt.scatter(x_jupiter_trajectory[-1], y_jupiter_trajectory[-1], color='orange', s=100, label='Jupiter (end position)')
plt.scatter(x_sun, y_sun, color='yellow', s=200, label='Sun')
plt.title("Rocketship Movement Near Jupiter with Moving Bodies (Euler-Backward)")
plt.xlabel("x-position (m)")
plt.ylabel("y-position (m)")
plt.axis('equal')
plt.legend()
plt.grid()
plt.show()
