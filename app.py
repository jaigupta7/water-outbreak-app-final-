import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load model
@st.cache_resource
def load_model():
    return joblib.load("typhoid_rf_model.pkl")

model = load_model()

st.title("💧 Typhoid Outbreak Prediction System (Random Forest Model)")
st.write("Enter the water and environmental parameters below:")

# Input fields
Year = st.number_input("Year", min_value=1900, max_value=2100, value=2024)
Contaminant = st.number_input("Contaminant Level (ppm)", 0.0, 500.0, 7.0)
pH = st.number_input("pH Level", 0.0, 14.0, 7.0)
Turbidity = st.number_input("Turbidity (NTU)", 0.0, 100.0, 2.0)
DO = st.number_input("Dissolved Oxygen (mg/L)", 0.0, 20.0, 7.0)
Nitrate = st.number_input("Nitrate Level (mg/L)", 0.0, 100.0, 10.0)
Lead = st.number_input("Lead Concentration (µg/L)", 0.0, 100.0, 5.0)
Bacteria = st.number_input("Bacteria Count (CFU/mL)", 0.0, 5000.0, 100.0)
CleanWater = st.number_input("Access to Clean Water (%)", 0.0, 100.0, 70.0)
Diarrhea = st.number_input("Diarrheal Cases per 100k", 0.0, 1000.0, 100.0)
Cholera = st.number_input("Cholera Cases per 100k", 0.0, 500.0, 20.0)
InfantMortality = st.number_input("Infant Mortality Rate", 0.0, 200.0, 10.0)
GDP = st.number_input("GDP per Capita (USD)", 0.0, 100000.0, 5000.0)
Healthcare = st.number_input("Healthcare Access Index", 0.0, 100.0, 50.0)
Urbanization = st.number_input("Urbanization Rate (%)", 0.0, 100.0, 40.0)
Sanitation = st.number_input("Sanitation Coverage (%)", 0.0, 100.0, 60.0)
Rainfall = st.number_input("Rainfall (mm/year)", 0.0, 5000.0, 1000.0)
Temperature = st.number_input("Temperature (°C)", 0.0, 50.0, 25.0)
Population = st.number_input("Population Density", 0.0, 10000.0, 500.0)

# Water treatment options
treatment = st.selectbox("Water Treatment Method", ["Boiling", "Chlorination", "Filtration", "Unknown"])

# Convert to one-hot encoding (same as training)
Water_Chlorination = 1 if treatment == "Chlorination" else 0
Water_Filtration = 1 if treatment == "Filtration" else 0
Water_Unknown = 1 if treatment == "Unknown" else 0

# Create input in correct order
input_data = np.array([[
    Year, Contaminant, pH, Turbidity, DO, Nitrate, Lead, Bacteria,
    CleanWater, Diarrhea, Cholera, InfantMortality, GDP, Healthcare,
    Urbanization, Sanitation, Rainfall, Temperature, Population,
    Water_Chlorination, Water_Filtration, Water_Unknown
]])

if st.button("Predict"):
    prediction = model.predict(input_data)[0]

    if prediction == 1:
        st.error("🚨 HIGH RISK: Typhoid outbreak likely")
    else:
        st.success("✅ LOW RISK: Typhoid outbreak unlikely")
