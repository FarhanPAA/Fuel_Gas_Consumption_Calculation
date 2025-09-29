import streamlit as st 
from calculation import calculate

st.title('Fuel Gas Consumption Calculation with AGA3')

STEP = 1e-6
FMT = "%.6f"

with st.container(border=True):
    st.write("Select Measurement Units")
    pressure_unit = st.selectbox(label= 'Select Pressure Unit', options= ['psi', 'bar'])
    temperature_unit = st.selectbox(label = 'Select Temperature Unit', options= ['Fahrenheit', 'Celcius', 'kelvin'])
    dp_unit = st.selectbox(label= 'Select Differential Pressure Unit', options= ['mbar', 'inwc'])

with st.form("main_form"):
    with st.container(border=True):
        flow_pressure = st.number_input(f"Enter Flowing Gauge Pressure in {pressure_unit}",step=STEP, format=FMT)
        atm_pressure = st.number_input(f"Enter atmospheric pressure in {pressure_unit}")
        flow_temperature = st.number_input(f"Enter temperature in {temperature_unit} ")
        differential_pressure = st.number_input(f"Enter differential Pressure in {dp_unit}")
        
    with st.container(border=True):
        base_pressure = st.number_input(f"Enter Absolute Base Pressure in {pressure_unit}")
    
    submitted = st.form_submit_button("calculate")
    
    if submitted:
        gas_flow, z_f, z_b = calculate(p=flow_pressure, t= flow_temperature, d_p= differential_pressure, p_atm=atm_pressure,p_unit=pressure_unit, d_p_unit= dp_unit)
        
        st.write(f"Fuel Gas Flow: {gas_flow:.4f}")
        st.write(f"Flow Compressibility: {z_f}")
        st.write(f"Base Compressibility: {z_b}")