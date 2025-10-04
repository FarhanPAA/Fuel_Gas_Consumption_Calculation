from src.aga8 import calculate_gas_properties
from src.aga3 import aga3_calculate
PSI_TO_BAR = 0.06894757293178308
INWC_TO_MBAR = 2.490889

def calculate(
    p,t,d_p, p_atm, p_b, p_unit, d_p_unit, t_unit, t_base, pressure_tap,length_unit,              
    d0, D0, d0_tb, D0_tb, alpha_d,alpha_D, mu, N2, CO2, C1, C2, C3 , iC4 , nC4 , iC5 , nC5 , nC6 , nC7 , nC8, nC9, nC10, H2, O2, CO, H2O, H2S, He, Ar, gas_properties_given = False, z_f_manual = 0.99, z_b_manual = 0.995, molar_mass_manual = 16.83,
    k_manual =1.3 
):
    if p_unit == 'bar':
        p = p/PSI_TO_BAR
        p_b = p_b/PSI_TO_BAR
        p_atm = p_atm/PSI_TO_BAR
        
    if t_unit == 'F':
        t = (t-32)*5/9
        t_base = (t_base-32)*5/9
        d0_tb = (d0_tb-32)*5/9
        D0_tb = (D0_tb-32)*5/9
        alpha_D = alpha_D*9/5
        alpha_d = alpha_d*9/5
        
    if pressure_tap == 'Downstream':
        if d_p_unit == 'mbar':
            p_u = p + d_p/(1000*PSI_TO_BAR)
        elif d_p_unit == 'inwc':
            p_u = p + (d_p*INWC_TO_MBAR)/(1000*PSI_TO_BAR)
    if pressure_tap == 'Upstream':
        p_u = p

    
    if gas_properties_given == False:
        
        properties = calculate_gas_properties (p_psig=p_u, p_atm= p_atm,p_base=p_b, t=t, t_base=t_base, N2=N2, CO2=CO2, C1=C1, C2=C2,C3=C3,iC4=iC4, nC4=nC4,iC5=iC5, nC5=nC5, nC6=nC6, nC7=nC7, nC8=nC8, nC9 = nC9, nC10= nC10, H2 = H2, O2 = O2, CO = CO, H2O = H2O, H2S = H2S, He = He, Ar= Ar)
        z_f= properties['z_f']
        z_b= properties['z_b']
        molar_mass = properties['mm']
        k= properties['k']
    else:
        z_f = z_f_manual
        z_b = z_b_manual
        molar_mass = molar_mass_manual
        k= k_manual
    
    result = aga3_calculate(p=p_u,t=t,d_p=d_p, p_atm=p_atm , p_b=p_b ,d_p_unit=d_p_unit, t_b=t_base,  d0=d0, D0=D0, d0_tb = d0_tb, D0_tb = D0_tb, alpha_d = alpha_d, alpha_D = alpha_D ,Z_f=z_f,Z_b=z_b, M_gas=molar_mass, k=k, mu=mu, length_unit=length_unit)
    
    return result['volumetric_flow'], z_f, z_b, k
