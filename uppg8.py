import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11      # Gravitational constant
MSun = 1.989e30      # Mass of the Sun
MEarth = 5.972e24    # Mass of Earth
MJupiter = 1.898e27  # Mass of Jupiter
MShip = 1000         # Mass of the spaceship

AU = 1.496e11             # Astronomical unit
earthRadius = 6.371e6     # Earths radius
jupiterRadius = 7.1492e7  # Jupiters radius

# Initial positions
xEarth0 = 1 * AU
yEarth0 = 0
vxEarth0 = 0
vyEarth0 = 29780  # Earths velocity around the Sun

xJupiter0 = 5.2 * AU
yJupiter0 = 0
vxJupiter0 = 0
vyJupiter0 = 13720  # Jupiters velocity around the Sun

xShip0 = xEarth0                # Ship starts near Earth
yShip0 = earthRadius + 400000   # 400 km above Earths surface
vxShip0 = -15000                # Give ship an initial velocity towards Jupiter
vyShip0 = vyEarth0              # Small delta-v to escape Earth

# Time step
dt = 60 * 30                             # 30 min in seconds
totalTime = 100 * 365.25 * 24 * 60 * 60  # 100 years in seconds

# Function to calculate the acceleration due to gravity
def acceleration(x, y, xOther, yOther, MOther):
    r = np.sqrt((x - xOther)**2 + (y - yOther)**2)
    ax = -G * MOther * (x - xOther) / r**3
    ay = -G * MOther * (y - yOther) / r**3
    return ax, ay

# Runge-Kutta 4th order method for system of multiple objects
def rungeKuttaSystem(xShip0, yShip0, vxShip0, vyShip0, xEarth0, yEarth0, vxEarth0, vyEarth0, xJupiter0, yJupiter0, vxJupiter0, vyJupiter0, dt, totalTime):
    nSteps = int(totalTime / dt)
    
    # Preallocate memory for positions and velocities
    xShip = np.zeros(nSteps)
    yShip = np.zeros(nSteps)
    vxShip = np.zeros(nSteps)
    vyShip = np.zeros(nSteps)
    
    xEarth = np.zeros(nSteps)
    yEarth = np.zeros(nSteps)
    vxEarth = np.zeros(nSteps)
    vyEarth = np.zeros(nSteps)
    
    xJupiter = np.zeros(nSteps)
    yJupiter = np.zeros(nSteps)
    vxJupiter = np.zeros(nSteps)
    vyJupiter = np.zeros(nSteps)
    
    # Initial conditions
    xShip[0], yShip[0], vxShip[0], vyShip[0] = xShip0, yShip0, vxShip0, vyShip0
    xEarth[0], yEarth[0], vxEarth[0], vyEarth[0] = xEarth0, yEarth0, vxEarth0, vyEarth0
    xJupiter[0], yJupiter[0], vxJupiter[0], vyJupiter[0] = xJupiter0, yJupiter0, vxJupiter0, vyJupiter0

    # Runge-Kutta integration loop
    for i in range(1, nSteps):
        # For the spaceship
        # Calculate acceleration from the Sun, Earth, and Jupiter
        axSun, aySun = acceleration(xShip[i-1], yShip[i-1], 0, 0, MSun)  # From Sun
        axEarth, ayEarth = acceleration(xShip[i-1], yShip[i-1], xEarth[i-1], yEarth[i-1], MEarth)  # From Earth
        axJupiter, ayJupiter = acceleration(xShip[i-1], yShip[i-1], xJupiter[i-1], yJupiter[i-1], MJupiter)  # From Jupiter

        # Combine accelerations for the ship
        axTotal = axSun + axEarth + axJupiter
        ayTotal = aySun + ayEarth + ayJupiter

        # Update ship's velocity and position
        vxShip[i] = vxShip[i-1] + axTotal * dt
        vyShip[i] = vyShip[i-1] + ayTotal * dt
        xShip[i] = xShip[i-1] + vxShip[i-1] * dt
        yShip[i] = yShip[i-1] + vyShip[i-1] * dt

        # Update Earth's position (Earth-Sun)
        axEarthSun, ayEarthSun = acceleration(xEarth[i-1], yEarth[i-1], 0, 0, MSun)
        vxEarth[i] = vxEarth[i-1] + axEarthSun * dt
        vyEarth[i] = vyEarth[i-1] + ayEarthSun * dt
        xEarth[i] = xEarth[i-1] + vxEarth[i-1] * dt
        yEarth[i] = yEarth[i-1] + vyEarth[i-1] * dt

        # Update Jupiter's position (Jupiter-Sun)
        axJupiterSun, ayJupiterSun = acceleration(xJupiter[i-1], yJupiter[i-1], 0, 0, MSun)
        vxJupiter[i] = vxJupiter[i-1] + axJupiterSun * dt
        vyJupiter[i] = vyJupiter[i-1] + ayJupiterSun * dt
        xJupiter[i] = xJupiter[i-1] + vxJupiter[i-1] * dt
        yJupiter[i] = yJupiter[i-1] + vyJupiter[i-1] * dt
    
    return xShip, yShip, xEarth, yEarth, xJupiter, yJupiter

# Run the simulation
xShip, yShip, xEarth, yEarth, xJupiter, yJupiter = rungeKuttaSystem(xShip0, yShip0, vxShip0, vyShip0, xEarth0, yEarth0, vxEarth0, vyEarth0, xJupiter0, yJupiter0, vxJupiter0, vyJupiter0, dt, totalTime)

# Plotting
plt.figure(figsize=(10, 10))
plt.plot(xShip / AU, yShip / AU, label="Ship", color="blue", linewidth=0.5)
plt.plot(xEarth / AU, yEarth / AU, label="Earth", color="green", linewidth=0.5)
plt.plot(xJupiter / AU, yJupiter / AU, label="Jupiter", color="orange")
plt.scatter(0, 0, color='yellow', label="Sun")
plt.title("Trajectories of Spaceship, Earth, and Jupiter")
plt.xlabel("x-position")
plt.ylabel("y-position")
plt.legend()
plt.grid()
plt.axis("equal")
plt.show()
