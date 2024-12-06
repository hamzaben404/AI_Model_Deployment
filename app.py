from flask import Flask, request, jsonify
from keras.applications import VGG16
from keras.applications.vgg16 import preprocess_input, decode_predictions
from keras.preprocessing.image import load_img, img_to_array
from werkzeug.utils import secure_filename
import numpy as np
import os
import pickle
from transformers import pipeline
from flask import render_template

# Initialize the Flask app
app = Flask(__name__)

# Load the pre-trained VGG16 model
model = VGG16(weights='imagenet')

# Load the regression model at the start of the app
with open('reg_model.pkl', 'rb') as f:
    reg_model = pickle.load(f)
    
# Load the text generation model (GPT-2 in this case)
text_generator = pipeline("text-generation", model="gpt2")

# Configure the upload folder and allowed file types
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for regression model predictions
@app.route('/regpredict', methods=['POST'])
def regpredict():
    # Ensure the request contains valid JSON data
    if not request.json or 'features' not in request.json:
        return jsonify({'error': 'Invalid input. JSON with "features" key is required.'}), 400

    # Extract features from the JSON request
    features = request.json['features']

    # Ensure features are in the correct format
    try:
        features = np.array(features).reshape(1, -1)
    except Exception as e:
        return jsonify({'error': f'Invalid features format: {e}'}), 400

    # Make a prediction
    try:
        prediction = reg_model.predict(features)
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        return jsonify({'error': f'Prediction error: {e}'}), 500

# Route for predictions
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only PNG, JPG, and JPEG are allowed.'}), 400

    try:
        # Sanitize the filename to prevent directory traversal attacks
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Save the uploaded file securely
        file.save(filepath)

        # Preprocess the image
        image = load_img(filepath, target_size=(224, 224))
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image = preprocess_input(image)

        # Get predictions from the VGG16 model
        predictions = model.predict(image)
        decoded_predictions = decode_predictions(predictions, top=3)[0]

        # Cleanup: Remove the temporary file
        os.remove(filepath)

        # Return the predictions as JSON
        return jsonify({
            'predictions': [
                {'label': pred[1], 'probability': float(pred[2])}
                for pred in decoded_predictions
            ]
        })

    except Exception as e:
        os.remove(filepath)
        return jsonify({'error': str(e)}), 500


#JSON-Based
# Route for text generation
@app.route('/textgen', methods=['POST'])
def textgen():
    # Ensure the request contains valid JSON data
    if not request.json or 'prompt' not in request.json:
        return jsonify({'error': 'Invalid input. JSON with "prompt" key is required.'}), 400

    # Extract the prompt from the JSON request
    prompt = request.json['prompt']
    try:
        # Generate text using the Hugging Face model
        results = text_generator(prompt, max_length=100, num_return_sequences=1)
        generated_text = results[0]['generated_text']

        # Return the generated text
        return jsonify({'generated_text': generated_text})
    except Exception as e:
        return jsonify({'error': f'Text generation error: {e}'}), 500
    

# @app.route('/home', methods=['GET'])
# def home():
#     return jsonify({
#         "application_name": "AI Model Deployment",
#         "endpoints": {
#             "/predict": "Image classification using VGG16. Accepts image uploads.",
#             "/regpredict": "Regression model predictions. Accepts JSON input with features.",
#             "/textgen": "Text generation using Hugging Face GPT-2. Accepts JSON input with a prompt."
#         },
#         "deployment_instructions": "Run `docker-compose up` to start the application. Use API clients like Postman or cURL to test the endpoints."
#     })

# HTML-Based
@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')


# Main entry point to run the app
if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(debug=True, host='0.0.0.0', port=5001)
