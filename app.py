import os

import joblib
import pandas as pd
import streamlit as st
from google import genai
from google.genai import types
from streamlit.errors import StreamlitSecretNotFoundError


# 1. Streamlit page configuration
st.set_page_config(
    page_title="AI Heart Health Assistant",
    page_icon="❤️",
    layout="wide"
)


# 2. Load saved ML components
@st.cache_resource
def load_ml_components():
    model = joblib.load("knn_heart_model.pkl")
    scaler = joblib.load("heart_scaler.pkl")
    expected_columns = joblib.load("heart_columns.pkl")
    return model, scaler, expected_columns


model, scaler, expected_columns = load_ml_components()


# 3. Configure Google Gemini
try:
    api_key = st.secrets.get("GEMINI_API_KEY", "")
except StreamlitSecretNotFoundError:
    api_key = ""

api_key = api_key or os.getenv("GEMINI_API_KEY", "")

if api_key:
    try:
        gemini_client = genai.Client(api_key=api_key)
    except Exception as e:
        gemini_client = None
        st.warning(
            "Gemini client could not be initialized. "
            f"Technical details: {type(e).__name__}: {e}"
        )
else:
    gemini_client = None

# Current lightweight Gemini model. Change this only if unavailable
# in your Google AI Studio account.
GEMINI_MODEL = "gemini-3.5-flash-lite"


# 4. Application heading
st.title("❤️ AI-Powered Heart Health Assistant")
st.write(
    "Enter your health information to receive a machine-learning "
    "prediction and educational information about heart health."
)
st.warning(
    "This application is for educational purposes only. "
    "It cannot diagnose a disease or replace a qualified doctor."
)


# 5. Patient input form
st.subheader("Patient Health Information")

with st.form("heart_health_form"):
    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("Age", 18, 100, 40)
        sex = st.selectbox("Sex", ["M", "F"])
        chest_pain = st.selectbox(
            "Chest Pain Type", ["ATA", "NAP", "TA", "ASY"]
        )
        resting_bp = st.number_input(
            "Resting Blood Pressure (mm Hg)",
            min_value=80, max_value=200, value=120
        )
        cholesterol = st.number_input(
            "Cholesterol (mg/dL)",
            min_value=100, max_value=600, value=200
        )

    with col2:
        fasting_bs = st.selectbox(
            "Fasting Blood Sugar > 120 mg/dL", [0, 1]
        )
        resting_ecg = st.selectbox(
            "Resting ECG", ["Normal", "ST", "LVH"]
        )
        max_hr = st.slider("Maximum Heart Rate", 60, 220, 150)
        exercise_angina = st.selectbox(
            "Exercise-Induced Angina", ["Y", "N"]
        )
        oldpeak = st.slider("Oldpeak (ST Depression)", 0.0, 6.0, 1.0)
        st_slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"])

    submitted = st.form_submit_button("Predict and Explain")


# 6. Prepare patient features
if submitted:
    raw_input = {
        "Age": age,
        "RestingBP": resting_bp,
        "Cholesterol": cholesterol,
        "FastingBS": fasting_bs,
        "MaxHR": max_hr,
        "Oldpeak": oldpeak,
        "Sex_" + sex: 1,
        "ChestPainType_" + chest_pain: 1,
        "RestingECG_" + resting_ecg: 1,
        "ExerciseAngina_" + exercise_angina: 1,
        "ST_Slope_" + st_slope: 1
    }

    input_df = pd.DataFrame([raw_input])

    for col in expected_columns:
        if col not in input_df.columns:
            input_df[col] = 0

    input_df = input_df[expected_columns]
    scaled_input = scaler.transform(input_df)
    prediction = int(model.predict(scaled_input)[0])

    st.session_state["patient_context"] = {
        "features": {
            "Age": age,
            "Sex": sex,
            "Chest Pain Type": chest_pain,
            "Resting Blood Pressure": resting_bp,
            "Cholesterol": cholesterol,
            "Fasting Blood Sugar Flag": fasting_bs,
            "Resting ECG": resting_ecg,
            "Maximum Heart Rate": max_hr,
            "Exercise-Induced Angina": exercise_angina,
            "Oldpeak": oldpeak,
            "ST Slope": st_slope
        },
        "prediction": prediction
    }

    # Start a fresh conversation after a new prediction.
    st.session_state["chat_history"] = []
    st.session_state.pop("explanation", None)


