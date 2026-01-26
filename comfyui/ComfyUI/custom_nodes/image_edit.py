import os
import subprocess
import numpy as np
import libcore_hng.utils.app_logger as app_logger
import pycorex.configs.app_init as app
from PIL import Image
from pathlib import Path

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
        
        # ルート取得
        base_dir = os.getenv("PROJECT_ROOT")
        if not base_dir:
            raise RuntimeError("PROJECT_ROOT environment variable is not set")
        print(base_dir)
        
        # pycorex初期化
        app.init_app(__file__, "logger.json", "pycorex.json")
        app_logger.info("ImageEdit node called")
        app_logger.info(f"project_root: {app.core.config.project_root_path}")

        # Tensor → PIL Imageに変換
        image_np = (input_image[0].cpu().numpy() * 255).astype(np.uint8)
        image_pil = Image.fromarray(image_np)

        # 出力先
        save_dir = Path(base_dir) / "source_image"
        save_dir.mkdir(parents=True, exist_ok=True)        
        # ファイル名
        import uuid
        filename = f"{uuid.uuid4().hex}.png"
        app_logger.info(f"Generated filename: {filename}")

        # 元画像保存
        image_path = save_dir / filename
        image_pil.save(image_path)
        app_logger.info(f"Input image saved to: {image_path}")

        try:
            # プロンプトを外部スクリプトに渡して実行
            script_path = os.path.join(os.path.dirname(__file__), "..", "utils", "image_edit_output.py")
            app_logger.info("Calling external image edit script...")
            subprocess.run([
                "python",
                script_path,
                "--prompt", prompt,
                "--input", image_path,
            ], check=True, env=os.environ.copy())
        except subprocess.CalledProcessError as e:        
            app_logger.error(f"External script failed: {e}")
        finally:
            try:
                # 画像削除
                if image_path.exists():
                    image_path.unlink()
                    app_logger.info(f"Temporary image file deleted: {image_path}")

            except Exception as e:
                app_logger.error(f"Failed to delete temporary image file: {e}")
        
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