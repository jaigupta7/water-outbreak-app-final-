import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load model
@st.cache_resource
def load_model():
    return joblib.load("typhoid_rf_model.pkl")

model = load_model()

# UI Title & Header
st.set_page_config(page_title="Swasthya Alert", layout="wide")

# --------------------------------------------------------
# 🔥 GLOBAL CSS FOR LARGE FONT SIZE
# --------------------------------------------------------
st.set_page_config(page_title="Swasthya Alert", layout="wide")

# 🔥 ADD THIS CSS RIGHT HERE
st.markdown("""
<style>

label {
    font-size: 30px !important;
    font-weight: 700 !important;
    color: #000 !important;
}

input[type=number] {
    font-size: 24px !important;
    height: 55px !important;
}

.css-6hp17o, .css-1wa3eu0-placeholder {
    font-size: 24px !important;
}

</style>
""", unsafe_allow_html=True)
# -----------------------------

# Your normal code continues below
st.markdown("<h1 style='text-align:center; color:#2C6E49;'>🛡️ Swasthya Alert – Outbreak Prediction System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px;'>Enter water quality & environmental parameters to assess outbreak risk</p>", unsafe_allow_html=True)


# Title
st.markdown("<h1 style='text-align:center; color:#2C6E49;'>🛡️ Swasthya Alert – Outbreak Prediction System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:22px;'>Enter water quality & environmental parameters to assess outbreak risk</p>", unsafe_allow_html=True)

st.write("---")

# Split layout
col1, col2, col3 = st.columns(3)

with col1:
    Year = st.number_input("📅 Year", 1900, 2100, 2024)
    Contaminant = st.number_input("🧪 Contaminant Level (ppm)", 0.0, 500.0, 7.0)
    pH = st.number_input("⚗️ pH Level", 0.0, 14.0, 7.0)
    Turbidity = st.number_input("🌫️ Turbidity (NTU)", 0.0, 100.0, 2.0)
    DO = st.number_input("💧 Dissolved Oxygen (mg/L)", 0.0, 20.0, 7.0)
    Nitrate = st.number_input("🌱 Nitrate Level (mg/L)", 0.0, 100.0, 10.0)
    Lead = st.number_input("🔩 Lead Concentration (µg/L)", 0.0, 100.0, 5.0)

with col2:
    Bacteria = st.number_input("🦠 Bacteria Count (CFU/mL)", 0.0, 5000.0, 100.0)
    CleanWater = st.number_input("🚰 Clean Water Access (%)", 0.0, 100.0, 70.0)
    Diarrhea = st.number_input("🤢 Diarrheal Cases per 100k", 0.0, 1000.0, 100.0)
    Cholera = st.number_input("🧫 Cholera Cases per 100k", 0.0, 500.0, 20.0)
    InfantMortality = st.number_input("👶 Infant Mortality Rate", 0.0, 200.0, 10.0)
    GDP = st.number_input("💵 GDP per Capita (USD)", 0.0, 100000.0, 5000.0)

with col3:
    Healthcare = st.number_input("🏥 Healthcare Access Index", 0.0, 100.0, 50.0)
    Urbanization = st.number_input("🏙 Urbanization Rate (%)", 0.0, 100.0, 40.0)
    Sanitation = st.number_input("🚿 Sanitation Coverage (%)", 0.0, 100.0, 60.0)
    Rainfall = st.number_input("🌧️ Rainfall (mm/year)", 0.0, 5000.0, 1000.0)
    Temperature = st.number_input("🌡️ Temperature (°C)", 0.0, 50.0, 25.0)
    Population = st.number_input("👥 Population Density", 0.0, 10000.0, 500.0)

st.write("### 💧 Water Treatment Method")
treatment = st.selectbox("", ["Boiling", "Chlorination", "Filtration", "Unknown"])

# One-hot encoding
Water_Chlorination = 1 if treatment == "Chlorination" else 0
Water_Filtration = 1 if treatment == "Filtration" else 0
Water_Unknown = 1 if treatment == "Unknown" else 0

# Input array (order important)
input_data = np.array([[
    Year, Contaminant, pH, Turbidity, DO, Nitrate, Lead, Bacteria,
    CleanWater, Diarrhea, Cholera, InfantMortality, GDP, Healthcare,
    Urbanization, Sanitation, Rainfall, Temperature, Population,
    Water_Chlorination, Water_Filtration, Water_Unknown
]])

# Prediction button
st.write("---")
center = st.columns(3)[1]

with center:
    if st.button("🔍 Predict Outbreak Risk", use_container_width=True):
        prediction = model.predict(input_data)[0]

        if prediction == 1:
            st.error("🚨 **HIGH RISK:** Outbreak likely")
            st.warning("⚠️ Immediate preventive action recommended!")
        else:
            st.success("✅ **LOW RISK:** Outbreak unlikely")

