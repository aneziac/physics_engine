physics_engine.py
=================
The physics engine itself.

Global
------

Classes
-------
Object
******
An object is defined as any matter, no matter the size. Ex: planet, particle, cube.
Subclasses differ based on shape.

Variables
^^^^^^^^^
For physical properties of all objects in the world. Every object that’s a member of the object class has a setting for each of these properties. These are static, versus the non-initial values, which change.
- An “i” prefix on any of these variables refers to its initial value
- “reality” refers to either WLD or SPACE depending on the object
- “d” means delta, or change

1. instances
     Global variable in the class. List of all instances of the class
2. x, y
     X position and Y position in reality
3. xv, yv
     X velocity and Y velocity in dreality/dt
4. xa, ya
     X acceleration and Y acceleration in dvelocity/dt
5. m
     Mass
6. c
     Color. RGB tuple
7. e
     Coefficient of restitution (COR) for bouncing off surfaces.

Methods
^^^^^^^
1. Init
     -Initializes every initial variable
     -Adds itself to the list of objects
2. Reset
     Reverts to initial values for an object, resetting its simulation.
3. Update
     Updates all variables based on what happened last dt. For universal laws of physics that are visible at all scales. Draws velocity and acceleration vectors if SHOW_VECTORS is true.