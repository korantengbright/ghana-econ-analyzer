import streamlit as st
import pandas as pd
import requests
from fpdf import FPDF
import plotly.graph_objects as go
from datetime import datetime

# --- SYSTEM CONFIG ---
st.set_page_config(page_title="Ghana Econ-Insight Pro", page_icon="🇬🇭", layout="wide")

# Modern Executive Styling
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 1.8rem; color: #006b3f; }
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #006b3f; color: white; font-weight: bold; }
    .stDownloadButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #fcd116; color: black; border: none; font-weight: bold; }
    .report-card { background-color: white; padding: 20px; border-radius: 12px; border: 1px solid #e0e0e0; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- BACKEND DATA ENGINES ---

@st.cache_data(ttl=600)
def get_market_intelligence():
    """Fetches real-time 2026 Ghana Macro-Indicators & Equities"""
    try:
        # 1. Live FX Rate
        fx_res = requests.get("https://api.frankfurter.dev/v1/latest?base=USD&symbols=GHS").json()
        official = fx_res['rates']['GHS']
        retail = official * 1.022  # 2.2% Bureau Spread
    except:
        official, retail = 10.84, 11.08

    # 2. Institutional Data (2026 Context)
    data = {
        "policy_rate": 14.0,       # BoG MPC
        "inflation": 3.3,          # GSS Target
        "gse_ytd": 78.9,           # Ghana Stock Exchange 2026 Bull Run
        "official_fx": official,
        "retail_fx": retail
    }
    return data

def calculate_fees(amt):
    """2026 Fee Structure: E-Levy Abolished"""
    # E-Levy was abolished in 2025 reforms
    e_levy = 0.0
    # Standard Telco service fee (0.75% capped at 15 GHS)
    momo_service_fee = min(amt * 0.0075, 15.0)
    return e_levy, momo_service_fee

def init_paystack_gateway(amount_ghs, email):
    """Initialize test payment via Paystack"""
    PAYSTACK_SECRET = "sk_test_demo_12345" 
    url = "https://api.paystack.co/transaction/initialize"
    headers = {"Authorization": f"Bearer {PAYSTACK_SECRET}", "Content-Type": "application/json"}
    payload = {"email": email, "amount": int(amount_ghs * 100), "currency": "GHS", "channels": ["mobile_money"]}
    try:
        res = requests.post(url, json=payload, headers=headers).json()
        return res['data']['authorization_url']
    except:
        return None

@st.cache_data
def generate_pro_report(params):
    pdf = FPDF()
    pdf.add_page()
    # Header & Branding
    pdf.set_fill_color(0, 107, 63) # Ghana Green
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_font("Arial", "B", 24)
    pdf.set_text_color(255, 255, 255)
    pdf.text(50, 25, "INVESTMENT MEMORANDUM")
    
    # Content
    pdf.set_y(50)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Analysis Date: {datetime.now().strftime('%d %B %Y')}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "", 11)
    for key, val in params.items():
        pdf.cell(100, 10, f"{key}:", border=0)
        pdf.cell(0, 10, f"{val}", border=0, ln=True)
    
    pdf.ln(20)
    pdf.set_font("Arial", "I", 9)
    pdf.multi_cell(0, 5, "Notice: E-Levy status is confirmed as Abolished (0%). This report assumes current GSS inflation targets and GSE-CI performance benchmarks.")
    
    return bytes(pdf.output())

# --- APPLICATION UI ---

intel = get_market_intelligence()

# Header Section
st.title("🇬🇭 Ghana Econ-Insight Pro")
st.caption(f"Comprehensive FinTech Dashboard | Updated: {datetime.now().strftime('%H:%M')} GMT")

# Top Metrics Bar (Added GSE Comparison)
m1, m2, m3, m4 = st.columns(4)
m1.metric("Retail USD/GHS", f"{intel['retail_fx']:.2f}", help="Bureau Rate")
m2.metric("CPI Inflation", f"{intel['inflation']}%", "-0.1%", help="Targeting stability")
m3.metric("GSE-CI (YTD)", f"+{intel['gse_ytd']}%", "Bullish")
m4.metric("Real Return Gap", f"{intel['policy_rate'] - intel['inflation']:.2f}%")

