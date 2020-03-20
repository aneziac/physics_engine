import menu
import physics_engine as pe
import materials as mat

SIM_NAMES = ["Earth 01", "Space 01"] # simulation names
SIM_TYPES = ["Earth", "Space"]
SIM = menu.menu()

if SIM == 0:
    pe.Ball("ball 1", [20, 50], [0, 0], [0, 0], mat.Iron, (0, 255, 0), 0.7, 1)
    pe.Ball("ball 2", [40, 50], [0, 0], [0, 0], mat.Copper, (0, 0, 255), 0.9, 0.8)
    pe.Ball("ball 3", [10, 50], [0, 0], [0, 0], mat.Aluminum, (255, 0, 0), 0.6, 0.5)
    pe.Ball("ball 4", [30, 50], [0, 0], [0, 0], mat.Gold, (100, 50, 0), 0.6, 3)
    SIM_TYPE = SIM_TYPES.index("Earth")

elif SIM == 1:
    # implement camera later
    pe.Satellite("asteroid", [20, 200], [0, 1], [0, 0], mat.Asteroid, (61, 61, 41), 0.5, 3)
    pe.Satellite("star", [200, 200], [0, 0], [0, 0], mat.Sun, (255, 204, 0), 0.5, 10)
    pe.Satellite("planet", [200, 350], [3, 0], [0, 0], mat.Rocky_Planet, (255, 0, 0), 0.5, 5)
    SIM_TYPE = SIM_TYPES.index("Space")
