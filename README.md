# ❤️ Heart Disease Prediction & AI Health Assistant

An end-to-end Machine Learning application that predicts heart disease risk from patient health parameters and provides AI-generated educational explanations using Google's Gemini API.

The project combines a trained K-Nearest Neighbors (KNN) model with an interactive Streamlit interface to demonstrate how Machine Learning and Generative AI can work together in a healthcare-related application.

> **Medical Disclaimer:** This application is for educational and demonstration purposes only. It is not a medical diagnostic tool and cannot replace a qualified healthcare professional.

## ✨ Features

- **Heart Disease Prediction:** Uses a trained KNN classification model to generate a prediction from user-provided health parameters.
- **Interactive Web Interface:** Built with Streamlit for easy data entry and result visualization.
- **AI-Powered Explanations:** Integrates Google's Gemini API to explain prediction-related information in simple language.
- **Health Parameter Processing:** Uses a saved scaler and feature-column configuration to prepare input data for the model.
- **Model Persistence:** Loads the trained model and preprocessing artifacts from saved `.pkl` files.
- **Docker Support:** Includes a Dockerfile for containerizing the application.
- **Cloud Deployment Ready:** Designed for deployment to Hugging Face Spaces using the Docker SDK.

## 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application programming |
| Pandas | Data processing |
| Scikit-learn | Machine Learning and preprocessing |
| K-Nearest Neighbors (KNN) | Heart disease classification |
| Streamlit | Interactive web application |
| Google Gemini API | AI-generated educational explanations |
| Joblib | Loading saved ML artifacts |
| Docker | Application containerization |
| Hugging Face Spaces | Cloud hosting target |

## 🏗️ Project Structure

```text
Machine-Learning-Part-3/
├── app.py
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── README.md
├── knn_heart_model.pkl
├── heart_scaler.pkl
├── heart_columns.pkl
├── HeartdiseaseFinal.ipynb
└── .streamlit/
    └── secrets.toml
```

**Important:** Keep API keys and other secrets out of public repositories. The `.streamlit/secrets.toml` file should remain private and must not be committed to Git.

## ⚙️ Run Locally

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Machine-Learning-Part-3
```

Replace the placeholder with your actual repository URL.

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create `.streamlit/secrets.toml` for local development:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Replace the placeholder with your own API key. Never publish this file or share your key.

### 5. Start the application

```powershell
python -m streamlit run app.py
```

Open the local URL displayed in your terminal, usually `http://localhost:8501`.

## 🐳 Run with Docker

Build the image from the project root:

```bash
docker build -t heart-disease-ai .
```

Run the container:

```bash
docker run --rm -p 7860:7860 \
  -e GEMINI_API_KEY="YOUR_GEMINI_API_KEY" \
  heart-disease-ai
```

Open `http://localhost:7860`.

Keep your API key private. Avoid putting real keys into shell history, screenshots, source files, or public logs.

## ☁️ Hugging Face Spaces Deployment

1. Create a new Space on Hugging Face.
2. Select **Docker** as the Space SDK.
3. Upload or push the project files required to build the application.
4. Add `GEMINI_API_KEY` under the Space's **Settings → Secrets**.
5. Ensure the Docker container listens on port `7860`.
6. Wait for the build to complete and test the deployed application.

Do not upload `.streamlit/secrets.toml` or any file containing a real API key.

## 🔄 Application Workflow

1. The user enters health-related parameters in the Streamlit interface.
2. The application prepares the input using the saved feature configuration and scaler.
3. The trained KNN model generates a classification prediction.
4. The Gemini API can provide an educational explanation based on the application's supported functionality.
5. The interface displays the results to the user.

## 🔐 Security

- Store API keys in environment variables or the hosting platform's secrets manager.
- Exclude `.streamlit/secrets.toml` from Git and Docker images.
- Never commit passwords, tokens, or private credentials.
- Rotate the API key immediately if it is accidentally exposed.

## ⚠️ Limitations

- Predictions depend on the training data, model performance, preprocessing, and quality of the user-provided inputs.
- A model prediction does not confirm whether a person has heart disease.
- AI-generated explanations may be incomplete or incorrect.
- The application is not intended for emergency decisions or treatment recommendations.

If you have symptoms that concern you, seek advice from a qualified healthcare professional. For possible emergency symptoms, contact your local emergency service.

## 🎯 Project Goals

This project demonstrates practical integration of:

- Machine Learning inference
- Saved model and preprocessing artifacts
- Interactive application development
- Generative AI API integration
- Docker-based deployment preparation
- Cloud application hosting

## 👨‍💻 Author

**Satyam Singh**

Aspiring AI/ML Engineer | Machine Learning | Generative AI | Python

- GitHub: [Student-Satyam](https://github.com/Student-Satyam)

---

If you find this project useful, consider giving the repository a ⭐ on GitHub.

**Disclaimer:** This project is intended for learning and demonstration. It does not provide medical advice, diagnosis, or treatment.