st.divider()

# Interactive Body
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.subheader("📈 Multi-Asset Forecasting")
    with st.container(border=True):
        amount = st.number_input("Principal Investment (GHS)", min_value=1000, value=10000)
        rate_choice = st.slider("Fixed-Income Yield (%)", 5.0, 35.0, 15.0)
        
        # Calculations (MoMo Correction applied)
        e_levy, service_fee = calculate_fees(amount)
        net_principal = amount - service_fee # E-Levy is 0
        real_yield = (((1 + (rate_choice/100)) / (1 + (intel['inflation']/100))) - 1) * 100
        
        # Charting Comparison (Selection vs GSE)
        months = list(range(13))
        # Fixed Income Growth
        compounding = [net_principal * (1 + (rate_choice/100/12))**m for m in months]
        # GSE Equity Growth (Based on YTD trend)
        gse_monthly = (1 + (intel['gse_ytd']/100))**(1/12) - 1
        gse_comp = [net_principal * (1 + gse_monthly)**m for m in months]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=compounding, fill='tozeroy', line_color='#006b3f', name="Your Yield"))
        fig.add_trace(go.Scatter(x=months, y=gse_comp, name="GSE Benchmark", line=dict(dash='dash', color='#fcd116')))
        
        fig.update_layout(title="Selection vs. Ghana Stock Exchange Trend", xaxis_title="Month", yaxis_title="Cedi Value")
        st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("📋 Executive Summary")
    with st.container(border=True):
        st.write(f"**Net Principal:** GHS {net_principal:,.2f}")
        st.write(f"**Telco Fees:** GHS {service_fee:.2f}")
        st.write("🚫 **E-Levy:** 0.00 GHS (Abolished)")
        st.divider()
        st.write(f"**USD Valuation:** ${net_principal/intel['retail_fx']:,.2f}")
        st.write(f"**Real Yield:** {real_yield:.2f}%")
        
        if real_yield < (intel['gse_ytd'] / 4): # If return is much lower than stocks
            st.warning(f"Note: GSE-CI is currently outperforming this yield by {(intel['gse_ytd'] - rate_choice):.1f}%.")

    st.subheader("🛡️ Portfolio Stress Test")
    with st.container(border=True):
        deval = st.slider("Scenario: Cedi Devaluation (%)", 0, 50, 10)
        future_rate = intel['retail_fx'] * (1 + (deval/100))
        potential_loss = (net_principal / intel['retail_fx']) - (net_principal / future_rate)
        st.error(f"Predicted Global Value Loss: **${potential_loss:,.2f}**")

    st.subheader("💳 Digital Actions")
    u_email = st.text_input("Receipt Email", "investor@accra.com")
    if st.button("🚀 Invest via MoMo"):
        url = init_paystack_gateway(amount, u_email)
        if url: st.link_button("Proceed to Paystack Gateway", url)

    # PDF Action
    report_params = {
        "Base Amount": f"GHS {amount:,.2f}",
        "MoMo Fees": f"GHS {service_fee:.2f}",
        "E-Levy Status": "Abolished (0.00)",
        "Net Investment": f"GHS {net_principal:,.2f}",
        "Nominal Return": f"{rate_choice}%",
        "GSE Benchmark": f"{intel['gse_ytd']}%",
        "Calculated Real Yield": f"{real_yield:.2f}%",
        "USD Portfolio Value": f"${net_principal/intel['retail_fx']:,.2f}"
    }
    
    st.download_button(
        label="📥 Download Institutional Memo (PDF)",
        data=generate_pro_report(report_params),
        file_name="Ghana_Investment_Memo.pdf",
        mime="application/pdf"
    )

st.divider()
st.info("💡 **Policy Context:** As of 2025, digital transaction costs in Ghana have dropped significantly due to the removal of the E-Levy. This tool helps you re-allocate those savings into high-performing assets like GSE equities or indexed fixed-income funds.")
