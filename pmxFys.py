#%%
import numpy as np
import matplotlib.pyplot as plt
import os

from objects import FallingObject, Ball, Cube


def simulate(obj: FallingObject, time, resolution):
    time, dt = np.linspace(time[0], time[-1], resolution, retstep=True)
    s = np.empty(resolution)

    for i in range(resolution):
        obj.update(dt)
        s[i] = obj.pos

    return time, s


# Define the integrate function
def integrate(array, time, start=0):
    """Integrate using the trapezoidal method."""
    array = np.nan_to_num(array)
    integrated = np.zeros(len(time))
    integrated[0] = start

    for i in range(1, len(time)):
        dt = time[i] - time[i-1]
        integrated[i] = integrated[i-1] + 0.5 * (array[i] + array[i-1]) * dt

    return integrated




#%%
# Fysiske konstanter og initialverdier
g = -9.81         # [m/s^2]
airDensity = 1.29 # [kg/m^3]

# Lag Boks objekt
boks = FallingObject(
    area=12.5e-2 * 19.5e-2,
    mass=0.21,
    dragCoeff=1.03,
    airDensity=airDensity,
    pos=0,
    vel=0,
    acc=g
)

simRes = 100000



#%% Empirisk Posisjon
t_tracked, s_tracked = np.loadtxt(
    "data/BoksFallTracked.csv",
    delimiter=",",
    skiprows=7, # Hopp over de linjene hvor boksen ikke ennå faller
    usecols=(0, 1),
    unpack=True
)


#%% Behandle data
s_tracked *= -1  # Snu retning til nedover

s_tracked -= s_tracked[0]  # Nullstill posisjon
t_tracked -= t_tracked[0]  # Nullstill tid


# Deriver for å få hastighet og akselerasjon
v_tracked = np.gradient(s_tracked, t_tracked)
a_tracked = np.gradient(v_tracked, t_tracked)


fall_duration = t_tracked[-1]  # Total tid for fallet




#%% Empirisk Akselerasjon
a_measured, t_measured = np.loadtxt(
    "data/BoksFallMeasured.csv",
    delimiter="\t",
    skiprows=2,
    usecols=(5, 9),
    unpack=True
)

fall_start_index = 83
fall_end_index = 96



# Behandle tid
t_measured -= t_measured[0]  # Nullstill tid relativt (første måling er 0)
t_measured *= 0.001 # Convert from milliseconds to seconds
t_measured -= t_measured[fall_start_index]  # Nullstill tid for å matche idpunktet når boksen slippes.



# Behandle akselerasjon
# Convert from micro:bit readings to m/s^2

# Remove faulty values that wrongly affects the average
a_measured[[21, 22]] = np.nan

# Find the value that microbit sends when standing still.
a_gravity = a_measured[6:35] # Acceleration when still
a_gravity_mean = np.nanmean(a_gravity)

# Convert to m/s^2
a_measured = ((a_measured / a_gravity_mean)) * 9.81 - 9.81 #  a_emp to m/s^2


# At the beginning of the fall, the microbit did not register the full acceleration. Set it manually to 9.81 m/s²
a_measured[fall_start_index] = -9.81



# Integrer for hastighet og posisjon

# Cut the data to only include the fall
t_measured = t_measured[fall_start_index:fall_end_index]
a_measured = a_measured[fall_start_index:fall_end_index]

# Integrer for å få hastighet og posisjon
v_measured = integrate(a_measured, t_measured)
s_measured = integrate(v_measured, t_measured)





#%% Beregn fritt fall (uten luftmotstand)
t_free = np.linspace(0, fall_duration, simRes)
s_free = 1/2 * g * t_free**2
v_free = g * t_free
a_free = g * np.ones_like(t_free)





#%% Beregn simulert fall med luftmotstand
t_air, s_air = simulate(boks, t_free, simRes)
v_air = np.gradient(s_air, t_air)
a_air = np.gradient(v_air, t_air)

