import os
from twine_to_rpy_model import TwineToRenpy

def process_conversion(html_path, output_dir):
    # Initialize the model
    model = TwineToRenpy()

    # Update paths in the model
    model.data['html_path'] = html_path
    model.data['script_dir'] = output_dir

    # Run the conversion
    if model.run():
        # Log all generated .rpy files
        generated_files = [f for f in os.listdir(output_dir) if f.endswith('.rpy')]
        print(f"Generated files: {generated_files}")
        return True, generated_files
    else:
        return False, "Conversion failed. Check the input file."
