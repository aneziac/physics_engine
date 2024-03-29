![logo](logo/logo.png)

![version](https://img.shields.io/badge/version-0.4.0-blue)
![MIT License](https://img.shields.io/badge/license-MIT-blue)

**physics_engine** is a 2D physics engine and editor featuring simulations at multiple scales. 
It was created as a hobbyist project.

# Features
- Time controls (Note that this is still a work in progress.)
- Customizable objects
- Laws of physics including orbits, drag, conservation of momentum, buoyancy etc.

# Dependencies
- [pygame](https://www.pygame.org/)

# Usage
Clone or download the repository to use the software.
Dependencies can be dowloaded using the Makefile:

``$ make``

The engine can be run as a module with the following command:

``$ python -m physics_engine``

# Configuration
General settings can be changed in ``physics_engine/data/settings.py`` and the simulation parameters can be changed in ``physics_engine/data/sims.py``.
See the documentation to customize simulations further.

# License
[MIT License](https://choosealicense.com/licenses/mit/)
