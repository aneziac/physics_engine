class Material():
    def __init__(self, d):
        self.d = d # density in kg/m^3
        # velocity vector fields?

class Fluid(Material):
    pass

class Element(Material):
    pass

class Body(Material):
    pass

Vacuum = Material(0)
English_Brown_Oak = Material(740)
Air = Fluid(1.225)
Water = Fluid(1000)
Aluminum = Element(2700)
Iron = Element(7870)
Copper = Element(8960)
Gold = Element(19320)
Rocky_Planet = Body(5000)
Gas_Planet = Body(1225)
Sun = Body(1410)
Asteroid = Body(2000)
