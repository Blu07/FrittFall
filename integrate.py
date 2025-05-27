import numpy as np


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