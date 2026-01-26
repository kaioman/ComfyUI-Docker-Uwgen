import os
import libcore_hng.utils.app_logger as app_logger
import pycorex.configs.app_init as app
from pycorex.gemini_client import GeminiClient
from pycorex.uwgen_client import UwgenClient

def generate_caption_from_image(prompt, input_image, input_dir, image_file_name):

    # プロジェクトルート
    app_logger.info(f"Project root:{app.core.config.project_root_path}")
    
    # UwgenClient初期化
    client = UwgenClient()
    app_logger.info(f"Uwgen endpoint:{client.endpoint}")
    
    # 画像ファイルパスを取得
    source_file_path = os.path.join(input_dir, image_file_name)
    
    # キャプションファイル名を構成する
    base_name = os.path.splitext(os.path.basename(image_file_name))[0]
    caption_filename = f"{base_name}.txt"

    try:
        # 画像解析を実行
        result = client.analyze_image(
            prompt=prompt,
            source_image_path=source_file_path,
            model=GeminiClient.GeminiModel.GEMINI_3_0_PRO_IMAGE_PREVIEW.value
        )
        
        # 解析結果を取得
        raw_caption = result["text"]
        app_logger.info(f"result: {result}")
        app_logger.info(f"raw_caption: {raw_caption}")
        
    except Exception as e:
        app_logger.error(f"Unexpected error: {e}")

    return raw_caption, caption_filename

def save_caption_to_file(raw_caption, caption_filename, lora_name):
    
    # フォーマット済キャプション取得
    caption = format_caption(raw_caption, lora_name)
    
    # キャプションファイルの保存先パス
    output_dir = app.core.config.project_root_path / "captions"
    os.makedirs(output_dir, exist_ok=True)
    caption_filepath = os.path.join(output_dir, caption_filename)

    # キャプションファイル保存
    with open(caption_filepath, "w", encoding="utf-8") as f:
        f.write(caption)
        
    return caption_filepath

def format_caption(raw_caption: str, lora_name):
    
    # 前後の空白除去
    caption = raw_caption.strip()
    
    # LoRA名を先頭に付与
    caption = f"{lora_name}, {caption}"
    
    return caption