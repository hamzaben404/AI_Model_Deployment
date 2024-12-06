# **AI Model Deployment**

This project demonstrates how to deploy various AI models using Flask and Docker. The application provides RESTful APIs for interacting with the models, including image classification, regression predictions, and text generation.

---

## **Features**
### Available Endpoints
1. **`/predict`**  
   - **Purpose:** Perform image classification using the pre-trained VGG16 model.  
   - **Input:** Image file (PNG, JPG, or JPEG).  
   - **Output:** Predicted labels and probabilities.  

2. **`/regpredict`**  
   - **Purpose:** Predict outcomes using a regression model saved as a Pickle file.  
   - **Input:** JSON payload containing features for the regression model.  
   - **Output:** Predicted value.  

3. **`/textgen`**  
   - **Purpose:** Generate text using the Hugging Face GPT-2 model.  
   - **Input:** JSON payload with a text prompt.  
   - **Output:** Generated text based on the prompt.  

4. **`/home`**  
   - **Purpose:** Display documentation about the application and its usage.

---

## **Project Structure**

```
VGG16_Flask_App/
├── app.py                 # Main Flask application
├── reg_model.pkl          # Saved regression model
├── requirements.txt       # Python dependencies
├── Dockerfile             # Dockerfile for containerization
├── docker-compose.yml     # Docker Compose configuration
├── README.md              # Documentation for the project
├── .gitignore             # Files/folders to ignore in GitHub
├── templates/             # HTML templates (e.g., home.html)
│   └── home.html
└── static/                # Folder for temporarily stored uploaded files
```

---

## **Setup Instructions**

### Prerequisites
- Docker installed on your system.
- Basic knowledge of Python and RESTful APIs (optional).

### **1. Clone the Repository**
```bash
git clone https://github.com/your_username/AI_Model_Deployment.git
cd AI_Model_Deployment
```

### **2. Build and Run the Docker Container**
```bash
docker-compose build
docker-compose up
```

### **3. Access the Application**
- **Base URL:** `http://127.0.0.1:5000`  
- Available endpoints:
  - `/predict`: For image classification.
  - `/regpredict`: For regression predictions.
  - `/textgen`: For text generation.
  - `/home`: For application documentation.

---

## **Usage Examples**

### Image Classification (`/predict`)
**Request:**
```bash
curl -X POST -F "file=@path_to_image.jpg" http://127.0.0.1:5000/predict
```
**Response:**
```json
{
    "predictions": [
        {"label": "tabby", "probability": 0.85},
        {"label": "tiger_cat", "probability": 0.10},
        {"label": "Egyptian_cat", "probability": 0.05}
    ]
}
```

### Regression Model (`/regpredict`)
**Request:**
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"features": [1.5]}' \
http://127.0.0.1:5000/regpredict
```
**Response:**
```json
{
    "prediction": [42.36]
}
```

### Text Generation (`/textgen`)
**Request:**
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"prompt": "Once upon a time"}' \
http://127.0.0.1:5000/textgen
```
**Response:**
```json
{
    "generated_text": "Once upon a time in a faraway land, there lived a brave knight..."
}
```

---

## **Deployment Instructions**

### **1. Clone and Navigate to the Repository**
```bash
git clone https://github.com/your_username/AI_Model_Deployment.git
cd AI_Model_Deployment
```

### **2. Build the Docker Image**
```bash
docker-compose build
```

### **3. Run the Docker Container**
```bash
docker-compose up
```

---

## **Contributing**
Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request with your improvements.

---

## **Contact**
For questions or support, contact:  
**Your Name**  
Email: hamzabenatmane00@gmail.com  
GitHub: [hamzaben404](https://github.com/hamzaben404)
