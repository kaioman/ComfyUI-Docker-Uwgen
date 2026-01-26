import os
import libcore_hng.utils.app_logger as app_logger
import pycorex.configs.app_init as app
from utils.image_analyze_gen_caption import (
    generate_caption_from_image, 
    save_caption_to_file
)

class ImageAnalyze:
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":{
                "prompt": ("STRING", {"multiline": True}),
                "input_image": ("IMAGE",),
                "input_dir": ("STRING", {"default": "default_input_dir"}),
                "image_file_name": ("STRING", {"default": "default_image_file_name"}),
                "lora_name": ("STRING", {"default": "default_lora"}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "run"
    CATEGORY = "Image/Analyzing"

    def run(self, prompt, input_image, input_dir, image_file_name, lora_name):

        # ルート取得
        base_dir = os.getenv("PROJECT_ROOT")
        if not base_dir:
            raise RuntimeError("PROJECT_ROOT environment variable is not set")
        
        # pycorex初期化
        app.init_app(__file__, "logger.json", "pycorex.json")
        app_logger.info("ImageAnalyze node called")
        app_logger.info(f"project_root: {app.core.config.project_root_path}")
        app_logger.info(f"input_dir: {input_dir}")
        app_logger.info(f"image_file_name: {image_file_name}")

        # 画像解析してキャプションを生成する
        raw_caption, caption_filename = generate_caption_from_image(prompt, input_image, input_dir, image_file_name)
        
        # キャプションファイルを保存する
        save_caption_to_file(raw_caption, caption_filename, lora_name)
        
        return (input_image, )
    
NODE_CLASS_MAPPINGS = {
    "ImageAnalyze": ImageAnalyze
}