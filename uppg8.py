import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11  # Gravitational constant
MSun = 1.989e30  # Suns mass
MJupiter = 1.898e27  # Jupiters mass
MEarth = 5.972e24  # Earths mass
AU = 1.496e11  # 1 AU

# Initial positions and velocities
xSun, ySun = 0, 0
xJupiter, yJupiter = 5.2 * AU, 0
vxJupiter, vyJupiter = 0, 13000
xEarth, yEarth = AU, 0
vxEarth, vyEarth = 0, 29780

# Spaceship initial values
x0 = xEarth + 1e7  # A bit over earths position
y0 = 1e6  # A bit over x-axis
vx0 = 3.286e4  # Starting velocities
vy0 = 1.986e4  

# Timesteps and total time
dt = 60 * 30  # 30 minutes in seconds
totalTime = 20 * 365.25 * 24 * 60 * 60  # 10 years in seconds

def acceleration(x, y, xTarget, yTarget, massTarget):
    r = np.sqrt((x - xTarget)**2 + (y - yTarget)**2)
    ax = -G * massTarget * (x - xTarget) / r**3
    ay = -G * massTarget * (y - yTarget) / r**3
    return ax, ay

# Euler-backwards
def eulerBackwardMethod(x0, y0, vx0, vy0, dt, totalTime, MSun, MJupiter, xJupiter, yJupiter, vxJupiter, vyJupiter):
    #Pre allocating and setting initial values
    nSteps = int(totalTime / dt)
    x = np.zeros(nSteps)
    y = np.zeros(nSteps)
    vx = np.zeros(nSteps)
    vy = np.zeros(nSteps)

    time = np.zeros(nSteps)
    sunVelocity = np.zeros(nSteps)


    xJup = xJupiter
    yJup = yJupiter
    vxJup = vxJupiter
    vyJup = vyJupiter

    xJupiterArray = np.zeros(nSteps)
    yJupiterArray = np.zeros(nSteps)

    x[0], y[0], vx[0], vy[0] = x0, y0, vx0, vy0
    xJupiterArray[0], yJupiterArray[0] = xJup, yJup

    time[0] = 0

    # Simulating movement
    for i in range(1, nSteps):
        time[i] = time[i-1] + dt
        # Acceleration on Jupiter
        axJup, ayJup = acceleration(xJup, yJup, xSun, ySun, MSun)

        # Updating Jupiters values
        vxJup += axJup * dt
        vyJup += ayJup * dt
        xJup += vxJup * dt
        yJup += vyJup * dt
        xJupiterArray[i] = xJup
        yJupiterArray[i] = yJup

        # How the ship will be affected
        axEarth, ayEarth = acceleration(x[i-1], y[i-1], xSun, ySun, MSun)
        axShipJup, ayShipJup = acceleration(x[i-1], y[i-1], xJup, yJup, MJupiter)

        # Total acceleration of spaceship
        totalAx = axEarth + axShipJup
        totalAy = ayEarth + ayShipJup

        # Updating velocities and positions (implicit)
        vx[i] = vx[i-1] + totalAx * dt
        vy[i] = vy[i-1] + totalAy * dt
        x[i] = x[i-1] + vx[i] * dt
        y[i] = y[i-1] + vy[i] * dt
    
        # Velocity which the sun is affecting the spaceship with
        sunVelocity[i] = np.sqrt(2*G*MSun/np.sqrt(x[i]**2 + y[i]**2))

    return x, y, xJupiterArray, yJupiterArray, vx, vy, time, sunVelocity


xTrajectory, yTrajectory, xJupiterTrajectory, yJupiterTrajectory, vx, vy, time, sunVelocity = eulerBackwardMethod(x0, y0, vx0, vy0, dt, totalTime, MSun, MJupiter, xJupiter, yJupiter, vxJupiter, vyJupiter)

plt.figure(figsize=(10, 10))
plt.plot(time, np.sqrt(vx**2 + vy**2), label='Spaceships velocity over time')
plt.plot(time, sunVelocity, label='Suns effect on the spaceship')
plt.plot()
plt.xlabel("Time")
plt.ylabel("Velocity")

plt.legend()
plt.grid()
plt.show()
plt.plot(xTrajectory, yTrajectory, label='Spaceships path', linewidth=0.5)
plt.plot(xJupiterTrajectory, yJupiterTrajectory, color='orange', label='Jupiters path', linewidth=0.5)
plt.scatter(xEarth, yEarth, color='blue', s=50, label='Earth')
plt.scatter(xJupiterTrajectory[-1], yJupiterTrajectory[-1], color='orange', s=100, label='Jupiter (end)')
plt.scatter(xSun, ySun, color='yellow', s=200, label='Sun')
plt.title("Spaceships path (Euler-Backwards)")
plt.xlabel("x-pos")
plt.ylabel("y-pos")
plt.axis('equal')
plt.legend()
plt.grid()
plt.show()