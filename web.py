import streamlit as st 
from calculation import calculate

st.title('Fuel Gas Consumption Calculation with AGA3')

STEP = 1e-6
FMT = "%.6f"

with st.container(border=True):
    st.write("Select Measurement Units")
    pressure_unit = st.selectbox(label= 'Select pressure unit', options= ['psi', 'bar'])
    temperature_unit = st.selectbox(label = 'Select temperature unit', options= ['Fahrenheit', 'Celcius'])
    dp_unit = st.selectbox(label= 'Select differential pressure unit', options= ['mbar', 'inwc'])

with st.form("main_form"):
    with st.container(border=True):
        flow_pressure = st.number_input(f"Enter flowing gauge pressure in {pressure_unit}",step=STEP, format=FMT)
        atm_pressure = st.number_input(f"Enter atmospheric pressure in {pressure_unit}",step=STEP, format=FMT)
        flow_temperature = st.number_input(f"Enter temperature in degree {temperature_unit} ",step=STEP, format=FMT)
        differential_pressure = st.number_input(f"Enter differential Pressure in {dp_unit}",step=STEP, format=FMT)
        
    with st.container(border=True):
        base_pressure = st.number_input(f"Enter absolute base pressure in {pressure_unit}",step=STEP, format=FMT)
        base_temp = st.number_input(f"Ente base temperature in {pressure_unit}",step=STEP, format=FMT)
    
    submitted = st.form_submit_button("calculate")
    
    if submitted:
        gas_flow, z_f, z_b = calculate(
            p=flow_pressure, t= flow_temperature, d_p= differential_pressure, p_atm=atm_pressure,p_unit=pressure_unit, p_b= base_pressure,d_p_unit= dp_unit)
        
        st.write(f"Fuel Gas Flow: {gas_flow:.4f}")
        st.write(f"Flow Compressibility: {z_f}")
        st.write(f"Base Compressibility: {z_b}")