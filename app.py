 import streamlit as st

# Page settings
st.set_page_config(
    page_title="Smart Solar AI",
    page_icon="☀️",
    layout="wide"
)

# Title
st.title("☀️ Smart Solar AI")
st.write(
    "AI-powered solar energy assistant for solar system sizing, "
    "battery, inverter, savings and CO₂ reduction."
)

st.divider()

# User inputs
st.header("🔹 Enter Your Information")

col1, col2 = st.columns(2)

with col1:
    location = st.text_input("📍 Location", "Mianwali")
    monthly_units = st.number_input(
        "⚡ Monthly Electricity Consumption (kWh)",
        min_value=0.0,
        value=500.0
    )
    roof_area = st.number_input(
        "🏠 Available Roof Area (m²)",
        min_value=0.0,
        value=50.0
    )

with col2:
    tariff = st.number_input(
        "💰 Electricity Tariff (PKR/kWh)",
        min_value=0.0,
        value=50.0
    )
    backup_hours = st.number_input(
        "🔋 Required Battery Backup (hours)",
        min_value=0.0,
        value=4.0
    )
    essential_load = st.number_input(
        "⚡ Essential Load During Backup (kW)",
        min_value=0.0,
        value=2.0
    )

st.divider()

# Button
if st.button("🔍 Analyze Solar System", use_container_width=True):

    # Basic solar calculations
    daily_consumption = monthly_units / 30

    # Assumption: approximately 4 peak sun hours
    solar_size = daily_consumption / 4

    # Approximate 550 W panel
    panel_watt = 0.55
    number_of_panels = round(solar_size / panel_watt)

    # Inverter recommendation
    inverter_size = round(solar_size * 1.1, 1)

    # Battery calculation
    battery_capacity = essential_load * backup_hours

    # Electricity cost
    monthly_bill = monthly_units * tariff
    yearly_bill = monthly_bill * 12

    # Approximate solar generation
    yearly_solar_generation = solar_size * 4 * 365

    # CO2 assumption
    co2_factor = 0.4
    yearly_co2_reduction = yearly_solar_generation * co2_factor

    st.success("Solar analysis completed!")

    st.header("📊 Solar System Recommendation")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Solar Size", f"{solar_size:.2f} kW")
    c2.metric("Solar Panels", f"{number_of_panels}")
    c3.metric("Inverter", f"{inverter_size:.2f} kW")
    c4.metric("Battery", f"{battery_capacity:.2f} kWh")

    st.divider()

    st.subheader("☀️ Estimated Solar Generation")

    st.write(
        f"Estimated yearly solar generation: "
        f"**{yearly_solar_generation:,.0f} kWh/year**"
    )

    st.subheader("💰 Electricity Cost & Savings")

    st.write(f"Estimated monthly electricity bill: **PKR {monthly_bill:,.0f}**")
    st.write(f"Estimated yearly electricity bill: **PKR {yearly_bill:,.0f}**")

    st.subheader("🌱 Environmental Benefit")

    st.write(
        f"Estimated CO₂ emissions avoided: "
        f"**{yearly_co2_reduction:,.0f} kg CO₂/year**"
    )

    st.subheader("🤖 AI Recommendation")

    st.info(
        f"For a location in {location}, based on the entered electricity "
        f"consumption, a solar system of approximately {solar_size:.2f} kW "
        f"is recommended. The estimated inverter size is {inverter_size:.2f} kW "
        f"and the estimated battery capacity for the specified backup load "
        f"is {battery_capacity:.2f} kWh."
    )

    st.caption(
        "Note: These are preliminary estimates. Actual solar system sizing "
        "depends on site conditions, solar irradiation, equipment specifications, "
        "and detailed electrical design."
    )
