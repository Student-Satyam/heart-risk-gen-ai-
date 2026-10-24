❤️ Heart Risk Gen AI

An AI-powered heart disease prediction web application built using Machine Learning, Streamlit, and Generative AI.

The application predicts the possibility of heart disease based on user-provided health parameters and provides an AI-generated explanation with general health guidance.

🚀 Features

Heart Disease Prediction: Uses a trained Machine Learning model to generate predictions.

Interactive Web Interface: Built with Streamlit for a simple and user-friendly experience.

AI-Powered Explanation: Uses the Gemini API to explain the prediction in simple language.

Health Guidance: Provides general lifestyle and preventive health information.

Model Preprocessing: Uses saved preprocessing files to prepare input data for prediction.

🛠️ Tech Stack

Python

Machine Learning

Scikit-learn

Streamlit

Google Gemini API

Pandas and NumPy

Pickle for loading saved model and preprocessing files

📁 Project Structure

heart-risk-gen-ai/
├── app.py
├── knn_heart_model.pkl
├── heart_scaler.pkl
├── heart_columns.pkl
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── secrets.toml

Note: The secrets.toml file is used locally for secrets and must not be uploaded to GitHub.

⚙️ Run Locally

1. Clone the repository

git clone https://github.com/Student-Satyam/heart-risk-gen-ai-.git
cd heart-risk-gen-ai-

2. Create a virtual environment

python -m venv .venv

Activate it on Windows:

.\.venv\Scripts\Activate.ps1

3. Install dependencies

pip install -r requirements.txt

4. Configure the Gemini API key

Create .streamlit/secrets.toml and add:

GEMINI_API_KEY = "your_actual_gemini_api_key"

Replace the placeholder with your own API key. Never publish your API key in your repository.

5. Run the application

streamlit run app.py

The application will open in your browser, usually at http://localhost:8501.

☁️ Deployment

The application can be deployed using Streamlit Community Cloud.

Push the project to GitHub.

Sign in to Streamlit Community Cloud.

Connect the GitHub repository.

Select app.py as the main file.

Add GEMINI_API_KEY in the app's Secrets settings.

Deploy the application.

Docker is not required for this deployment method.

🔐 Security

Keep API keys private.

Do not commit .streamlit/secrets.toml.

Store deployment secrets in the hosting platform's secrets settings.

⚠️ Medical Disclaimer

This application is an educational and informational project. Its predictions and AI-generated explanations are not a medical diagnosis and must not replace professional medical advice. Consult a qualified healthcare professional for medical concerns.

👨‍💻 Author

Satyam Singh

GitHub: Student-Satyam

Built as a Machine Learning and Generative AI project to explore the integration of predictive models with AI-generated explanations.
