#%%
import numpy as np
import matplotlib.pyplot as plt
import os

from objects import FallingObject, Ball, Cube


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
m = 1.000          # [kg]
airDensity = 1.29 # [kg/m^3]

# Lag objekt
ball = FallingObject(
    area=12.5e-2 * 19.5e-2,
    mass=0.2,
    dragCoeff=0.58,
    airDensity=airDensity,
    pos=s0,
    vel=v0,
    acc=g
)

simRes = 100000

#%% Last inn empiriske data
dataFileName = os.path.join("data", "BoksFall.csv")
imageFolderPath = os.path.join("..", "bilder")

t, s_emp = np.loadtxt(
    dataFileName,
    delimiter=",",
    skiprows=2,
    usecols=(0, 1),
    unpack=True
)

#%% Behandle empiriske data

s_emp *= -1  # Snu retning til nedover

# Deriver for å få hastighet og akselerasjon
v_emp = np.gradient(s_emp, t)
a_emp = np.gradient(v_emp, t)



#%% Beregn fritt fall (uten luftmotstand)
s_cal = g / 2 * t**2 + v0 * t + s0
v_cal = np.gradient(s_cal, t)
a_cal = np.gradient(v_cal, t)



#%% Beregn simulert fall med luftmotstand
t_air, s_air = simulate(ball, t[0], 1.2, simRes)
v_air = np.gradient(s_air, t_air)
a_air = np.gradient(v_air, t_air)

# Velg ut simulert data med samme oppløsning som empiriske data
subset_indices = np.linspace(0, simRes-1, len(t), dtype=int)
s_air = s_air[subset_indices]
v_air = v_air[subset_indices]
a_air = a_air[subset_indices]



#%% Plot posisjon
plt.figure(1, figsize=(12, 9))
plt.plot(t, s_cal, label="Fritt Fall")
plt.plot(t, s_air, label="Luftmotstand")
plt.plot(t, s_emp, label="Empiriske Verdier")
plt.title("Posisjon [m]")
plt.xlabel("Tid [s]")
plt.ylabel("Posisjon [m]")
plt.legend()
plt.grid()
plt.show(block=False)

#%% Plot hastighet
plt.figure(2, figsize=(12, 9))
plt.plot(t, v_cal, label="Fritt Fall")
plt.plot(t, v_air, label="Luftmotstand")
plt.plot(t, v_emp, label="Empiriske Verdier")
plt.title("Hastighet [m/s]")
plt.xlabel("Tid [s]")
plt.ylabel("Hastighet [m/s]")
plt.legend()
plt.grid()
plt.show(block=False)

#%% Plot akselerasjon
plt.figure(3, figsize=(12, 9))
plt.plot(t, a_cal, label="Fritt Fall")
plt.plot(t, a_air, label="Luftmotstand")
plt.plot(t, a_emp, label="Empiriske Verdier")
plt.title("Akselerasjon [m/s²]")
plt.xlabel("Tid [s]")
plt.ylabel("Akselerasjon [m/s²]")
plt.legend()
plt.grid()
plt.show()