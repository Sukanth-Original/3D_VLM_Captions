import subprocess
import sys
import os
import time

from dotenv import load_dotenv, set_key

env_file = "MIT.env"

from phase3 import phase3_py
import config


import os
import config

import os
import config
import importlib

destination = input("Enter the destination path: ")

# Extract the file name and extension
file_name = os.path.basename(destination)
file_name_without_ext, file_extension = os.path.splitext(file_name)

# Update config variables
config.config_file_path = file_name_without_ext
config.model_name = file_name
config.config_file_path_2 = os.path.join(file_name_without_ext, "output_desc.txt")
config.destination = os.path.abspath(destination)

# Print the updated values (optional, for verification)
print(f"config_file_path: {config.config_file_path}")
print(f"model_name: {config.model_name}")
print(f"config_file_path_2: {config.config_file_path_2}")
print(f"destination: {config.destination}")

# Save the changes to config.py
with open("config.py", "r") as config_file:
    lines = config_file.readlines()

with open("config.py", "w") as config_file:
    for line in lines:
        if line.startswith("config_file_path ="):
            config_file.write(f"config_file_path = r'{config.config_file_path}'\n")
        elif line.startswith("model_name ="):
            config_file.write(f"model_name = '{config.model_name}'\n")
        elif line.startswith("config_file_path_2 ="):
            config_file.write(f"config_file_path_2 = r'{config.config_file_path_2}'\n")
        elif line.startswith("destination ="):
            config_file.write(f"destination = r'{config.destination}'\n")
        else:
            config_file.write(line)

# Reload the config module
import importlib

importlib.reload(config)  # Force reload of the updated config

time.sleep(5)

print("config.py has been updated and reloaded successfully.")

from phase2 import phase2_py

print(phase2_py())