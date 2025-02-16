## 3D_VLM_Captions

A Code that generates captions for your 3D Model

Uncut Video Demonstration: https://youtu.be/Wop6hv2dUaE

Usage Instructions:

1. Paste your desired 3D Model in .STL format at "STL_Files" in the directory
2. Run main.py
3. Type the name of the model -- "Panda.STL" when prompted to type the name.
4. Wait for Phase1, Phase2 and Phase3 to end -- to get your desired output.



#Phase1:
1. Initialises the environment in Blender
2. Uses bpy
3. Initialises the coordinates of the object X, Y, Z - Mid-point of the 3-dimensional volume.
4. clear_scene() - Clears the scene of any previous objects (meshes, lights, cameras)
5. add_light_source(b1, b2, b3, name of the light source) - collects the coordinates where it needs to be spawned, the name is specified
6. import_stl(filename, width of the object) - collects the file to be imported, the width of the object is collected to get normalized to a max width of 20 units
7. spawn_camera(a, b, c, name of the camera) - collects the coordinates to be spawned in the 3D space
8. take_snapshot(camera's name, path to export the snapshot) - takes the camera's name and uses this camera and saves it in the specified directory

Positions of the Face Cameras:
    ("faceCamera1", (X + d2, Y, Z)),
    ("faceCamera2", (X - d2, Y, Z)),
    ("faceCamera3", (X, Y + d2, Z)),
    ("faceCamera4", (X, Y - d2, Z)),
    ("faceCamera5", (X, Y, Z + d2)),
    ("faceCamera6", (X, Y, Z - d2))

Where d2 is an offset, d2 is determined by 1.25*(height+width+height)

Positions of the Light Sources:

    ("lightSource1", (X + d1, Y+3, Z)),
    ("lightSource2", (X - d1, Y+3, Z)),
    ("lightSource3", (X, Y + d1, Z+3)),
    ("lightSource4", (X, Y - d1, Z+3)),
    ("lightSource5", (X+3, Y, Z + d1)),
    ("lightSource6", (X+3, Y, Z - d1)),
    ("lightSource7", (X - d1_root3, Y - d1_root3, Z - d1_root3)),
    ("lightSource8", (X - d1_root3, Y - d1_root3, Z + d1_root3)),
    ("lightSource9", (X - d1_root3, Y + d1_root3, Z - d1_root3)),
    ("lightSource10", (X - d1_root3, Y + d1_root3, Z + d1_root3)),
    ("lightSource11", (X + d1_root3, Y - d1_root3, Z - d1_root3)),
    ("lightSource12", (X + d1_root3, Y - d1_root3, Z + d1_root3)),
    ("lightSource13", (X + d1_root3, Y + d1_root3, Z - d1_root3)),
    ("lightSource14", (X + d1_root3, Y + d1_root3, Z + d1_root3))

Where d1 is an offset, d1 is determined by (height+width+height)/2
d1_root3 = d1 / math.sqrt(3)

Positions of the Vertex Cameras:

    ("vertexCamera1", (X - d2_root3, Y - d2_root3, Z - d2_root3)),
    ("vertexCamera2", (X - d2_root3, Y - d2_root3, Z + d2_root3)),
    ("vertexCamera3", (X - d2_root3, Y + d2_root3, Z - d2_root3)),
    ("vertexCamera4", (X - d2_root3, Y + d2_root3, Z + d2_root3)),
    ("vertexCamera5", (X + d2_root3, Y - d2_root3, Z - d2_root3)),
    ("vertexCamera6", (X + d2_root3, Y - d2_root3, Z + d2_root3)),
    ("vertexCamera7", (X + d2_root3, Y + d2_root3, Z - d2_root3)),
    ("vertexCamera8", (X + d2_root3, Y + d2_root3, Z + d2_root3))

d2_root3 = d2 / math.sqrt(3)

Run Flow:

1. Spawn all the objects - object of interest, light sources and cameras (14)
2. Use take_snapshot to take photos from all 14 angles

#Phase 2:
1. Uses a VLM through OpenRouter to generate captions of all the 14 images.
2. Google Gemini 2.0 Flash was used but the model is easily swapable

#Phase 3:
1. Uses Google Gemini 2.0 to collect all the 14 captions and summarises into one caption of the entire 3D model.

#Main.py:

Runs all the above code in the sequential order:
1. Phase1
2. Phase2
3. Phase3

#Purpose of config.py:
For easy communication of directories changing throughout all 3 phases.
This prevents sequential flow of information and establishes a centralized approach.
This addresses a potential issue with bpy (Blender) -- Runs in it's own Python instead of using the IDE's Python
So this makes sure the codes are independent.

#Purpose of FLAG in MIT.env:
Phase1 runs independently and gets hard to track when the code gets over. Blender's Python is relatively less controllable and led to potential issues where the code wouldn't stop after finishes running or main.py proceeds to the Phase2 before completing Phase1 -- main.py is unaware of happenings of Phase1

FLAG makes sure that when Phase1 code ends, Phase2 starts. and so on.

