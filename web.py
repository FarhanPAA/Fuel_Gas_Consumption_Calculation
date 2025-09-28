import streamlit as st 
from calculation import calculate

st.title('Fuel Gas Consumption Calculation with AGA3')

with st.form("main_form"):
    with st.container(border=True):
        flow_pressure = st.number_input("Enter Pressure in psig")
        flow_temperature = st.number_input("Enter temperature in Fahrenheit")
        differential_pressure = st.number_input("Enter differential Pressure in mbar")
    
    submitted = st.form_submit_button("calculate")
    
    if submitted:
        gas_flow, z_f, z_b = calculate(p=flow_pressure, t= flow_temperature, d_p= differential_pressure)
        
        st.write(f"Fuel Gas Flow: {gas_flow:.4f}")