import os
import tempfile
import subprocess
import numpy as np
from PIL import Image

class ImageEdit:
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":{
                "prompt": ("STRING", {"multiline": True}),
                "input_image": ("IMAGE",),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "run"
    CATEGORY = "Image/Editing"
    
    def run(self, prompt, input_image):
        print("ImageEdit node called", flush=True)
        print(prompt, flush=True)

        # Tensor → PIL Imageに変換
        image_np = (input_image[0].cpu().numpy() * 255).astype(np.uint8)
        image_pil = Image.fromarray(image_np)
        
        # 一時ファイルに保存
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            image_path = tmp_file.name
            image_pil.save(image_path)
            
        # プロンプトを外部スクリプトに渡して実行
        script_path = os.path.join(os.path.dirname(__file__), "..", "utils", "image_edit_output.py")
        subprocess.run([
            "python",
            script_path,
            "--prompt", prompt,
            "--input", image_path,
        ], check=True)
        
        # ダミー出力
        return (input_image,)

class NullSink:
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":{
                "x": ("IMAGE",)
            }
        }
    
    RETURN_TYPES = ()
    FUNCTION = "run"
    CATEGORY = "Image/Utils"
    OUTPUT_NODE = True
    
    def run(self, x):
        print("NullSink node called", flush=True)
        return ()
    
NODE_CLASS_MAPPINGS = {
    "NullSink": NullSink,
    "ImageEdit": ImageEdit
}