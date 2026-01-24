import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="External image edit script")
    parser.add_argument("--prompt", required=True, help="Prompt text")
    parser.add_argument("--input", required=True, help="Input image path")
    return parser.parse_args()

def main():
    args = parse_args()

    prompt = args.prompt
    input_path = args.input

    print(f"prompt:{prompt}")
    print(f"input_path:{input_path}")
    
if __name__ == "__main__":
    main()
