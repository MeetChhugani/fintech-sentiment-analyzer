import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Page config
st.set_page_config(
    page_title="Fintech Sentiment Analyzer",
    page_icon="📈",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data/financial_news_events.csv')
    df = df.dropna(subset=['Sentiment', 'Index_Change_Percent', 'Headline']).copy()
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# Title
st.title("📈 Fintech Sentiment Analyzer")
st.markdown("**Does financial news sentiment predict market movement?**")
st.markdown("---")

# Sidebar filters
st.sidebar.header("🔍 Filters")
selected_index = st.sidebar.multiselect(
    "Market Index",
    options=df['Market_Index'].unique(),
    default=['NSE Nifty', 'BSE Sensex']
)
selected_sector = st.sidebar.multiselect(
    "Sector",
    options=df['Sector'].unique(),
    default=df['Sector'].unique()
)
selected_impact = st.sidebar.multiselect(
    "Impact Level",
    options=['Low', 'Medium', 'High'],
    default=['Low', 'Medium', 'High']
)

# Filter data
filtered = df[
    (df['Market_Index'].isin(selected_index)) &
    (df['Sector'].isin(selected_sector)) &
    (df['Impact_Level'].isin(selected_impact))
]

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total News", len(filtered))
col2.metric("Negative News", len(filtered[filtered['Sentiment']=='Negative']))
col3.metric("Avg Market Change", f"{filtered['Index_Change_Percent'].mean():.2f}%")
col4.metric("Sectors Covered", filtered['Sector'].nunique())

st.markdown("---")

# Row 1 — two charts
c1, c2 = st.columns(2)

with c1:
    st.subheader("Sentiment Distribution")
    fig1 = px.pie(filtered, names='Sentiment',
              color='Sentiment',
              color_discrete_map={'Positive':'green','Negative':'red','Neutral':'gray'})
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("Avg Market Movement by Sentiment")
    sent_avg = filtered.groupby('Sentiment')['Index_Change_Percent'].mean().reset_index()
    fig2 = px.bar(sent_avg, x='Sentiment', y='Index_Change_Percent',
                  color='Sentiment',
                  color_discrete_map={'Positive':'green','Negative':'red','Neutral':'gray'})
    st.plotly_chart(fig2, use_container_width=True)

# Row 2 — sector chart
st.subheader("Sector-wise Sentiment Distribution")
sector_sent = filtered.groupby(['Sector','Sentiment']).size().reset_index(name='Count')
fig3 = px.bar(sector_sent, x='Sector', y='Count', color='Sentiment',
              barmode='group',
              color_discrete_map={'Positive':'green','Negative':'red','Neutral':'gray'})
fig3.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig3, use_container_width=True)

# Row 3 — negative sector impact
st.subheader("Sectors Most Impacted by Negative News")
neg_df = filtered[filtered['Sentiment']=='Negative']
if len(neg_df) > 0:
    sector_avg = neg_df.groupby('Sector')['Index_Change_Percent'].mean().sort_values().reset_index()
    colors = ['#FF1744' if x < 0 else '#00C853' for x in sector_avg['Index_Change_Percent']]
    fig4, ax = plt.subplots(figsize=(12, 5))
    ax.barh(sector_avg['Sector'], sector_avg['Index_Change_Percent'], color=colors)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.set_title('Avg Market Change During Negative News — By Sector')
    ax.set_xlabel('Avg Index Change (%)')
    plt.tight_layout()
    st.pyplot(fig4)

# Raw data
st.markdown("---")
st.subheader("📋 Raw Data")
st.dataframe(filtered[['Date','Headline','Sentiment','Market_Index','Index_Change_Percent','Sector','Impact_Level']].reset_index(drop=True))

# AI News Analyzer
st.markdown("---")
st.subheader("🤖 AI News Analyzer")
st.markdown("Paste any financial headline — AI will predict sentiment & market impact")

headline_input = st.text_area(
    "Enter Financial Headline",
    placeholder="e.g. RBI raises interest rates by 25 basis points amid inflation concerns"
)

if st.button("Analyze"):
    if not headline_input:
        st.warning("Please enter a headline")
    else:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            st.error("GROQ_API_KEY not found in .env file")
        else:
            with st.spinner("Analyzing..."):
                try:
                    client = Groq(api_key=api_key)

                    prompt = f"""You are a financial analyst expert in Indian and global markets.
Analyze this financial headline and respond in exactly this format:

Headline: {headline_input}

Sentiment: [Positive/Negative/Neutral]
Market Impact: [Up/Down/Neutral]
Sector Affected: [sector name]
Confidence: [High/Medium/Low]
Reasoning: [2-3 lines explaining why]"""

                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=300
                    )

                    result = response.choices[0].message.content

                    st.success("✅ Analysis Complete")
                    st.markdown(result)

                except Exception as e:
                    st.error(f"Error: {str(e)}")