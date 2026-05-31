# 📈 Fintech Sentiment Analyzer

> Does financial news sentiment predict market movement?

A data analysis dashboard that explores the relationship between financial news sentiment and market index movements across global and Indian markets (NSE Nifty & BSE Sensex).

🔗 **Live Demo:** [fintech-sentiment-analyzer.streamlit.app](https://fintech-sentiment-analyzer-7emjz5hnngnyfjwvmn4p3o.streamlit.app/)

---

## 🚀 Features

- **Sentiment Distribution Analysis** — Breakdown of Positive, Negative, and Neutral news across 3,000+ financial headlines
- **Market Movement Correlation** — How sentiment impacts average index change across 18 global indices
- **Sector-wise Analysis** — Which sectors are most affected by negative news
- **India Focus** — Dedicated analysis for NSE Nifty & BSE Sensex
- **Interactive Filters** — Filter by Market Index, Sector, and Impact Level
- **🤖 AI News Analyzer** — Paste any financial headline and get instant sentiment prediction, market impact, and reasoning powered by LLaMA 3.3 70B via Groq

---

## 🛠️ Tech Stack

| Tool | Usage |
|------|-------|
| Python | Core language |
| Pandas | Data manipulation |
| Plotly & Seaborn | Visualizations |
| Streamlit | Dashboard deployment |
| Groq + LLaMA 3.3 70B | AI headline analysis |

---

## 📊 Key Findings

- **Real Estate** is the most negatively impacted sector during bad news (-0.99% avg change)
- **Automotive & Aerospace** show resilience — positive market movement even during negative news
- **NSE Nifty** exhibits "sell the rumor, buy the news" behavior — negative sentiment days show positive median returns
- High impact news does not always correlate with larger market moves

---

## 📁 Project Structure
fintech-sentiment-analyzer/
├── app/
│   └── app.py          # Streamlit dashboard
├── data/
│   └── financial_news_events.csv
├── notebooks/
│   └── 01_eda_analysis.ipynb
└── requirements.txt

---

## 👤 Author

**Meet Chhugani**  
B.Tech IT — Data Science | Gyanmanjari Innovative University  
[GitHub](https://github.com/MeetChhugani)
