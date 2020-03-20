common.py
=========
For functions, variables, and classes shared between multiple files that aren't settings.

Functions
---------
1. trect([x, y, a, b])
     Transforms coordinates for a rectangle from the original Quadrant IV to the more intuitive Quadrant I.
2. rect([x, y, a, b])
     Creates a black rectangle at the specified coordinates. For testing and simple operations.
3. tcirc([x, y])
     Transforms 2 coordinates from Quadrant IV to Quadrant I.

Variables
---------
1. total_time
     The total time that's passed since the simulation began.
2. events
     A list of events that have occurred during the simulation.
3. pause
    Boolean that determines whether the engine is paused.
4. uicolor

3. SCREEN
     The screen itself. Main surface to write to.
