import subprocess
import sys
import os
import time

from dotenv import load_dotenv, set_key

env_file = "MIT.env"

from phase2 import phase2_py
from phase3 import phase3_py
import config

def get_blender_path():
    if sys.platform == "win32":
        return r"C:\Program Files\Blender Foundation\Blender 3.6\blender.exe"
    elif sys.platform == "darwin":  # macOS
        return "/Applications/Blender.app/Contents/MacOS/Blender"
    else:  # Linux
        return "blender"  # Assumes Blender is in your PATH

def blender_launch():
    blender_path = get_blender_path()

    if not os.path.exists(blender_path) and blender_path != "blender":
        print(f"Blender executable not found at {blender_path}")
        return

    try:
        subprocess.Popen([blender_path])
        print("Blender launched successfully!")
    except Exception as e:
        print(f"Error launching Blender: {e}")

def blender_script(script_name="phase1.py"):
    blender_path = get_blender_path()

    if not os.path.exists(blender_path) and blender_path != "blender":
        print(f"Blender executable not found at {blender_path}")
        return

    script_path = os.path.join(os.path.dirname(__file__), script_name)
    if not os.path.exists(script_path):
        print(f"Script not found: {script_path}")
        return

    try:
        subprocess.Popen([blender_path, "--python", script_path])
        print(f"Blender launched with script: {script_name}")
    except Exception as e:
        print(f"Error launching Blender with script: {e}")



load_dotenv(env_file)
set_key(env_file, "FLAG", "False")
load_dotenv(env_file, override=True)



destination = input("Enter the destination path: ")

# Extract the file name and extension
file_name = os.path.basename(destination)
file_name_without_ext, file_extension = os.path.splitext(file_name)

# Update config.py
config.config_file_path = file_name_without_ext
config.model_name = file_name
config.config_file_path_2 = os.path.join(file_name_without_ext, "output_desc.txt")

# Get the relative path
relative_path = os.path.relpath(destination)

# Update config.py with the relative path
config.destination = relative_path

# Print the updated values (optional, for verification)
print(f"config_file_path: {config.config_file_path}")
print(f"model_name: {config.model_name}")
print(f"config_file_path_2: {config.config_file_path_2}")
print(f"destination: {config.destination}")

# Save the changes to config.py
with open("config.py", "w") as config_file:
    config_file.write(f"config_file_path = r'{config.config_file_path}'\n")
    config_file.write(f"model_name = '{config.model_name}'\n")
    config_file.write(f"config_file_path_2 = r'{config.config_file_path_2}'\n")
    config_file.write(f"destination = r'{config.destination}'\n")

print("config.py has been updated successfully.")


config.FLAG = False
print("Starting Phase-1 Shortly")
time.sleep(2)


blender_script()

while True:
    load_dotenv(env_file, override=True)  # Reload to check updated values
    flag = os.getenv("FLAG")

    if flag == "True":
        print("Starting Phase-2 Shortly")
        time.sleep(2) 
        print("Running Phase-2")
        from phase2 import phase2_py

        phase2_py()
        print("Starting Phase-3 Shortly")
        time.sleep(2)
        print("Running Phase-3")
        from phase3 import phase3_py

        caption = phase3_py()
        print(caption)
        break
    else:
        print("Running Phase1.")
        time.sleep(1)


# Create the results directory if it doesn't exist
# Create a 'results' directory relative to the script's location
results_dir = os.path.join("results")
os.makedirs(results_dir, exist_ok=True)

# Save the caption to a file
caption_filename = f"{file_name_without_ext}.txt"
caption_path = os.path.join(results_dir, caption_filename)

with open(caption_path, "w") as caption_file:
    caption_file.write(caption)

# Print the relative path
relative_caption_path = os.path.relpath(caption_path)
print(f"Caption saved to: {relative_caption_path}")