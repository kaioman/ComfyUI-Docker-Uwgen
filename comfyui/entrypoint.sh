#!/bin/bash
COMFYUI_DIR="/home/${APP_USER}/ComfyUI"
COMFYUI_MAIN_PY="${COMFYUI_DIR}/main.py"

# If ComfyUI main.py does not exist, install it.
if [ ! -f "$COMFYUI_MAIN_PY" ]; then
    echo "Cloning ComfyUI repository..."
    git clone https://github.com/comfyanonymous/ComfyUI.git "$COMFYUI_DIR"
    git clone https://github.com/ltdrdata/ComfyUI-Manager.git "$COMFYUI_DIR"/custom_nodes/ComfyUI-Manager
fi

# RUN ComfyUI. 
echo "Starting ComfyUI..."
python3 "$COMFYUI_MAIN_PY" --listen 0.0.0.0
