import random

# 表情
expressions = [
    "smiling", "soft smile", "serious expression", "calm expression",
    "winking", "eyes closed", "laughing lightly", "gentle smile"
]

# ポーズ
poses = [
    "standing", "walking", "posing with one hand on her hip",
    "touching her cheek", "holding her hair", "hands together in front",
    "waving", "looking back over her shoulder", "light step forward"
]

# 背景
backgrounds = [
    "city street", "park", "cafe", "shopping district", "suburban road",
    "near a bus stop", "in front of a building", "riverside walkway",
    "quiet residential area", "open plaza"
]

# ライティング
lighting = [
    "natural sunlight", "soft daylight", "warm evening light",
    "overcast sky", "backlit lighting", "golden hour light",
    "cool morning light"
]

# カメラアングル
camera_angles = [
    "full body shot", "head-to-toe shot", "slightly low angle",
    "eye-level angle", "slightly high angle", "wide shot"
]

# 向き（orientation）
orientations = [
    "facing forward",
    "facing sideways",
    "side profile",
    "three-quarter view",
    "looking back over her shoulder",
    "turning around",
    "back view",
    "facing away from the camera"
]

# 服装バリエーション（同系統で identity を壊さない）
clothes = [
    "a white frilled high-neck blouse and a light blue cardigan",
    "a white blouse with a pastel cardigan",
    "a soft beige knit top with a light outer layer",
    "a pale pink blouse with a thin cardigan",
    "a simple white top with a pastel-colored cardigan",
    "a cream-colored blouse with a light jacket",
]

# 人物同一性を強く担保するベース
base_identity = (
    "A young woman with straight brown hair and bangs. "
    "Same face as the original image, preserve the original facial structure, same hairstyle and bangs."
)

def generate_prompt():
    return (
        f"{base_identity} "
        f"She is wearing {random.choice(clothes)}. "
        f"{random.choice(camera_angles)}, full body, {random.choice(orientations)}. "
        f"{random.choice(poses)}, {random.choice(expressions)}. "
        f"Background: {random.choice(backgrounds)}, {random.choice(lighting)}. "
        "High quality, realistic, 2K."
    )

# 100パターン生成
prompts = [generate_prompt() for _ in range(100)]

# 出力 
for i, p in enumerate(prompts, 1): 
    print(f"{i}. {p}\n")