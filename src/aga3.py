import math

PSI_TO_BAR = 0.06894757293178308

def flange_tap_cd_constants(D: float, N: float, beta: float):
    """
    Calculate the five AGA-3 discharge-coefficient constants (Cd0 … Cd4)
    for a flange-tapped orifice plate.

    Parameters
    ----------
    D    : float – internal pipe diameter at flowing temperature
    N    : float – N4 conversion constant (same length units as D)
    beta : float – bore ratio d/D

    Returns
    -------
    dict with keys 'Cd0' … 'Cd4'
    """

    # ----- fixed AGA-3 constants -----
    A0, A1, A2, A3, A4, A5, A6 = 0.5961, 0.0291, -0.229, 0.003, 2.8, 0.000511, 0.021
    S1, S2, S3, S4, S5, S6, S7, S8 = 0.0049, 0.0433, 0.0712, -0.1145, -0.2300, -0.0116, -0.5200, -0.1400

    # ----- step-by-step evaluation -----
    L1 = L2 = N / D                               # 1. tap positions
    M2 = 2.0 * L2 / (1.0 - beta)                  # 2. dam height

    Tu = (S2 + S3 * math.exp(-8.5 * L1) +
          S4 * math.exp(-6.0 * L2)) * beta**4 / (1.0 - beta**4)  # 3. upstream corr.

    Td = S6 * (M2 + S7 * M2**1.3) * beta**1.1     # 4. downstream corr.

    # 5. small-pipe correction
    Ts = 0.0 if D > A4 * N else A3 * (1.0 - beta) * (A4 - D / N)

    # 6. discharge-coefficient constants (Re = 4000)
    Cd0 = A0 + A1 * beta**2 + A2 * beta**8 + Tu + Td + Ts
    Cd1 = A5 * beta**0.7 * 250.0**0.7
    Cd2 = A6 * beta**4 * 250.0**0.35
    Cd3 = S1 * beta**(4 + 0.8) * 4.75**0.8 * 250.0**0.35
    Cd4 = (S5 * Tu + S8 * Td) * beta**0.8 * 4.75**0.8

    return (Cd0, Cd1, Cd2, Cd3, Cd4)

def flange_tap_cd(cd_all, F_l, tol = 5e-6, max_iter = 10):
  XC = 1.142139337256165
  A  = 4.343524261523267
  B  = 3.764387693320165

  Cd0, Cd1, Cd2, Cd3, Cd4 = cd_all

  Cd = Cd0

  for _ in range(max_iter):
      # Step 2 – dimensionless flow parameter X ------------------------------
      X = F_l / Cd

      # Step 3 – correlation Fc and derivative Dc ---------------------------
      if X < XC:  # low‑Re branch (4‑40 / 4‑41)
          Fc = (
              Cd0
              + (Cd1 * X ** 0.35 + Cd2 + Cd3 * X ** 0.8) * X ** 0.35
              + Cd4 * X ** 0.8
          )
          Dc = (
              (0.7 * Cd1 * X ** 0.35 + 0.35 * Cd2 + 1.15 * Cd3 * X ** 0.8)
              * X ** 0.35
              + 0.8 * Cd4 * X ** 0.8
          )
      else:       # high‑Re branch (4‑42 / 4‑43)
          Fc = (
              Cd0
              + Cd1 * X ** 0.7
              + (Cd2 + Cd3 * X ** 0.8) * (A - B / X)
              + Cd4 * X ** 0.8
          )
          Dc = (
              0.7 * Cd1 * X ** 0.7
              + (Cd2 + Cd3 * X ** 0.8) * B / X
              + 0.8 * Cd3 * (A - B / X) * X ** 0.8
              + 0.8 * Cd4 * X ** 0.8
          )

      # Step 4 – Newton update (4‑44) ---------------------------------------
      delta_Cd = (Cd - Fc) / (1.0 + Dc / Cd)
      Cd -= delta_Cd

      if abs(delta_Cd) < tol:
          break

  Cd_f = (F_l / Cd) > 1.0  # True → X > 1 → Re < 4 000

  return Cd, Cd_f

