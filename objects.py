
import numpy as np

class FallingObject:
    
    G = -9.81  # [m/s^2]
    
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
        
        dragForce = 1/2 * self.airDensity * self.dragCoeff * self.area * v**2
        self.acc = self.G + ( dragForce / self.mass )



class Ball(FallingObject):
    
    def __init__(self, radius, mass, dragCoeff, airDensity, pos, vel, acc):
        super().__init__(mass, np.pi*radius**2, dragCoeff, airDensity, pos, vel, acc)
        
        self.radius = radius


class Cube(FallingObject):
    
    dragCoeff = 1.05  # Face down 
    
    def __init__(self, radius, mass, airDensity, pos, vel, acc):
        super().__init__(mass, np.pi*radius**2, self.dragCoeff, airDensity, pos, vel, acc)
        
        self.radius = radius
        
