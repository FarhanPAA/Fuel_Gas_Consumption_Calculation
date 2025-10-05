import streamlit as st
from calculation import calculate

# ---------- Page setup (no emoji icon) ----------
st.set_page_config(page_title="AGA-3 Fuel Gas Calculator", layout="wide")
st.title("Fuel Gas Consumption Calculation with AGA-3")

# Safer spacing at the very top to avoid title clipping
st.markdown(
    """
    <style>
      .block-container {padding-top: 5rem; padding-bottom: 2.0rem;}
      div[data-testid="stMetricValue"] > div {font-weight: 700;}
      div[data-testid="stMetricLabel"] > p {font-size: 0.95rem;}
      .stAlert {margin-top: 0.2rem; margin-bottom: 0.6rem;}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Constants ----------
STEP = 1e-6
FMT  = "%.6f"

# ---------- SECTION: Measurement Units ----------
with st.container(border=True):
    st.markdown("### Select Measurement Units")
    col1, col2 = st.columns(2)
    with col1:
        pressure_unit = st.selectbox(
            label="Select pressure unit",
            options=["psi", "bar"],
            help="Choose the unit for gauge, atmospheric, and base pressures."
        )
        temperature_unit = st.selectbox(
            label="Select temperature unit",
            options=["Fahrenheit", "Celsius"],
            help="All temperature fields below will use this unit."
        )
        if temperature_unit == "Fahrenheit":
            t_unit = "F"
        elif temperature_unit == "Celsius":
            t_unit = "C"
    with col2:
        dp_unit = st.selectbox(
            label="Select differential pressure unit",
            options=["mbar", "inwc"],
            help="DP transmitter output unit."
        )
        length_unit = st.selectbox(
            label="Enter length unit",
            options=["mm", "in"],
            help="Units for orifice and pipe diameters."
        )

# ---------- SECTION: Gas Properties Mode ----------
with st.container(border=True):   
    st.markdown("### Gas Properties Mode")
    col1, col2 = st.columns(2)
    with col1:
        gas_properties_method = st.selectbox(
            label="Enter Gas Properties Calculation Method",
            options=["AGA8", "Manual"],
            help="AGA8: derive Z and k from composition. Manual: enter Z_f, Z_b, k, and molar mass."
        )
    # keep logic the same
    gas_properties_given = (gas_properties_method == "Manual")

# ---------- FORM ----------
with st.form("main_form", clear_on_submit=False):
    # ----- Sensor inputs -----
    with st.container(border=True):
        st.markdown("### Enter Sensor Inputs")
        col1, col2 = st.columns(2)
        with col1:
            flow_pressure = st.number_input(
                f"Enter flowing gauge pressure in {pressure_unit}",
                step=STEP, format=FMT,
                help="Gauge pressure from PT (positive)."
            )
            pressure_tap = st.selectbox(
                label="Enter pressure sensor tapping position",
                options=["Upstream", "Downstream"],
                help="AGA-3 allows either; ensure it matches your DP impulse line scheme."
            )
            atm_pressure = st.number_input(
                f"Enter atmospheric pressure in {pressure_unit}",
                step=STEP, format=FMT,
                help="Local atmospheric pressure (absolute), e.g., 14.7 psia."
            )
        with col2:
            flow_temperature = st.number_input(
                f"Enter temperature in degree {temperature_unit}",
                step=STEP, format=FMT,
                help="Flowing temperature measured by RTD/thermowell."
            )
            differential_pressure = st.number_input(
                f"Enter differential Pressure in {dp_unit}",
                step=STEP, format=FMT,
                help="DP across orifice from DP transmitter."
            )

    # ----- Base conditions -----
    with st.container(border=True):
        st.markdown("### Enter Base Conditions")
        col1, col2 = st.columns(2)
        with col1:
            base_pressure = st.number_input(
                f"Enter absolute base pressure in {pressure_unit}",
                step=STEP, format=FMT,
                help="Typical: 14.696 psia (or 1.01325 bar)."
            )
        with col2:
            base_temp = st.number_input(
                f"Ente base temperature in {temperature_unit}",
                step=STEP, format=FMT,
                help="Common: 60°F or 15°C, depending on standard."
            )

    # ----- Orifice/Pipe geometry -----
    with st.container(border=True):
        st.markdown("### Enter Orifice and Pipe Information")
        col1, col2 = st.columns(2)
        with col1:
            orifice_dia = st.number_input(
                f"Enter orifice diameter in {length_unit}",
                step=STEP, format=FMT,
                help="Bore diameter at flowing temperature."
            )
            pipe_dia = st.number_input(
                f"Enter pipe diameter in {length_unit}",
                step=STEP, format=FMT,
                help="Pipe ID at flowing temperature."
            )
            orifice_ref_temp = st.number_input(
                f"Enter reference temperature for orifice diameter in degree {temperature_unit}",
                step=STEP, format=FMT,
                help="Temperature at which orifice was measured (manufacturing cert)."
            )
        with col2:
            pipe_ref_temp = st.number_input(
                f"Enter reference temperature for pipe diameter in degree {temperature_unit}",
                step=STEP, format=FMT,
                help="Temperature at which pipe ID is specified."
            )
            orifice_exp_coeff = st.number_input(
                f"Enter expansion coefficient for orifice per degree {temperature_unit}",
                step=1e-8, format="%.8f",
                help="Linear thermal expansion coefficient (e.g., ~1.1e-5/°C for SS)."
            )
            pipe_exp_coeff = st.number_input(
                f"Enter expansion coefficient for pipe per degree {temperature_unit}",
                step=1e-8, format="%.8f",
                help="Linear thermal expansion coefficient of pipe material."
            )

    # ----- Viscosity -----
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            mu = st.number_input(
                "Enter viscosity of gas in cP",
                step=STEP, format=FMT,
                help="Dynamic viscosity at flowing conditions (centipoise)."
            )
        with col2:
            st.write("")  # placeholder to keep two-column layout

    # ----- Gas properties OR composition -----
    if gas_properties_given:
        with st.container(border=True):
            st.markdown("### Enter Gas Properties (Manual)")
            col1, col2 = st.columns(2)
            with col1:
                k_manual = st.number_input(
                    "Isentropic expansion coefficient (k)",
                    step=STEP, format=FMT,
                    help="Often ~1.20–1.35 for natural gas."
                )
                z_f_manual = st.number_input(
                    "Compressibility factor at flowing (Z_f)",
                    step=STEP, format=FMT
                )
            with col2:
                z_b_manual = st.number_input(
                    "Compressibility factor at base (Z_b)",
                    step=STEP, format=FMT
                )
                molar_mass_manual = st.number_input(
                    "Molar mass of gas (g/mol)",
                    step=STEP, format=FMT
                )
    else:
        with st.container(border=True):
            st.markdown("### Enter Gas Composition in percentage")
            c1 = st.columns(4)
            N2  = c1[0].number_input("Nitrogen (N₂)",        min_value=0.0, max_value=100.0, value=0.0,  step=STEP, format=FMT)
            CO2 = c1[1].number_input("Carbon Dioxide (CO₂)", min_value=0.0, max_value=100.0, value=0.0,  step=STEP, format=FMT)
            C1  = c1[2].number_input("Methane (C₁)",         min_value=0.0, max_value=100.0, value=100.0, step=STEP, format=FMT)
            C2  = c1[3].number_input("Ethane (C₂)",          min_value=0.0, max_value=100.0, value=0.0,  step=STEP, format=FMT)

            c2 = st.columns(4)
            C3  = c2[0].number_input("Propane (C₃)",         min_value=0.0, max_value=100.0, value=0.0, step=STEP, format=FMT)
            iC4 = c2[1].number_input("iso-Butane (i-C₄)",    min_value=0.0, max_value=100.0, value=0.0, step=STEP, format=FMT)
            nC4 = c2[2].number_input("n-Butane (n-C₄)",      min_value=0.0, max_value=100.0, value=0.0, step=STEP, format=FMT)
            iC5 = c2[3].number_input("iso-Pentane (i-C₅)",   min_value=0.0, max_value=100.0, value=0.0, step=STEP, format=FMT)

            c3 = st.columns(4)
            nC5 = c3[0].number_input("n-Pentane (n-C₅)",     min_value=0.0, max_value=100.0, value=0.0, step=STEP, format=FMT)
            nC6 = c3[1].number_input("n-Hexane (n-C₆)",      min_value=0.0, max_value=100.0, value=0.0, step=STEP, format=FMT)
            nC7 = c3[2].number_input("n-Heptane (n-C₇)",     min_value=0.0, max_value=100.0, value=0.0, step=STEP, format=FMT)
            nC8 = c3[3].number_input("n-Octane (n-C₈)",      min_value=0.0, max_value=100.0, value=0.0, step=STEP, format=FMT)

            # --- Added species ---
            c4 = st.columns(4)
            H2  = c4[0].number_input("Hydrogen (H₂)",        min_value=0.0, max_value=100.0, value=0.0, step=STEP, format=FMT)
            H2O = c4[1].number_input("Water (H₂O)",          min_value=0.0, max_value=100.0, value=0.0, step=STEP, format=FMT)
            O2  = c4[2].number_input("Oxygen (O₂)",          min_value=0.0, max_value=100.0, value=0.0, step=STEP, format=FMT)
            CO  = c4[3].number_input("Carbon Monoxide (CO)", min_value=0.0, max_value=100.0, value=0.0, step=STEP, format=FMT)

            c5 = st.columns(4)
            H2S = c5[0].number_input("Hydrogen Sulfide (H₂S)", min_value=0.0, max_value=100.0, value=0.0, step=STEP, format=FMT)
            He  = c5[1].number_input("Helium (He)",            min_value=0.0, max_value=100.0, value=0.0, step=STEP, format=FMT)
            Ar  = c5[2].number_input("Argon (Ar)",             min_value=0.0, max_value=100.0, value=0.0, step=STEP, format=FMT)
            c5[3].write("")  # keep 4-column alignment

            # --- nC9, nC10 added here ---
            c6 = st.columns(4)
            nC9  = c6[0].number_input("n-Nonane (n-C₉)",   min_value=0.0, max_value=100.0, value=0.0, step=STEP, format=FMT)
            nC10 = c6[1].number_input("n-Decane (n-C₁₀)",  min_value=0.0, max_value=100.0, value=0.0, step=STEP, format=FMT)
            c6[2].write("")  # keep alignment
            c6[3].write("")

            total_pct = (
                N2 + CO2 + C1 + C2 + C3 + iC4 + nC4 + iC5 + nC5 + nC6 + nC7 + nC8
                + H2 + H2O + O2 + CO + H2S + He + Ar + nC9 + nC10
            )
            st.caption(f"Composition total: {total_pct:.6f} %")

            if abs(total_pct - 100.0) > 1e-3:
                st.error("Composition should sum to 100%. Adjust the inputs.")

    # ----- Submit -----
    submitted = st.form_submit_button("Calculate")

    # ---------- VALIDATION ----------
    if submitted:
        errors = []

        # absolute zero per selected unit
        abs_zero = -459.67 if t_unit == "F" else -273.15
        temp_fields = [
            ("Flow temperature", flow_temperature),
            ("Base temperature", base_temp),
            ("Orifice reference temperature", orifice_ref_temp),
            ("Pipe reference temperature", pipe_ref_temp),
        ]
        for label, val in temp_fields:
            if val <= abs_zero:
                errors.append(f"{label} must be above absolute zero ({abs_zero}°{t_unit}).")

        # pressures / dp
        if flow_pressure < 0:
            errors.append("Flowing gauge pressure cannot be negative.")
        if atm_pressure <= 0:
            errors.append("Atmospheric pressure must be positive.")
        if base_pressure <= 0:
            errors.append("Absolute base pressure must be > 0.")
        if differential_pressure <= 0:
            errors.append("Differential pressure must be > 0.")

        # diameters and beta
        beta_for_warning = None
        if orifice_dia <= 0 or pipe_dia <= 0:
            errors.append("Orifice and pipe diameters must be > 0.")
        else:
            if pipe_dia <= orifice_dia:
                errors.append("Pipe diameter must be greater than orifice diameter (β < 1).")
            else:
                beta_for_warning = orifice_dia / pipe_dia
                if not (0.10 < beta_for_warning < 0.75):
                    st.warning(f"β ratio is {beta_for_warning:.4f}. Typical AGA-3 range is 0.10–0.75. Verify sizes.")

        # thermal expansion coefficients
        if orifice_exp_coeff <= 0:
            errors.append("Orifice expansion coefficient must be positive.")
        elif not (1e-7 <= orifice_exp_coeff <= 1e-4):
            st.warning(
                f"Orifice expansion coefficient looks unusual ({orifice_exp_coeff:g} per °{t_unit}). "
                "Typical metals ~1e-6–1e-5/°C."
            )

        if pipe_exp_coeff <= 0:
            errors.append("Pipe expansion coefficient must be positive.")
        elif not (1e-7 <= pipe_exp_coeff <= 1e-4):
            st.warning(
                f"Pipe expansion coefficient looks unusual ({pipe_exp_coeff:g} per °{t_unit}). "
                "Typical metals ~1e-6–1e-5/°C."
            )

        # viscosity
        if mu <= 0:
            errors.append("Viscosity must be > 0 cP.")

        # manual gas properties sanity
        if gas_properties_given:
            if k_manual <= 1.0 or k_manual > 2.0:
                st.warning("Isentropic exponent k is usually ~1.20–1.35 for natural gas. Your value is unusual.")
            if not (0 < z_f_manual <= 2):
                errors.append("Compressibility factor at flowing must be between 0 and 2 (non-zero).")
            if not (0 < z_b_manual <= 2):
                errors.append("Compressibility factor at base must be between 0 and 2 (non-zero).")
            if molar_mass_manual <= 0:
                errors.append("Molar mass must be > 0 g/mol.")
        else:
            # enforce composition sum (blocks calc)
            if abs(total_pct - 100.0) > 1e-3:
                errors.append("Composition must sum to 100.000%. Adjust the inputs.")

        if errors:
            st.error("Please fix the following before calculation:")
            for e in errors:
                st.write(f"• {e}")
            st.stop()

        # ---------- CALCULATION (logic unchanged) ----------
        try:
            with st.spinner("Computing AGA-3 flow ..."):
                if gas_properties_given:
                    gas_flow, z_f, z_b, k, molar_mass = calculate(
                        p=flow_pressure, t=flow_temperature, d_p=differential_pressure, p_atm=atm_pressure,
                        p_unit=pressure_unit, p_b=base_pressure, d_p_unit=dp_unit, t_unit=t_unit, t_base=base_temp,
                        pressure_tap=pressure_tap, length_unit=length_unit, d0=orifice_dia, D0=pipe_dia,
                        d0_tb=orifice_ref_temp, D0_tb=pipe_ref_temp, alpha_d=orifice_exp_coeff, alpha_D=pipe_exp_coeff,
                        z_f_manual=z_f_manual, z_b_manual=z_b_manual, molar_mass_manual=molar_mass_manual,
                        k_manual=k_manual, gas_properties_given=True, mu=mu
                    )
                else:
                    gas_flow, z_f, z_b, k, molar_mass = calculate(
                        p=flow_pressure, t=flow_temperature, d_p=differential_pressure, p_atm=atm_pressure,
                        p_unit=pressure_unit, p_b=base_pressure, d_p_unit=dp_unit, t_unit=t_unit, t_base=base_temp,
                        pressure_tap=pressure_tap, length_unit=length_unit, d0=orifice_dia, D0=pipe_dia,
                        d0_tb=orifice_ref_temp, D0_tb=pipe_ref_temp, alpha_d=orifice_exp_coeff, alpha_D=pipe_exp_coeff,
                        N2=N2, CO2=CO2, C1=C1, C2=C2, C3=C3, iC4=iC4, nC4=nC4, iC5=iC5, nC5=nC5,
                        nC6=nC6, nC7=nC7, nC8=nC8, nC9=nC9, nC10=nC10, H2=H2, O2=O2, CO=CO, H2O=H2O,
                        H2S=H2S, He=He, Ar=Ar, mu=mu, gas_properties_given=False
                    )
                    
            # ---------- RESULTS ----------
            FT3_PER_M3 = 35.3147
            m3_per_hour = gas_flow * 1_000_000 / (FT3_PER_M3 * 24)  # MMSCF/D → m³/h

            with st.container(border=True):
                st.subheader("Results")

                # Row 1
                r1c1, r1c2 = st.columns(2)
                with r1c1:
                    st.metric("Fuel Gas Flow", f"{gas_flow:.4f} MMSCF/D")
                with r1c2:
                    st.metric("Fuel Gas Flow", f"{m3_per_hour:,.2f} m³/h")

                if gas_properties_given == False:
                # Row 2
                    r2c1, r2c2 = st.columns(2)
                    with r2c1:
                        st.metric("Z (flow)", f"{z_f:.6f}")
                    with r2c2:
                        st.metric("Z (base)", f"{z_b:.6f}")

                    # Row 3
                    r3c1, r3c2 = st.columns(2)
                    with r3c1:
                        st.metric("k (isentropic exp.)", f"{k:.6f}")
                    with r3c2:
                        st.metric("Molar mass", f"{molar_mass:.5f} g/mol")


        except Exception as e:
            st.exception(e)
            st.error("Calculation failed. Re-check unit selections, ranges, and consistency of inputs.")
