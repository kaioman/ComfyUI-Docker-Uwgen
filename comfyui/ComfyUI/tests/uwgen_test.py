import os
import libcore_hng.utils.app_logger as app_logger
import pycorex.configs.app_init as app

# ルート取得
base_dir = os.getenv("PROJECT_ROOT")
if not base_dir:
    raise RuntimeError("PROJECT_ROOT environment variable is not set")
print(base_dir)

# pycorex初期化
app.init_app(__file__, "logger.json", "pycorex.json")
app_logger.info("init_app called")
