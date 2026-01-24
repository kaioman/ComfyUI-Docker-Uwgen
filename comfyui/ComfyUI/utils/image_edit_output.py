import argparse
import libcore_hng.utils.app_logger as app_logger
import pycorex.configs.app_init as app
from pycorex.gemini_client import GeminiClient
from pycorex.uwgen_client import UwgenClient
from pycorex.exceptions.no_candidates_error import NoCandidatesError

def parse_args():
    parser = argparse.ArgumentParser(description="External image edit script")
    parser.add_argument("--prompt", required=True, help="Prompt text")
    parser.add_argument("--input", required=True, help="Input image path")
    return parser.parse_args()

def main():
    args = parse_args()

    # 引数取得
    prompt = args.prompt
    input_path = args.input
    
    # pycorex初期化
    app.init_app(__file__, "logger.json", "pycorex.json")

    # プロジェクトルート
    app_logger.info(f"Project root:{app.core.config.project_root_path}")
    
    # UwgenClient初期化
    client = UwgenClient()
    app_logger.info(f"Uwgen endpoint:{client.endpoint}")
    
    # 元画像取得
    source_file_path = input_path
    app_logger.info(f"Source file path:{source_file_path}")
    
    try:
        # 画像生成を実行
        result = client.edit_image(
            prompt=prompt,
            source_image_path=source_file_path,
            model=GeminiClient.GeminiModel.GEMINI_3_0_PRO_IMAGE_PREVIEW.value,
            resolution=GeminiClient.ImageSize.TWO_K.value,
            aspect=GeminiClient.AspectRatio.SQUARE.value,
            safety_filter = GeminiClient.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT.value,
            safety_level = GeminiClient.SafetyFilterLevel.BLOCK_ONLY_HIGH.value
        )
        
        # 画像ファイルを出力する
        client.output_images(result["images"], "gen_images")

    except NoCandidatesError as e:
        app_logger.error(f"Image generation failed: {e}")
    except Exception as e:
        app_logger.error(f"Unexpected error: {e}")
    
if __name__ == "__main__":
    main()
