import streamlit as st
import math
import pandas as pd

st.set_page_config(
    page_title="Smart Solar AI",
    page_icon="☀️",
    layout="wide"
)

st.title("☀️ Smart Solar AI")

st.write(
    "AI-powered solar energy assistant for solar system sizing, "
    "battery, inverter, savings, payback and CO₂ reduction."
)

st.divider()

st.header("🔹 Enter Your Information")

col1, col2 = st.columns(2)

with col1:
    location = st.text_input("📍 Location")

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
        ["On-Grid", "Hybrid", "Off-Grid"]
    )

    panel_power = st.selectbox(
        "☀️ Solar Panel Size (W)",
        [450, 500, 550, 580, 600],
        index=2
    )

st.divider()

if st.button("🔍 Analyze Solar System", use_container_width=True):

    if monthly_units <= 0:
        st.error("Please enter monthly electricity consumption greater than 0.")
        st.stop()

    daily_consumption = monthly_units / 30

    peak_sun_hours = 4.5
    performance_ratio = 0.80

    solar_size = daily_consumption / (
        peak_sun_hours * performance_ratio
    )

    solar_size = round(solar_size, 2)

    panel_kw = panel_power / 1000

    number_of_panels = math.ceil(
        solar_size / panel_kw
    )

    actual_solar_capacity = round(
        number_of_panels * panel_kw,
        2
    )

    area_per_panel = 2.2

    required_roof_area = (
        number_of_panels * area_per_panel
    )

    roof_status = roof_area >= required_roof_area

    inverter_size = round(
        actual_solar_capacity * 0.9,
        2
    )

    if inverter_size < 1:
        inverter_size = 1.0

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

    monthly_bill = monthly_units * tariff
    yearly_bill = monthly_bill * 12

    monthly_solar_generation = (
        actual_solar_capacity
        * peak_sun_hours
        * 30
        * performance_ratio
    )

    yearly_solar_generation = (
        actual_solar_capacity
        * peak_sun_hours
        * 365
        * performance_ratio
    )

    monthly_solar_generation = round(
        monthly_solar_generation,
        0
    )

    yearly_solar_generation = round(
        yearly_solar_generation,
        0
    )

    yearly_consumption = monthly_units * 12

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

    annual_solar_value = (
        yearly_solar_generation * tariff
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

    if annual_savings > 0:
        payback_years = round(
            total_cost / annual_savings,
            1
        )
    else:
        payback_years = 0

    co2_factor = 0.4

    yearly_co2_reduction = (
        yearly_solar_generation *
        co2_factor
    )

    yearly_co2_reduction = round(
        yearly_co2_reduction,
        0
    )

    yearly_co2_tonnes = round(
        yearly_co2_reduction / 1000,
        2
    )

    st.success("✅ Solar system analysis completed!")

    st.header("📊 Recommended Solar System")

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

    if system_type == "On-Grid":
        c4.metric(
            "🔋 Battery",
            "Not Required"
        )
    else:
        c4.metric(
            "🔋 Battery",
            f"{battery_capacity:.2f} kWh"
        )

    st.divider()

    st.subheader("🔧 System Details")

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

    st.divider()

    st.subheader("☀️ Estimated Solar Generation")

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

    st.divider()

    st.subheader("💰 Financial Analysis")

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

    st.divider()

    st.subheader("🔋 Battery Backup Analysis")

    st.write(
        f"**Required Backup Load:** "
        f"{essential_load:.2f} kW"
    )

    st.write(
        f"**Required Backup Time:** "
        f"{backup_hours:.1f} hours"
    )

    if system_type == "On-Grid":
        st.info(
            "ℹ️ On-grid systems normally operate without "
            "battery storage. Battery cost is excluded."
        )
    else:
        st.write(
            f"**Recommended Battery Capacity:** "
            f"{battery_capacity:.2f} kWh"
        )

    st.divider()

    st.subheader("🌱 Environmental Impact")

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
        "☘️ Solar energy can reduce dependence on grid "
        "electricity and associated carbon emissions."
    )

    st.divider()

    st.subheader("📈 Electricity vs Solar Generation")

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

    st.bar_chart(chart_data)

    st.divider()

    st.subheader("🤖 Smart Solar Recommendation")

    if system_type == "On-Grid":
        battery_text = (
            "Battery storage is not included because "
            "the selected system is On-Grid."
        )
    else:
        battery_text = (
            f"Approximately {battery_capacity:.2f} kWh "
            f"battery capacity is recommended for the "
            f"required backup."
        )

    recommendation = f"""
For {location}, based on the entered electricity consumption,
a solar system of approximately {actual_solar_capacity:.2f} kW
is recommended.

The system can use approximately {number_of_panels} solar panels
of {panel_power} W each.

A {inverter_size:.2f} kW inverter is recommended.

{battery_text}

The estimated yearly solar generation is
{yearly_solar_generation:,.0f} kWh.

Estimated annual savings are approximately
PKR {annual_savings:,.0f}.

Estimated payback period is approximately
{payback_years} years.

The system could avoid approximately
{yearly_co2_tonnes:.2f} tonnes of CO₂ emissions per year.
"""

    st.info(recommendation)

    st.caption(
        "⚠️ These are preliminary estimates for a prototype. "
        "Actual solar design depends on solar irradiation, "
        "shading, orientation, tilt, equipment specifications, "
        "electrical loads, battery chemistry, tariff structure "
        "and detailed engineering analysis."
    )
