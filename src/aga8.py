import pvtlib

def calculate_gas_properties(
    p_psig, t_farenheit, N2, CO2, C1, C2, C3, iC4, nC4, iC5, nC5, nC6, nC7, nC8,
    p_base = 1.0155977, t_base = 15.5555556, method = 'DETAIL'
):
    p = (p_psig+14.73)*0.068947
    t = (t_farenheit-32)*5/9
    
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