# 7. Display ML prediction
if "patient_context" in st.session_state:
    patient = st.session_state["patient_context"]
    prediction = patient["prediction"]

    st.divider()
    st.subheader("Your ML Prediction")

    if prediction == 1:
        st.error(
            "The model predicted: Heart Disease Present (Class 1). "
            "This is a machine-learning prediction, not a confirmed diagnosis. "
            "Please consult a qualified healthcare professional."
        )
    elif prediction == 0:
        st.success(
            "The model predicted: No Heart Disease (Class 0). "
            "This does not guarantee that your heart is healthy "
            "or rule out a heart condition."
        )
    else:
        st.warning("The model returned an unexpected class.")


    # 8. Gemini explanation
    st.divider()
    st.subheader("🤖 AI Health Explanation")

    if st.button("Explain My Results"):
        if not gemini_client:
            st.error(
                "Gemini API key is missing or the client could not be "
                "initialized. Check .streamlit/secrets.toml and "
                "your GEMINI_API_KEY setting."
            )
        else:
            features = patient["features"]

            system_prompt = """
You are an AI health education assistant in a heart-health
machine-learning demonstration application. You are NOT a doctor.

Explain health concepts in simple English. Explain the predicted class
without claiming it confirms disease. Do not invent a diagnosis, the
cause of symptoms, or the location of a blockage. Explain which
measurements may deserve medical review without claiming that any
single measurement proves disease.

Give general, evidence-based heart-health information. Discuss balanced
food choices, appropriate physical activity, smoking cessation, sleep,
and medical follow-up when relevant. Do not prescribe medicines, change
dosages, or advise stopping treatment. Dietary and exercise advice may
require individual medical guidance.

Do not interpret the prediction as a probability or percentage.
Clearly state the limits of this application's information.

Dataset class labels:
Class 0 = No heart disease in the dataset.
Class 1 = Heart disease present in the dataset.

Do not present the prediction as a confirmed medical diagnosis or imply
that you can determine the actual cause of heart disease from these
measurements alone.

If the user reports new or persistent chest pain, severe shortness of
breath, fainting, or other potentially serious symptoms, advise urgent
medical assessment. For symptoms suggestive of a heart attack, advise
calling local emergency services immediately.
"""

            user_prompt = f"""
Explain this educational ML prediction in simple, patient-friendly English.

Patient features: {features}
Predicted class: {prediction}

Class 0 means no heart disease in the dataset.
Class 1 means heart disease present in the dataset.

Use these headings:
- What the model predicted
- Understanding the entered features
- What these results cannot tell us
- General heart-health habits
- Foods and dietary habits
- When to consult a doctor

Do not claim this prediction confirms or rules out a medical condition.
"""

            try:
                with st.spinner("Gemini is preparing your explanation..."):
                    response = gemini_client.models.generate_content(
                        model=GEMINI_MODEL,
                        contents=user_prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=system_prompt
                        )
                    )
                    explanation = response.text

                    if not explanation:
                        raise ValueError(
                            "Gemini returned an empty explanation."
                        )

                    st.session_state["explanation"] = explanation

            except Exception as e:
                error_text = str(e).upper()
                if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                    st.warning(
                        "Gemini API rate or usage limit reached. "
                        "Check Google AI Studio usage limits and try later."
                    )
                else:
                    st.error("Could not generate the AI explanation.")
                    st.caption(
                        f"Technical error: {type(e).__name__}: {e}"
                    )

    if "explanation" in st.session_state:
        st.markdown(st.session_state["explanation"])


    # 9. Patient chatbot
    st.divider()
    st.subheader("💬 Ask Your Heart Health Assistant")
    st.write(
        "Ask general questions about heart health, your entered features, "
        "healthy food, or questions to discuss with your doctor."
    )

    if not gemini_client:
        st.info("Configure your Gemini API key to enable the chatbot.")
    else:
        for message in st.session_state.get("chat_history", []):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        question = st.chat_input("Ask a heart-health question...")

        if question:
            st.session_state["chat_history"].append(
                {"role": "user", "content": question}
            )

            with st.chat_message("user"):
                st.markdown(question)

            features = patient["features"]
            chatbot_system_prompt = f"""
You are a cautious heart-health education chatbot, not a doctor.
You cannot diagnose, prescribe, or replace a medical professional.

Patient features: {features}
ML predicted class: {patient["prediction"]}

Dataset class labels:
Class 0 = No heart disease in the dataset.
Class 1 = Heart disease present in the dataset.

Use the features and model output as context, not as proof of disease
or its cause. Explain medical terms in simple English. Give general,
evidence-based information about nutrition, physical activity,
prevention, and medical follow-up.

Do not claim to know where a blockage is occurring. Do not infer a
diagnosis from symptoms or measurements. Do not recommend starting,
stopping, or changing medication. If information is insufficient,
say so clearly.

For new or persistent chest pain, severe shortness of breath, fainting,
or other serious symptoms, advise urgent medical assessment. If a heart
attack is suspected, advise calling local emergency services immediately.
Never delay emergency care to continue chatting.
"""

            # Convert chat history to Gemini's user/model roles.
            gemini_contents = []
            for message in st.session_state["chat_history"][-10:]:
                role = "model" if message["role"] == "assistant" else "user"
                gemini_contents.append({
                    "role": role,
                    "parts": [{"text": message["content"]}]
                })

            try:
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = gemini_client.models.generate_content(
                            model=GEMINI_MODEL,
                            contents=gemini_contents,
                            config=types.GenerateContentConfig(
                                system_instruction=chatbot_system_prompt
                            )
                        )
                        answer = response.text

                        if not answer:
                            raise ValueError(
                                "Gemini returned an empty response."
                            )

                    st.markdown(answer)

                st.session_state["chat_history"].append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as e:
                error_text = str(e).upper()
                if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                    st.warning(
                        "Gemini API rate or usage limit reached. "
                        "Check Google AI Studio usage limits and try later."
                    )
                else:
                    st.error("The chatbot could not respond.")
                    st.caption(
                        f"Technical error: {type(e).__name__}: {e}"
                    )
