import streamlit as st
import pandas as pd
import numpy as np

# Page Configuration
st.set_page_config(page_title="Triple Whale's Sonar Demo", layout="wide")

# Header
st.title("Triple Whale's Sonar + Klaviyo Demo")
st.markdown(
    """
    Discover how **Triple Whale's Sonar** enhances Klaviyo's abandoned cart flows by:
    - Capturing more customer events.
    - Matching more visitors to their profiles.
    - Triggering significantly more flows.
    - Increasing revenue by an average of **22%** on Sonar-triggered flows.
    """
)

# User Input
st.subheader("Your Current Performance")
flows_triggered = st.slider(
    "How many Klaviyo flows are currently being triggered daily?", min_value=1, max_value=500, step=1, value=300
)
current_revenue = st.slider(
    "What is the current daily revenue from these flows? ($)", min_value=100, max_value=1000, step=10, value=500
)

# Dummy DataFrame: Visitor Checkout Events
st.subheader("Visitors Starting Checkout")
visitor_data = pd.DataFrame({
    "Visitor Name": ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace"],
    "Email": [
        "alice@example.com", "bob@example.com", "charlie@example.com",
        "diana@example.com", "eve@example.com", "frank@example.com", "grace@example.com"
    ],
    "Checkout Date": [
        "2024-12-01", "2024-12-01", "2024-12-02",
        "2024-12-03", "2024-12-03", "2024-12-04", "2024-12-05"
    ],
    "Matched Without Sonar": [True, False, False, True, False, False, False],
    "Matched With Sonar": [True, True, False, True, True, True, False],  # Sonar also fails to match some users
})

# Add a column indicating additional events captured by Sonar
visitor_data["Additional Events Captured by Sonar"] = (
    visitor_data["Matched With Sonar"] & ~visitor_data["Matched Without Sonar"]
).astype(int)

# Display the DataFrame with highlighting for additional events
st.dataframe(visitor_data.style.applymap(
    lambda x: "background-color: #FFDDC1;" if x == 1 else "",
    subset=["Additional Events Captured by Sonar"]
))

st.markdown(
    """
    The table above highlights how **Sonar** identifies and matches more visitors to their profiles compared to "Without Sonar."
    """
)

# Generate randomized distribution for flows and revenue over 3 months (90 days)
days = np.arange(1, 91)  # 90 days (3 months)

# Base growth trend for flows
growth_trend = 0.5 * (1 + np.tanh((days - 45) / 15))  # Tanh curve to simulate slow-start growth
base_flows = flows_triggered * (0.5 + growth_trend)  # Base flows with growth trend
flows_without_sonar = base_flows + np.random.normal(0, 5, len(days))  # Add noise

# Daily uplift for Sonar flows (fluctuates between 30% and 50%)
sonar_flow_uplift = np.random.uniform(1.3, 1.5, len(days))  # Daily fluctuation
flows_with_sonar = flows_without_sonar * sonar_flow_uplift

# Revenue correlates with flows
revenue_without_sonar = (flows_without_sonar / flows_triggered) * current_revenue

# Daily uplift for Sonar revenue (fluctuates around 22%, e.g., 18% to 26%)
sonar_revenue_uplift = np.random.uniform(1.18, 1.26, len(days))  # Daily fluctuation
revenue_with_sonar = revenue_without_sonar * sonar_revenue_uplift

# Calculate totals for metrics
total_flows_without_sonar = int(flows_without_sonar.sum())
total_flows_with_sonar = int(flows_with_sonar.sum())
total_revenue_without_sonar = int(revenue_without_sonar.sum())
total_revenue_with_sonar = int(revenue_with_sonar.sum())

additional_flows = total_flows_with_sonar - total_flows_without_sonar
additional_revenue = total_revenue_with_sonar - total_revenue_without_sonar

# Flows Area Chart
st.subheader("Flows Triggered Over 3 Months")
st.markdown(
    """
    The chart below shows the difference in flows triggered without and with Sonar over the course of 3 months:
    """
)

flows_data = pd.DataFrame({"Day": days, "Without Sonar": flows_without_sonar, "With Sonar": flows_with_sonar}).set_index("Day")
st.area_chart(
    flows_data,
    color=["rgba(0, 0, 255, 0.6)", "rgba(255, 0, 0, 0.6)"]  # Adjust transparency to prevent blending
)

