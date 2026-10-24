# ❤️ Heart Risk Gen AI

An AI-powered heart disease prediction web application built using Machine Learning, Streamlit, and Generative AI.

The application predicts the possibility of heart disease based on user-provided health parameters and provides an AI-generated explanation with general health guidance.

## 🚀 Features

- **Heart Disease Prediction:** Uses a trained Machine Learning model to generate predictions.
- **Interactive Web Interface:** Built with Streamlit for a simple and user-friendly experience.
- **AI-Powered Explanation:** Uses the Gemini API to explain the prediction in simple language.
- **Health Guidance:** Provides general lifestyle and preventive health information.
- **Model Preprocessing:** Uses saved preprocessing files to prepare input data for prediction.

## 🛠️ Tech Stack

- Python
- Machine Learning
- Scikit-learn
- Streamlit
- Google Gemini API
- Pandas and NumPy
- Pickle for loading saved model and preprocessing files

## 📁 Project Structure

```text
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
```

**Note:** The `secrets.toml` file is used locally for secrets and must not be uploaded to GitHub.

## ⚙️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com
