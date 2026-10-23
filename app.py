import streamlit as st
import requests

# Set the page configuration
st.set_page_config(page_title="Water Potability Predictor", page_icon="💧", layout="centered")

st.title("💧 Water Potability Prediction App")
st.write("Adjust the sliders below to check if the water is safe to drink.")

# Create a form for user inputs
with st.form("prediction_form"):
    st.subheader("Water Parameters")
    
    # Replaced number_input with slider and added appropriate min/max ranges
    ph = st.number_input("pH (0 to 14)", min_value=0.0, max_value=14.0, value=7.0, step=0.1)
    Hardness = st.number_input("Hardness (mg/L)", min_value=0.0, value=196.0, step=1.0)
    Solids = st.number_input("Solids (TDS in ppm)", min_value=0.0, value=22014.0, step=100.0)
    Chloramines = st.number_input("Chloramines (ppm)", min_value=0.0, value=7.1, step=0.1)
    Sulfate = st.number_input("Sulfate (mg/L)", min_value=0.0, value=333.0, step=1.0)
    Conductivity = st.number_input("Conductivity (μS/cm)", min_value=0.0, value=426.0, step=1.0)
    Organic_carbon = st.number_input("Organic Carbon (ppm)", min_value=0.0, value=14.2, step=0.1)
    Trihalomethanes = st.number_input("Trihalomethanes (μg/L)", min_value=0.0, value=66.3, step=0.1)
    Turbidity = st.number_input("Turbidity (NTU)", min_value=0.0, value=3.9, step=0.1)
    
    # Submit button
    submit_button = st.form_submit_button("Predict Water Quality")

# When the user clicks the button
if submit_button:
    # Prepare the data to send to the FastAPI backend
    input_data = {
        "ph": ph,
        "Hardness": Hardness,
        "Solids": Solids,
        "Chloramines": Chloramines,
        "Sulfate": Sulfate,
        "Conductivity": Conductivity,
        "Organic_carbon": Organic_carbon,
        "Trihalomethanes": Trihalomethanes,
        "Turbidity": Turbidity
    }
    
    try:
        # Send a POST request to your FastAPI server
        response = requests.post("http://127.0.0.1:8000/predict", json=input_data)
        
        # Display the result
        if response.status_code == 200:
            result = response.json()
            if result['prediction'] == 1:
                st.success(f"✅ Result: {result['status']}")
                st.balloons()
            else:
                st.error(f"❌ Result: {result['status']}")
        else:
            st.error(f"Failed to get prediction. Error Code: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        st.error("Connection Error: Make sure your FastAPI backend (`uvicorn api:app --reload`) is running in another terminal!")