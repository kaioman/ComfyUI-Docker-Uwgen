import subprocess

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

        # プロンプトを外部スクリプトに渡して実行
        subprocess.run([
            "python3",
            "image_edit_output.py",
            "--prompt", prompt,
            "--input", input_image,
        ], check=True)
        
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