# GRID SIMULATION
A Ursina program used to create structures and buildings. WIP.

Originally written by L.Kam

![image](https://github.com/AlotarioPersonal/3d-grid-simulation/assets/126506217/e8d0ec5a-e95e-4cb6-a945-88537e1d906a)


A program simulating 'Grid,' a 3-dimensional digital space designed to create structures. it's based heavily off
'The Grid' from Tron.

![image](https://github.com/AlotarioPersonal/3d-grid-simulation/assets/126506217/2d4bc7e5-beaa-448b-8192-794006cab6a3)


This is NOT the interaction system that's replacing OmicronOS. I'll be making a post about that shortly.

HOW IT WORKS, STEP BY STEP
----------
1. Upon boot, three things are created; the Player, the Grid, and BASIS, the first true structure.
2. BASIS is the base structure for all the structures that come after it. it's a blank cube, that's placed
underneath the world and used as a duplicatable entity.
3. The Grid, every frame, is locked into a static enabled state, position, size, and rotation. You cannot modify or delete The Grid.
4. The player is given two abilities: The ability to move, and omnipotency. (I'm serious.)
The player's detailed abilities are as follows:
-Free range of movement, albiet with gravity
-The ability to create and transform 'structures,' which i'll explain in a minute
-The ability to delete structures.
5. 'Structures' are 3D objects that the player creates from the matter of the grid. The options are:
-Cube
-Torus
-Spike/Diamond
-Torus
6. Grid is a live program. Once you leave, everything you create is erased permanently, and you cannot retrieve it.
