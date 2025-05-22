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
m = 0.00244       # [kg]
radius = 0.02     # [m]
airDensity = 1.29 # [kg/m^3]

# Lag objekt
ball = Ball(
    radius=radius,
    mass=m,
    dragCoeff=0.42,
    airDensity=airDensity,
    pos=s0,
    vel=v0,
    acc=g
)

simRes = 100000

#%% Last inn empiriske data
dataFileName = os.path.join("data", "fall2.csv")
imageFolderPath = os.path.join("..", "bilder")

a_emp, t_emp = np.loadtxt(
    dataFileName,
    delimiter="\t",
    skiprows=2,
    max_rows=3000,
    usecols=(7, 9),
    unpack=True
)

t_emp *= 10E-4  # Convert from microseconds to seconds


# Manual correction


# Find the value that microbit sends when standing still.
a_still = a_emp[0:35] # Acceleration when still
a_still_mean = np.nanmean(a_still)

# Convert 
a_emp = ((a_emp / a_still_mean)) * 9.81 - 9.81 #  a_emp to m/s^2


a_emp[56] = 108 # When the microbit hit the ground, it didn't register the full acceleration. Set it manually.
a_emp[[57,58]] = -9.81




# Plot raw acceleration data
plt.figure("Raw akselerasjon", figsize=(12, 9))
plt.plot(t_emp[0:len(a_still)], a_still, label="akselerasjon")
plt.hlines(a_still_mean, t_emp[0], t_emp[len(a_still)-1], color="red", linestyle="--", label="null")
plt.title("Rå akselerasjon [m/s²]")
plt.xlabel("Tid [s]")
plt.ylabel("Akselerasjon [m/s²]")
plt.legend()
plt.grid()
plt.show(block=False)




#%% Behandle empiriske data

# a_emp *= -1  # Snu retning til nedover

t_min = t_emp[0]
t_max = t_emp[-1]


for i in range(len(a_emp)):
    t = t_emp[i]
    # t_emp[i] = i
    
    if t < t_min or t > t_max:
        a_emp[i] = np.nan
        
    

# Integrate a_emp over t_emp to get v_emp
# Interpolate and reset start to 0 for a_emp
t_emp = t_emp - t_emp[0]
interpLength = len(t_emp) * 16
new_t_emp = np.linspace(t_emp[0], t_emp[-1], interpLength)

a_emp = np.nan_to_num(a_emp)
a_emp = np.interp(new_t_emp, t_emp, a_emp)

t_emp = new_t_emp

# Define the integrate function
def integrate(array, time, start=0):
    integrated = np.zeros(len(time))
    integrated[0] = start
    for i in range(1, len(time)):
        integrated[i] = integrated[i-1] + array[i] * (time[i] - time[i-1])
    return integrated

v_emp = integrate(a_emp, t_emp)
s_emp = integrate(v_emp, t_emp)


# t = t_emp
# s_emp = 1/2 * np.nan_to_num(a_emp) * (t-t[0])**2 + v_emp[i-1] * (t-t[0])
# print(s_emp)

# Integrate a_emp over t_emp to get v_emp



# # Deriver for å få hastighet og akselerasjon
# v_emp = np.gradient(s_emp, t)
# a_emp = np.gradient(v_emp, t)



# #%% Beregn fritt fall (uten luftmotstand)
# s_cal = g / 2 * t**2 + v0 * t + s0
# v_cal = np.gradient(s_cal, t)
# a_cal = np.gradient(v_cal, t)



# #%% Beregn simulert fall med luftmotstand
# t_air, s_air = simulate(ball, t[0], 1.2, simRes)
# v_air = np.gradient(s_air, t_air)
# a_air = np.gradient(v_air, t_air)

# # Velg ut simulert data med samme oppløsning som empiriske data
# subset_indices = np.linspace(0, simRes-1, len(t), dtype=int)
# s_air = s_air[subset_indices]
# v_air = v_air[subset_indices]
# a_air = a_air[subset_indices]



#%% Plot posisjon
# plt.figure("Posisjon", figsize=(12, 9))
# # plt.plot(t, s_cal, label="Fritt Fall")
# # plt.plot(t, s_air, label="Luftmotstand")
# # plt.plot(t_emp, s_emp, label="Empiriske Verdier")
# plt.title("Posisjon [m]")
# plt.xlabel("Tid [s]")
# plt.ylabel("Posisjon [m]")
# plt.legend()
# plt.grid()
# plt.show(block=False)




#%% Plot hastighet
plt.figure("Hastighet", figsize=(12, 9))
# plt.plot(t, v_cal, label="Fritt Fall")
# plt.plot(t, v_air, label="Luftmotstand")
plt.plot(t_emp, v_emp, label="Fart")
plt.plot(t_emp, s_emp, label="Posisjon")
plt.title("Hastighet [m/s]")
plt.xlabel("Tid [s]")
plt.ylabel("Hastighet [m/s]")
plt.legend()
plt.grid()
# plt.show(block=False)

#%% Plot akselerasjon
# plt.figure("Akselerasjon", figsize=(12, 9))
# plt.plot(t, a_cal, label="Fritt Fall")
# plt.plot(t, a_air, label="Luftmotstand")
plt.plot(t_emp, a_emp, label="akselerasjon")

plt.title("Akselerasjon [m/s²]")
plt.xlabel("Tid [s]")
plt.ylabel("Akselerasjon [m/s²]")
plt.legend()
plt.grid()
plt.show()