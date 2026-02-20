import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Diet Coach", layout="wide")

st.title("🏥 AI-Powered Adaptive Diet Coach for Metabolic Health")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age (years)", min_value=1, max_value=120, value=30)
    weight = st.number_input("Weight (kg)", min_value=10.0, max_value=200.0, value=70.0)
    height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=175.0)

with col2:
    blood_sugar = st.number_input("Blood Sugar Level (mg/dL)", min_value=50, max_value=500, value=100)
    activity_level = st.selectbox("Activity Level", ["Low", "Medium", "High"])

def calculate_bmi(weight, height):
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight", "#3498db"
    elif bmi < 25:
        return "Normal Weight", "#2ecc71"
    elif bmi < 30:
        return "Overweight", "#f39c12"
    else:
        return "Obese", "#e74c3c"

def get_diet_recommendation(bmi, blood_sugar, activity_level):
    if blood_sugar > 125:
        diet_type = "Low-Carb / Diabetic-Friendly"
    elif bmi >= 25:
        diet_type = "Calorie-Controlled / Weight Loss"
    elif bmi < 18.5:
        diet_type = "High-Calorie / Muscle Building"
    else:
        diet_type = "Balanced / Maintenance"
    
    return diet_type

def get_meal_plan(diet_type, activity_level):
    meal_plans = {
        "Low-Carb / Diabetic-Friendly": {
            "Breakfast": "Oatmeal with berries, nuts, and Greek yogurt",
            "Lunch": "Grilled chicken with quinoa and steamed broccoli",
            "Dinner": "Baked salmon with sweet potato and green salad"
        },
        "Calorie-Controlled / Weight Loss": {
            "Breakfast": "Egg whites with whole wheat toast and tomato",
            "Lunch": "Grilled turkey breast with brown rice and vegetables",
            "Dinner": "Baked white fish with roasted vegetables and lentils"
        },
        "High-Calorie / Muscle Building": {
            "Breakfast": "Whole eggs, oats, banana, and peanut butter",
            "Lunch": "Lean beef with pasta, olive oil, and avocado",
            "Dinner": "Grilled chicken thigh with rice, nuts, and olive oil"
        },
        "Balanced / Maintenance": {
            "Breakfast": "Scrambled eggs with whole wheat bread and fruit",
            "Lunch": "Grilled chicken with brown rice and mixed vegetables",
            "Dinner": "Baked fish with sweet potato and garden salad"
        }
    }
    
    return meal_plans.get(diet_type, meal_plans["Balanced / Maintenance"])

if st.button("Generate Diet Analysis", type="primary", use_container_width=True):
    bmi = calculate_bmi(weight, height)
    category, color = categorize_bmi(bmi)
    diet_type = get_diet_recommendation(bmi, blood_sugar, activity_level)
    meal_plan = get_meal_plan(diet_type, activity_level)
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("BMI", bmi)
        st.metric("Height", f"{height} cm")
        st.metric("Weight", f"{weight} kg")
    
    with col2:
        st.markdown(f"### Health Category")
        st.markdown(f"<h2 style='color: {color};'>{category}</h2>", unsafe_allow_html=True)
        st.metric("Blood Sugar Level", f"{blood_sugar} mg/dL")
        st.metric("Activity Level", activity_level)
    
    with col3:
        st.markdown("### Diet Recommendation")
        st.markdown(f"<h3 style='color: #9b59b6;'>{diet_type}</h3>", unsafe_allow_html=True)
    
    st.divider()
    
    st.subheader("📋 Recommended Sample Meal Plan")
    
    meal_col1, meal_col2, meal_col3 = st.columns(3)
    
    with meal_col1:
        st.markdown("### Breakfast")
        st.write(meal_plan["Breakfast"])
    
    with meal_col2:
        st.markdown("### Lunch")
        st.write(meal_plan["Lunch"])
    
    with meal_col3:
        st.markdown("### Dinner")
        st.write(meal_plan["Dinner"])
    
    st.divider()
    
    st.info("💡 **Note:** This is a general recommendation. Consult a healthcare professional for personalized advice.")
