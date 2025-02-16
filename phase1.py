# Phase1:

import bpy
import os
import mathutils
import time
import math
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from dotenv import load_dotenv, set_key
import os

env_file = "MIT.env"

import config
from config import model_name

# Constants
DIRECTORY = r"STL_Files"
X, Y, Z = 10, 10, 10  # Target coordinates for object midpoint placement

# Global variables for object properties
width, depth, height = 0, 0, 0  # Object size

time_wait=0.5

b1, b2, b3 = 15, 10, 10  # Example offsets


def clear_scene():
    """
    Removes all objects, lights, and cameras from the scene.
    """
    print("Clearing the scene...")
    
    # Ensure we're in object mode
    if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    
    # Select all objects
    bpy.ops.object.select_all(action='SELECT')
    
    # Delete selected objects
    bpy.ops.object.delete()
    
    # Clear all meshes, lights, and cameras from memory
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)
    for light in bpy.data.lights:
        bpy.data.lights.remove(light)
    for camera in bpy.data.cameras:
        bpy.data.cameras.remove(camera)
    
    print("Scene cleared.")

def add_light_source(b1, b2, b3, name="LightSource"):
    """
    Adds a light source above the object at position (X+b1, Y+b2, Z+b3).
    """

    time.sleep(time_wait)

    print("Adding light source...")

    # Create a new light source
    bpy.ops.object.light_add(type='POINT', location=(b1, b2, b3))
    light = bpy.context.object
    light.name = "ObjectLight"

    # Adjust light properties for better illumination
    light.data.energy = 2000 # Increase light intensity
    light.data.shadow_soft_size = 1.0  # Soften shadows

    print(f"Light source added at ({b1+20}, {b2}, {b3})")


def import_stl(filename, target_width=20):
    """
    Imports an STL file, resizes it to the target width while maintaining proportions,
    places its midpoint at (X, Y, Z), and calculates the object's size.
    """
    global width, depth, height

    filepath = os.path.join(DIRECTORY, filename)
    model_name = os.path.splitext(filename)[0]  # Extract model name


    print("Importing mesh...")
    bpy.ops.import_mesh.stl(filepath=filepath)
    imported_object = bpy.context.selected_objects[-1]

    # Get original dimensions
    original_dimensions = imported_object.dimensions
    original_width = original_dimensions.x

    # Calculate scale factor
    scale_factor = target_width / original_width

    # Apply scaling
    imported_object.scale *= scale_factor

    # Update mesh
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # Compute new object size
    width, depth, height = imported_object.dimensions

    # Calculate the offset to move the object's midpoint to (X, Y, Z)
    bbox_center_local = sum((mathutils.Vector(corner) for corner in imported_object.bound_box), mathutils.Vector()) / 8
    offset = mathutils.Vector((X, Y, Z)) - imported_object.matrix_world @ bbox_center_local

    # Move the object so its midpoint is at (X, Y, Z)
    imported_object.location += offset

    print(f"Mesh imported and resized with midpoint at ({X}, {Y}, {Z})")
    print(f"Object size: Width = {width}, Depth = {depth}, Height = {height}")
    return model_name  # Return model name for directory creation



def spawn_camera(a, b, c, name="TrackingCamera"):
    """
    Spawns a camera at (a, b, c) with perfect midpoint tracking using constraints.
    Returns the camera object.
    """
    print(f"Spawning camera {name}...")

    time.sleep(time_wait)


    # Create camera
    bpy.ops.object.camera_add(location=(a, b, c))
    camera = bpy.context.object
    camera.name = name

    # Create empty at midpoint
    bpy.ops.object.empty_add(location=(X, Y, Z))
    empty = bpy.context.object
    empty.name = f"Midpoint_Target_{name}"

    # Add track-to constraint to make camera face the midpoint
    constraint = camera.constraints.new(type='TRACK_TO')
    constraint.target = empty
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'

    print(f"Camera {name} placed at ({a}, {b}, {c}) and tracking midpoint ({X}, {Y}, {Z})")
    return camera

def take_snapshot(camera, output_path):
    """
    Takes a snapshot using the specified camera and saves it to the specified path.
    """
    print(f"Taking snapshot with camera {camera.name}...")
    time.sleep(time_wait)

    # Set render settings
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.filepath = output_path

    # Set the specified camera as the active camera
    bpy.context.scene.camera = camera

    # Render the image
    bpy.ops.render.render(write_still=True)

    print(f"Snapshot saved to {output_path}")

clear_scene()
# Example usage



stl_filename = model_name  # Replace with your STL file name

model_name = import_stl(stl_filename, target_width=20)

base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "")
face_dir = os.path.join(base_dir, model_name, "face_images")
vertex_dir = os.path.join(base_dir, model_name, "vertex_images")



# Create directories if they don't exist
os.makedirs(face_dir, exist_ok=True)
os.makedirs(vertex_dir, exist_ok=True)

# Spawn multiple cameras

d2 = 1.25*(height+width+height)
d1 = (height+width+height)/2
a = X

face_cameras = [
    ("faceCamera1", (X + d2, Y, Z)),
    ("faceCamera2", (X - d2, Y, Z)),
    ("faceCamera3", (X, Y + d2, Z)),
    ("faceCamera4", (X, Y - d2, Z)),
    ("faceCamera5", (X, Y, Z + d2)),
    ("faceCamera6", (X, Y, Z - d2))
]
d2_root3 = d2 / math.sqrt(3)  # Distance component along each axis
d1_root3 = d1 / math.sqrt(3)  # Distance component along each axis


light_source = [
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
]

vertex_cameras = [
    ("vertexCamera1", (X - d2_root3, Y - d2_root3, Z - d2_root3)),
    ("vertexCamera2", (X - d2_root3, Y - d2_root3, Z + d2_root3)),
    ("vertexCamera3", (X - d2_root3, Y + d2_root3, Z - d2_root3)),
    ("vertexCamera4", (X - d2_root3, Y + d2_root3, Z + d2_root3)),
    ("vertexCamera5", (X + d2_root3, Y - d2_root3, Z - d2_root3)),
    ("vertexCamera6", (X + d2_root3, Y - d2_root3, Z + d2_root3)),
    ("vertexCamera7", (X + d2_root3, Y + d2_root3, Z - d2_root3)),
    ("vertexCamera8", (X + d2_root3, Y + d2_root3, Z + d2_root3))
]

light_source_dict = dict(light_source)

for name, pos in face_cameras + vertex_cameras:
    spawn_camera(*pos, name)

# Add light sources using the light_source_dict
for light_name, light_pos in light_source_dict.items():
    add_light_source(*light_pos, light_name)

# Take snapshots for face cameras
for name, pos in face_cameras:
    camera_obj = bpy.data.objects[name]
    take_snapshot(camera_obj, os.path.join(face_dir, f"{name}.png"))


for name, pos in vertex_cameras:
    camera_obj = bpy.data.objects[name]
    take_snapshot(camera_obj, os.path.join(vertex_dir, f"{name}.png"))



load_dotenv(env_file)
set_key(env_file, "FLAG", "True")
load_dotenv(env_file, override=True)

sys.exit()


# End of Phase1 - A Sukanth Original Design