class Material():
    def __init__(self, d):
        self.d = d  # density in kg/m^3
        # velocity vector fields?


class Fluid(Material):
    pass


class Element(Material):
    def __init__(self, symbol, d, atomic_number, atomic_weight):
        self.symbol = symbol
        super().__init__(d)  # https://www.chemicool.com/densities.html at 20 degrees celsius
        self.atomic_number = atomic_number
        self.atomic_weight = atomic_weight


class Body(Material):
    pass


Vacuum = Material(0)
English_Brown_Oak = Material(740)

Air = Fluid(1.225)
Water = Fluid(1000)

Aluminum = Element("Al", 2702, 13, 26.982)
Iron = Element("Fe", 7870, 26, 55.845)
Copper = Element("Cu", 8960, 29, 63.546)
Gold = Element("Au", 19320, 79, 196.97)

Rocky_Planet = Body(5000)
Gas_Planet = Body(1225)
Sun = Body(1410)
Asteroid = Body(2000)
