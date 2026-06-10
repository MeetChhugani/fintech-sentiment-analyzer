import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# --- Page Config ---
st.set_page_config(
    page_title="Fintech Sentiment Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Inject Premium Custom CSS & Fonts ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    /* Apply Font */
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Outfit', 'Space Grotesk', sans-serif !important;
        color: #E2E8F0 !important;
    }
    
    /* Background Gradient */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #0A0F1D 0%, #03050A 100%) !important;
    }
    
    /* Hide Default Header & Footer Decoration */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Block container styling */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1300px !important;
    }
    
    /* Custom Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #05070C !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    /* Glassmorphic Header Card with Animated Radial Glow */
    .header-card {
        background: linear-gradient(135deg, rgba(13, 20, 38, 0.45) 0%, rgba(6, 9, 19, 0.3) 100%);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 24px;
        padding: 35px 25px;
        text-align: center;
        backdrop-filter: blur(25px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.08);
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
    }
    
    .header-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(0, 242, 254, 0.06) 0%, transparent 60%);
        pointer-events: none;
    }
    
    .header-card h1 {
        font-size: 3.2rem;
        font-weight: 800;
        margin: 0 0 10px 0;
        background: linear-gradient(90deg, #00F2FE 0%, #4FACFE 50%, #8A2387 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1.5px;
    }
    
    .header-card p {
        font-size: 1.25rem;
        color: #94A3B8;
        margin: 0;
        font-weight: 400;
    }
    
    /* Styled Section Subheaders */
    .section-header {
        background: linear-gradient(90deg, rgba(0, 242, 254, 0.1) 0%, rgba(0, 242, 254, 0) 100%);
        border-left: 4px solid #00F2FE;
        padding: 10px 20px;
        border-radius: 0 12px 12px 0;
        margin: 28px 0 18px 0;
        font-weight: 700;
        font-size: 1.35rem;
        color: #F1F5F9;
        letter-spacing: -0.5px;
    }
    
    /* Custom Glass Cards with Hover Scale & Glowing borders */
    .glass-card {
        background: rgba(8, 12, 24, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 24px;
        backdrop-filter: blur(20px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.03);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-card:hover {
        border-color: rgba(0, 242, 254, 0.2);
        box-shadow: 0 15px 35px rgba(0, 242, 254, 0.08);
    }
    
    /* Custom CSS styled Inputs & Dropdowns */
    div[data-baseweb="select"], div[data-baseweb="input"], input, textarea {
        background-color: rgba(4, 6, 12, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        color: #F8FAFC !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-baseweb="select"]:hover, div[data-baseweb="input"]:hover, input:hover, textarea:hover {
        border-color: rgba(0, 242, 254, 0.4) !important;
        background-color: rgba(8, 12, 24, 0.95) !important;
        box-shadow: 0 0 12px rgba(0, 242, 254, 0.15) !important;
    }
    
    /* Predict Button Override */
    div.stButton > button {
        background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%) !important;
        color: #03050A !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        border: none !important;
        padding: 12px 28px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 18px rgba(0, 242, 254, 0.25) !important;
        letter-spacing: -0.2px;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 24px rgba(0, 242, 254, 0.4) !important;
        background: linear-gradient(135deg, #00E676 0%, #00F2FE 100%) !important;
    }

    /* Custom KPI Card Styling */
    .kpi-card {
        background: rgba(8, 12, 24, 0.55);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-top: 4px solid #4FACFE;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3), inset 0 1px 1px rgba(255, 255, 255, 0.02);
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(0, 242, 254, 0.06);
    }
    
    .kpi-card-positive {
        border-top: 4px solid #10B981;
    }
    
    .kpi-card-negative {
        border-top: 4px solid #F43F5E;
    }
    
    .kpi-card-neutral {
        border-top: 4px solid #64748B;
    }
    
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 4px;
        letter-spacing: -1px;
    }
    
    .kpi-label {
        font-size: 0.85rem;
        color: #94A3B8;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 1px;
    }

    /* AI Analysis Console */
    .ai-results-card {
        background: rgba(8, 12, 24, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.45);
        margin-top: 20px;
    }
    
    .ai-badge {
        display: inline-block;
        padding: 6px 14px;
        font-size: 0.85rem;
        font-weight: 700;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-right: 8px;
        margin-bottom: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    .badge-positive {
        background-color: rgba(16, 185, 129, 0.15);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .badge-negative {
        background-color: rgba(244, 63, 94, 0.15);
        color: #F43F5E;
        border: 1px solid rgba(244, 63, 94, 0.3);
    }
    
    .badge-neutral {
        background-color: rgba(100, 116, 139, 0.15);
        color: #94A3B8;
        border: 1px solid rgba(100, 116, 139, 0.3);
    }
    
    .badge-impact-up {
        background-color: rgba(16, 185, 129, 0.15);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .badge-impact-down {
        background-color: rgba(244, 63, 94, 0.15);
        color: #F43F5E;
        border: 1px solid rgba(244, 63, 94, 0.3);
    }
    
    .badge-confidence-high {
        background-color: rgba(16, 185, 129, 0.15);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .badge-confidence-medium {
        background-color: rgba(245, 158, 11, 0.15);
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    
    .badge-confidence-low {
        background-color: rgba(239, 68, 68, 0.15);
        color: #EF4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    .ai-reasoning-box {
        background-color: rgba(4, 6, 12, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 16px;
        margin-top: 15px;
        color: #CBD5E1;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv('data/financial_news_events.csv')
    df = df.dropna(subset=['Sentiment', 'Index_Change_Percent', 'Headline']).copy()
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# --- Title Header ---
st.markdown("""
    <div class='header-card'>
        <h1>📈 Fintech Sentiment Analyzer</h1>
        <p>Does financial news sentiment predict market movement? AI-powered Sentiment Extraction &amp; Market Impact Correlation</p>
    </div>
""", unsafe_allow_html=True)

# --- Sidebar Filters ---
st.sidebar.markdown("<div class='section-header' style='margin-top: 0;'>🔍 Filters</div>", unsafe_allow_html=True)

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

# Filter data based on selections
filtered = df[
    (df['Market_Index'].isin(selected_index)) &
    (df['Sector'].isin(selected_sector)) &
    (df['Impact_Level'].isin(selected_impact))
]

# --- KPI Metric Cards ---
total_articles = len(filtered)
neg_articles = len(filtered[filtered['Sentiment']=='Negative'])
avg_change = filtered['Index_Change_Percent'].mean()
sectors_covered = filtered['Sector'].nunique()

avg_change_str = f"{avg_change:+.2f}%" if not pd.isna(avg_change) else "0.00%"
avg_change_class = "kpi-card-positive" if avg_change > 0 else ("kpi-card-negative" if avg_change < 0 else "kpi-card-neutral")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
        <div class="kpi-card kpi-card-neutral">
            <div class="kpi-value">{total_articles:,}</div>
            <div class="kpi-label">Total Articles</div>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
        <div class="kpi-card kpi-card-negative">
            <div class="kpi-value">{neg_articles:,}</div>
            <div class="kpi-label">Negative News</div>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
        <div class="kpi-card {avg_change_class}">
            <div class="kpi-value">{avg_change_str}</div>
            <div class="kpi-label">Avg Index Change</div>
        </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
        <div class="kpi-card kpi-card-neutral" style="border-top-color: #8A2387;">
            <div class="kpi-value">{sectors_covered}</div>
            <div class="kpi-label">Sectors Covered</div>
        </div>
    """, unsafe_allow_html=True)

# --- Row 1: Charts & Distribution ---
st.markdown("<div class='section-header'>📊 Sentiment &amp; Index Correlation Metrics</div>", unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0; color:#F8FAFC; font-weight:600; font-size:1.15rem; margin-bottom:15px;'>Sentiment Distribution</h4>", unsafe_allow_html=True)
    
    fig1 = px.pie(
        filtered, 
        names='Sentiment',
        color='Sentiment',
        color_discrete_map={'Positive': '#10B981', 'Negative': '#F43F5E', 'Neutral': '#64748B'},
        hole=0.4
    )
    fig1.update_traces(
        textinfo='percent+label',
        marker=dict(line=dict(color='#080C18', width=2))
    )
    fig1.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Outfit, sans-serif", color="#E2E8F0"),
        margin=dict(t=10, b=10, l=10, r=10),
        showlegend=False
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0; color:#F8FAFC; font-weight:600; font-size:1.15rem; margin-bottom:15px;'>Avg Market Movement by Sentiment</h4>", unsafe_allow_html=True)
    
    sent_avg = filtered.groupby('Sentiment')['Index_Change_Percent'].mean().reset_index()
    fig2 = px.bar(
        sent_avg, 
        x='Sentiment', 
        y='Index_Change_Percent',
        color='Sentiment',
        color_discrete_map={'Positive': '#10B981', 'Negative': '#F43F5E', 'Neutral': '#64748B'}
    )
    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Outfit, sans-serif", color="#E2E8F0"),
        margin=dict(t=20, b=20, l=20, r=20),
        xaxis=dict(showgrid=False, title_text=""),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title_text="Avg Index Change (%)")
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Row 2: Sector-wise Sentiment Distribution ---
st.markdown("<div class='section-header'>🏢 Sector-wise Sentiment Analysis</div>", unsafe_allow_html=True)
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

sector_sent = filtered.groupby(['Sector','Sentiment']).size().reset_index(name='Count')
fig3 = px.bar(
    sector_sent, 
    x='Sector', 
    y='Count', 
    color='Sentiment',
    barmode='group',
    color_discrete_map={'Positive': '#10B981', 'Negative': '#F43F5E', 'Neutral': '#64748B'}
)
fig3.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Outfit, sans-serif", color="#E2E8F0"),
    margin=dict(t=20, b=30, l=20, r=20),
    xaxis=dict(showgrid=False, tickangle=-45, title_text=""),
    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title_text="Count")
)
st.plotly_chart(fig3, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- Row 3: Sectors Most Impacted by Negative News ---
neg_df = filtered[filtered['Sentiment']=='Negative']
if len(neg_df) > 0:
    st.markdown("<div class='section-header'>⚠️ Sector Damage Report (Negative Sentiment Impact)</div>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    
    sector_avg = neg_df.groupby('Sector')['Index_Change_Percent'].mean().sort_values(ascending=True).reset_index()
    
    # Map colors based on index change value
    sector_avg['Color'] = sector_avg['Index_Change_Percent'].apply(lambda x: '#F43F5E' if x < 0 else '#10B981')
    
    fig4 = px.bar(
        sector_avg,
        y='Sector',
        x='Index_Change_Percent',
        orientation='h',
        color='Color',
        color_discrete_map={'#F43F5E': '#F43F5E', '#10B981': '#10B981'}
    )
    fig4.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Outfit, sans-serif", color="#E2E8F0"),
        margin=dict(t=10, b=20, l=20, r=20),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title_text="Avg Index Change (%)"),
        yaxis=dict(showgrid=False, title_text=""),
        showlegend=False
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Row 4: Raw Data Event Logs ---
st.markdown("<div class='section-header'>📋 Verified Financial Event Logs</div>", unsafe_allow_html=True)
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.dataframe(
    filtered[['Date','Headline','Sentiment','Market_Index','Index_Change_Percent','Sector','Impact_Level']].reset_index(drop=True),
    use_container_width=True
)
st.markdown("</div>", unsafe_allow_html=True)

# --- Row 5: AI News Analyzer Console ---
st.markdown("<div class='section-header'>🤖 Real-time AI Sentiment Analyzer Console</div>", unsafe_allow_html=True)
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.markdown("<p style='color: #94A3B8; font-size: 0.95rem; margin-bottom: 20px;'>Input a financial headline or market alert to predict sentiment, market direction, and sector impact using LLaMA-3.3-70B.</p>", unsafe_allow_html=True)

headline_input = st.text_area(
    "Enter Financial Headline",
    placeholder="e.g. RBI raises interest rates by 25 basis points amid inflation concerns",
    height=80,
    label_visibility="collapsed"
)

analyze_clicked = st.button("⚡ Execute AI Analysis", use_container_width=True)

if analyze_clicked:
    if not headline_input:
        st.warning("⚠️ Please enter a headline to analyze.")
    else:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            st.error("❌ GROQ_API_KEY not found in environment or .env file.")
        else:
            with st.spinner("🤖 Simulating market dynamics and processing sentiment analysis..."):
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

                    # Parse output using regular expressions for structured layout
                    sentiment_match = re.search(r"Sentiment:\s*\*?\[?([A-Za-z]+)\]?.*?$", result, re.MULTILINE | re.IGNORECASE)
                    impact_match = re.search(r"Market Impact:\s*\*?\[?([A-Za-z]+)\]?.*?$", result, re.MULTILINE | re.IGNORECASE)
                    sector_match = re.search(r"Sector Affected:\s*\*?\[?([^\n\]\*]+)\]?.*?$", result, re.MULTILINE | re.IGNORECASE)
                    confidence_match = re.search(r"Confidence:\s*\*?\[?([A-Za-z]+)\]?.*?$", result, re.MULTILINE | re.IGNORECASE)
                    reasoning_match = re.search(r"Reasoning:\s*\*?\[?([\s\S]+)", result, re.MULTILINE | re.IGNORECASE)

                    sentiment = sentiment_match.group(1).strip() if sentiment_match else "Neutral"
                    impact = impact_match.group(1).strip() if impact_match else "Neutral"
                    sector = sector_match.group(1).strip() if sector_match else "General / Macro"
                    confidence = confidence_match.group(1).strip() if confidence_match else "Medium"
                    
                    reasoning = reasoning_match.group(1).strip() if reasoning_match else result
                    # Clean up trailing markdown brackets or characters
                    reasoning = re.sub(r"^\]", "", reasoning).strip()

                    # Select badge styling classes
                    sent_class = "badge-positive" if sentiment.lower() == "positive" else ("badge-negative" if sentiment.lower() == "negative" else "badge-neutral")
                    impact_class = "badge-impact-up" if impact.lower() in ["up", "positive"] else ("badge-impact-down" if impact.lower() in ["down", "negative"] else "badge-neutral")
                    conf_class = "badge-confidence-high" if confidence.lower() == "high" else ("badge-confidence-medium" if confidence.lower() == "medium" else "badge-confidence-low")

                    st.markdown(f"""
                        <div class="ai-results-card">
                            <h4 style="margin-top:0; color:#F8FAFC; font-weight:600; font-size:1.15rem; margin-bottom:15px;">📊 AI Sentiment Verdict</h4>
                            <div style="margin-bottom:12px;">
                                <span class="ai-badge {sent_class}">Sentiment: {sentiment}</span>
                                <span class="ai-badge {impact_class}">Market Impact: {impact}</span>
                                <span class="ai-badge {conf_class}">Confidence: {confidence}</span>
                            </div>
                            <div style="font-size:0.95rem; color:#E2E8F0; margin-top:10px; margin-bottom: 15px;">
                                <strong>Sector Affected:</strong> <span style="color:#00F2FE; font-weight:600;">{sector}</span>
                            </div>
                            <div class="ai-reasoning-box">
                                <strong style="color: #F8FAFC;">Analyst Reasoning:</strong><br>
                                {reasoning}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"❌ Groq API Error: {str(e)}")

st.markdown("</div>", unsafe_allow_html=True)