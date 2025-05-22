#%%
import numpy as np
import matplotlib.pyplot as plt
import os

from objects import FallingObject, Ball


def simulate(obj: FallingObject, start, end, resolution):
    time, dt = np.linspace(start, end, resolution, retstep=True)
    s = np.empty(resolution)

    for i in range(resolution):
        obj.update(dt)
        s[i] = obj.pos

    return time, s

#%%
# Fysiske konstanter og initialverdier
g = -9.81         # [m/s^2]
v0 = 0            # [m/s]
s0 = 0            # [m]
airDensity = 1.29  # [kg/m^3]
radius = 1.3e-2     # [m]
m = 0.31e-3        # [kg]
dragCoeff = 0.45  # [kg/m^3]


# Simulation resolution
simRes = 1000000

# Load empirical data
dataFileName = os.path.join("data", "BallFall2.csv")
imageFolderPath = os.path.join("..", "bilder")

t_emp, s_emp = np.loadtxt(
    dataFileName,
    delimiter=",",
    skiprows=4,
    usecols=(0, 1),
    unpack=True
)

# Process empirical data
s_emp *= -1  # Snu retning til nedover
s_emp -= s_emp[0]  # Nullstill posisjon
t_emp -= t_emp[0]  # Nullstill tid

# Derive velocity and acceleration
v_emp = np.gradient(s_emp, t_emp)
a_emp = np.gradient(v_emp, t_emp)



# Simulate with air resistance
ball = Ball(
    radius=radius,
    mass=m,
    dragCoeff=dragCoeff,
    airDensity=airDensity,
    pos=s0,
    vel=v0,
    acc=g
)


# Simulate
t_sim, s_air = simulate(ball, 0, t_emp[-1], simRes)

    
# Select simulated data with the same resolution as empirical data
subset_indices = np.linspace(0, simRes-1, len(t_emp), dtype=int)
s_air = s_air[subset_indices]

v_air = np.gradient(s_air, t_emp)
a_air = np.gradient(v_air, t_emp)





# Modell uten luftmotstand

s_cal = g / 2 * t_emp**2 + v0 * t_emp + s0
v_cal = np.gradient(s_cal, t_emp)
a_cal = np.gradient(v_cal, t_emp)






#%% Plot posisjon
plt.figure(1, figsize=(12, 9))
plt.plot(t_emp, s_cal, label="Fritt Fall")
plt.plot(t_emp, s_air, label="Luftmotstand")
plt.plot(t_emp, s_emp, label="Empiriske Verdier")
plt.title("Posisjon [m]")
plt.xlabel("Tid [s]")
plt.ylabel("Posisjon [m]")
plt.legend()
plt.grid()
plt.show(block=False)

#%% Plot hastighet
plt.figure(2, figsize=(12, 9))
plt.plot(t_emp, v_cal, label="Fritt Fall")
plt.plot(t_emp, v_air, label="Luftmotstand")
plt.plot(t_emp, v_emp, label="Empiriske Verdier")
plt.title("Hastighet [m/s]")
plt.xlabel("Tid [s]")
plt.ylabel("Hastighet [m/s]")
plt.legend()
plt.grid()
plt.show(block=False)

#%% Plot akselerasjon
plt.figure(3, figsize=(12, 9))
plt.plot(t_emp, a_cal, label="Fritt Fall")
plt.plot(t_emp, a_air, label="Luftmotstand")
plt.plot(t_emp, a_emp, label="Empiriske Verdier")
plt.title("Akselerasjon [m/s²]")
plt.xlabel("Tid [s]")
plt.ylabel("Akselerasjon [m/s²]")
plt.legend()
plt.grid()
plt.show()