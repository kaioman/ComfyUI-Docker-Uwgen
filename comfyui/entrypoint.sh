#!/bin/bash
COMFYUI_DIR="/home/${APP_USER}/ComfyUI"
COMFYUI_MAIN_PY="${COMFYUI_DIR}/main.py"

# If ComfyUI main.py does not exist, install it.
if [ ! -f $COMFYUI_MAIN_PY ]; then
    cd $COMFYUI_DIR
    # If the file exists, git clone will not be possible, so if .gitkeep exists, delete it.
    if [ -f "${COMFYUI_DIR}/.gitkeep" ]; then
        rm "${COMFYUI_DIR}/.gitkeep"
    fi

    git clone https://github.com/comfyanonymous/ComfyUI.git $COMFYUI_DIR
    pip install --user -r requirements.txt
    # Also install ComfyUI Manager.
    git clone https://github.com/ltdrdata/ComfyUI-Manager.git $COMFYUI_DIR/custom_nodes/ComfyUI-Manager
fi

# RUN ComfyUI. 
python3 $COMFYUI_MAIN_PY --listen 0.0.0.0
