import numpy as np 


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