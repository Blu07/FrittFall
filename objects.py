
import numpy as np

class FallingObject:
    
    g = -9.81  # [m/s^2]
    
    def __init__(self, mass, area, dragCoeff, airDensity, pos, vel, acc):
        self.mass = mass
        self.area = area
        self.dragCoeff = dragCoeff
        
        self.airDensity = airDensity
        
        self.pos = pos
        self.vel = vel
        self.acc = acc
        
    
    def update(self, dt):
        """Update the position, velocity and acceleration based on falling in air.
        """
        v = self.vel + self.acc * dt
        
        self.vel = v
        self.pos = self.pos + v * dt
        
        dragForce = 1/2 * self.airDensity * self.dragCoeff * self.area * abs(v)*v # v^2, but keep the sign of v
        self.acc = self.g - ( dragForce / self.mass )

    def reset(self, pos=None, vel=None, acc=None):
        """Reset the position, velocity and acceleration of the object.
        """
        if pos is not None:
            self.pos = pos
        if vel is not None:
            self.vel = vel
        if acc is not None:
            self.acc = acc

class Ball(FallingObject):
    
    def __init__(self, radius, mass, dragCoeff, airDensity, pos, vel, acc):
        super().__init__(mass, np.pi*radius**2, dragCoeff, airDensity, pos, vel, acc)
        
        self.radius = radius


class Cube(FallingObject):
    
    def __init__(self, sideLen, mass, dragCoeff, airDensity, pos, vel, acc):
        super().__init__(mass, sideLen**2, dragCoeff, airDensity, pos, vel, acc)
        
        self.sideLen = sideLen
        