t_air_terminal = np.linspace(0, 4, simRes)
boks.reset(pos=0, vel=0, acc=g)
s_air_terminal = simulate(boks, t_air_terminal, simRes)[1]
v_air_terminal = np.gradient(s_air_terminal, t_air_terminal)
a_air_terminal = np.gradient(v_air_terminal, t_air_terminal)



DPI = 600
imageFolder = "figures"


#%% Plot micro:bit data
# plt.figure("Målt av micro:bit", figsize=(12, 9))
# plt.plot(t_measured, a_measured, label="Målt akselerasjon")
# plt.plot(t_measured, v_measured, label="Hastighet")
# plt.plot(t_measured, s_measured, label="Posisjon")
# plt.title("Målt av micro:bit")
# plt.xlabel("Tid [s]")
# plt.ylabel("[m]    [m/s]    [m/s²]")
# plt.ylim([-12, 1])
# plt.legend()
# plt.grid()
# plt.show(block=False)
# plt.savefig(os.path.join(imageFolder, "microbit_data.png"), dpi=DPI, bbox_inches='tight')


# #%% Plot Tracker data
# plt.figure("Målt i Tracker", figsize=(12, 9))
# plt.plot(t_tracked, a_tracked, label="Akselerasjon")
# plt.plot(t_tracked, v_tracked, label="Hastighet")
# plt.plot(t_tracked, s_tracked, label="Målt Posisjon")
# plt.title("Målt i Tracker")
# plt.xlabel("Tid [s]")
# plt.ylabel("[m]    [m/s]    [m/s²]")
# plt.ylim([-12, 1])
# plt.legend()
# plt.grid()
# plt.show(block=False)
# plt.savefig(os.path.join(imageFolder, "tracker_data.png"), dpi=DPI, bbox_inches='tight')


# #%% Plot Tracker data, men uten akselerasjon
# plt.figure("Målt i Tracker uten a", figsize=(12, 9))
# plt.plot(t_tracked, v_tracked, label="Hastighet")
# plt.plot(t_tracked, s_tracked, label="Målt Posisjon")
# plt.title("Målt i Tracker (uten akselerasjon)")
# plt.xlabel("Tid [s]")
# plt.ylabel("[m]    [m/s]")
# plt.ylim([-12, 1])
# plt.legend()
# plt.grid()
# plt.show(block=False)
# plt.savefig(os.path.join(imageFolder, "tracker_data_no_acceleration.png"), dpi=DPI, bbox_inches='tight')


# #%% Plot fritt fall
# plt.figure("Fritt Fall", figsize=(12, 9))
# plt.plot(t_free, a_free, label="Akselerasjon")
# plt.plot(t_free, v_free, label="Hastighet")
# plt.plot(t_free, s_free, label="Posisjon")
# plt.title("Fritt Fall uten luftmotstand")
# plt.xlabel("Tid [s]")
# plt.ylabel("[m]    [m/s]    [m/s²]")
# plt.ylim([-12, 1])
# plt.legend()
# plt.grid()
# plt.show(block=False)
# plt.savefig(os.path.join(imageFolder, "free_fall.png"), dpi=DPI, bbox_inches='tight')


# #%% Plot luftmotstand
# plt.figure("Luftmotstand", figsize=(12, 9))
# plt.plot(t_air, a_air, label="Akselerasjon")
# plt.plot(t_air, v_air, label="Hastighet")
# plt.plot(t_air, s_air, label="Posisjon")
# plt.title("Fall med luftmotstand")
# plt.xlabel("Tid [s]")
# plt.ylabel("[m]    [m/s]    [m/s²]")
# plt.legend()
# plt.grid()
# plt.show(block=False)
# plt.savefig(os.path.join(imageFolder, "air_resistance.png"), dpi=DPI, bbox_inches='tight')




