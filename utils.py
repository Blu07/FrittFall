import numpy as np 

from objects import FallingObject

def calculateCd(s_emp, a_emp, v_emp, t_emp, A, m, airDensity):
    
    coeffList = []
    g = -9.81 # [m/s^2]
    aD = airDensity # [kg/m^3]
    
    for i in range(len(s_emp)):
        a = a_emp[i]
        v = v_emp[i]
        time = t_emp[i]
        
        Cd = 2*m * ( g - a )/( aD * A * v**2 )
        
        
        if Cd < 0.5 and Cd > -2 and time > 0.4:
            coeffList.append(Cd)
        else:
            coeffList.append(np.nan)




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



def simulate(obj: FallingObject, time, resolution):
    time, dt = np.linspace(time[0], time[-1], resolution, retstep=True)
    s = np.empty(resolution)
    v = np.empty(resolution)
    a = np.empty(resolution)

    for i in range(resolution):
        obj.update(dt)
        s[i] = obj.pos
        v[i] = obj.vel
        a[i] = obj.acc

    return time, s, v, a