import sys
import os
import time
sys.path.append("...")

# ---INTERNAL---
from physics_engine.data import settings as st, sims, assets as at, objects
from physics_engine.common import common as cm
from physics_engine.loop import ui, backgrounds, controls

# ---EXTERNAL---
try:
    import pygame as pg
except ImportError:
    os.system("make")

# initializes pygame
pg.init()
pg.font.init()


class Screen:
    def __init__(self, width, height, title):
        self.SCREEN = pg.display.set_mode([width, height])  # creates screen
        self.trans = cm.Transform()
        self.files = cm.Files()
        self.events = []
        pg.display.set_caption(title)
        sims.Simulation.create_sims()
        self.CONTROLS = controls.Controls()
        self.UI = ui.UI()
        self.BACKGROUNDS = backgrounds.Backgrounds()
        self.reset()
        print("Initialized\nRunning...")

    def render_physics(self, dt, wld_dims):
        for instance in objects.Object.instances:
            if instance.show:
                instance.update(dt, self.events, wld_dims)
        for instance in objects.Object.instances:
            if instance.show:
                instance.render(self.SCREEN, wld_dims)

        if st.SHOW_VECTORS:
            for instance in objects.Object.instances:
                if instance.show:
                    instance.render_vectors(self.SCREEN, wld_dims)

    def update(self):
        if st.EVENT_LOG:
            for event in self.events:
                self.data.write(event)
            self.events.clear()

        pg.display.update()

    def reset(self):
        if st.EVENT_LOG:
            self.data = open("logs/event_logs/event_log_" + str(self.files.num_files('.../logs/event_logs')) + ".txt", "w")
            self.data.write("Simulation %s on " % self.sim_type + time.ctime(time.time()) + "\n\n")
        else:
            self.data = None
        wld_dims, sim_type = sims.Simulation.pick_sim(self.SCREEN)
        self.CONTROLS.reset(wld_dims, sim_type)
        self.BACKGROUNDS.reset(sim_type)
        self.UI.reset(sim_type)

    def loop(self):
        keys = pg.key.get_pressed()

        dt, pause, scl_dims, scl_index, menu = self.CONTROLS.all(keys, self.data)
        if menu:
            self.reset()

        self.BACKGROUNDS.render(self.SCREEN, scl_dims)
        self.render_physics(dt, scl_dims)
        self.UI.render(self.SCREEN, keys, dt, pause, scl_index)

        cm.clock.update_info(dt)

        self.update()


def main():

    at.LoadAssets()

    screen = Screen(st.SCR_WIDTH, st.SCR_WIDTH, "physics_engine")

    # main loop
    while True:
        screen.loop()


if __name__ == '__main__':
    main()
