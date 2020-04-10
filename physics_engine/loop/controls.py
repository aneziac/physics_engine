import pygame as pg
import sys
from math import floor
from physics_engine.data import settings as st, objects as objs
from physics_engine.common import common as cm


class Controls:
    def __init__(self):
        self.pause = False
        self.current_zoom = 2
        self.files = cm.Files()

    def reset(self, wld_dims, sim_type):
        self.wld_dims = wld_dims
        self.sim_type = sim_type

    def all(self, keys, data):
        self.quit_game(keys)
        self.speeds(keys)
        menu = self.menu(keys, data)
        self.reset_sim(keys)
        check_pause = self.check_pause(keys)
        zooms = self.zooms(keys)
        return check_pause[0], check_pause[1], zooms[0], zooms[1], menu

    def quit_game(self, keys):
        # enables quitting by pressing q or clicking red x
        for event in pg.event.get():
            if event.type == pg.QUIT or keys[pg.K_q]:
                pg.quit()
                sys.exit()

    def zooms(self, keys):
        for x in range(len(st.ZOOMS)):
            if keys[eval("pg.K_" + str(x + 1))]:
                self.current_zoom = x
        return [x * st.ZOOMS[self.current_zoom] for x in self.wld_dims], self.current_zoom

    def speeds(self, keys):
        cm.clock.reset_speed()

        if keys[pg.K_t]:
            cm.clock.scale_speed(-1)

        for x in range(len(st.SPEED_KEYS)):
            key = st.SPEED_KEYS[x]

            if key not in 'abcdefghijklmnopqrstuvwxyz':
                if key == ';':
                    key = 'SEMICOLON'

            if keys[eval("pg.K_" + key)]:
                cm.clock.scale_speed(st.SPEEDS[floor(abs(((len(st.SPEED_KEYS) + 1) / 2) - x - 1))] ** ((x // (len(st.SPEED_KEYS) / 2)) * 2 - 1))
                return

    def check_pause(self, keys):
        if keys[pg.K_SPACE]:
            while pg.key.get_pressed()[pg.K_SPACE]:
                pg.event.get()
            self.pause = not self.pause
            dt = 0
            cm.clock.update()

        if self.pause:
            dt = 0
        else:
            dt = round(cm.clock.elapsed(), 6)
            cm.clock.update()

        return dt, self.pause

    def menu(self, keys, data):
        if keys[pg.K_m]:
            if st.EVENT_LOG:
                data.write("\nSimulation ended at %.2f secs" % cm.clock.total_time)
                data.close()
                print("Results written to logs/event_logs/event_log_" + str(self.files.num_files('.../logs/event_logs')) + ".txt")

            return True

    def reset_sim(self, keys):
        if keys[pg.K_r] or cm.clock.total_time < 0 or cm.clock.frame < 0:
            objs.Object.reset_all()
