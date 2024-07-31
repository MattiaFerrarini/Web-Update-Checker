#!/bin/bash

# set the DISPLAY environment variable to use the default display
export DISPLAY=:0

# set the XDG_RUNTIME_DIR environment variable to the runtime directory for the current user
export XDG_RUNTIME_DIR=/run/user/$(id -u)

# display a message instructing users to replace the path with their own folder path
echo "Please replace 'path/to/your/folder' with your own folder path."

# change the current directory to the target directory where the script is located
cd "path/to/your/folder"

# execute the script
python3 webUpdateChecker.py
