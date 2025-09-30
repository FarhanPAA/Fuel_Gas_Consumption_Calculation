from src.aga8 import calculate_gas_properties
from src.aga3 import aga3_calculate
PSI_TO_BAR = 0.06894757293178308

def calculate(
    p,t,d_p, p_atm, p_b, p_unit = 'psi', d_p_unit = 'mbar',                  
    d0=247.768, D0=387.535,                  
    gas_properties_given = False, z_f_manual = 0.99, z_b_manual = 0.995, molar_mass_manual = 16.83,
    N2 = 0.223, CO2 = 0.198, C1 = 96.284, C2 = 2.210, C3 = 0.624, iC4 = 0.175, nC4 = 0.139, iC5 = 0.064,
    nC5 = 0.031, nC6 = 0.025, nC7 = 0.022, nC8 = 0.005 
):
    if p_unit == 'bar':
        p = p/PSI_TO_BAR
        p_b = p_b/PSI_TO_BAR
        p_atm = p_atm/PSI_TO_BAR

    if gas_properties_given == False:
        properties = calculate_gas_properties(p_psig=p, p_atm= p_atm, t_fahrenheit=t, N2=N2, CO2=CO2, C1=C1, C2=C2,C3=C3,
                                        iC4=iC4, nC4=nC4,iC5=iC5, nC5=nC5, nC6=nC6, nC7=nC7, nC8=nC8)
        z_f= properties['z_f']
        z_b= properties['z_b']
        molar_mass = properties['mm']
    else:
        z_f = z_f_manual
        z_b = z_b_manual
        molar_mass = molar_mass_manual
    
    result = aga3_calculate(p=p,t=t,d_p=d_p, p_atm=p_atm , p_b=p_b ,d_p_unit=d_p_unit ,Z_f=z_f,Z_b=z_b, M_gas=molar_mass,d0=d0,D0=D0)
    
    return result['volumetric_flow'], z_f, z_b

'''
gas_flow, _, _ = calculate(p=100, t= 70, d_p= 100, p_atm=14.73, p_b=14.73 , p_unit='psi', d_p_unit= 'mbar')

print(gas_flow)

gas_flow, _, _ = calculate(p=100*PSI_TO_BAR, t= 70, d_p= 100, p_atm=14.73*PSI_TO_BAR, p_b=14.73*PSI_TO_BAR, p_unit='bar', d_p_unit= 'mbar')

print(gas_flow)

'''

gas_flow,_,_ = calculate(p=6.89, t= 70, d_p= 100, p_atm=1.01,p_unit='bar', p_b= 1.01, d_p_unit= 'mbar')

print(gas_flow)