import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11  # Gravitational constant
MSun = 1.989e30  # Suns mass
MEarth = 5.972e24  # Earths mass
earthRadius = 6.371e6  # Earths radius

# Initial values
x0 = 1.496e11  # Starting distance from Earth to Sun
y0 = 0  # Starting at y = 0
vx0 = 0  # Start velocity
vy0 = 29780  # Circular velocity around the sun

# Timesteps
dt = 60 * 60  # 1 hour in seconds
totalTime = 5 * 365.25 * 24 * 60 * 60  # 5 years in seconds

def acceleration(x, y):
    r = np.sqrt(x**2 + y**2)   # Radius
    ax = -G * MSun * x / r**3  # Acceleration for x
    ay = -G * MSun * y / r**3  # Acceleration for y
    return ax, ay

# Eulers method
def eulerMethod(x0, y0, vx0, vy0, dt, totalTime):
    nSteps = int(totalTime / dt)
    x = np.zeros(nSteps)
    y = np.zeros(nSteps)
    vx = np.zeros(nSteps)
    vy = np.zeros(nSteps)
    
    x[0], y[0], vx[0], vy[0] = x0, y0, vx0, vy0
    
    for i in range(1, nSteps):
        ax, ay = acceleration(x[i-1], y[i-1])
        vx[i] = vx[i-1] + ax * dt
        vy[i] = vy[i-1] + ay * dt
        x[i] = x[i-1] + vx[i-1] * dt
        y[i] = y[i-1] + vy[i-1] * dt
    
    return x, y

# Runge-Kutta 4th order method
def rungeKuttaMethod(x0, y0, vx0, vy0, dt, totalTime):
    nSteps = int(totalTime / dt)
    x = np.zeros(nSteps)
    y = np.zeros(nSteps)
    vx = np.zeros(nSteps)
    vy = np.zeros(nSteps)
    
    x[0], y[0], vx[0], vy[0] = x0, y0, vx0, vy0
    
    for i in range(1, nSteps):
        # Calculate k1 values
        ax1, ay1 = acceleration(x[i-1], y[i-1])
        k1vx = ax1 * dt
        k1vy = ay1 * dt
        k1x = vx[i-1] * dt
        k1y = vy[i-1] * dt

        # Calculate k2 values
        ax2, ay2 = acceleration(x[i-1] + 0.5 * k1x, y[i-1] + 0.5 * k1y)
        k2vx = ax2 * dt
        k2vy = ay2 * dt
        k2x = (vx[i-1] + 0.5 * k1vx) * dt
        k2y = (vy[i-1] + 0.5 * k1vy) * dt

        # Calculate k3 values
        ax3, ay3 = acceleration(x[i-1] + 0.5 * k2x, y[i-1] + 0.5 * k2y)
        k3vx = ax3 * dt
        k3vy = ay3 * dt
        k3x = (vx[i-1] + 0.5 * k2vx) * dt
        k3y = (vy[i-1] + 0.5 * k2vy) * dt

        # Calculate k4 values
        ax4, ay4 = acceleration(x[i-1] + k3x, y[i-1] + k3y)
        k4vx = ax4 * dt
        k4vy = ay4 * dt
        k4x = (vx[i-1] + k3vx) * dt
        k4y = (vy[i-1] + k3vy) * dt

        # Update positions and velocities
        vx[i] = vx[i-1] + (k1vx + 2*k2vx + 2*k3vx + k4vx) / 6
        vy[i] = vy[i-1] + (k1vy + 2*k2vy + 2*k3vy + k4vy) / 6
        x[i] = x[i-1] + (k1x + 2*k2x + 2*k3x + k4x) / 6
        y[i] = y[i-1] + (k1y + 2*k2y + 2*k3y + k4y) / 6
    
    return x, y

# Getting values and running our methods
xEuler, yEuler = eulerMethod(x0, y0, vx0, vy0, dt, totalTime)
xRK4, yRK4 = rungeKuttaMethod(x0, y0, vx0, vy0, dt, totalTime)

# Plotting the paths
plt.figure(figsize=(10, 6))

# Euler
plt.subplot(1, 2, 1)
plt.plot(xEuler, yEuler, label='Path', linewidth=0.5)
plt.scatter(xEuler[0], yEuler[0], color='blue', s=earthRadius*1e-6, label='Earth')
plt.title("Euler-metod")
plt.xlabel("x-position ")
plt.ylabel("y-position ")
plt.axis('equal')
plt.gca().add_artist(plt.Circle((0, 0), 6.96e9, color='yellow', label='Sun'))
plt.legend(loc='upper right')

# Runge-Kutta
plt.subplot(1, 2, 2)
plt.plot(xRK4, yRK4, label='Path', linewidth=0.5)
plt.scatter(xRK4[0], yRK4[0], color='blue', s=earthRadius*1e-6, label='Earth')
plt.title("Runge-Kutta 4-metod")
plt.xlabel("x-position")
plt.ylabel("y-position")
plt.axis('equal')
plt.gca().add_artist(plt.Circle((0, 0), 6.96e9, color='yellow', label='Sun'))
plt.legend(loc='upper right')

plt.tight_layout()
plt.show()

# Calculating total energy
def totalEnergy(x, y, vx, vy):
    kineticEnergy = 0.5 * MEarth * (vx**2 + vy**2)
    potentialEnergy = -G * MSun * MEarth / np.sqrt(x**2 + y**2)
    return kineticEnergy + potentialEnergy

# Getting the energy from our energy-function
energiesEuler = totalEnergy(xEuler, yEuler, np.zeros_like(xEuler), np.zeros_like(yEuler))
energiesRK4 = totalEnergy(xRK4, yRK4, np.zeros_like(xRK4), np.zeros_like(yRK4))

# Plotting how the energy varies by time
plt.figure(figsize=(6, 6))
plt.plot(energiesEuler, label='Total energy (Euler)', color='blue')
plt.plot(energiesRK4, label='Total energi (Runge-Kutta)', color='red')
plt.title('Total energy over time')
plt.xlabel('Timesteps')
plt.ylabel('Energy (Joules)')
plt.legend()
plt.grid()
plt.show()
