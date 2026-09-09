import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib


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
st.subheader("AI-Powered Solar & Energy Management System")

st.write(
    "Smart Solar AI analyzes your electricity consumption, roof area, "
    "backup requirements and energy usage to recommend a suitable "
    "solar and battery system."
)


# =========================================================
# LOAD ML MODEL
# =========================================================

try:
    model = joblib.load("electricity_model.pkl")
    model_loaded = True
except:
    model_loaded = False


# =========================================================
# USER INPUTS
# =========================================================

st.header("📋 Enter Your Energy Information")

city = st.text_input(
    "City",
    value="Lahore"
)

monthly_units = st.number_input(
    "Monthly Electricity Consumption (kWh)",
    min_value=0.0,
    value=300.0,
    step=10.0
)

monthly_bill = st.number_input(
    "Monthly Electricity Bill (Rs.)",
    min_value=0.0,
    value=15000.0,
    step=500.0
)

roof_area = st.number_input(
    "Available Roof Area (m²)",
    min_value=0.0,
    value=50.0,
    step=1.0
)

peak_sun_hours = st.number_input(
    "Average Peak Sun Hours",
    min_value=1.0,
    max_value=10.0,
    value=5.0,
    step=0.5
)

temperature = st.number_input(
    "Average Temperature (°C)",
    min_value=0.0,
    max_value=50.0,
    value=30.0,
    step=1.0
)

backup_hours = st.number_input(
    "Required Battery Backup (hours)",
    min_value=0.0,
    max_value=24.0,
    value=4.0,
    step=1.0
)

backup_load_kw = st.number_input(
    "Backup Load (kW)",
    min_value=0.1,
    max_value=20.0,
    value=1.5,
    step=0.1
)

important_loads = st.multiselect(
    "Select the appliances you want to keep running during backup",
    [
        "Refrigerator",
        "Fans",
        "Lights",
        "TV",
        "Water Pump",
        "Computer",
        "Washing Machine",
        "Air Conditioner"
    ],
    default=[
        "Refrigerator",
        "Fans",
        "Lights"
    ]
)


# =========================================================
# ANALYZE BUTTON
# =========================================================

