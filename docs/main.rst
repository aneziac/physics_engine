main.py
=======
For the core loop including keyboards. Also responsible for backgrounds.

Variables
---------

Initial
*******
1. STARS
2. elapsed
    Used to find time since last frame.
3. pause
    Boolean that determines whether the engine is paused.
4. data
    Datastream for event logs.
5. PLAY
    Stores play.png asset.
6. PAUSE
    Stores pause.png asset.
7. IPLAY
    Stores iplay.png asset.
8. IPAUSE
    Stores ipause.png asset.
9. uicolor
    Determines whether to use black or white UI.

Main loop
*********
1. keys
    List of all keyboard presses in the frame.
2. 