def aga3_calculate(
    p,                           # in psig
    t,                           # flow temperature in Farenheit
    d_p,                         # differential pressure, in mbar depending on d_p_unit
    Z_f,                         # compressibility at flowing
    Z_b,                         # compressibility at base
    M_gas,                       # molecular weight of gas
    d0,                          # orifice dia at reference temp (length_unit)
    D0,                          # pipe dia at reference temp (length_unit)
    pressure_tap="upstream",     # 'upstream, 'downstream'
    p_atm = 14.73,               # Atmospheric Pressure in choosen unit
    d_p_unit = 'mbar',           # 'mbar', 'inwc'
    t_unit = 'F',                # 'F', 'C', 'K'
    R=0.0831451,                 # ideal gas constant (bar, kg, m, K)
    p_b=14.73,                   # base pressure in psia
    t_b=60.00,                   # base temperature in F/C/K (follows t_unit conversion rules below)
    k=1.3,                       # isentropic exponent
    mu=0.010268,                 # viscosity in cP
    length_unit="mm",            # "mm", "in"
    d0_tb=68.00,                 # orifice reference temp (will be converted like t per your original)
    D0_tb=68.00,                 # pipe reference temp (same)
    alpha_d=0.00000889,          # temp coeff of orifice
    alpha_D=0.00000620,          # temp coeff of pipe

):       
    
  p = (p + p_atm)*PSI_TO_BAR
  p_b =  p_b*PSI_TO_BAR
    
  if d_p_unit == "mbar":
    d_p = d_p
  elif d_p_unit == "inwc":
    d_p = d_p*2.490889
  else:
    print("Differential Pressure Unit not recognized")

  if pressure_tap == "downstream":
    p_u = p + d_p/1000 # d_p is in mbars, p_d is in bar
  elif pressure_tap == "upstream":
    p_u = p
  else:
    print("Pressure tap not recognized")

  if t_unit == "K":
    t = t
    t_b = t_b
  elif t_unit == "C":
    t = t+273.15
    t_b = t_b+273.15
    d0_tb = d0_tb+273.15
    D0_tb = D0_tb+273.15
  elif t_unit == "F":
    t = (t-32)*5/9+273.15
    t_b = (t_b-32)*5/9+273.15
    d0_tb = (d0_tb-32)*5/9+273.15
    D0_tb = (D0_tb-32)*5/9+273.15
    alpha_D = alpha_D*5/9
    alpha_d = alpha_d*5/9
  else:
    print("Temperature Unit not recognized")

  if length_unit == "in":
    d0 = d0*25.4
    D0 = D0*25.4
  elif length_unit == "mm":
    d0 = d0
    D0 = D0
  else:
    print("Length Unit not recognized")

  # Density at flowing condition (kg/m3)
  rho_f = (p_u*M_gas)/(Z_f*R*t)
  rho_b = (p_b*M_gas)/(Z_b*R*t_b)

  d = d0*(1+alpha_d*(t-d0_tb))
  D = D0*(1+alpha_D*(t-D0_tb))
  beta = d/D

  E_v = 1/(1-beta**4)**(1/2)

  if k>0:
    x = d_p/(p_u*1000) # d_p in mbar
    Y_p = (0.41+0.35*beta**4)/k
    Y = 1-Y_p*x
  else:
    Y = 1

  F_le = (4000*0.1*D*mu)/(E_v*Y*d**2)
  F_lp = (2*rho_f*d_p)**(1/2)

  if F_le< (1000*F_lp):
    F_l = F_le/F_lp
  else:
    F_l = 1000

  Cd_all = flange_tap_cd_constants(D, 25.4, beta)
  Cd, Cd_f = flange_tap_cd(Cd_all, F_l)
  F_mass = (3.1415926/4)*0.03600*E_v*d**2
  qm= F_mass*Cd*Y*F_lp
  qb = F_mass*Cd*Y*F_lp/rho_b

  qbs = qb*35.3147*24/10**6

  dict = {
      'volumetric_flow': qbs,
      'beta': beta,
      'velocity_of_approach_ev': E_v,
      'fluid_expansion_factor_y': Y,
      'coefficient_of_discharge_cd': Cd
  }

  return dict