# 📈 Fintech Sentiment Analyzer

[![Streamlit App](https://static.streamlit.io/badge_hosted_sec_auto_light.svg)](https://fintech-sentiment-analyzer-7emjz5hnngnyfjwvmn4p3o.streamlit.app/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Groq LLaMA 3.3](https://img.shields.io/badge/AI-LLaMA%203.3%2070B-orange.svg?logo=meta&logoColor=white)](https://groq.com/)
[![Plotly](https://img.shields.io/badge/Visualization-Plotly-purple.svg?logo=plotly&logoColor=white)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Does financial news sentiment predict market movement?** An interactive, AI-powered analytics dashboard that correlates 3,000+ financial headlines with index price changes across Indian and global markets (NSE Nifty, BSE Sensex, and 16 other indices).

---

## 💎 Premium UI Overhaul

The dashboard features a **state-of-the-art glassmorphic design** built for professional trading environments:
- 🌌 **Midnight Cyber Theme:** A customized radial background gradient and Outfit/Space Grotesk typography inspired by institutional trading terminals.
- 🧪 **Glassmorphism UI Components:** Card panels styled with native backdrop blurs, delicate glowing borders, and reactive hover animations.
- ⚡ **Dynamic Indicator Cards:** Glowing status-based KPI blocks for real-time market averages and article counts.
- 📊 **Next-Gen Visualizations:** Plots rendered using responsive, dark-theme Plotly visualizations replacing standard static plots.

---

## 🚀 Features

- **Sentiment Distribution & Donut Charting** — Multi-class breakdown of Positive, Negative, and Neutral financial headlines.
- **Average Market Index Reaction** — Analyzes the percentage index changes correlated directly to the prevailing sentiment of published articles.
- **Sector-wise Multi-Group Analysis** — Grouped bar charts charting sentiment counts across individual industry sectors.
- **Negative Sentiment Damage Report** — A custom-colored damage chart displaying average index losses per sector during negative news events.
- **Interactive Multi-Filters** — Instantly filter all data models by Market Index, Sector, and News Impact Level.
- **🤖 Real-time AI News Console** — Paste any raw headline to predict sentiment, market impact, and target sector with reasoning, powered by **LLaMA 3.3 70B via the Groq API**.

---

## 📊 Key Findings from EDA

- 🏢 **Real Estate** is the most vulnerable sector during bad news, exhibiting an average index return of **-0.99%**.
- 🚗 **Automotive & Aerospace** show the most resilience, frequently maintaining positive index yields even on days with negative sentiment.
- 📈 **NSE Nifty & BSE Sensex** exhibit "sell the rumor, buy the news" behavior—often showing positive median gains on negative sentiment days, indicating preemptive pricing.
- 📉 **Impact Level Disconnect** — High-impact news alerts do not always match the largest historical index standard deviations, highlighting the noise-to-signal ratio in financial media.

---

## 📁 Project Structure

```text
fintech-sentiment-analyzer/
├── app/
│   └── app.py                     # Streamlit dashboard & UI Styles
├── data/
│   ├── financial_news_events.csv  # News sentiment dataset
│   ├── financial_news_events.json
│   └── financial_news_events.xlsx
├── notebooks/
│   └── 01_eda_analysis.ipynb      # EDA and Jupyter notebooks
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 🛠️ Setup & Local Execution

### 1. Clone & Navigate
```bash
git clone https://github.com/MeetChhugani/fintech-sentiment-analyzer.git
cd fintech-sentiment-analyzer
```

### 2. Configure Virtual Environment
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the Streamlit Dashboard
```bash
streamlit run app/app.py
```

---

## 👤 Author

**Meet Chhugani**  
*B.Tech IT — Data Science | Gyanmanjari Innovative University*  
- GitHub: [@MeetChhugani](https://github.com/MeetChhugani)
- LinkedIn: [Meet Chhugani](https://linkedin.com/in/meet-chhugani)
