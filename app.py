import os
import threading
import time
import requests
from flask import Flask, render_template, request, jsonify
from inference_sdk import InferenceHTTPClient

app = Flask(__name__)

# Initialize Roboflow Inference Client using new API key
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="SUxPc1PBNC08yu5jmTnN"  # Updated API key
)

# Ensure the 'uploads' directory exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/page2')
def page2():
    return render_template('index2.html')

@app.route('/upload-single-image', methods=['POST'])
def upload_single_image():
    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    result = CLIENT.infer(file_path, model_id="fish-freshness-6-sb0n6-z5dqy/1")
    return jsonify(result)

@app.route('/upload-batch-images', methods=['POST'])
def upload_batch_images():
    files = request.files.getlist('files')
    results = []

    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        result = CLIENT.infer(file_path, model_id="fish-freshness-6-sb0n6-z5dqy/1")
        results.append({file.filename: result})

    return jsonify(results)

def keep_alive():
    """Periodically send a GET request to keep the app alive."""
    while True:
        try:
            requests.get("https://flaskapi-ylia.onrender.com")  # Replace with your deployed URL
            print("Keep-alive ping successful.")
        except Exception as e:
            print(f"Keep-alive ping failed: {e}")
        time.sleep(600)  # Ping every 10 minutes

if __name__ == '__main__':
    # Start the keep-alive thread
    threading.Thread(target=keep_alive, daemon=True).start()

    # Use the PORT environment variable provided by Render, or default to 5000 for local development
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
