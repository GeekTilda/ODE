import numpy as np
import matplotlib.pyplot as plt

# Konstant
G = 6.67430e-11  # Gravitationskonstant
MSun = 1.989e30  # Solens massa
MJupiter = 1.898e27  # Jupiters massa
MEarth = 5.972e24  # Jordens massa
AU = 1.496e11  # 1 AU i meter

# Initiala positioner och hastigheter
xSun, ySun = 0, 0  # Solens position
xJupiter, yJupiter = 5.2 * AU, 0  # Jupiters position
vxJupiter, vyJupiter = 0, 13000  # Jupiters hastighet (ca 13 km/s)
xEarth, yEarth = AU, 0  # Jordens position
vxEarth, vyEarth = 0, 29780  # Jordens hastighet

# Rymdskeppets initiala värden
x0 = xEarth + 1e7  # Lite utanför jordens position
y0 = 1e6  # Lite ovanför x-axeln
vx0 = 3.286e4  # Start hastighet
vy0 = 1.986e4  # Initiera hastighet för att simuleras

# Tidssteg och total tid
dt = 60 * 30  # 30 minuter i sekunder
totalTime = 10 * 365.25 * 24 * 60 * 60  # 10 år i sekunder

def acceleration(x, y, xTarget, yTarget, massTarget):
    r = np.sqrt((x - xTarget)**2 + (y - yTarget)**2)
    ax = -G * massTarget * (x - xTarget) / r**3
    ay = -G * massTarget * (y - yTarget) / r**3
    return ax, ay

# Euler-Bakåt metod med rörliga kroppar
def eulerBackwardMethod(x0, y0, vx0, vy0, dt, totalTime, MSun, MJupiter, xJupiter, yJupiter, vxJupiter, vyJupiter):
    nSteps = int(totalTime / dt)
    x = np.zeros(nSteps)
    y = np.zeros(nSteps)
    vx = np.zeros(nSteps)
    vy = np.zeros(nSteps)

    time = np.zeros(nSteps)
    sunVelocity = np.zeros(nSteps)

    # Jupiters position och hastighet
    xJup = xJupiter
    yJup = yJupiter
    vxJup = vxJupiter
    vyJup = vyJupiter

    # Skapa arrayer för Jupiters positioner
    xJupiterArray = np.zeros(nSteps)
    yJupiterArray = np.zeros(nSteps)

    # Initialisering av positioner och hastigheter
    x[0], y[0], vx[0], vy[0] = x0, y0, vx0, vy0
    xJupiterArray[0], yJupiterArray[0] = xJup, yJup

    time[0] = 0

    # Simulera rörelse
    for i in range(1, nSteps):
        time[i] = time[i-1] + dt
        # Beräkna accelerationen för Jupiters position
        axJup, ayJup = acceleration(xJup, yJup, xSun, ySun, MSun)

        # Uppdatera Jupiters hastighet och position
        vxJup += axJup * dt
        vyJup += ayJup * dt
        xJup += vxJup * dt
        yJup += vyJup * dt

        # Spara Jupiters position i arrays
        xJupiterArray[i] = xJup
        yJupiterArray[i] = yJup

        # Beräkna accelerationen för rymdskeppet baserat på både solen och Jupiter
        axEarth, ayEarth = acceleration(x[i-1], y[i-1], xSun, ySun, MSun)
        axShipJup, ayShipJup = acceleration(x[i-1], y[i-1], xJup, yJup, MJupiter)

        # Total acceleration på rymdskeppet
        totalAx = axEarth + axShipJup
        totalAy = ayEarth + ayShipJup

        # Uppdatera hastigheter (implicit)
        vx[i] = vx[i-1] + totalAx * dt
        vy[i] = vy[i-1] + totalAy * dt

        # Uppdatera positioner för rymdskeppet
        x[i] = x[i-1] + vx[i] * dt
        y[i] = y[i-1] + vy[i] * dt
    
        # Hastigheten som solen påverkar rymdskeppet med
        sunVelocity[i] = np.sqrt(2*G*MSun/np.sqrt(x[i]**2 + y[i]**2))

    return x, y, xJupiterArray, yJupiterArray, vx, vy, time, sunVelocity

# Simulera rörelsen
xTrajectory, yTrajectory, xJupiterTrajectory, yJupiterTrajectory, vx, vy, time, sunVelocity = eulerBackwardMethod(
    x0, y0, vx0, vy0, dt, totalTime, MSun, MJupiter, xJupiter, yJupiter, vxJupiter, vyJupiter
)

# Hastighet över tid
plt.figure(figsize=(10, 10))
plt.plot(time, np.sqrt(vx**2 + vy**2), label='Rymdskeppets hastighet över tid')
plt.plot(time, sunVelocity, label='Solens påverkan på skeppet')
plt.plot()
plt.xlabel("Tid")
plt.ylabel("Hastighet")

# Plotta banorna
plt.legend()
plt.grid()
plt.show()
plt.plot(xTrajectory, yTrajectory, label='Rymdskeppets bana', linewidth=0.5)
plt.plot(xJupiterTrajectory, yJupiterTrajectory, color='orange', label='Jupiters bana', linewidth=0.5)
plt.scatter(xEarth, yEarth, color='blue', s=50, label='Jorden')
plt.scatter(xJupiterTrajectory[-1], yJupiterTrajectory[-1], color='orange', s=100, label='Jupiter (slutposition)')
plt.scatter(xSun, ySun, color='yellow', s=200, label='Solen')
plt.title("Rymdskeppets rörelse nära Jupiter med rörliga kroppar (Euler-Bakåt)")
plt.xlabel("x-position (m)")
plt.ylabel("y-position (m)")
plt.axis('equal')
plt.legend()
plt.grid()
plt.show()