import pygame as pg
import sys
import random as rm
import time
import os
import common as cm
import settings as st
import sims
import physics_engine as pe

def main():

    STARS = []
    for x in range(st.STARS_AMOUNT):
        STARS.append([(rm.randint(0, st.SCR_WIDTH), rm.randint(0, st.SCR_HEIGHT)), rm.randint(2, 3)])

    pe.reset_all()
    elapsed = time.time()
    pause = False

    if st.EVENT_LOG:
        data = open("event_logs/event_log_" + str(len([name for name in os.listdir('./event_logs') if name != '.DS_Store']) + 1) + ".txt", "w")
        data.write("Simulation %s on " % sims.SIM_NAMES[sims.SIM] + time.ctime(time.time()) + "\n\n")

    # asset loading
    PLAY = pg.image.load(os.path.join('assets','play.png'))
    PAUSE = pg.image.load(os.path.join('assets', 'pause.png'))
    IPLAY = pg.image.load(os.path.join('assets','iplay.png'))
    IPAUSE = pg.image.load(os.path.join('assets', 'ipause.png'))
    
    if sims.SIM_TYPE == 1:
        uicolor = (255, 255, 255)
        cm.wld_width, cm.wld_height = st.DSPACE_WIDTH, st.DSPACE_HEIGHT
    else:
        uicolor = (0, 0, 0)

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

        zooms = [0.2, 0.5, 1, 2, 5]
        if keys[pg.K_1]:
            if sims.SIM_TYPE == 0:
                cm.wld_width, cm.wld_height = st.DWLD_WIDTH, st.DWLD_HEIGHT * zooms[0]
            else:
                cm.wld_width, cm.wld_height = st.DSPACE_WIDTH, st.DSPACE_HEIGHT * zooms[0]
        elif keys[pg.K_2]:
            if sims.SIM_TYPE == 0:
                cm.wld_width, cm.wld_height = st.DWLD_WIDTH, st.DWLD_HEIGHT * zooms[1]
            else:
                cm.wld_width, cm.wld_height = st.DSPACE_WIDTH, st.DSPACE_HEIGHT * zooms[1]
        elif keys[pg.K_3]:
            if sims.SIM_TYPE == 0:
                cm.wld_width, cm.wld_height = st.DWLD_WIDTH, st.DWLD_HEIGHT * zooms[2]
            else:
                cm.wld_width, cm.wld_height = st.DSPACE_WIDTH, st.DSPACE_HEIGHT * zooms[2]
        elif keys[pg.K_4]:
            if sims.SIM_TYPE == 0:
                cm.wld_width, cm.wld_height = st.DWLD_WIDTH, st.DWLD_HEIGHT * zooms[3]
            else:
                cm.wld_width, cm.wld_height = st.DSPACE_WIDTH, st.DSPACE_HEIGHT * zooms[3]
        elif keys[pg.K_5]:
            if sims.SIM_TYPE == 0:
                cm.wld_width, cm.wld_height = st.DWLD_WIDTH, st.DWLD_HEIGHT * zooms[4]
            else:
                cm.wld_width, cm.wld_height = st.DSPACE_WIDTH, st.DSPACE_HEIGHT * zooms[4]

        if sims.SIM_TYPE == 0:
            # builds Y-axis scale
            for x in range(st.TICK_MARKS):
                a = x * round(st.SCR_HEIGHT / st.TICK_MARKS)
                if x % 2 == 0:
                    pg.draw.rect(cm.SCREEN, (240, 240, 240), cm.trect([0, a, st.SCR_WIDTH, st.SCR_HEIGHT/st.TICK_MARKS]))
                cm.rect((0, a, 5, 2))
                cm.SCREEN.blit(st.FONTS.render(str(int((x * cm.wld_height) / st.TICK_MARKS)) + " " + st.UNIT, True, pg.Color('black')), cm.trect((2, a + 13, 10, a)))

        elif sims.SIM_TYPE == 1:
            cm.SCREEN.fill((0, 0, 0))
            for x in range(st.STARS_AMOUNT):
                pg.draw.circle(cm.SCREEN, (255, 255, 255), STARS[x][0], STARS[x][1])

        if keys[pg.K_SPACE]:
            while pg.key.get_pressed()[pg.K_SPACE]:
                pg.event.get()
                elapsed = time.time()
            pause = not pause

        sim_speed = st.DEFAULT_SIM_SPEED

        if keys[pg.K_t]:
            sim_speed *= -1
        if keys[pg.K_a]:
            sim_speed /= 100
        elif keys[pg.K_s]:
            sim_speed /= 50
        elif keys[pg.K_d]:
            sim_speed /= 10
        elif keys[pg.K_f]:
            sim_speed /= 2
        elif keys[pg.K_j]:
            sim_speed *= 2
        elif keys[pg.K_k]:
            sim_speed *= 10
        elif keys[pg.K_l]:
            sim_speed *= 50
        elif keys[pg.K_SEMICOLON]:
            sim_speed *= 100

        if pause:
            dt = 0
        else:
            dt = (time.time() - elapsed) * sim_speed
            elapsed = time.time()

        cm.total_time += dt

        if keys[pg.K_r] or cm.total_time < 0:
            pe.reset_all()
            dt = 0
            cm.total_time = 0

        # render layer
        for instance in pe.Object.instances:
            instance.update(dt)
        for instance in pe.Object.instances:
            instance.render()

        # GUI and debug layer
        cm.SCREEN.blit(st.FONTS.render(str(round(cm.total_time, 2)), True, pg.Color('blue')), cm.trect((st.SCR_WIDTH - 55, st.SCR_HEIGHT - 10, 0, 0)))

        if keys[pg.K_a] or keys[pg.K_s] or keys[pg.K_d]:
            if keys[pg.K_t]:
                tcoffset = round(100 * 2 / 7) # time control offset
            else:
                tcoffset = round(100 * 4 / 7)
        elif keys[pg.K_j] or keys[pg.K_k] or keys[pg.K_l]:
            if keys[pg.K_t]:
                tcoffset = round(100 * 0 / 7)
            else:
                tcoffset = round(100 * 6 / 7)
        else:
            if keys[pg.K_t]:
                tcoffset = round(100 * 1 / 7)
            else:
                tcoffset = round(100 * 5 / 7)

        pg.draw.rect(cm.SCREEN, (200, 200, 200), cm.trect((10 + tcoffset, st.SCR_HEIGHT - 35, 14, 20)))
        cm.SCREEN.blit(st.FONTT.render(str(sim_speed) + "x", True, uicolor), cm.tcirc((53, st.SCR_HEIGHT - 35)))

        if sims.SIM_TYPE == 0:
            pg.draw.rect(cm.SCREEN, (200, 200, 200), cm.trect(((st.FONTS.size("1 2 3 4 5")[0] / 5) * zooms.index(cm.wld_height / st.DWLD_HEIGHT) + 320, st.SCR_HEIGHT - 35 - st.FONTS.size("1 2 3 4 5")[1], st.FONTS.size("1 2 3 4 5")[0] / 5, st.FONTS.size("1 2 3 4 5")[1])))
        elif sims.SIM_TYPE == 1:
            pg.draw.rect(cm.SCREEN, (200, 200, 200), cm.trect(((st.FONTS.size("1 2 3 4 5")[0] / 5) * zooms.index(cm.wld_height / st.DSPACE_HEIGHT) + 320, st.SCR_HEIGHT - 35 - st.FONTS.size("1 2 3 4 5")[1], st.FONTS.size("1 2 3 4 5")[0] / 5, st.FONTS.size("1 2 3 4 5")[1])))

        cm.SCREEN.blit(st.FONTS.render("1 2 3 4 5", True, uicolor), cm.tcirc((320, st.SCR_HEIGHT - 35)))

        if pause:
            if sims.SIM_TYPE == 0:
                cm.SCREEN.blit(PAUSE, cm.tcirc((10, st.SCR_HEIGHT - 15)))
            else:
                cm.SCREEN.blit(IPAUSE, cm.tcirc((10, st.SCR_HEIGHT - 15)))
        else:
            if sims.SIM_TYPE == 0:
                cm.SCREEN.blit(PLAY, cm.tcirc((10, st.SCR_HEIGHT - 15)))
            else:
                cm.SCREEN.blit(IPLAY, cm.tcirc((10, st.SCR_HEIGHT - 15)))

        if st.SHOW_VECTORS:
            for instance in pe.Object.instances:
                instance.render_vectors()

        if st.EVENT_LOG:
            for event in cm.events:
                data.write(event)
            cm.events.clear()

        # updates frame and resets
        pg.display.update()

main()
