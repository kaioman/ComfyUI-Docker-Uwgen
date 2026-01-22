import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="External image edit script")
    parser.add_argument("--prompt", required=True, help="Prompt text")
    parser.add_argument("--input", required=True, help="Input image path")
    return parser.parse_args()

def main():
    args = parse_args()
    
    input_image = args.input