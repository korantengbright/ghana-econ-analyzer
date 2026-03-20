# 🇬🇭 Ghana Econ-Insight: Real-Time Investment & Macro Analyzer

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)
![Framework: Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)

**Ghana Econ-Insight** is a specialized financial tool designed for the Ghanaian market. It bridges the gap between raw macroeconomic data and personal investment strategy by providing real-time "Real Rate of Return" calculations, currency hedge analysis, and professional PDF reporting.

[🚀 View Live App](https://YOUR-APP-LINK.streamlit.app)

---

## 🌟 Key Features

- **Automated Macro Ingestion:** Scrapes the latest National Consumer Price Index (CPI) and Inflation data directly from the Bank of Ghana (BoG) bulletins.
- **Live FX Tracking:** Real-time GHS/USD exchange rate monitoring via the Frankfurter API.
- **Real Return Calculator:** Uses the Fisher Equation logic to calculate actual wealth growth after accounting for Ghana's unique inflationary environment.
- **Professional PDF Export:** Generates an instant, formatted investment memo for personal or client use.
- **Cached Performance:** Uses `@st.cache_data` to ensure fast loading times even when institutional websites are slow.

---

## 📊 Why This Matters (The Economic Context)
In a high-inflation environment like Ghana's, nominal interest rates (like a 15-20% T-Bill) are misleading. This tool provides the **Real Interest Rate**, which is the only metric that truly measures purchasing power growth.

---

## 🛠️ Tech Stack & Skills Demonstrated

- **Language:** Python 3.10+
- **Data Engineering:** `BeautifulSoup4` (Web Scraping), `Tabula-py` (PDF Table Extraction), `Requests` (API Integration).
- **Statistics & Analysis:** `Pandas`, `NumPy`, `Statsmodels`.
- **Visualization:** `Plotly Express` (Interactive Time-Series).
- **Web Deployment:** `Streamlit`.

---

## 🚀 Getting Started

### Prerequisites
- Python installed locally
- Java Runtime Environment (Required for `tabula-py` to read PDFs)

### Local Installation
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/ghana-econ-analyzer.git](https://github.com/YOUR_USERNAME/ghana-econ-analyzer.git)
   cd ghana-econ-analyzer