# Revenue Area Chart
st.subheader("Revenue Generated Over 3 Months")
st.markdown(
    """
    The chart below illustrates the uplift in revenue generated with Sonar-triggered flows over the course of 3 months:
    """
)

revenue_data = pd.DataFrame({"Day": days, "Without Sonar": revenue_without_sonar, "With Sonar": revenue_with_sonar}).set_index("Day")
st.area_chart(
    revenue_data,
    color=["rgba(0, 0, 255, 0.6)", "rgba(255, 0, 0, 0.6)"]  # Adjust transparency to prevent blending
)

# Flows Summary Metrics
st.subheader("Flows Summary")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Flows Triggered (Without Sonar)", value=f"{total_flows_without_sonar:,}")
with col2:
    st.metric(label="Total Flows Triggered (With Sonar)", value=f"{total_flows_with_sonar:,}", delta=f"+{additional_flows:,}")
with col3:
    st.metric(label="Additional Flows Triggered", value=f"+{additional_flows:,}")

# Revenue Summary Metrics
st.subheader("Revenue Summary")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Revenue ($) (Without Sonar)", value=f"${total_revenue_without_sonar:,}")
with col2:
    st.metric(label="Total Revenue ($) (With Sonar)", value=f"${total_revenue_with_sonar:,}", delta=f"+${additional_revenue:,}")
with col3:
    st.metric(label="Additional Revenue ($)", value=f"+${additional_revenue:,}")

# Top 10 Shops Leveraging Sonar
st.subheader("Top 10 Shops Leveraging Sonar")
st.markdown(
    """
    Based on 30 days of data from November 2024, here are the top 10 shops getting the most value from Sonar:
    """
)

# Create the Top Shops DataFrame with percentage conversion for 'Sonar to Total Ratio'
top_shops = pd.DataFrame({
    "Shop Name": [f"Anonymized Shop {i+1}" for i in range(10)],
    "GMV Tier": [
        "30M-40M", ">125M", "100M-125M", "60M-75M", ">125M",
        "75M-100M", "50M-60M", "40M-50M", "30M-40M", ">125M"
    ],
    "Total CV Conv to Usd": [1561120, 6191415, 3727144, 1366531, 1212964, 985321, 875124, 765231, 654876, 543112],
    "Sonar CV Conv Usd": [367928, 356874, 262831, 163046, 114246, 109374, 87423, 75431, 65324, 54211],
    "% Increase in Revenue from Sonar": [
        f"{(367928 / 1561120) * 100:.2f}%",
        f"{(356874 / 6191415) * 100:.2f}%",
        f"{(262831 / 3727144) * 100:.2f}%",
        f"{(163046 / 1366531) * 100:.2f}%",
        f"{(114246 / 1212964) * 100:.2f}%",
        f"{(109374 / 985321) * 100:.2f}%",
        f"{(87423 / 875124) * 100:.2f}%",
        f"{(75431 / 765231) * 100:.2f}%",
        f"{(65324 / 654876) * 100:.2f}%",
        f"{(54211 / 543112) * 100:.2f}%"
    ]
})

# Format 'Total CV Conv to Usd' and 'Sonar CV Conv Usd' columns as dollar amounts
top_shops['Total CV Conv to Usd'] = top_shops['Total CV Conv to Usd'].apply(lambda x: f"${x:,.2f}")
top_shops['Sonar CV Conv Usd'] = top_shops['Sonar CV Conv Usd'].apply(lambda x: f"${x:,.2f}")

# Display the table
st.dataframe(top_shops)

# Case Studies and Value Highlights
st.subheader("How Sonar Drives Results")
st.markdown(
    """
    - **Paw.com**: Increased matched user profiles by 40%, leading to an uplift in triggered flows and a significant increase in revenue.  
      [Read the full case study here](https://www.triplewhale.com/case-studies/paw-com)
    """
)
st.markdown(
    """
    - **Ampersand**: Leveraged Sonar to improve abandoned cart flows, achieving a **25% increase in revenue** from email campaigns.  
      [Read the full case study here](https://www.triplewhale.com/case-studies/ampersand)
    """
)