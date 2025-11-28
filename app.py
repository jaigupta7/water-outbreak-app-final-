import streamlit as st
import pandas as pd
import numpy as np
import joblib

# --- Load model ---
@st.cache_resource
def load_model():
    return joblib.load("typhoid_rf_model.pkl") 

try:
    model = load_model()
except:
    # Fallback for testing if file is missing
    class MockModel:
        def predict(self, data): return [0] 
    model = MockModel()
    # st.error("Model file 'typhoid_rf_model.pkl' not found. Please upload it.")
    # st.stop()

# --- UI Title & Header ---
st.set_page_config(page_title="Swasthya Alert", layout="wide")

# ==========================================
# 🎨 CUSTOM CSS: LARGE LABELS & LARGE INPUTS
# ==========================================
st.markdown(
    """
    <style>
    /* 1. Change the Label (Top text like 'Year') */
    .stNumberInput label p, .stSelectbox label p {
        font-size: 1.6rem !important;
        font-weight: 700 !important;
    }

    /* 2. Change the Input Value (The number inside the box) */
    .stNumberInput input {
        font-size: 1.5rem !important;  /* Size of the number */
        font-weight: 600 !important;   /* Make the number bold */
        color: #2E86C1 !important;     /* Optional: Make number Blue */
        height: 2.5rem !important;     /* Make box taller to fit the number */
    }

    /* 3. Change the Selectbox Value (The text inside dropdown) */
    .stSelectbox div[data-baseweb="select"] div {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <h1 style='text-align: center; color: #2E86C1;'>🛡 Swasthya Alert</h1>
    <h3 style='text-align: center;'>Early Warning System for Water-Related Disease Outbreaks</h3>
    """, unsafe_allow_html=True)

st.write("---")

# --- Split layout ---
col1, col2, col3 = st.columns(3)

with col1:
    Year = st.number_input("📅 Year", 1900, 2100, 2024)
    Contaminant = st.number_input("🧪 Contaminant", 0.0, 500.0, 7.0)
    pH = st.number_input("⚗ pH Level", 0.0, 14.0, 7.0)
    Turbidity = st.number_input("🌫 Turbidity", 0.0, 100.0, 2.0)
    DO = st.number_input("💧 Dissolved Oxygen", 0.0, 20.0, 7.0)
    Nitrate = st.number_input("🌱 Nitrate Level", 0.0, 100.0, 10.0)
    Lead = st.number_input("🔩 Lead Conc.", 0.0, 100.0, 5.0)

with col2:
    Bacteria = st.number_input("🦠 Bacteria Count", 0.0, 5000.0, 100.0)
    CleanWater = st.number_input("🚰 Clean Water %", 0.0, 100.0, 70.0)
    Diarrhea = st.number_input("🤢 Diarrhea Cases", 0.0, 1000.0, 100.0)
    Cholera = st.number_input("🧫 Cholera Cases", 0.0, 500.0, 20.0)
    InfantMortality = st.number_input("👶 Infant Mortality", 0.0, 200.0, 10.0)
    GDP = st.number_input("💵 GDP (USD)", 0.0, 100000.0, 5000.0)

with col3:
    Healthcare = st.number_input("🏥 Healthcare Idx", 0.0, 100.0, 50.0)
    Urbanization = st.number_input("🏙 Urbanization %", 0.0, 100.0, 40.0)
    Sanitation = st.number_input("🚿 Sanitation %", 0.0, 100.0, 60.0)
    Rainfall = st.number_input("🌧 Rainfall (mm)", 0.0, 5000.0, 1000.0)
    Temperature = st.number_input("🌡 Temp (°C)", 0.0, 50.0, 25.0)
    Population = st.number_input("👥 Pop. Density", 0.0, 10000.0, 500.0)

st.write("---")

# --- Treatment Selection ---
st.write("### 💧 Water Treatment Method")
treatment = st.selectbox("Select Method", ["Boiling", "Chlorination", "Filtration", "Unknown"])

# --- One-hot encoding ---
Water_Chlorination = 1 if treatment == "Chlorination" else 0
Water_Filtration = 1 if treatment == "Filtration" else 0
Water_Unknown = 1 if treatment == "Unknown" else 0

# --- Input array ---
input_data = np.array([[
    Year, Contaminant, pH, Turbidity, DO, Nitrate, Lead, Bacteria,
    CleanWater, Diarrhea, Cholera, InfantMortality, GDP, Healthcare,
    Urbanization, Sanitation, Rainfall, Temperature, Population,
    Water_Chlorination, Water_Filtration, Water_Unknown
]])

# --- Prediction button ---
st.write("---")
center = st.columns(3)[1]

with center:
    if st.button("🔍 Predict Outbreak Risk", use_container_width=True):
        prediction = model.predict(input_data)[0]

        if prediction == 1:
            st.error("🚨 *HIGH RISK:* Outbreak likely")
            st.warning("⚠ Immediate preventive action recommended!")
        else:
            st.success("✅ *LOW RISK:* Outbreak unlikely")

