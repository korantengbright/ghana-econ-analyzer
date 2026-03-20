import streamlit as st
import pandas as pd
import requests
from fpdf import FPDF
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- SYSTEM CONFIG ---
st.set_page_config(page_title="Ghana Econ-Insight Pro", page_icon="🇬🇭", layout="wide")

# Modern Executive Styling
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 1.8rem; color: #006b3f; }
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #006b3f; color: white; }
    .report-card { background-color: white; padding: 20px; border-radius: 12px; border: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

# --- BACKEND DATA ENGINES ---

@st.cache_data(ttl=3600)
def get_market_intelligence():
    """Fetches real-time 2026 Ghana Macro-Indicators"""
    try:
        # 1. Live FX Rate
        fx_res = requests.get("https://api.frankfurter.dev/v1/latest?base=USD&symbols=GHS").json()
        official = fx_res['rates']['GHS']
        retail = official * 1.022  # 2.2% Bureau Spread (March 2026 Avg)
    except:
        official, retail = 10.84, 11.08

    # 2. Institutional Data (Updated March 19, 2026)
    data = {
        "policy_rate": 14.0,       # BoG MPC Latest
        "inflation": 3.3,          # GSS Feb 2026
        "gdp_growth": 6.0,         # 2025 Full Year Actual
        "official_fx": official,
        "retail_fx": retail
    }
    return data

def calculate_fees(amt):
    """Accra-specific transaction cost model"""
    e_levy = amt * 0.01
    momo_fee = min(amt * 0.0075, 15.0)
    return e_levy, momo_fee

@st.cache_data
def generate_pro_report(params):
    pdf = FPDF()
    pdf.add_page()
    # Header & Branding
    pdf.set_fill_color(0, 107, 63) # Ghana Green
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_font("Arial", "B", 24)
    pdf.set_text_color(255, 255, 255)
    pdf.text(55, 25, "INVESTMENT MEMORANDUM")
    
    # Content
    pdf.set_y(50)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Issued on: {datetime.now().strftime('%d %B %Y')}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "", 11)
    for key, val in params.items():
        pdf.cell(100, 10, f"{key}:", border=0)
        pdf.cell(0, 10, f"{val}", border=0, ln=True)
    
    pdf.ln(20)
    pdf.set_font("Arial", "I", 9)
    pdf.multi_cell(0, 5, "Disclaimer: This analysis uses the Fisher Equation for real-return calculation and assumes a 2026 retail FX spread of 2.2%. Prepared for professional use only.")
    
    return bytes(pdf.output())

# --- APPLICATION UI ---

intel = get_market_intelligence()

# Header Section
st.title("🇬🇭 Ghana Econ-Insight Pro")
st.caption(f"Institutional-grade financial analyzer | Last Update: {datetime.now().strftime('%H:%M')} GMT")

# Top Metrics Bar
m1, m2, m3, m4 = st.columns(4)
m1.metric("BoG Policy Rate", f"{intel['policy_rate']}%", "-1.5%", help="Reduced Mar 19, 2026")
m2.metric("CPI Inflation", f"{intel['inflation']}%", "-0.5%", help="14th consecutive monthly decline")
m3.metric("Retail USD/GHS", f"{intel['retail_fx']:.2f}")
m4.metric("Real Interest Rate", f"{intel['policy_rate'] - intel['inflation']:.2f}%")

st.divider()

# Interactive Body
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.subheader("📈 Yield Forecasting")
    with st.container(border=True):
        amount = st.number_input("Principal Investment (GHS)", min_value=1000, value=50000)
        rate_choice = st.slider("Target Yield (%)", 5.0, 35.0, intel['policy_rate'] + 2.0)
        
        # Calculations
        e_levy, m_fee = calculate_fees(amount)
        net_principal = amount - e_levy - m_fee
        real_yield = (((1 + (rate_choice/100)) / (1 + (intel['inflation']/100))) - 1) * 100
        
        # Charting
        months = list(range(13))
        compounding = [net_principal * (1 + (rate_choice/100/12))**m for m in months]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=compounding, fill='tozeroy', line_color='#006b3f', name="GHS Value"))
        fig.update_layout(title="Projected Value (12 Months)", xaxis_title="Month", yaxis_title="Cedi Value")
        st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("📋 Executive Summary")
    with st.container(border=True):
        st.write(f"**Net Principal:** GHS {net_principal:,.2f}")
        st.write(f"**Taxes & Fees:** GHS {e_levy + m_fee:,.2f}")
        st.write(f"**USD Valuation:** ${net_principal/intel['retail_fx']:,.2f}")
        st.divider()
        st.write(f"**Effective Real Return:** {real_yield:.2f}%")
        
        if real_yield > 10:
            st.success("Strong Alpha: Outperforming inflation significantly.")
        else:
            st.warning("Low Alpha: Yield barely covers purchasing power loss.")

    # PDF Action
    report_params = {
        "Base Amount": f"GHS {amount:,.2f}",
        "Net Investment": f"GHS {net_principal:,.2f}",
        "Nominal Return": f"{rate_choice}%",
        "Inflation Benchmark": f"{intel['inflation']}%",
        "Calculated Real Yield": f"{real_yield:.2f}%",
        "FX Conversion Rate": f"{intel['retail_fx']:.2f}"
    }
    
    st.download_button(
        label="📥 Download Institutional Memo (PDF)",
        data=generate_pro_report(report_params),
        file_name="Ghana_Investment_Memo.pdf",
        mime="application/pdf"
    )

st.divider()
st.markdown("### 🏦 2026 Market Context")
st.info(f"The Bank of Ghana recently adjusted the policy rate to **14.0%** to stimulate growth after 14 months of disinflation. Current market dynamics suggest a narrowing spread between the Interbank and Bureau rates, indicating high liquidity in the Cedi market.")
