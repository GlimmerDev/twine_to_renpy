import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from api import process_conversion

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'outputs')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Ensure upload and output directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    # Save uploaded file
    uploaded_file = request.files.get('html_file')
    if not uploaded_file:
        return jsonify({'error': 'No file uploaded.'}), 400

    # Save the uploaded file securely
    filename = secure_filename(uploaded_file.filename)
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    uploaded_file.save(upload_path)

    # Process conversion
    success, result = process_conversion(upload_path, app.config['OUTPUT_FOLDER'])

    if success:
        # Generate download URLs for all output files
        download_urls = [
            f'/download/{filename}' for filename in result
        ]
        return jsonify({'message': 'Conversion successful!', 'download_urls': download_urls})
    else:
        return jsonify({'error': result}), 400

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")  # Log missing file
        return jsonify({'error': 'File not found.'}), 404
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