if st.button(
    "🔍 Analyze My Solar System",
    type="primary"
):

    # =====================================================
    # BASIC ENERGY CALCULATIONS
    # =====================================================

    daily_energy = monthly_units / 30

    system_efficiency = 0.80

    solar_size = (
        daily_energy /
        (peak_sun_hours * system_efficiency)
    )

    roof_required = solar_size * 6

    daily_solar_generation = (
        solar_size *
        peak_sun_hours *
        system_efficiency
    )


    # =====================================================
    # APPLIANCE POWER
    # =====================================================

    appliance_power = {

        "Refrigerator": 200,

        "Fans": 300,

        "Lights": 150,

        "TV": 150,

        "Water Pump": 750,

        "Computer": 300,

        "Washing Machine": 500,

        "Air Conditioner": 1500
    }


    calculated_load_w = sum(
        appliance_power[load]
        for load in important_loads
    )

    calculated_load_kw = (
        calculated_load_w / 1000
    )


    if calculated_load_kw > 0:

        backup_load_for_battery = calculated_load_kw

    else:

        backup_load_for_battery = backup_load_kw


    # =====================================================
    # BATTERY CALCULATION
    # =====================================================

    battery_dod = 0.80

    battery_efficiency = 0.90

    battery_capacity = (
        backup_load_for_battery
        * backup_hours
        /
        (
            battery_dod
            * battery_efficiency
        )
    )


    # =====================================================
    # SAVINGS CALCULATION
    # =====================================================

    solar_saving_percentage = 0.70

    monthly_savings = (
        monthly_bill *
        solar_saving_percentage
    )

    yearly_savings = (
        monthly_savings * 12
    )


    # =====================================================
    # SOLAR PANEL & INVERTER RECOMMENDATION
    # =====================================================

    panel_watt = 550

    panel_count = int(
        (
            solar_size * 1000
            + panel_watt
            - 1
        )
        //
        panel_watt
    )

    actual_solar_capacity = (
        panel_count *
        panel_watt
    ) / 1000


    inverter_size = (
        actual_solar_capacity * 1.10
    )


    if inverter_size <= 3:

        recommended_inverter = 3

    elif inverter_size <= 5:

        recommended_inverter = 5

    elif inverter_size <= 6:

        recommended_inverter = 6

    elif inverter_size <= 8:

        recommended_inverter = 8

    elif inverter_size <= 10:

        recommended_inverter = 10

    else:

        recommended_inverter = round(
            inverter_size
        )


    panel_area = 2.5

    required_panel_area = (
        panel_count *
        panel_area
    )


    # =====================================================
    # BATTERY RECOMMENDATION
    # =====================================================

    if battery_capacity <= 5:

        battery_recommendation = "5 kWh battery"

        recommended_battery_capacity = 5

    elif battery_capacity <= 10:

        battery_recommendation = "10 kWh battery"

        recommended_battery_capacity = 10

    elif battery_capacity <= 15:

        battery_recommendation = "15 kWh battery"

        recommended_battery_capacity = 15

    elif battery_capacity <= 20:

        battery_recommendation = "20 kWh battery"

        recommended_battery_capacity = 20

    else:

        recommended_battery_capacity = int(
            np.ceil(battery_capacity)
        )

        battery_recommendation = (
            f"{recommended_battery_capacity} kWh battery"
        )


    # =====================================================
    # STEP 36
    # COMPLETE SOLAR SYSTEM COST
    # =====================================================

    panel_cost_each = 35000

    inverter_cost_per_kw = 55000

    battery_cost_per_kwh = 50000


    total_panel_cost = (
        panel_count *
        panel_cost_each
    )


    total_inverter_cost = (
        recommended_inverter *
        inverter_cost_per_kw
    )


    total_battery_cost = (
        recommended_battery_capacity *
        battery_cost_per_kwh
    )


    equipment_cost = (
        total_panel_cost
        + total_inverter_cost
        + total_battery_cost
    )


    installation_rate = 0.10

    installation_cost = (
        equipment_cost *
        installation_rate
    )


    total_system_cost = (
        equipment_cost
        + installation_cost
    )


    if yearly_savings > 0:

        payback_period = (
            total_system_cost /
            yearly_savings
        )

    else:

        payback_period = 0


    # =====================================================
    # CO2 CALCULATION
    # =====================================================

    co2_factor = 0.45

    yearly_solar_generation = (
        daily_solar_generation *
        365
    )

    yearly_co2_reduction = (
        yearly_solar_generation *
        co2_factor
    )


    # =====================================================
    # AI CONSUMPTION PREDICTION
    # =====================================================

    if model_loaded:

        prediction_input = [[
            temperature,
            daily_solar_generation
        ]]

        predicted_consumption = (
            model.predict(
                prediction_input
            )[0]
        )

    else:

        predicted_consumption = daily_energy


    # =====================================================
    # ANOMALY DETECTION
    # =====================================================

    lower_limit = daily_energy * 0.70

    upper_limit = daily_energy * 1.30


    if predicted_consumption > upper_limit:

        anomaly_message = (
            "⚠️ High energy consumption detected."
        )

        anomaly_status = "High Consumption"


    elif predicted_consumption < lower_limit:

        anomaly_message = (
            "ℹ️ Energy consumption is unusually low."
        )

        anomaly_status = "Low Consumption"


    else:

        anomaly_message = (
            "✅ Energy consumption appears normal."
        )

        anomaly_status = "Normal"


    # =====================================================
    # MAIN DASHBOARD
    # =====================================================

    st.divider()

    st.header("📊 Energy Summary")


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Recommended Solar",
            f"{solar_size:.2f} kW"
        )


    with col2:

        st.metric(
            "Battery Capacity",
            f"{battery_capacity:.2f} kWh"
        )


    with col3:

        st.metric(
            "Yearly Savings",
            f"Rs. {yearly_savings:,.0f}"
        )


    with col4:

        st.metric(
            "Payback Period",
            f"{payback_period:.1f} years"
        )


    # =====================================================
    # SYSTEM DETAILS
    # =====================================================

    st.divider()

    st.header("⚡ System Details")


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Daily Energy Consumption",
            f"{daily_energy:.2f} kWh"
        )


    with col2:

        st.metric(
            "Daily Solar Generation",
            f"{daily_solar_generation:.2f} kWh"
        )


    with col3:

        st.metric(
            "Required Roof Area",
            f"{roof_required:.1f} m²"
        )


    # =====================================================
    # CRITICAL LOAD ANALYSIS
    # =====================================================

    st.divider()

    st.header("🔌 Critical Load Analysis")


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Calculated Critical Load",
            f"{calculated_load_kw:.2f} kW"
        )


    with col2:

        st.metric(
            "Required Backup",
            f"{backup_hours:.1f} hours"
        )


    if important_loads:

        st.write(
            "**Selected Backup Appliances:**"
        )

        for load in important_loads:

            st.write(
                f"• {load} — "
                f"{appliance_power[load]} W"
            )

    else:

        st.info(
            "No specific backup appliances selected."
        )


    # =====================================================
    # SOLAR RECOMMENDATION
    # =====================================================

    st.divider()

    st.header("☀️ Solar Recommendation")


    st.write(
        f"Recommended Solar System: "
        f"**{solar_size:.2f} kW**"
    )


    st.write(
        f"Estimated Daily Solar Generation: "
        f"**{daily_solar_generation:.2f} kWh**"
    )


    # =====================================================
    # SOLAR PANEL & INVERTER
    # =====================================================

    st.divider()

    st.header(
        "🔧 Solar Panel & Inverter Recommendation"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Number of Solar Panels",
            f"{panel_count}"
        )


    with col2:

        st.metric(
            "Panel Capacity",
            f"{actual_solar_capacity:.2f} kW"
        )


    with col3:

        st.metric(
            "Recommended Inverter",
            f"{recommended_inverter} kW"
        )


    st.write(
        f"☀️ Panel Specification: "
        f"**{panel_watt} W per panel**"
    )


    st.write(
        f"🏠 Estimated Panel Area Required: "
        f"**{required_panel_area:.1f} m²**"
    )


    if roof_area >= required_panel_area:

        st.success(
            "✅ The selected solar panels can fit "
            "within the available roof area."
        )

    else:

        st.warning(
            "⚠️ The available roof area may not be "
            "enough for the calculated number of panels."
        )


    # =====================================================
    # BATTERY RECOMMENDATION
    # =====================================================

    st.divider()

    st.header("🔋 Battery Recommendation")


    st.write(
        f"Required Battery Capacity: "
        f"**{battery_capacity:.2f} kWh**"
    )


    st.success(
        f"🔋 Recommended Battery: "
        f"**{battery_recommendation}**"
    )


    # =====================================================
    # STEP 36 COST ANALYSIS
    # =====================================================

    st.divider()

    st.header(
        "💰 Complete Solar System Cost Analysis"
    )


    st.write(
        "The following cost is calculated using "
        "prototype assumptions for the hackathon."
    )


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Solar Panels Cost",
            f"Rs. {total_panel_cost:,.0f}"
        )

        st.metric(
            "Inverter Cost",
            f"Rs. {total_inverter_cost:,.0f}"
        )

        st.metric(
            "Battery Cost",
            f"Rs. {total_battery_cost:,.0f}"
        )


    with col2:

        st.metric(
            "Installation Cost",
            f"Rs. {installation_cost:,.0f}"
        )

        st.metric(
            "Equipment Cost",
            f"Rs. {equipment_cost:,.0f}"
        )

        st.metric(
            "TOTAL SYSTEM COST",
            f"Rs. {total_system_cost:,.0f}"
        )


    st.write("### 📋 Cost Breakdown")


    cost_data = pd.DataFrame({

        "Component": [
            "Solar Panels",
            "Inverter",
            "Battery",
            "Installation & Other"
        ],

        "Cost (Rs.)": [
            total_panel_cost,
            total_inverter_cost,
            total_battery_cost,
            installation_cost
        ]
    })


    fig_cost = px.bar(
        cost_data,
        x="Component",
        y="Cost (Rs.)",
        title="Solar System Cost Breakdown"
    )


    st.plotly_chart(
        fig_cost,
        use_container_width=True
    )


    st.success(
        f"💰 Estimated Total Solar System Cost: "
        f"**Rs. {total_system_cost:,.0f}**"
    )


    st.info(
        f"📊 Estimated Payback Period: "
        f"**{payback_period:.1f} years**"
    )


    st.caption(
        "Prototype assumptions: 550 W panel = Rs. 35,000, "
        "inverter = Rs. 55,000/kW, battery = Rs. 50,000/kWh, "
        "installation & other costs = 10% of equipment cost. "
        "These values are for demonstration and should be replaced "
        "with current market quotations for real-world deployment."
    )


    # =====================================================
    # STEP 37
    # SOLAR SYSTEM SIZE COMPARISON
    # =====================================================

    st.divider()

    st.header(
        "🔄 Solar System Size Comparison"
    )


    st.write(
        "Compare three possible solar system sizes "
        "based on solar capacity, panels, inverter, "
        "generation, cost and estimated savings."
    )


    # THREE SYSTEM OPTIONS

    basic_solar_size = solar_size * 0.80

    recommended_solar_size = solar_size

    high_coverage_solar_size = solar_size * 1.20


    # =====================================================
    # SYSTEM CALCULATION FUNCTION
    # =====================================================

    def calculate_system_option(system_size):

        panels = max(
            1,
            int(
                (
                    system_size * 1000
                    + panel_watt
                    - 1
                )
                //
                panel_watt
            )
        )


        actual_capacity = (
            panels *
            panel_watt
        ) / 1000


        inverter_capacity = (
            actual_capacity *
            1.10
        )


        if inverter_capacity <= 3:

            inverter = 3

        elif inverter_capacity <= 5:

            inverter = 5

        elif inverter_capacity <= 6:

            inverter = 6

        elif inverter_capacity <= 8:

            inverter = 8

        elif inverter_capacity <= 10:

            inverter = 10

        else:

            inverter = round(
                inverter_capacity
            )


        generation = (
            actual_capacity
            * peak_sun_hours
            * system_efficiency
        )


        coverage = (

            (
                generation /
                daily_energy
            ) * 100

            if daily_energy > 0

            else 0
        )


        panel_cost = (
            panels *
            panel_cost_each
        )


        inverter_cost = (
            inverter *
            inverter_cost_per_kw
        )


        system_equipment_cost = (
            panel_cost
            + inverter_cost
            + total_battery_cost
        )


        installation = (
            system_equipment_cost *
            installation_rate
        )


        total_cost = (
            system_equipment_cost
            + installation
        )


        savings_factor = min(
            coverage / 70,
            1.0
        )


        annual_savings = (
            yearly_savings *
            savings_factor
        )


        if annual_savings > 0:

            payback = (
                total_cost /
                annual_savings
            )

        else:

            payback = 0


        return {

            "Solar Size": actual_capacity,

            "Panels": panels,

            "Inverter": inverter,

            "Generation": generation,

            "Coverage": coverage,

            "Cost": total_cost,

            "Savings": annual_savings,

            "Payback": payback
        }


    # =====================================================
    # CALCULATE OPTIONS
    # =====================================================

    basic_option = calculate_system_option(
        basic_solar_size
    )


    recommended_option = calculate_system_option(
        recommended_solar_size
    )


    high_option = calculate_system_option(
        high_coverage_solar_size
    )


    # =====================================================
    # COMPARISON TABLE
    # =====================================================

    comparison_data = pd.DataFrame({

        "Parameter": [

            "Solar Size",

            "Solar Panels",

            "Inverter",

            "Daily Generation",

            "Solar Coverage",

            "Total Cost",

            "Yearly Savings",

            "Payback"
        ],


        "🟢 Basic System": [

            f"{basic_option['Solar Size']:.2f} kW",

            f"{basic_option['Panels']} × {panel_watt} W",

            f"{basic_option['Inverter']} kW",

            f"{basic_option['Generation']:.2f} kWh",

            f"{basic_option['Coverage']:.1f}%",

            f"Rs. {basic_option['Cost']:,.0f}",

            f"Rs. {basic_option['Savings']:,.0f}",

            f"{basic_option['Payback']:.1f} years"
        ],


        "🔵 Recommended System": [

            f"{recommended_option['Solar Size']:.2f} kW",

            f"{recommended_option['Panels']} × {panel_watt} W",

            f"{recommended_option['Inverter']} kW",

            f"{recommended_option['Generation']:.2f} kWh",

            f"{recommended_option['Coverage']:.1f}%",

            f"Rs. {recommended_option['Cost']:,.0f}",

            f"Rs. {recommended_option['Savings']:,.0f}",

            f"{recommended_option['Payback']:.1f} years"
        ],


        "🟣 High Coverage System": [

            f"{high_option['Solar Size']:.2f} kW",

            f"{high_option['Panels']} × {panel_watt} W",

            f"{high_option['Inverter']} kW",

            f"{high_option['Generation']:.2f} kWh",

            f"{high_option['Coverage']:.1f}%",

            f"Rs. {high_option['Cost']:,.0f}",

            f"Rs. {high_option['Savings']:,.0f}",

            f"{high_option['Payback']:.1f} years"
        ]
    })


    st.table(
        comparison_data
    )


    # =====================================================
    # OPTION CARDS
    # =====================================================

    col1, col2, col3 = st.columns(3)


    with col1:

        st.subheader("🟢 Basic System")

        st.write(
            f"Solar: **{basic_option['Solar Size']:.2f} kW**"
        )

        st.write(
            f"Panels: **{basic_option['Panels']}**"
        )

        st.write(
            f"Inverter: **{basic_option['Inverter']} kW**"
        )

        st.write(
            f"Cost: **Rs. {basic_option['Cost']:,.0f}**"
        )


    with col2:

        st.subheader("🔵 Recommended System")

        st.write(
            f"Solar: **{recommended_option['Solar Size']:.2f} kW**"
        )

        st.write(
            f"Panels: **{recommended_option['Panels']}**"
        )

        st.write(
            f"Inverter: **{recommended_option['Inverter']} kW**"
        )

        st.write(
            f"Cost: **Rs. {recommended_option['Cost']:,.0f}**"
        )


    with col3:

        st.subheader("🟣 High Coverage System")

        st.write(
            f"Solar: **{high_option['Solar Size']:.2f} kW**"
        )

        st.write(
            f"Panels: **{high_option['Panels']}**"
        )

        st.write(
            f"Inverter: **{high_option['Inverter']} kW**"
        )

        st.write(
            f"Cost: **Rs. {high_option['Cost']:,.0f}**"
        )


    # =====================================================
    # AI SYSTEM SIZE RECOMMENDATION
    # =====================================================

    if roof_area >= high_option["Solar Size"] * 6:

        st.success(
            "⭐ AI Recommendation: The High Coverage System "
            "can fit within the available roof area and "
            "provides greater solar generation."
        )


    elif roof_area >= recommended_option["Solar Size"] * 6:

        st.info(
            "⭐ AI Recommendation: The Recommended System "
            "provides a balanced option between solar "
            "generation, system size and cost."
        )


    else:

        st.warning(
            "⚠️ AI Recommendation: Available roof area is "
            "limited. The Basic System may be more practical."
        )


    st.caption(
        "Comparison values are simplified prototype estimates "
        "for hackathon demonstration and should be validated "
        "with actual site conditions and market quotations."
    )


    # =====================================================
    # SMART SOLAR SUITABILITY
    # =====================================================

    st.divider()

    st.header(
        "🧠 Smart Solar Suitability Analysis"
    )


    solar_coverage = (

        (
            daily_solar_generation /
            daily_energy
        ) * 100

        if daily_energy > 0

        else 0
    )


    roof_suitable = (
        roof_area >= required_panel_area
    )


    if roof_suitable and solar_coverage >= 90:

        st.success(
            "🟢 Excellent: The recommended solar "
            "system is suitable for your energy "
            "demand and roof area."
        )


    elif roof_suitable and solar_coverage >= 70:

        st.info(
            "🟡 Good: The solar system can cover "
            "a significant portion of your electricity demand."
        )


    elif not roof_suitable:

        st.warning(
            "🟠 Roof area limitation: The available "
            "roof area may not be sufficient."
        )


    else:

        st.warning(
            "🔴 The proposed solar system may not "
            "provide enough energy to cover your demand."
        )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Solar Coverage",
            f"{solar_coverage:.1f}%"
        )


    with col2:

        st.metric(
            "Available Roof",
            f"{roof_area:.1f} m²"
        )


    with col3:

        st.metric(
            "Required Roof",
            f"{required_panel_area:.1f} m²"
        )


    if solar_coverage >= 90 and roof_suitable:

        st.write(
            "✅ **Recommendation:** Your current "
            "inputs indicate that a solar installation "
            "is technically suitable."
        )


    elif solar_coverage >= 70 and roof_suitable:

        st.write(
            "✅ **Recommendation:** Solar installation "
            "is feasible, but some electricity may "
            "still come from the grid."
        )


    elif not roof_suitable:

        st.write(
            "⚠️ **Recommendation:** Consider reducing "
            "the system size or evaluating additional roof space."
        )


    else:

        st.write(
            "⚠️ **Recommendation:** Consider increasing "
            "the solar system size if sufficient roof space is available."
        )


    # =====================================================
    # AI CONSUMPTION PREDICTION
    # =====================================================

    st.divider()

    st.header(
        "🤖 AI Energy Consumption Prediction"
    )


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Current Daily Consumption",
            f"{daily_energy:.2f} kWh"
        )


    with col2:

        st.metric(
            "AI Predicted Consumption",
            f"{predicted_consumption:.2f} kWh"
        )


    if predicted_consumption > daily_energy:

        st.warning(
            "📈 AI predicts higher energy consumption "
            "than your current average."
        )

    else:

        st.success(
            "📉 AI predicts energy consumption "
            "close to or below your current average."
        )


    # =====================================================
    # ANOMALY DETECTION
    # =====================================================

    st.divider()

    st.header(
        "🚨 Energy Anomaly Detection"
    )


    st.write(
        f"**Status:** {anomaly_status}"
    )


    st.write(
        anomaly_message
    )


    # =====================================================
    # FINANCIAL ANALYSIS
    # =====================================================

    st.divider()

    st.header("💵 Financial Analysis")


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Monthly Savings",
            f"Rs. {monthly_savings:,.0f}"
        )


    with col2:

        st.metric(
            "Yearly Savings",
            f"Rs. {yearly_savings:,.0f}"
        )


    with col3:

        st.metric(
            "Total System Cost",
            f"Rs. {total_system_cost:,.0f}"
        )


    st.metric(
        "Updated Payback Period",
        f"{payback_period:.1f} years"
    )


    # =====================================================
    # ENERGY DASHBOARD
    # =====================================================

    st.divider()

    st.header("📈 Energy Dashboard")


    monthly_consumption = pd.DataFrame({

        "Month": [

            "Jan", "Feb", "Mar",
            "Apr", "May", "Jun",
            "Jul", "Aug", "Sep",
            "Oct", "Nov", "Dec"
        ],

        "Consumption (kWh)": [

            monthly_units * 0.90,
            monthly_units * 0.88,
            monthly_units * 0.95,
            monthly_units * 1.00,
            monthly_units * 1.10,
            monthly_units * 1.20,
            monthly_units * 1.25,
            monthly_units * 1.22,
            monthly_units * 1.10,
            monthly_units * 0.98,
            monthly_units * 0.90,
            monthly_units * 0.87
        ]
    })


    fig_consumption = px.line(

        monthly_consumption,

        x="Month",

        y="Consumption (kWh)",

        markers=True,

        title="Estimated Monthly Electricity Consumption"
    )


    st.plotly_chart(

        fig_consumption,

        use_container_width=True
    )


    # =====================================================
    # DAILY SOLAR GENERATION CHART
    # =====================================================

    days = list(range(1, 31))


    solar_values = [

        daily_solar_generation
        *
        (
            0.85 +
            np.random.random() * 0.30
        )

        for _ in days
    ]


    solar_data = pd.DataFrame({

        "Day": days,

        "Solar Generation (kWh)": solar_values
    })


    fig_solar = px.line(

        solar_data,

        x="Day",

        y="Solar Generation (kWh)",

        markers=True,

        title="Estimated Daily Solar Generation"
    )


    st.plotly_chart(

        fig_solar,

        use_container_width=True
    )


    # =====================================================
    # ENVIRONMENTAL IMPACT
    # =====================================================

    st.divider()

    st.header("🌱 Environmental Impact")


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Yearly Solar Generation",
            f"{yearly_solar_generation:,.0f} kWh"
        )


    with col2:

        st.metric(
            "Estimated CO₂ Reduction",
            f"{yearly_co2_reduction:,.0f} kg/year"
        )


    st.success(
        "🌱 Solar energy can reduce dependence on "
        "grid electricity and help reduce carbon emissions."
    )


    # =====================================================
    # SMART AI RECOMMENDATIONS
    # =====================================================

    st.divider()

    st.header(
        "💡 Smart AI Recommendations"
    )


    recommendations = []


    if solar_coverage >= 90:

        recommendations.append(
            "☀️ Your solar system can cover most "
            "of your estimated daily energy demand."
        )


    elif solar_coverage >= 70:

        recommendations.append(
            "☀️ Solar can significantly reduce "
            "your dependence on grid electricity."
        )


    else:

        recommendations.append(
            "☀️ Consider a larger solar system "
            "if sufficient roof space is available."
        )


    if battery_capacity > 10:

        recommendations.append(
            "🔋 A relatively large battery is required "
            "for your selected backup load and duration."
        )


    else:

        recommendations.append(
            "🔋 Your required backup battery size "
            "is relatively moderate."
        )


    if calculated_load_kw > backup_load_kw:

        recommendations.append(
            "⚡ Your selected critical appliances "
            "require more power than the initially "
            "specified backup load."
        )


    if not roof_suitable:

        recommendations.append(
            "🏠 Available roof area may limit the "
            "recommended solar panel installation."
        )


    if predicted_consumption > upper_limit:

        recommendations.append(
            "🚨 AI indicates potentially high energy "
            "consumption. Consider checking major loads."
        )


    if predicted_consumption <= upper_limit:

        recommendations.append(
            "✅ Energy consumption is within a "
            "reasonable range based on the prototype AI model."
        )


    for recommendation in recommendations:

        st.write(
            f"• {recommendation}"
        )


    # =====================================================
    # FINAL SUMMARY
    # =====================================================

    st.divider()

    st.header(
        "📌 Smart Solar AI Final Recommendation"
    )


    st.info(

        f"""
        **Location:** {city}

        **Recommended Solar System:** {solar_size:.2f} kW

        **Solar Panels:** {panel_count} × {panel_watt} W

        **Actual Solar Capacity:** {actual_solar_capacity:.2f} kW

        **Recommended Inverter:** {recommended_inverter} kW

        **Required Battery:** {battery_capacity:.2f} kWh

        **Recommended Battery:** {battery_recommendation}

        **Daily Solar Generation:** {daily_solar_generation:.2f} kWh

        **Solar Coverage:** {solar_coverage:.1f}%

        **Total System Cost:** Rs. {total_system_cost:,.0f}

        **Estimated Yearly Savings:** Rs. {yearly_savings:,.0f}

        **Estimated Payback:** {payback_period:.1f} years

        **Estimated CO₂ Reduction:** {yearly_co2_reduction:,.0f} kg/year
        """
    )


     
