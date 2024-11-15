import os
from flask import Flask, render_template, request, jsonify
from inference_sdk import InferenceHTTPClient

app = Flask(__name__)

# Initialize Roboflow Inference Client using environment variable
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY environment variable is not set.")

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key=api_key
)

# Ensure the 'uploads' directory exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def perform_inference(file_path):
    """Helper function to perform inference on a given file."""
    return CLIENT.infer(file_path, model_id="fish-freshness-6-sb0n6-z5dqy/1")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload-single-image', methods=['POST'])
def upload_single_image():
    file = request.files['file']
    if file and allowed_file(file.filename):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        result = perform_inference(file_path)
        return jsonify(result)
    else:
        return jsonify({"error": "File type not allowed."}), 400

@app.route('/upload-batch-images', methods=['POST'])
def upload_batch_images():
    files = request.files.getlist('files')
    results = []

    for file in files:
        if file and allowed_file(file.filename):
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            result = perform_inference(file_path)
            results.append({file.filename: result})
        else:
            results.append({file.filename: "File type not allowed."})

    return jsonify(results)

if __name__ == '__main__':
    # Use the PORT environment variable provided by Render, or default to 5000 for local development
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True if os.environ.get('FLASK_ENV') != 'production' else False)
