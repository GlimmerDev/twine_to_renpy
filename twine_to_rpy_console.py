import os
import sys
import argparse
from twine_to_rpy_model import TwineToRenpy

def main():
    parser = argparse.ArgumentParser(description="Convert Twine HTML to Ren'Py scripts.")
    parser.add_argument('-i', '--input', required=True, help="Path to the Twine HTML file.")
    parser.add_argument('-o', '--output', required=True, help="Directory to save the Ren'Py scripts.")
    parser.add_argument('--config', help="Path to a custom config.json file (optional).")

    args = parser.parse_args()

    input_path = args.input
    output_path = args.output
    config_path = args.config

    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' does not exist.")
        sys.exit(1)

    if not os.path.exists(output_path):
        print(f"Error: Output directory '{output_path}' does not exist. Creating it...")
        os.makedirs(output_path)

    converter = TwineToRenpy()

    # Use custom config path if provided
    if config_path:
        if os.path.exists(config_path):
            converter.config_path = config_path
            if not converter.load_config():
                print("Error: Failed to load custom config file.")
                sys.exit(1)
        else:
            print(f"Error: Config file '{config_path}' does not exist.")
            sys.exit(1)

    # Update paths in the converter
    converter.data['html_path'] = input_path
    converter.data['script_dir'] = output_path

    print("Starting conversion...")
    if converter.run():
        print(f"Conversion successful! Ren'Py scripts saved to '{output_path}'.")
    else:
        print("Conversion failed. Check the input file and ensure it is a valid Twine HTML file.")

if __name__ == '__main__':
    main()
