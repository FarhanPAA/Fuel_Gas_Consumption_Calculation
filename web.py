import streamlit as st 
from calculation import calculate

st.title('Fuel Gas Consumption Calculation with AGA3')

STEP = 1e-6
FMT = "%.6f"

with st.container(border=True):
    st.write("Select Measurement Units")
    pressure_unit = st.selectbox(label= 'Select pressure unit', options= ['psi', 'bar'])
    temperature_unit = st.selectbox(label = 'Select temperature unit', options= ['Fahrenheit', 'Celsius'])
    if temperature_unit == 'Fahrenheit':
        t_unit = 'F'
    elif temperature_unit == 'Celsius':
        t_unit = 'C'
    dp_unit = st.selectbox(label= 'Select differential pressure unit', options= ['mbar', 'inwc'])
    length_unit = st.selectbox(label="Enter length unit", options=['mm', 'in'])

with st.form("main_form"):
    with st.container(border=True):
        flow_pressure = st.number_input(f"Enter flowing gauge pressure in {pressure_unit}",step=STEP, format=FMT)
        pressure_tap = st.selectbox(label="Enter pressure sensor tapping position", options=['Upstream', 'Downstream'])
        atm_pressure = st.number_input(f"Enter atmospheric pressure in {pressure_unit}",step=STEP, format=FMT)
        flow_temperature = st.number_input(f"Enter temperature in degree {temperature_unit} ",step=STEP, format=FMT)
        differential_pressure = st.number_input(f"Enter differential Pressure in {dp_unit}",step=STEP, format=FMT)
        
    with st.container(border=True):
        base_pressure = st.number_input(f"Enter absolute base pressure in {pressure_unit}",step=STEP, format=FMT)
        base_temp = st.number_input(f"Ente base temperature in {pressure_unit}",step=STEP, format=FMT)
        
    with st.container(border=True):
        orifice_dia = st.number_input(f"Enter orifice diameter in {length_unit}",step=STEP, format=FMT)
        pipe_dia = st.number_input(f"Enter pipe diameter in {length_unit}",step=STEP, format=FMT)
        orifice_ref_temp = st.number_input(f"Enter reference temperature for orifice diameter in degree {temperature_unit}",step=STEP, format=FMT )
        pipe_ref_temp = st.number_input(f"Enter reference temperature for pipe diameter in degree {temperature_unit}",step=STEP, format=FMT )
        orifice_exp_coeff = st.number_input(f"Enter expansion coefficient for orifice per degree {temperature_unit}", step=1e-8, format="%.8f")
        pipe_exp_coeff = st.number_input(f"Enter expansion coefficient for pipe per degree {temperature_unit}", step=1e-8, format="%.8f")
    
    submitted = st.form_submit_button("calculate")
    
    if submitted:
        gas_flow, z_f, z_b = calculate(
            p=flow_pressure, t= flow_temperature, d_p= differential_pressure, p_atm=atm_pressure,p_unit=pressure_unit, p_b= base_pressure,d_p_unit= dp_unit, t_unit=t_unit, t_base=base_temp, pressure_tap=pressure_tap, length_unit=length_unit, d0=orifice_dia, D0=pipe_dia, d0_tb=orifice_ref_temp, D0_tb=pipe_ref_temp, alpha_d=orifice_exp_coeff, alpha_D = pipe_exp_coeff)
        
        st.write(f"Fuel Gas Flow: {gas_flow:.4f}")
        st.write(f"Flow Compressibility: {z_f}")
        st.write(f"Base Compressibility: {z_b}")