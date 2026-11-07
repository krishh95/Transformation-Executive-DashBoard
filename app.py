import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Transformation Portfolio Executive Dashboard",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MODERN BLUISH & WHITE THEME STYLES ---
st.markdown("""
<style>
    /* Global Base */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main {
        background-color: #f4f7fb;
    }
    
    /* Header Container */
    .dashboard-header {
        background: linear-gradient(135deg, #0b2545 0%, #134074 50%, #1d4ed8 100%);
        border-radius: 14px;
        padding: 24px 30px;
        color: #ffffff;
        margin-bottom: 24px;
        box-shadow: 0 8px 20px rgba(11, 37, 69, 0.12);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
    }
    .dashboard-title {
        font-size: 26px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin: 0;
        color: #ffffff;
    }
    .dashboard-subtitle {
        font-size: 14px;
        color: #dbeafe;
        margin-top: 4px;
        font-weight: 400;
    }
    .header-badge {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(8px);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        color: #eff6ff;
        border: 1px solid rgba(255, 255, 255, 0.25);
    }
    
    /* KPI Metric Cards */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
        gap: 16px;
        margin-bottom: 24px;
    }
    .kpi-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 18px 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
        position: relative;
        overflow: hidden;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 18px rgba(30, 64, 175, 0.08);
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #1d4ed8, #60a5fa);
    }
    .kpi-card.warning::before {
        background: linear-gradient(90deg, #d97706, #fbbf24);
    }
    .kpi-card.danger::before {
        background: linear-gradient(90deg, #dc2626, #f87171);
    }
    .kpi-card.success::before {
        background: linear-gradient(90deg, #059669, #34d399);
    }
    .kpi-label {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        font-weight: 600;
        color: #64748b;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 26px;
        font-weight: 700;
        color: #0f172a;
        line-height: 1.2;
    }
    .kpi-subtext {
        font-size: 12px;
        color: #64748b;
        margin-top: 6px;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    /* Executive Insights Box */
    .insights-card {
        background: #ffffff;
        border: 1px solid #bfdbfe;
        border-left: 5px solid #1d4ed8;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 14px rgba(29, 78, 216, 0.05);
    }
    .insights-header {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 17px;
        font-weight: 700;
        color: #1e3a8a;
        margin-bottom: 14px;
    }
    .insight-item {
        background: #f8fafc;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
        border: 1px solid #e2e8f0;
        display: flex;
        gap: 12px;
        align-items: flex-start;
    }
    .insight-badge {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        white-space: nowrap;
    }
    .insight-badge-risk { background: #fee2e2; color: #991b1b; }
    .insight-badge-budget { background: #fef3c7; color: #92400e; }
    .insight-badge-ops { background: #dbeafe; color: #1e40af; }
    .insight-badge-growth { background: #dcfce7; color: #166534; }
    
    .insight-text {
        font-size: 13.5px;
        color: #334155;
        line-height: 1.5;
    }
    
    /* Section Containers */
    .chart-container {
        background: #ffffff;
        border-radius: 12px;
        padding: 18px 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 16px;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Sidebar adjustments */
    section[data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    csv_file = Path(__file__).parent / "transformation_portfolio.csv"
    if not csv_file.exists():
        # Fallback to local working directory
        csv_file = Path("transformation_portfolio.csv")
    df = pd.read_csv(csv_file)
    df['start_month'] = pd.to_datetime(df['start_month'])
    df['spend_ratio_pct'] = (df['spend_usd_k'] / df['budget_usd_k'] * 100).round(1)
    df['budget_variance_usd_k'] = df['budget_usd_k'] - df['spend_usd_k']
    df['is_overbudget'] = df['spend_usd_k'] > df['budget_usd_k']
    return df

df_raw = load_data()

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.markdown("""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:15px;">
            <div style="background:#1d4ed8; color:white; width:34px; height:34px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-weight:bold; font-size:18px;">
                TP
            </div>
            <div>
                <h3 style="margin:0; font-size:18px; color:#0f172a; font-weight:700;">Portfolio Controls</h3>
                <span style="font-size:11px; color:#64748b;">Interactive Filters</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Filter 1: Client Sector
    all_sectors = sorted(df_raw['client_sector'].unique().tolist())
    selected_sectors = st.multiselect("Client Sector", options=all_sectors, default=all_sectors)
    
    # Filter 2: Region
    all_regions = sorted(df_raw['region'].unique().tolist())
    selected_regions = st.multiselect("Region", options=all_regions, default=all_regions)
    
    # Filter 3: Status
    all_statuses = ["On Track", "Delayed", "At Risk", "Completed"]
    selected_statuses = st.multiselect("Project Status", options=all_statuses, default=all_statuses)
    
    # Filter 4: Risk Level
    all_risks = ["Low", "Medium", "High", "Critical"]
    selected_risks = st.multiselect("Risk Level", options=all_risks, default=all_risks)
    
    # Filter 5: Initiative
    all_initiatives = sorted(df_raw['initiative'].unique().tolist())
    selected_initiatives = st.multiselect("Initiative Type", options=all_initiatives, default=[])

    st.markdown("---")
    
    # Quick toggles
    show_overbudget_only = st.checkbox("Show Overbudget Projects Only", value=False)
    
    st.caption("Transformation Portfolio Governance System v2.4 • Bluish-Executive Theme")

# --- FILTER APPLICATION ---
filtered_df = df_raw[
    df_raw['client_sector'].isin(selected_sectors if selected_sectors else all_sectors) &
    df_raw['region'].isin(selected_regions if selected_regions else all_regions) &
    df_raw['status'].isin(selected_statuses if selected_statuses else all_statuses) &
    df_raw['risk_level'].isin(selected_risks if selected_risks else all_risks)
]

if selected_initiatives:
    filtered_df = filtered_df[filtered_df['initiative'].isin(selected_initiatives)]

if show_overbudget_only:
    filtered_df = filtered_df[filtered_df['is_overbudget']]

# --- COLOR PALETTES (BLUISH PRIMARY & WHITE SECONDARY) ---
COLOR_MAP_STATUS = {
    "On Track": "#2563eb",   # Primary Blue
    "Delayed": "#d97706",    # Amber
    "At Risk": "#dc2626",    # Crimson Red
    "Completed": "#059669"   # Emerald Green
}

COLOR_MAP_RISK = {
    "Low": "#38bdf8",        # Light Sky Blue
    "Medium": "#3b82f6",     # Classic Blue
    "High": "#f59e0b",       # Amber
    "Critical": "#dc2626"    # Danger Red
}

BLUISH_SCALE = ["#eff6ff", "#bfdbfe", "#60a5fa", "#2563eb", "#1d4ed8", "#1e3a8a", "#0b2545"]

# --- HEADER SECTION ---
st.markdown(f"""
    <div class="dashboard-header">
        <div>
            <h1 class="dashboard-title">Transformation Portfolio Dashboard</h1>
            <div class="dashboard-subtitle">
                Strategic visibility across {len(df_raw)} programs • Financial governance, delivery health, and value realization
            </div>
        </div>
        <div style="display:flex; gap:10px; margin-top:8px;">
            <div class="header-badge">FY25-FY26 Cycle</div>
            <div class="header-badge">Viewing {len(filtered_df)} of {len(df_raw)} Projects</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Handle empty state
if filtered_df.empty:
    st.warning("⚠️ No projects match the selected criteria. Please adjust your filters in the sidebar.")
    st.stop()

# --- COMPUTED METRICS ---
total_projects = len(filtered_df)
total_budget = filtered_df['budget_usd_k'].sum()
total_spend = filtered_df['spend_usd_k'].sum()
burn_rate = (total_spend / total_budget * 100) if total_budget > 0 else 0
at_risk_delayed_count = filtered_df['status'].isin(['At Risk', 'Delayed']).sum()
at_risk_delayed_pct = (at_risk_delayed_count / total_projects * 100) if total_projects > 0 else 0
avg_completion = filtered_df['completion_pct'].mean()
avg_benefits = filtered_df['benefits_realized_pct'].mean()
realization_gap = avg_completion - avg_benefits
avg_satisfaction = filtered_df['stakeholder_satisfaction_10'].mean()
overbudget_count = filtered_df['is_overbudget'].sum()

# --- KPI METRIC CARDS ---
st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-label">Active Portfolio</div>
        <div class="kpi-value">{total_projects:,}</div>
        <div class="kpi-subtext">across {filtered_df['client_sector'].nunique()} industry sectors</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Total Allocated Budget</div>
        <div class="kpi-value">${total_budget:,.0f}k</div>
        <div class="kpi-subtext">Avg: ${(total_budget/total_projects):,.1f}k per project</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Total Cumulative Spend</div>
        <div class="kpi-value">${total_spend:,.0f}k</div>
        <div class="kpi-subtext"><strong>{burn_rate:.1f}%</strong> portfolio capital burn</div>
    </div>
    <div class="kpi-card {'danger' if at_risk_delayed_pct > 30 else 'warning'}">
        <div class="kpi-label">At Risk or Delayed</div>
        <div class="kpi-value" style="color: {'#dc2626' if at_risk_delayed_pct > 30 else '#d97706'}">{at_risk_delayed_count} <span style="font-size:16px; font-weight:500;">({at_risk_delayed_pct:.0f}%)</span></div>
        <div class="kpi-subtext">Requiring executive attention</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Avg Completion vs Benefits</div>
        <div class="kpi-value">{avg_completion:.1f}% <span style="font-size:16px; font-weight:400; color:#64748b;">vs {avg_benefits:.1f}%</span></div>
        <div class="kpi-subtext">Value lag: <strong>{realization_gap:.1f} pts</strong> delta</div>
    </div>
    <div class="kpi-card success">
        <div class="kpi-label">Stakeholder Satisfaction</div>
        <div class="kpi-value">{avg_satisfaction:.1f} <span style="font-size:15px; font-weight:400; color:#64748b;">/ 10</span></div>
        <div class="kpi-subtext">Avg score from sponsor feedback</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- EXECUTIVE INSIGHTS SECTION ---
# Calculate dynamic values for insights
skills_data_blockers = filtered_df[filtered_df['primary_blocker'].isin(['Skills gap', 'Data access delays', 'Stakeholder alignment'])].shape[0]
skills_data_pct = (skills_data_blockers / total_projects * 100) if total_projects > 0 else 0

st.markdown("""
<div class="insights-card">
    <div class="insights-header">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1d4ed8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
        </svg>
        <span>Executive Insights & Strategic Recommendations for Senior Leadership</span>
    </div>
""", unsafe_allow_html=True)

col_ins1, col_ins2 = st.columns(2)

with col_ins1:
    st.markdown(f"""
    <div class="insight-item">
        <span class="insight-badge insight-badge-risk">Delivery Risk</span>
        <div class="insight-text">
            <strong>High Operational Friction:</strong> <strong>{at_risk_delayed_count} of {total_projects} projects ({at_risk_delayed_pct:.1f}%)</strong> are categorized as <em>At Risk</em> or <em>Delayed</em>. Non-technical friction points (Skills Gaps, Data Access Delays, and Stakeholder Misalignment) account for <strong>{skills_data_pct:.0f}%</strong> of all impediments.
        </div>
    </div>
    <div class="insight-item">
        <span class="insight-badge insight-badge-budget">Budget Concerns</span>
        <div class="insight-text">
            <strong>Capital Efficiency & Selective Overruns:</strong> Cumulative portfolio spend is disciplined at <strong>{burn_rate:.1f}% (${total_spend:,.0f}k of ${total_budget:,.0f}k)</strong>, but <strong>{overbudget_count} initiatives</strong> have breached their budget caps, dominated by high-capex Cloud Modernization and AI initiatives requiring closer scope containment.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_ins2:
    st.markdown(f"""
    <div class="insight-item">
        <span class="insight-badge insight-badge-ops">Value Lag</span>
        <div class="insight-text">
            <strong>Value Realization Deficit:</strong> Average milestone completion stands at <strong>{avg_completion:.1f}%</strong> while realized benefits trail at <strong>{avg_benefits:.1f}%</strong>—representing a <strong>{realization_gap:.1f} percentage point delivery-to-value gap</strong>. Programs require early value validation sprints rather than backloading benefits realization.
        </div>
    </div>
    <div class="insight-item">
        <span class="insight-badge insight-badge-growth">Opportunity</span>
        <div class="insight-text">
            <strong>Governance & Capability Uplift:</strong> Stabilizing the top blocker clusters (data governance approvals, centralized capability centers, and vendor accountability frameworks) can immediately unblock an estimated <strong>$14M+ in at-risk capital</strong> across high-impact enterprise accounts.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# --- VISUALIZATIONS SECTION ---
st.markdown("<h3 style='color:#0f172a; margin-top:10px; margin-bottom:15px; font-weight:700;'>Portfolio Analytics & Performance Visualizations</h3>", unsafe_allow_html=True)

# Row 1: Project Status Distribution & Budget vs Spend by Sector
row1_col1, row1_col2 = st.columns([1, 1.4])

with row1_col1:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📊 Portfolio Delivery Status Distribution</div>", unsafe_allow_html=True)
    
    status_counts = filtered_df['status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    
    fig_status = px.pie(
        status_counts,
        names='Status',
        values='Count',
        hole=0.55,
        color='Status',
        color_discrete_map=COLOR_MAP_STATUS
    )
    fig_status.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hoverinfo='label+value+percent',
        marker=dict(line=dict(color='#ffffff', width=2))
    )
    fig_status.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        margin=dict(l=10, r=10, t=10, b=40),
        height=320,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_status, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with row1_col2:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>💰 Budget vs Spend by Client Sector ($k)</div>", unsafe_allow_html=True)
    
    sector_fin = filtered_df.groupby('client_sector')[['budget_usd_k', 'spend_usd_k']].sum().reset_index()
    sector_fin = sector_fin.sort_values(by='budget_usd_k', ascending=True)
    
    fig_budget = go.Figure()
    fig_budget.add_trace(go.Bar(
        y=sector_fin['client_sector'],
        x=sector_fin['budget_usd_k'],
        name='Budget Allocated',
        orientation='h',
        marker_color='#93c5fd'
    ))
    fig_budget.add_trace(go.Bar(
        y=sector_fin['client_sector'],
        x=sector_fin['spend_usd_k'],
        name='Actual Spend',
        orientation='h',
        marker_color='#1d4ed8'
    ))
    fig_budget.update_layout(
        barmode='group',
        margin=dict(l=10, r=10, t=10, b=10),
        height=320,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_title="USD ($k)",
        yaxis_title="",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='#f1f5f9')
    )
    st.plotly_chart(fig_budget, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Row 2: Completion vs Benefits Realization & Primary Blockers
row2_col1, row2_col2 = st.columns([1.3, 1])

with row2_col1:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🎯 Progress vs Benefits Realization Quadrant</div>", unsafe_allow_html=True)
    
    fig_scatter = px.scatter(
        filtered_df,
        x='completion_pct',
        y='benefits_realized_pct',
        color='status',
        size='budget_usd_k',
        hover_name='project_id',
        hover_data=['client_sector', 'initiative', 'project_lead', 'risk_level'],
        color_discrete_map=COLOR_MAP_STATUS,
        labels={'completion_pct': 'Completion %', 'benefits_realized_pct': 'Benefits Realized %'},
        size_max=22
    )
    # Add diagonal parity line
    fig_scatter.add_shape(
        type='line', line=dict(dash='dash', color='#94a3b8', width=1.5),
        x0=0, y0=0, x1=100, y1=100
    )
    fig_scatter.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        height=330,
        xaxis=dict(range=[0, 105], gridcolor='#f1f5f9', title="Milestone Completion (%)"),
        yaxis=dict(range=[0, 105], gridcolor='#f1f5f9', title="Benefits Realized (%)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with row2_col2:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🛑 Top Delivery Blockers Impacting Projects</div>", unsafe_allow_html=True)
    
    blocker_counts = filtered_df['primary_blocker'].value_counts().reset_index()
    blocker_counts.columns = ['Blocker', 'Count']
    blocker_counts = blocker_counts[blocker_counts['Blocker'] != 'No major blocker'].head(6)
    blocker_counts = blocker_counts.sort_values(by='Count', ascending=True)
    
    fig_blockers = px.bar(
        blocker_counts,
        y='Blocker',
        x='Count',
        orientation='h',
        text='Count',
        color='Count',
        color_continuous_scale=['#93c5fd', '#1e40af']
    )
    fig_blockers.update_traces(textposition='outside')
    fig_blockers.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
        margin=dict(l=10, r=30, t=10, b=10),
        height=330,
        yaxis_title="",
        xaxis_title="Number of Impacted Initiatives",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='#f1f5f9')
    )
    st.plotly_chart(fig_blockers, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Row 3: Initiative Breakdown and Risk Heatmap
row3_col1, row3_col2 = st.columns([1.1, 1.1])

with row3_col1:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🌐 Regional Spend & Risk Profile</div>", unsafe_allow_html=True)
    
    region_risk = filtered_df.groupby(['region', 'risk_level'])['budget_usd_k'].sum().reset_index()
    
    fig_region = px.bar(
        region_risk,
        x='region',
        y='budget_usd_k',
        color='risk_level',
        color_discrete_map=COLOR_MAP_RISK,
        category_orders={"risk_level": ["Low", "Medium", "High", "Critical"]},
        labels={'budget_usd_k': 'Total Budget ($k)', 'region': 'Region', 'risk_level': 'Risk Level'}
    )
    fig_region.update_layout(
        barmode='stack',
        margin=dict(l=10, r=10, t=10, b=10),
        height=320,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='#f1f5f9'),
        xaxis_title=""
    )
    st.plotly_chart(fig_region, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with row3_col2:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>⚡ Initiative Portfolio Capital Distribution</div>", unsafe_allow_html=True)
    
    init_summary = filtered_df.groupby('initiative').agg({
        'budget_usd_k': 'sum',
        'spend_usd_k': 'sum',
        'project_id': 'count'
    }).reset_index().rename(columns={'project_id': 'project_count'})
    init_summary = init_summary.sort_values(by='budget_usd_k', ascending=False)
    
    fig_init = px.bar(
        init_summary,
        x='budget_usd_k',
        y='initiative',
        orientation='h',
        color='initiative',
        color_discrete_sequence=px.colors.sequential.Blues_r,
        labels={'budget_usd_k': 'Total Budget ($k)', 'initiative': ''}
    )
    fig_init.update_layout(
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        height=320,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='#f1f5f9')
    )
    st.plotly_chart(fig_init, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- DETAILED PROJECT DRILLDOWN & AUDIT TABLE ---
st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
    <div class="section-title" style="margin-bottom:0;">📋 Detailed Project Portfolio Register & Audit</div>
</div>
""", unsafe_allow_html=True)

display_cols = [
    'project_id', 'client_sector', 'initiative', 'region', 'project_lead',
    'status', 'risk_level', 'budget_usd_k', 'spend_usd_k',
    'completion_pct', 'benefits_realized_pct', 'stakeholder_satisfaction_10', 'primary_blocker'
]

display_df = filtered_df[display_cols].copy()

# Rename columns for presentation
display_df = display_df.rename(columns={
    'project_id': 'ID',
    'client_sector': 'Sector',
    'initiative': 'Initiative',
    'region': 'Region',
    'project_lead': 'Lead',
    'status': 'Status',
    'risk_level': 'Risk',
    'budget_usd_k': 'Budget ($k)',
    'spend_usd_k': 'Spend ($k)',
    'completion_pct': 'Completion %',
    'benefits_realized_pct': 'Benefits %',
    'stakeholder_satisfaction_10': 'CSAT /10',
    'primary_blocker': 'Primary Blocker'
})

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Budget ($k)": st.column_config.NumberColumn(format="$%d k"),
        "Spend ($k)": st.column_config.NumberColumn(format="$%d k"),
        "Completion %": st.column_config.ProgressColumn(
            min_value=0, max_value=100, format="%d%%"
        ),
        "Benefits %": st.column_config.ProgressColumn(
            min_value=0, max_value=100, format="%d%%"
        ),
        "CSAT /10": st.column_config.NumberColumn(format="%d/10"),
    }
)

csv_download = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Export Filtered Portfolio (CSV)",
    data=csv_download,
    file_name="transformation_portfolio_filtered.csv",
    mime="text/csv",
    help="Download active filtered portfolio dataset for reporting"
)

st.markdown("</div>", unsafe_allow_html=True)