#%% Plot alle posisjon
plt.figure("Alle Posisjoner", figsize=(12, 9))
plt.plot(t_free, s_free, label="Fritt Fall")
plt.plot(t_air, s_air, label="Luftmotstand")
plt.plot(t_tracked, s_tracked, label="Tracker: Målt s")
plt.plot(t_measured, s_measured, label="micro:bit: Integrert a → v → s")
plt.title("Alle Posisjoner")
plt.ylabel("Posisjon [m]")
plt.xlabel("Tid [s]")
plt.legend()
plt.show(block=False)
plt.savefig(os.path.join(imageFolder, "all_positions.png"), dpi=DPI, bbox_inches='tight')



#%% Plot alle hastighet
plt.figure("Alle Hastigheter", figsize=(12, 9))
plt.plot(t_free, v_free, label="Fritt Fall")
plt.plot(t_air, v_air, label="Luftmotstand")
plt.plot(t_tracked, v_tracked, label="Tracker: Derivert s → v")
plt.plot(t_measured, v_measured, label="micro:bit: Integrert a → v")

plt.title("Alle Hastigheter")
plt.ylabel("Hastighet [m/s]")
plt.xlabel("Tid [s]")
plt.legend()
plt.show(block=False)
plt.savefig(os.path.join(imageFolder, "all_velocities.png"), dpi=DPI, bbox_inches='tight')



#%% Plot terminal hastighet
plt.figure("Terminal Hastighet", figsize=(12, 9))


# One axis for position, on for v and a
ax1 = plt.gca()
ax2 = ax1.twinx()

# Plot position on the first axis
ax1.plot(t_air_terminal, s_air_terminal, label="Posisjon", color="blue")
ax1.set_ylabel("Posisjon [m]")
ax1.set_xlabel("Tid [s]")
ax1.set_ylim([-30, 30/12])
ax1.legend(loc='upper left')
ax1.grid()

# Plot velocity and acceleration on the second axis
ax2.plot(t_air_terminal, v_air_terminal, label="Hastighet", color="green")
ax2.plot(t_air_terminal, a_air_terminal, label="Akselerasjon", color="red")
ax2.set_ylabel("Hastighet [m/s]      Akselerasjon [m/s²]")
ax2.set_ylim([-12, 1])
ax2.legend(loc='upper right')

ax2.grid()

plt.title("Fall med Luftmotstand oppnår terminal hastighet")
plt.xlabel("Tid [s]")
plt.legend()
plt.show(block=False)
plt.savefig(os.path.join(imageFolder, "terminal_velocity.png"), dpi=DPI, bbox_inches='tight')



#%% Plot alle akselerasjon
plt.figure("Alle Akselerasjoner", figsize=(12, 9))
plt.plot(t_free, a_free, label="Fritt Fall")
plt.plot(t_air, a_air, label="Luftmotstand")
plt.plot(t_tracked, a_tracked, label="Tracker: derivert s → v → a")
plt.plot(t_measured, a_measured, label="micro:bit: Målt a")
plt.title("Alle Akselerasjoner")
plt.ylabel("Akselerasjon [m/s²]")
plt.xlabel("Tid [s]")
plt.legend()
plt.show(block=False)
plt.savefig(os.path.join(imageFolder, "all_accelerations.png"), dpi=DPI, bbox_inches='tight')


# Plot alle akselerasjon uten tracker data
plt.figure("Akselerasjoner uten Tracker", figsize=(12, 9))
plt.plot(t_free, a_free, label="Fritt Fall")
plt.plot(t_air, a_air, label="Luftmotstand")
plt.plot(t_measured, a_measured, label="micro:bit: målt a", color="red")
plt.title("Akselerasjoner uten Tracker")
plt.ylabel("Akselerasjon [m/s²]")
plt.xlabel("Tid [s]")
plt.legend()
plt.grid()
plt.show(block=False)
plt.savefig(os.path.join(imageFolder, "all_accelerations_no_tracker.png"), dpi=DPI, bbox_inches='tight')

plt.show()

plt.close('all')  # Close all figures to free up memory




