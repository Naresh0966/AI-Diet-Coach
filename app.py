import streamlit as st
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
st.set_page_config(page_title="AI Diet Coach", layout="wide")

st.title("🏥 AI-Powered Adaptive Diet Coach for Metabolic Health")

@st.cache_resource
def load_model():
    try:
        with open('trained_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('label_encoder.pkl', 'rb') as f:
            le = pickle.load(f)
        return model, le
    except FileNotFoundError:
        st.error("Model files not found. Please run model.py first.")
        return None, None

model, le = load_model()

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age (years)", min_value=1, max_value=120, value=30)
    weight = st.number_input("Weight (kg)", min_value=10.0, max_value=200.0, value=70.0)
    height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=175.0)

with col2:
    blood_sugar = st.number_input("Blood Sugar Level (mg/dL)", min_value=50, max_value=500, value=100)
    activity_level_str = st.selectbox("Activity Level", ["Low", "Medium", "High"])
    activity_mapping = {"Low": 0, "Medium": 1, "High": 2}
    activity_level = activity_mapping[activity_level_str]

def calculate_bmi(weight, height):
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal Weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def get_diet_recommendation(risk_prediction):
    if risk_prediction == 1:
        return "High-Risk / Diabetic-Friendly"
    else:
        return "Balanced / Maintenance"

def get_ai_meal_plan(risk_level):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    
    try:
        client = OpenAI(api_key=api_key)
        prompt = f"Generate a healthy meal plan for a person with {risk_level} diabetic risk. Include breakfast, lunch, and dinner with healthy options. Keep it concise."
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"OpenAI API Error: {e}")
        return None

def get_meal_plan(diet_type):
    meal_plans = {
        "High-Risk / Diabetic-Friendly": {
            "Breakfast": "Oatmeal with berries, nuts, and Greek yogurt",
            "Lunch": "Grilled chicken with quinoa and steamed broccoli",
            "Dinner": "Baked salmon with sweet potato and green salad"
        },
        "Balanced / Maintenance": {
            "Breakfast": "Scrambled eggs with whole wheat bread and fruit",
            "Lunch": "Grilled chicken with brown rice and mixed vegetables",
            "Dinner": "Baked fish with sweet potato and garden salad"
        }
    }
    return meal_plans.get(diet_type, meal_plans["Balanced / Maintenance"])

if st.button("Generate Diet Analysis", type="primary", use_container_width=True):
    if model is None:
        st.error("Model not loaded. Cannot proceed.")
    else:
        bmi = calculate_bmi(weight, height)
        bmi_category = categorize_bmi(bmi)
        
        features = pd.DataFrame({
            'Age': [age],
            'Weight': [weight],
            'Height': [height],
            'BloodSugar': [blood_sugar],
            'ActivityLevel': [activity_level]
        })
        risk_prediction = model.predict(features)[0]
        risk_label = "High Risk" if risk_prediction == 1 else "Low Risk"
        
        diet_type = get_diet_recommendation(risk_prediction)
        meal_plan = get_meal_plan(diet_type)
        
        st.divider()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("BMI", bmi)
            st.metric("BMI Category", bmi_category)
            st.metric("Weight", f"{weight} kg")
        
        with col2:
            st.metric("Age", f"{age} years")
            st.metric("Height", f"{height} cm")
            st.metric("Blood Sugar", f"{blood_sugar} mg/dL")
        
        with col3:
            st.metric("Activity Level", activity_level_str)
            st.markdown("### Diabetic Risk")
            risk_color = "#e74c3c" if risk_prediction == 1 else "#2ecc71"
            st.markdown(f"<h2 style='color: {risk_color};'>{risk_label}</h2>", unsafe_allow_html=True)
        
        st.divider()
        
        col_chart, col_diet = st.columns(2)
        
        with col_chart:
            st.subheader("BMI Distribution")
            bmi_categories = ["Underweight", "Normal", "Overweight", "Obese"]
            bmi_values = [15, 22, 27, 32]

            # Correct BMI range detection
            if bmi < 18.5:
                user_bmi_range = 0
            elif bmi < 25:
                user_bmi_range = 1
            elif bmi < 30:
                user_bmi_range = 2
            else:
                user_bmi_range = 3

            bar_colors = ["#3498db"] * 4
            bar_colors[user_bmi_range] = "#e74c3c"

            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(bmi_categories, bmi_values, color=bar_colors, alpha=0.8)
            ax.axhline(y=bmi, color='red', linestyle='--', linewidth=2, label=f'Your BMI: {bmi}')
            ax.set_ylabel("BMI Value")
            ax.set_title("BMI Category Chart")
            ax.legend()
            st.pyplot(fig)
        
        with col_diet:
            st.subheader("🍽️ Diet Recommendation")
            st.markdown(f"### {diet_type}")
            st.write("**Breakfast:** " + meal_plan["Breakfast"])
            st.write("**Lunch:** " + meal_plan["Lunch"])
            st.write("**Dinner:** " + meal_plan["Dinner"])
        
        st.divider()
        
        st.subheader("🤖 AI-Generated Personalized Meal Plan")
        risk_level = "High" if risk_prediction == 1 else "Low"
        ai_meal_plan = get_ai_meal_plan(risk_level)
        
        if ai_meal_plan:
            st.write(ai_meal_plan)
        else:
            st.warning("OpenAI API key not configured or API error. Set OPENAI_API_KEY environment variable to enable AI meal plan generation.")
        
        st.divider()
        st.info("💡 **Note:** This is a general recommendation. Consult a healthcare professional for personalized advice.")