import pygame as pg
import sys
import time
import os

pg.init()

#---LOCAL---
from data import common as cm, settings as st, sims
from loop import ui, backgrounds, controls
import physics_engine as pe

def main():

    pe.reset_all()
    elapsed = time.time()

    if st.EVENT_LOG:
        data = open("event_logs/event_log_" + str(len([name for name in os.listdir('./event_logs') if name != '.DS_Store']) + 1) + ".txt", "w")
        data.write("Simulation %s on " % sims.SIM_NAMES[sims.SIM] + time.ctime(time.time()) + "\n\n")

    if sims.SIM_TYPE == 1:
        cm.uicolor = (255, 255, 255)
        cm.wld_width, cm.wld_height = st.DSPACE_WIDTH, st.DSPACE_HEIGHT

    # main loop
    while True:
        cm.SCREEN.fill((255, 255, 255))

        keys = pg.key.get_pressed()

        # enables quitting by pressing q or clicking red x
        for event in pg.event.get():
            if event.type == pg.QUIT or keys[pg.K_q]:
                if st.EVENT_LOG:
                    data.write("\nSimulation ended at %.2f secs" % cm.total_time)
                    data.close()
                    print("Results written to event_logs/event_log_" + str(len([name for name in os.listdir('./event_logs') if name != '.DS_Store'])) + ".txt")
                pg.quit()
                sys.exit()

        if keys[pg.K_SPACE]:
            while pg.key.get_pressed()[pg.K_SPACE]:
                pg.event.get()
            elapsed = time.time()
            cm.pause = not cm.pause

        controls.all(keys)

        if cm.pause:
            dt = 0
        else:
            dt = (time.time() - elapsed) * cm.sim_speed
            elapsed = time.time()

        cm.total_time += dt
        
        if keys[pg.K_r] or cm.total_time < 0:
            pe.reset_all()
            cm.total_time = 0

        backgrounds.render()

        # render layer
        for instance in pe.Object.instances:
            instance.update(dt)
        for instance in pe.Object.instances:
            instance.render()

        if st.SHOW_VECTORS:
            for instance in pe.Object.instances:
                instance.render_vectors()

        # user interface
        ui.render(keys)

        if st.EVENT_LOG:
            for event in cm.events:
                data.write(event)
            cm.events.clear()

        # updates frame and resets
        pg.display.update()

main()
