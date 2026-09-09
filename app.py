 ```python
import streamlit as st
import math
import pandas as pd

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Smart Solar AI",
    page_icon="☀️",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================

st.title("☀️ Smart Solar AI")

st.write(
    "AI-powered solar energy assistant for solar system sizing, "
    "battery, inverter, savings, payback and CO₂ reduction."
)

st.divider()

# =========================================================
# USER INPUTS
# =========================================================

st.header("🔹 Enter Your Information")

col1, col2 = st.columns(2)

with col1:

    location = st.text_input(
        "📍 Location",
        "Mianwali"
    )

    monthly_units = st.number_input(
        "⚡ Monthly Electricity Consumption (kWh)",
        min_value=0.0,
        value=500.0,
        step=50.0
    )

    roof_area = st.number_input(
        "🏠 Available Roof Area (m²)",
        min_value=0.0,
        value=50.0,
        step=5.0
    )

    tariff = st.number_input(
        "💰 Electricity Tariff (PKR/kWh)",
        min_value=0.0,
        value=50.0,
        step=5.0
    )

with col2:

    backup_hours = st.number_input(
        "🔋 Required Battery Backup (hours)",
        min_value=0.0,
        value=4.0,
        step=1.0
    )

    essential_load = st.number_input(
        "⚡ Essential Load During Backup (kW)",
        min_value=0.0,
        value=2.0,
        step=0.5
    )

    system_type = st.selectbox(
        "🔌 System Type",
        [
            "On-Grid",
            "Hybrid",
            "Off-Grid"
        ]
    )

    panel_power = st.selectbox(
        "☀️ Solar Panel Size",
        [450, 500, 550, 580, 600],
        index=2
    )

st.divider()

# =========================================================
# ANALYZE BUTTON
# =========================================================

if st.button(
    "🔍 Analyze Solar System",
    use_container_width=True
):

    # =====================================================
    # BASIC CALCULATIONS
    # =====================================================

    daily_consumption = monthly_units / 30

    # Approximate peak sun hours
    peak_sun_hours = 4.5

    # Performance ratio / system losses
    performance_ratio = 0.80

    # Recommended solar size
    solar_size = (
        daily_consumption /
        (peak_sun_hours * performance_ratio)
    )

    # Round solar size
    solar_size = round(solar_size, 2)

    # =====================================================
    # SOLAR PANELS
    # =====================================================

    panel_kw = panel_power / 1000

    number_of_panels = math.ceil(
        solar_size / panel_kw
    )

    actual_solar_capacity = round(
        number_of_panels * panel_kw,
        2
    )

    # =====================================================
    # ROOF AREA
    # =====================================================

    # Approximate area required per panel
    area_per_panel = 2.2

    required_roof_area = (
        number_of_panels * area_per_panel
    )

    roof_status = (
        roof_area >= required_roof_area
    )

    # =====================================================
    # INVERTER
    # =====================================================

    inverter_size = round(
        actual_solar_capacity * 0.9,
        2
    )

    # Minimum practical inverter
    if inverter_size < 1:
        inverter_size = 1.0

    # =====================================================
    # BATTERY
    # =====================================================

    # Battery calculations
    battery_efficiency = 0.90
    depth_of_discharge = 0.80

    usable_battery_energy = (
        essential_load * backup_hours
    )

    battery_capacity = (
        usable_battery_energy /
        (battery_efficiency * depth_of_discharge)
    )

    battery_capacity = round(
        battery_capacity,
        2
    )

    # =====================================================
    # ELECTRICITY BILL
    # =====================================================

    monthly_bill = (
        monthly_units * tariff
    )

    yearly_bill = (
        monthly_bill * 12
    )

    # =====================================================
    # SOLAR GENERATION
    # =====================================================

    monthly_solar_generation = (
        actual_solar_capacity *
        peak_sun_hours *
        30 *
        performance_ratio
    )

    yearly_solar_generation = (
        actual_solar_capacity *
        peak_sun_hours *
        365 *
        performance_ratio
    )

    monthly_solar_generation = round(
        monthly_solar_generation,
        0
    )

    yearly_solar_generation = round(
        yearly_solar_generation,
        0
    )

    # =====================================================
    # SOLAR COVERAGE
    # =====================================================

    yearly_consumption = (
        monthly_units * 12
    )

    solar_coverage = (
        yearly_solar_generation /
        yearly_consumption
    ) * 100

    solar_coverage = min(
        solar_coverage,
        100
    )

    solar_coverage = round(
        solar_coverage,
        1
    )

    # =====================================================
    # SAVINGS
    # =====================================================

    annual_solar_value = (
        yearly_solar_generation *
        tariff
    )

    annual_solar_value = min(
        annual_solar_value,
        yearly_bill
    )

    annual_savings = round(
        annual_solar_value,
        0
    )

    monthly_savings = round(
        annual_savings / 12,
        0
    )

    # =====================================================
    # SYSTEM COST
    # =====================================================

    # Approximate prototype costs
    solar_cost_per_kw = 180000

    inverter_cost_per_kw = 70000

    battery_cost_per_kwh = 85000

    solar_cost = (
        actual_solar_capacity *
        solar_cost_per_kw
    )

    inverter_cost = (
        inverter_size *
        inverter_cost_per_kw
    )

    battery_cost = (
        battery_capacity *
        battery_cost_per_kwh
    )

    if system_type == "On-Grid":
        battery_cost = 0

    total_cost = (
        solar_cost +
        inverter_cost +
        battery_cost
    )

    total_cost = round(
        total_cost,
        0
    )

    # =====================================================
    # PAYBACK
    # =====================================================

    if annual_savings > 0:

        payback_years = (
            total_cost /
            annual_savings
        )

        payback_years = round(
            payback_years,
            1
        )

    else:

        payback_years = 0

    # =====================================================
    # CO2 REDUCTION
    # =====================================================

    # Approximate grid emission factor
    co2_factor = 0.4

    yearly_co2_reduction = (
        yearly_solar_generation *
        co2_factor
    )

    yearly_co2_reduction = round(
        yearly_co2_reduction,
        0
    )

    # Convert kg to tonnes
    yearly_co2_tonnes = round(
        yearly_co2_reduction / 1000,
        2
    )

    # =====================================================
    # SUCCESS MESSAGE
    # =====================================================

    st.success(
        "✅ Solar system analysis completed!"
    )

    # =====================================================
    # MAIN RESULTS
    # =====================================================

    st.header(
        "📊 Recommended Solar System"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "☀️ Solar Size",
        f"{actual_solar_capacity:.2f} kW"
    )

    c2.metric(
        "🔆 Solar Panels",
        f"{number_of_panels}"
    )

    c3.metric(
        "⚡ Inverter",
        f"{inverter_size:.2f} kW"
    )

    c4.metric(
        "🔋 Battery",
        f"{battery_capacity:.2f} kWh"
    )

    # =====================================================
    # SYSTEM DETAILS
    # =====================================================

    st.divider()

    st.subheader(
        "🔧 System Details"
    )

    d1, d2, d3 = st.columns(3)

    d1.write(
        f"**Panel Size:** {panel_power} W"
    )

    d2.write(
        f"**Required Roof Area:** "
        f"{required_roof_area:.1f} m²"
    )

    d3.write(
        f"**Solar Coverage:** "
        f"{solar_coverage}%"
    )

    # =====================================================
    # ROOF CHECK
    # =====================================================

    if roof_status:

        st.success(
            f"🏠 Roof area is sufficient. "
            f"Estimated required area: "
            f"{required_roof_area:.1f} m²."
        )

    else:

        st.warning(
            f"⚠️ Available roof area may be insufficient. "
            f"You have {roof_area:.1f} m² but approximately "
            f"{required_roof_area:.1f} m² may be required."
        )

    # =====================================================
    # SOLAR GENERATION
    # =====================================================

    st.divider()

    st.subheader(
        "☀️ Estimated Solar Generation"
    )

    g1, g2, g3 = st.columns(3)

    g1.metric(
        "Daily Consumption",
        f"{daily_consumption:.1f} kWh"
    )

    g2.metric(
        "Monthly Solar Generation",
        f"{monthly_solar_generation:,.0f} kWh"
    )

    g3.metric(
        "Yearly Solar Generation",
        f"{yearly_solar_generation:,.0f} kWh"
    )

    # =====================================================
    # SAVINGS
    # =====================================================

    st.divider()

    st.subheader(
        "💰 Financial Analysis"
    )

    f1, f2, f3, f4 = st.columns(4)

    f1.metric(
        "Monthly Bill",
        f"PKR {monthly_bill:,.0f}"
    )

    f2.metric(
        "Monthly Savings",
        f"PKR {monthly_savings:,.0f}"
    )

    f3.metric(
        "Estimated System Cost",
        f"PKR {total_cost:,.0f}"
    )

    f4.metric(
        "Payback Period",
        f"{payback_years} years"
    )

    # =====================================================
    # BATTERY INFORMATION
    # =====================================================

    st.divider()

    st.subheader(
        "🔋 Battery Backup Analysis"
    )

    st.write(
        f"Required backup load: "
        f"**{essential_load:.2f} kW**"
    )

    st.write(
        f"Required backup time: "
        f"**{backup_hours:.1f} hours**"
    )

    st.write(
        f"Recommended battery capacity: "
        f"**{battery_capacity:.2f} kWh**"
    )

    if system_type == "On-Grid":

        st.info(
            "ℹ️ On-grid systems normally do not require battery "
            "storage. Battery cost has therefore been excluded "
            "from the estimated system cost."
        )

    # =====================================================
    # CO2
    # =====================================================

    st.divider()

    st.subheader(
        "🌱 Environmental Impact"
    )

    e1, e2 = st.columns(2)

    e1.metric(
        "Annual CO₂ Avoided",
        f"{yearly_co2_reduction:,.0f} kg"
    )

    e2.metric(
        "Annual CO₂ Avoided",
        f"{yearly_co2_tonnes:.2f} tonnes"
    )

    st.write(
        "☘️ Solar energy can reduce dependence on "
        "grid electricity and therefore reduce associated "
        "carbon emissions."
    )

    # =====================================================
    # CHART
    # =====================================================

    st.divider()

    st.subheader(
        "📈 Electricity vs Solar Generation"
    )

    chart_data = pd.DataFrame(
        {
            "Energy (kWh)": [
                monthly_units,
                monthly_solar_generation
            ]
        },
        index=[
            "Monthly Consumption",
            "Monthly Solar Generation"
        ]
    )

    st.bar_chart(
        chart_data
    )

    # =====================================================
    # AI-STYLE RECOMMENDATION
    # =====================================================

    st.divider()

    st.subheader(
        "🤖 Smart Solar Recommendation"
    )

    recommendation = f"""
    For {location}, based on the entered electricity consumption,
    a solar system of approximately {actual_solar_capacity:.2f} kW
    is recommended.

    The system can use approximately {number_of_panels} solar panels
    of {panel_power} W each.

    A {inverter_size:.2f} kW inverter is recommended.

    For {essential_load:.2f} kW essential load and
    {backup_hours:.1f} hours of backup, approximately
    {battery_capacity:.2f} kWh battery capacity is estimated.

    The system may generate approximately
    {yearly_solar_generation:,.0f} kWh per year.

    Estimated annual savings are approximately
    PKR {annual_savings:,.0f}.

    Estimated payback period is approximately
    {payback_years} years.

    The system could avoid approximately
    {yearly_co2_tonnes:.2f} tonnes of CO₂ emissions per year.
    """

    st.info(
        recommendation
    )

    # =====================================================
    # DISCLAIMER
    # =====================================================

    st.caption(
        "⚠️ These are preliminary estimates for a prototype. "
        "Actual solar design depends on site-specific solar "
        "irradiance, shading, orientation, tilt, equipment "
        "specifications, electrical loads, battery chemistry, "
        "tariff structure and detailed engineering analysis."
    )
```
