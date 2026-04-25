"""
ACC102 Mini Assignment - Track 4
ESG Explorer: Interactive S&P 500 ESG Dashboard (Fixed Version)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px  
import os

st.set_page_config(page_title="ESG Explorer", layout="wide")
st.title("🌱 ESG Explorer - S&P 500 (Upload Mode)")

st.sidebar.header("📂 Data Source")

use_local_file = st.sidebar.checkbox("Use local 'SP 500 ESG Risk Ratings.csv'", value=True)

df = None 

if use_local_file:
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'SP 500 ESG Risk Ratings.csv')
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, sep=None, engine='python', on_bad_lines='skip')
        st.sidebar.success("Loaded local file successfully.")
    else:
        st.sidebar.error(f"Local file not found: {file_path}")
        st.stop()
else:
    uploaded_file = st.sidebar.file_uploader("Upload ESG CSV/Excel", type=['csv', 'xlsx'])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, sep=None, engine='python', on_bad_lines='skip')
            else:
                df = pd.read_excel(uploaded_file)
            st.sidebar.success("File uploaded successfully!")
        except Exception as e:
            st.sidebar.error(f"Error reading file: {e}")
            st.stop()
    else:
        st.sidebar.warning("Please upload a file to proceed.")
        st.stop()

with st.spinner("Cleaning and processing data..."):
    
    df.columns = df.columns.str.strip().str.lower()

    def find_col(keyword):
        for col in df.columns:
            if keyword in col:
                return col
        return None

    col_map = {
        'symbol': find_col('symbol'),
        'name': find_col('name'),
        'sector': find_col('sector'),
        'esg_total': find_col('total esg'),
        'env_score': find_col('environment'),
        'social_score': find_col('social'),
        'gov_score': find_col('governance'),
        'dividend_yield': find_col('dividend'),
        'roe': find_col('roe')
    }

    col_map = {k: v for k, v in col_map.items() if v is not None}
    df = df.rename(columns={v: k for k, v in col_map.items()})

    required_cols = ['esg_total', 'env_score', 'social_score', 'gov_score']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        st.error(f"❌ Missing required columns: {missing_cols}")
        st.stop()

    clean_cols = ['esg_total', 'env_score', 'social_score', 'gov_score', 'dividend_yield', 'roe']
    for col in clean_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '').str.replace('$', '').str.replace(' ', '')
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].fillna(df[col].median())

    df['sector'] = df['sector'].fillna('Unknown')

    for col in ['esg_total', 'env_score', 'social_score', 'gov_score']:
        industry_avg = df.groupby('sector')[col].transform('mean')
        df[col + '_diff'] = df[col] - industry_avg

    def risk_category(score):
        if score < 10: return 'Negligible'
        elif score < 20: return 'Low'
        elif score < 30: return 'Medium'
        elif score < 40: return 'High'
        else: return 'Severe'

    df['risk_category'] = df['esg_total'].apply(risk_category)

    df['esg_composite'] = (df['gov_score'] * 0.40 + df['env_score'] * 0.35 + df['social_score'] * 0.25)
    df['rank_shift'] = df['esg_total'].rank() - df['esg_composite'].rank()

st.sidebar.header("🔎 Filters")

sectors = sorted(df['sector'].unique())
selected_sectors = st.sidebar.multiselect("Select Sector(s)", sectors, default=sectors)

risk_cats = ['Negligible', 'Low', 'Medium', 'High', 'Severe']
selected_risks = st.sidebar.multiselect("ESG Risk Category", risk_cats, default=risk_cats)

filtered_df = df[
    df['sector'].isin(selected_sectors) &
    df['risk_category'].isin(selected_risks)
]

st.sidebar.subheader("Find a Company")
search_query = st.sidebar.text_input("Enter Company Name or Symbol", "")

if search_query:
    filtered_df = filtered_df[
        filtered_df['name'].str.contains(search_query, case=False, na=False) |
        filtered_df['symbol'].str.contains(search_query, case=False, na=False)
    ]


col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Companies", len(filtered_df))
col2.metric("Avg ESG Score", f"{filtered_df['esg_total'].mean():.1f}")
col3.metric("Avg Env Score", f"{filtered_df['env_score'].mean():.1f}")
col4.metric("Avg Gov Score", f"{filtered_df['gov_score'].mean():.1f}")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📊 Industry Analysis", "🔬 Correlation Matrix", "🏆 Top/Bottom Leaders", "⭐ Custom Model", "📋 Raw Data"]
)

with tab1:
    st.subheader("ESG Score Distribution by Sector")
    fig1 = px.box(filtered_df, x='sector', y='esg_total', color='sector', title="ESG Score Boxplot")
    st.plotly_chart(fig1, use_container_width=True)
    
    st.subheader("Sector Average Breakdown")
    sector_avg = filtered_df.groupby('sector')[['env_score', 'social_score', 'gov_score']].mean().reset_index()
    fig2 = px.bar(sector_avg, x='sector', y=['env_score', 'social_score', 'gov_score'], barmode='group', title="E, S, G Scores by Sector")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("🎯 Sector Comparison Radar (E vs S vs G)")
    radar_data = filtered_df.groupby('sector')[['env_score', 'social_score', 'gov_score']].mean().reset_index()
    radar_df = radar_data.melt(id_vars='sector', var_name='Metric', value_name='Score')
    
    fig_radar = px.line_polar(radar_df, r='Score', theta='Metric', color='sector',
                               line_close=True, template="plotly_dark",
                               title="Average ESG Components by Sector")
    st.plotly_chart(fig_radar, use_container_width=True)


with tab2:
    st.subheader("Correlation Heatmap")
    corr_cols = ['esg_total', 'env_score', 'social_score', 'gov_score', 'roe']
    valid_cols = [c for c in corr_cols if c in filtered_df.columns]
    corr_matrix = filtered_df[valid_cols].corr()
    fig3 = px.imshow(corr_matrix, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r')
    st.plotly_chart(fig3, use_container_width=True)

with tab3:
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("🟢 Top 10 Leaders (Lowest Risk)")
        st.dataframe(filtered_df.nsmallest(10, 'esg_total')[['symbol', 'name', 'sector', 'esg_total']])
    with col_right:
        st.subheader("🔴 Bottom 10 Laggards (Highest Risk)")
        st.dataframe(filtered_df.nlargest(10, 'esg_total')[['symbol', 'name', 'sector', 'esg_total']])

with tab4:
    st.subheader("Custom ESG Composite Score Ranking")
    st.info("Weights: Gov(40%), Env(35%), Social(25%)")
    st.dataframe(filtered_df.nlargest(10, 'esg_composite')[['symbol', 'name', 'esg_composite', 'rank_shift']])

with tab5:
    st.subheader("Filtered Data")
    st.dataframe(filtered_df)
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Filtered CSV", csv, "filtered_esg_data.csv", "text/csv")

st.sidebar.markdown("---")
st.sidebar.info("ACC102 ESG Dashboard v2.2 (Optimized)")
st.sidebar.markdown("---")
st.sidebar.subheader("🤖 AI Disclosure")
st.sidebar.caption("""
This product was developed with the assistance of Google Gemini. 
AI was used for debugging, data cleaning logic, and UI optimization.
Access Date: April 2026.
""")
