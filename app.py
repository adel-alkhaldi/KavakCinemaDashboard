import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- PAGE CONFIGURATION & CUSTOM CSS ---
st.set_page_config(page_title="Cinema Recovery Plan", layout="wide", page_icon="🎬")

# Injecting CSS for stylization
st.markdown("""
<style>
    :root {
        --ink: #0f1117;
        --teal: #1a7a6e;
        --gold: #e8a020;
        --accent: #c8401b;
        --paper: #f7f6f2;
    }
    .report-header {
        background-color: #0f1117;
        color: white;
        padding: 40px 50px;
        border-radius: 8px;
        margin-bottom: 0px;
    }
    .eyebrow {
        font-family: 'Courier New', monospace;
        font-size: 12px;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #1a7a6e;
        margin-bottom: 10px;
    }
    .report-title {
        font-size: 38px;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 10px;
    }
    .report-subtitle {
        font-size: 16px;
        color: #aaa9a4;
        margin-bottom: 20px;
    }
    .alert-banner {
        background-color: #c8401b;
        color: white;
        padding: 12px 50px;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.04em;
        border-radius: 4px;
        margin-top: 10px;
        margin-bottom: 30px;
    }
    .section-label {
        font-family: 'Courier New', monospace;
        font-size: 11px;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #c8401b;
        margin-bottom: 0px;
        margin-top: 40px;
    }
    .section-title {
        font-size: 26px;
        font-weight: 700;
        border-bottom: 2px solid #dddbd4;
        padding-bottom: 10px;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)


# --- DATA LOADING & PREPARATION ---
@st.cache_data
def load_data():
    file_path = 'Business Case Data My Analysis.xlsx'
    df = pd.read_excel(file_path, sheet_name='Original Data')
    
    MONTHS_MULTIPLIER = 4.345238
    
    # Calculate Monthly Derived Metrics
    df['Monthly Customers'] = df['Weekly Customers'] * MONTHS_MULTIPLIER
    df['Monthly Popcorn Sales'] = df['Weekly Popcorn Sales'] * MONTHS_MULTIPLIER
    df['Monthly Soda Sales'] = df['Weekly Soda Sales'] * MONTHS_MULTIPLIER
    df['Monthly Food Sales'] = df['Weekly Food Sales'] * MONTHS_MULTIPLIER
    
    df['Monthly Ticket Profit'] = df['Monthly Customers'] * df['Profit per Ticket']
    df['Monthly Popcorn Profit'] = df['Monthly Popcorn Sales'] * df['Profit per Popcorn']
    df['Monthly Soda Profit'] = df['Monthly Soda Sales'] * df['Profit per Soda']
    df['Monthly Food Profit'] = df['Monthly Food Sales'] * df['Profit per Food']
    
    df['Total Profit'] = df['Monthly Ticket Profit'] + df['Monthly Popcorn Profit'] + df['Monthly Soda Profit'] + df['Monthly Food Profit']
    df['Quarter'] = np.ceil(df['Month'] / 3).astype(int)
    
    return df

df = load_data()

# Global Baseline Metrics
BASELINE_PROFIT = df['Total Profit'].sum()
TOTAL_CUSTOMERS = df['Monthly Customers'].sum()
ORIG_POPCORN_SALES = df['Monthly Popcorn Sales'].sum()
ORIG_SODA_SALES = df['Monthly Soda Sales'].sum()
ORIG_FOOD_SALES = df['Monthly Food Sales'].sum()

PROFIT_TICKET = df['Profit per Ticket'].iloc[0]
PROFIT_POPCORN = df['Profit per Popcorn'].iloc[0]
PROFIT_SODA = df['Profit per Soda'].iloc[0]
PROFIT_FOOD = df['Profit per Food'].iloc[0]

# --- SIDEBAR: INTERACTIVE LEVERS ---
st.sidebar.title("🎛️ Execution Levers")
st.sidebar.markdown("Adjust the variables to model the +20% recovery target.")

target_rate = st.sidebar.slider("🎯 Target Profit Growth Rate", min_value=0.0, max_value=0.50, value=0.20, step=0.01, format="%.2f")

st.sidebar.markdown("---")
st.sidebar.subheader("1. Combo Promotions")
combo_discount = st.sidebar.slider("Combo Discount Rate", min_value=0.0, max_value=0.30, value=0.12, step=0.01, format="%.2f")
combo_adoption = st.sidebar.slider("Combo Adoption Rate", min_value=0.0, max_value=1.00, value=0.75, step=0.01, format="%.2f")

st.sidebar.markdown("---")
st.sidebar.subheader("2. Delivery App Integration")
delivery_increase = st.sidebar.slider("F&B Delivery Boost", min_value=0.0, max_value=1.00, value=0.25, step=0.01, format="%.2f")

st.sidebar.markdown("---")
st.sidebar.subheader("3. Food Quality Control")
new_food_rate = st.sidebar.slider("New Hot Food Purchase Rate", min_value=0.0, max_value=1.00, value=0.25, step=0.01, format="%.2f")

st.sidebar.markdown("---")
st.sidebar.subheader("4. Operational Savings")
op_efficiency_rate = st.sidebar.slider("Efficiency Savings (% Profit)", min_value=0.0, max_value=0.20, value=0.075, step=0.005, format="%.3f")


# --- HEADER & ALERT BANNER ---
st.markdown("""
<div class="report-header">
    <p class="eyebrow">Kavak Business Case, Interactive Report</p>
    <h1 class="report-title">Cinema Performance Analysis<br>& Recovery Plan</h1>
    <p class="report-subtitle">A data-driven strategy to achieve +20% revenue growth & operational excellence.</p>
</div>
<div class="alert-banner">
    • PROBLEM STATEMENT: Mall Management Requires a 20% Additional Profits Margin to Continue Operations</div>
""", unsafe_allow_html=True)


# --- PHASE 1: EXECUTIVE SUMMARY ---
st.markdown('<p class="section-label">Section 01</p><h2 class="section-title">Executive Summary — KPI Dashboard</h2>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Baseline Annual Profit", f"${BASELINE_PROFIT:,.0f}")
c2.metric("Target Profit (+20%)", f"${BASELINE_PROFIT * 1.2:,.0f}")
c3.metric("Average CSAT", "4.3 / 10", "-7 months below 5.0")
c4.metric("Hot Food Attach Rate", "15.5%", "-Compared to 55% Popcorn")

st.info("**Bottom Line:** The cinema generates 501K annually but is operating below potential. The ~$100K gap is strictly achievable through a combination of operational flow improvements, quality control, and targeted F&B upselling.")


# --- PHASE 2: DATA EXPLORATION ---
st.markdown('<p class="section-label">Section 02</p><h2 class="section-title">Data Exploration: Trends & Correlations</h2>', unsafe_allow_html=True)

tab_profits, tab_corr = st.tabs(["Profitability Trends", "Variable Correlation (Kendall's Tau)"])

with tab_profits:
    col1, col2 = st.columns(2)
    with col1:
        fig_monthly = px.line(df, x='Month', y='Total Profit', markers=True, title="Monthly Profit Trend", color_discrete_sequence=['#1a7a6e'])
        fig_monthly.update_layout(yaxis_title="Total Profit ($)", xaxis=dict(tickmode='linear', tick0=1, dtick=1))
        st.plotly_chart(fig_monthly, use_container_width=True)
    with col2:
        q_profit = df.groupby('Quarter')['Total Profit'].sum().reset_index()
        fig_quarterly = px.bar(q_profit, x='Quarter', y='Total Profit', text_auto='.2s', title="Quarterly Aggregation", color_discrete_sequence=['#f0f0f0'])
        st.plotly_chart(fig_quarterly, use_container_width=True)

with tab_corr:
    cols_to_corr = ['Weekly Customers', 'Weekly Popcorn Sales', 'Weekly Soda Sales', 'Weekly Food Sales', 'Waiting Time', 'CSAT', 'Room Occupancy']
    corr_matrix = df[cols_to_corr].corr(method='kendall')
    fig_corr = px.imshow(corr_matrix, text_auto=".2f", aspect="auto", color_continuous_scale='RdBu_r', title="Kendall's Tau Correlation")
    st.plotly_chart(fig_corr, use_container_width=True)
    st.success("**Key Insight:** Occupancy highly correlates to sales, but wait time has an unexpected positive correlation with CSAT. This led us to investigate *what* is actually driving CSAT down in Phase 3.")


# --- PHASE 3: DISCOVERY & ROOT CAUSE ---
st.markdown('<p class="section-label">Section 03</p><h2 class="section-title">Discovery: Diagnosing Underperformance</h2>', unsafe_allow_html=True)

tab_food, tab_csat, tab_ops = st.tabs(["The Low F&B Sales Issue", "CSAT & Detractors", "Operational Inefficiency"])

with tab_food:
    st.subheader("Identified Issue: Low Purchase Rate of F&B Products")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        item_profits = {
            'Ticket': df['Monthly Ticket Profit'].sum(),
            'Popcorn': df['Monthly Popcorn Profit'].sum(),
            'Soda': df['Monthly Soda Profit'].sum(),
            'Hot Food': df['Monthly Food Profit'].sum()
        }
        fig_pie = px.pie(names=list(item_profits.keys()), values=list(item_profits.values()), title="Baseline Profit Distribution", hole=0.4,
                         color_discrete_sequence=['#f0f0f0', '#1a7a6e', '#e8a020', '#c8401b'])
        st.plotly_chart(fig_pie, use_container_width=True)
    with col_f2:
        purchase_rates = {
            'Popcorn': ORIG_POPCORN_SALES / TOTAL_CUSTOMERS,
            'Soda': ORIG_SODA_SALES / TOTAL_CUSTOMERS,
            'Hot Food': ORIG_FOOD_SALES / TOTAL_CUSTOMERS
        }
        fig_bar = px.bar(x=list(purchase_rates.keys()), y=list(purchase_rates.values()), text_auto='.1%', 
                         title="Item Purchase Rate per Customer", color_discrete_sequence=['#1a7a6e'])
        fig_bar.update_layout(yaxis=dict(tickformat=".0%"), xaxis_title="Item", yaxis_title="Purchase Rate")
        st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown("**Solutions Proposed:**\n1. Create F&B Combo Offers.\n2. Make Food available standalone via Delivery Apps (e.g., Talabat - Vox Cinema Case Study).")

with tab_csat:
    st.subheader("Identified Issue: Cinema Hygiene & Food Quality")
    csat_detractors = df.groupby('Main Detractors')['CSAT'].mean().reset_index()
    fig_csat = px.bar(csat_detractors, x='Main Detractors', y='CSAT', text_auto='.1f', title="Average CSAT by Main Detractor",
                      color='Main Detractors', color_discrete_sequence=['#e8a020', '#c8401b', '#5a5a6a', '#1a7a6e'])
    st.plotly_chart(fig_csat, use_container_width=True)
    st.warning("**The Root Cause:** Customers are forgiving of wait times (Avg CSAT 7.3), but severely punish the cinema for bad Food Quality (Avg CSAT 2.25). This explains the abysmal 15.5% hot food purchase rate. **Solution:** Implement strict Quality Control.")

with tab_ops:
    st.subheader("Identified Issue: Static Employee Count & Training Inefficiency")
    fig_ops = make_subplots(specs=[[{"secondary_y": True}]])
    fig_ops.add_trace(go.Bar(x=df['Month'], y=df['Weekly Customers'], name="Weekly Customers", marker_color='#f0f0f0'), secondary_y=False)
    fig_ops.add_trace(go.Scatter(x=df['Month'], y=df['Waiting Time'], name="Waiting Time (mins)", mode='lines+markers', marker_color='#c8401b'), secondary_y=True)
    fig_ops.update_layout(title_text="Operational Mismatch: Customers vs. Wait Time", xaxis_title="Month", xaxis=dict(tickmode='linear', tick0=1, dtick=1))
    fig_ops.update_yaxes(title_text="Customers", secondary_y=False)
    fig_ops.update_yaxes(title_text="Wait Time (Mins)", secondary_y=True)
    st.plotly_chart(fig_ops, use_container_width=True)
    
    st.error("**Data Evidence:** Month 12 has the highest customer count but the lowest wait time (7 mins). Month 5 has low customer demand but the highest wait time (25 mins).")
    st.markdown("**Solution:** Because FTEs are statically set to 15 year-round, we suffer redundancy and inefficiency. We will provide training and adapt flexible scheduling based on demand to map 7.5% operational savings.")


# --- PHASE 4: ACHIEVING TARGET ---
st.markdown('<p class="section-label">Section 04</p><h2 class="section-title">Recovery Plan: Achieving Target</h2>', unsafe_allow_html=True)

# Mathematical Execution Logic
target_profit = BASELINE_PROFIT * (1 + target_rate)

# Init 1: Combo Promotion
combo_price_orig = PROFIT_TICKET + PROFIT_POPCORN + PROFIT_SODA
combo_price_new = combo_price_orig * (1 - combo_discount)
promo_customers = TOTAL_CUSTOMERS * combo_adoption
ticket_only_customers = TOTAL_CUSTOMERS * (1 - combo_adoption)

new_profit_promo = promo_customers * combo_price_new
new_profit_tickets_only = ticket_only_customers * PROFIT_TICKET

# Init 2: Delivery App Boost
profit_deliv_popcorn = (ORIG_POPCORN_SALES * delivery_increase) * PROFIT_POPCORN
profit_deliv_soda = (ORIG_SODA_SALES * delivery_increase) * PROFIT_SODA
profit_deliv_food = (ORIG_FOOD_SALES * delivery_increase) * PROFIT_FOOD
total_init_2_profit = profit_deliv_popcorn + profit_deliv_soda + profit_deliv_food

# Init 3: Food Quality Control
new_food_sales = TOTAL_CUSTOMERS * new_food_rate
total_init_3_profit = new_food_sales * PROFIT_FOOD

# Init 4: Operational Efficiencies
init_4_delta = BASELINE_PROFIT * op_efficiency_rate

# Totals
total_achieved_profit = new_profit_promo + new_profit_tickets_only + total_init_2_profit + total_init_3_profit + init_4_delta
gap = total_achieved_profit - target_profit

c1, c2, c3 = st.columns(3)
c1.metric("Baseline Profit", f"${BASELINE_PROFIT:,.0f}")
c2.metric("Target Goal", f"${target_profit:,.0f}")
c3.metric("Projected with Initiatives", f"${total_achieved_profit:,.0f}", delta=f"${total_achieved_profit - target_profit:,.0f} Above Target")

st.markdown("<br>", unsafe_allow_html=True)

# 2 Comparative Bar Charts as requested
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    baseline_categories = ['Tickets', 'Popcorn', 'Soda', 'Hot Food']
    baseline_values = [item_profits['Ticket'], item_profits['Popcorn'], item_profits['Soda'], item_profits['Hot Food']]
    
    fig_base = px.bar(x=baseline_categories, y=baseline_values, text_auto='.2s', 
                      title="1. Baseline Profit Breakdown", 
                      color=baseline_categories, 
                      color_discrete_sequence=['#f0f0f0', '#1a7a6e', '#e8a020', '#c8401b'])
    fig_base.update_layout(xaxis_title="Category", yaxis_title="Total Profit ($)", showlegend=False)
    st.plotly_chart(fig_base, use_container_width=True)

with col_chart2:
    projected_categories = ['Tickets (Standalone)', 'Combos (Tkt+Pop+Soda)', 'Talabat App Delivery', 'In-Cinema Hot Food', 'Operational Savings']
    projected_values = [new_profit_tickets_only, new_profit_promo, total_init_2_profit, total_init_3_profit, init_4_delta]
    
    fig_proj = px.bar(x=projected_categories, y=projected_values, text_auto='.2s', 
                      title="2. Projected Profit With Initiatives", 
                      color=projected_categories,
                      color_discrete_sequence=['#f0f0f0', '#1a7a6e', '#e8a020', '#c8401b', '#5a5a6a'])
    fig_proj.update_layout(xaxis_title="Initiative Source", yaxis_title="Total Profit ($)", showlegend=False)
    st.plotly_chart(fig_proj, use_container_width=True)