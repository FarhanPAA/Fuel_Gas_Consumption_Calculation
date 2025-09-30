import pvtlib

PSI_TO_BAR = 0.06894757293178308

def calculate_gas_properties(
    p_psig,         # Upstream Pressure in PSIG
    t,              # Flow temperature in Celcius
    N2, CO2, C1, C2, C3, iC4, nC4, iC5, nC5, nC6, nC7, nC8,
    p_base,         # Base Pressure in PSIA
    p_atm,          # Atmospheric Pressure in PSIA
    t_base,         # Base Temperature in Celcius
    method = 'DETAIL'
):
    '''
    calculate_from_PT expcects pressure to be in PSIA and Temperature in degree Celsius,
    gas composition in percentage
    '''
    p = (p_psig+p_atm)*PSI_TO_BAR
    p_base = p_base*PSI_TO_BAR 
    
    composition = {
    'N2' : N2, 'CO2' : CO2, 'C1' : C1, 'C2' : C2, 'C3' : C3,
    'iC4' : iC4, 'nC4' : nC4, 'iC5' : iC5, 'nC5' : nC5, 
    'nC6' : nC6, 'nC7' : nC7, 'nC8' : nC8,
    }
    
    calculator = pvtlib.AGA8(method)
    
    gas_properties_flow = calculator.calculate_from_PT(
        composition=composition,
        pressure= p,
        temperature= t
    )
    
    gas_properties_base = calculator.calculate_from_PT(
        composition=composition,
        pressure=p_base,
        temperature=t_base
    )
    
    gas_properties = {
        'z_f' : gas_properties_flow['z'],
        'z_b' : gas_properties_base['z'],
        'mm'  : gas_properties_base['mm']
    }
    
    return gas_properties
