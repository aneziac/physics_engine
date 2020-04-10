import physics_engine.menu as menu
from physics_engine.data import materials as mats, colors, objects as objs
from physics_engine.common import common as cm
from physics_engine.loop import physics as phys


class Simulation:
    instances = []
    SIM_TYPES = ["Earth", "Space"]
    SIM_NAMES = []

    def __init__(self, name, sim_type, sim_dims, gravity_catalyst, objects, fluid=mats.Vacuum, temperature=0):
        Simulation.instances.append(self)
        self.name = name
        Simulation.SIM_NAMES.append(name)
        self.sim_type = sim_type
        if self.sim_type not in Simulation.SIM_TYPES:
            raise ValueError("Nonexistent Simulation Type")
        self.sim_dims = sim_dims
        self.gravity_catalyst = gravity_catalyst
        self.objects = objects
        self.fluid = fluid
        self.temperature = temperature

    def start(self):
        objs.Object.reset_all()
        cm.clock.update()

        for obj in self.objects:
            obj.show = True

        cm.clock.total_time = 0

        phys.Physics.physics_settings(self.fluid, self.temperature, self.gravity_catalyst)
        return self.sim_dims, self.sim_type

    @staticmethod
    def pick_sim(SCREEN):
        objs.Object.hide_all()
        chosen = menu.menu.reset(SCREEN, Simulation.SIM_NAMES)

        for sim in Simulation.instances:
            if sim.name == chosen:
                return sim.start()

    @staticmethod
    def create_sims():
        Simulation("Earth 01", "Earth", [50, 50], 1, [
            objs.Ball("green ball", [20, 50], [0, 0], [0, 0], mats.Iron, colors.GREEN, 0.7, 1),
            objs.Ball("blue ball", [40, 50], [0, 0], [0, 0], mats.Copper, colors.BLUE, 0.9, 0.8),
            objs.Ball("red ball", [10, 50], [0, 0], [0, 0], mats.Aluminum, colors.RED, 0.6, 0.5),
            objs.Ball("brown ball", [30, 50], [0, 0], [0, 0], mats.Gold, colors.BROWN, 0.6, 3)],
            mats.Air, 20),

        Simulation("Space 01", "Space", [400, 400], 100000, [
            # implement camera later
            objs.Satellite("asteroid", [20, 200], [0, 1], [0, 0], mats.Asteroid, (61, 61, 41), 0.5, 3),
            objs.Satellite("star", [200, 200], [0, 0], [0, 0], mats.Sun, (255, 204, 0), 0.5, 10),
            objs.Satellite("planet", [200, 350], [3, 0], [0, 0], mats.Rocky_Planet, colors.RED, 0.5, 5)],
        )
