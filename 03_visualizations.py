"""
Marketing Funnel Visualizations
Author: Marketing Analytics Project
Description: Create comprehensive visualizations for funnel analysis and attribution
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
sns.set_palette("husl")

# Load data
print("Loading data for visualizations...")
df = pd.read_csv('marketing_funnel_data.csv', parse_dates=['landing_timestamp'])
channel_metrics = pd.read_csv('channel_performance_metrics.csv')
roi_metrics = pd.read_csv('channel_roi_metrics.csv')
cohort_data = pd.read_csv('cohort_analysis.csv')

print(f"✓ Data loaded successfully")

# ============================================================================
# 1. INTERACTIVE FUNNEL FLOW VISUALIZATION (Plotly)
# ============================================================================

print("\nCreating interactive funnel visualizations...")

# Calculate funnel metrics
stages = {
    'Landing Page': df['stage_1_landing'].sum(),
    'Sign Up': df['stage_2_signup'].sum(),
    'Product View': df['stage_3_product_view'].sum(),
    'Add to Cart': df['stage_4_add_to_cart'].sum(),
    'Purchase': df['stage_5_purchase'].sum()
}

stage_names = list(stages.keys())
stage_values = list(stages.values())

# Create interactive funnel
fig_funnel = go.Figure(go.Funnel(
    y=stage_names,
    x=stage_values,
    textposition="inside",
    textinfo="value+percent initial",
    opacity=0.85,
    marker={
        "color": ["#3498db", "#2ecc71", "#f39c12", "#e74c3c", "#9b59b6"],
        "line": {"width": 2, "color": "white"}
    },
    connector={"line": {"color": "royalblue", "width": 3}}
))

fig_funnel.update_layout(
    title={
        'text': "Marketing Funnel: Stage-by-Stage Conversion Flow",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 20, 'color': '#2c3e50'}
    },
    height=600,
    font=dict(size=14),
    paper_bgcolor='#f8f9fa',
    plot_bgcolor='#ffffff'
)

fig_funnel.write_html('funnel_visualization.html')
print("✓ Created: funnel_visualization.html")

# ============================================================================
# 2. CHANNEL PERFORMANCE COMPARISON
# ============================================================================

# Create multi-metric channel comparison
fig_channel = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Conversion Rate by Channel', 'Revenue by Channel',
                    'Sessions by Channel', 'Revenue per User by Channel'),
    specs=[[{'type': 'bar'}, {'type': 'bar'}],
           [{'type': 'bar'}, {'type': 'bar'}]]
)

# Sort by conversion rate
channel_sorted = channel_metrics.sort_values('Conversion Rate', ascending=True)

# Conversion Rate
fig_channel.add_trace(
    go.Bar(
        y=channel_sorted['Channel'],
        x=channel_sorted['Conversion Rate'],
        orientation='h',
        marker_color='#3498db',
        text=[f"{x:.2f}%" for x in channel_sorted['Conversion Rate']],
        textposition='outside',
        name='Conversion Rate'
    ),
    row=1, col=1
)

# Revenue
fig_channel.add_trace(
    go.Bar(
        y=channel_sorted['Channel'],
        x=channel_sorted['Revenue'],
        orientation='h',
        marker_color='#2ecc71',
        text=[f"${x:,.0f}" for x in channel_sorted['Revenue']],
        textposition='outside',
        name='Revenue'
    ),
    row=1, col=2
)

# Sessions
fig_channel.add_trace(
    go.Bar(
        y=channel_sorted['Channel'],
        x=channel_sorted['Sessions'],
        orientation='h',
        marker_color='#f39c12',
        text=[f"{x:,}" for x in channel_sorted['Sessions']],
        textposition='outside',
        name='Sessions'
    ),
    row=2, col=1
)

# Revenue per User
fig_channel.add_trace(
    go.Bar(
        y=channel_sorted['Channel'],
        x=channel_sorted['Revenue/User'],
        orientation='h',
        marker_color='#9b59b6',
        text=[f"${x:.2f}" for x in channel_sorted['Revenue/User']],
        textposition='outside',
        name='Revenue/User'
    ),
    row=2, col=2
)

fig_channel.update_layout(
    title_text="Channel Performance Dashboard",
    title_x=0.5,
    title_font_size=20,
    showlegend=False,
    height=800,
    paper_bgcolor='#f8f9fa'
)

fig_channel.update_xaxes(showgrid=True, gridcolor='#e0e0e0')
fig_channel.update_yaxes(showgrid=False)

fig_channel.write_html('channel_performance_dashboard.html')
print("✓ Created: channel_performance_dashboard.html")

# ============================================================================
# 3. DEVICE PERFORMANCE HEATMAP
# ============================================================================

# Create channel x device performance matrix
channel_device = df.groupby(['channel', 'device']).agg({
    'user_id': 'count',
    'stage_5_purchase': 'sum'
}).reset_index()

channel_device['Conversion_Rate'] = (channel_device['stage_5_purchase'] / 
                                      channel_device['user_id']) * 100

# Pivot for heatmap
heatmap_data = channel_device.pivot(index='channel', columns='device', 
                                      values='Conversion_Rate')

fig_heatmap = go.Figure(data=go.Heatmap(
    z=heatmap_data.values,
    x=heatmap_data.columns,
    y=heatmap_data.index,
    colorscale='RdYlGn',
    text=np.round(heatmap_data.values, 2),
    texttemplate='%{text}%',
    textfont={"size": 14},
    colorbar=dict(title="Conv Rate %")
))

fig_heatmap.update_layout(
    title={
        'text': "Conversion Rate Heatmap: Channel x Device",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 18}
    },
    xaxis_title="Device Type",
    yaxis_title="Marketing Channel",
    height=500,
    font=dict(size=12),
    paper_bgcolor='#f8f9fa'
)

fig_heatmap.write_html('channel_device_heatmap.html')
print("✓ Created: channel_device_heatmap.html")

# ============================================================================
# 4. COHORT RETENTION ANALYSIS
# ============================================================================

# Sort cohorts by month
cohort_data['cohort_month'] = pd.to_datetime(cohort_data['cohort_month'])
cohort_sorted = cohort_data.sort_values('cohort_month')

fig_cohort = make_subplots(
    rows=2, cols=1,
    subplot_titles=('Conversion Rate Trend Over Time', 
                    'Revenue per User Trend Over Time'),
    vertical_spacing=0.15
)

# Conversion rate trend
fig_cohort.add_trace(
    go.Scatter(
        x=cohort_sorted['cohort_month'],
        y=cohort_sorted['Conversion_Rate'],
        mode='lines+markers',
        name='Conversion Rate',
        line=dict(color='#3498db', width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(52, 152, 219, 0.2)'
    ),
    row=1, col=1
)

# Revenue per user trend
fig_cohort.add_trace(
    go.Scatter(
        x=cohort_sorted['cohort_month'],
        y=cohort_sorted['Revenue_Per_User'],
        mode='lines+markers',
        name='Revenue/User',
        line=dict(color='#2ecc71', width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(46, 204, 113, 0.2)'
    ),
    row=2, col=1
)

fig_cohort.update_xaxes(title_text="Month", row=2, col=1)
fig_cohort.update_yaxes(title_text="Conversion Rate (%)", row=1, col=1)
fig_cohort.update_yaxes(title_text="Revenue per User ($)", row=2, col=1)

fig_cohort.update_layout(
    title_text="Cohort Performance Analysis",
    title_x=0.5,
    title_font_size=20,
    showlegend=True,
    height=800,
    paper_bgcolor='#f8f9fa'
)

fig_cohort.write_html('cohort_trends.html')
print("✓ Created: cohort_trends.html")

# ============================================================================
# 5. ROI/ROAS BUBBLE CHART
# ============================================================================

fig_roi = go.Figure()

fig_roi.add_trace(go.Scatter(
    x=roi_metrics['Spend'],
    y=roi_metrics['Revenue'],
    mode='markers+text',
    marker=dict(
        size=roi_metrics['ROAS'] * 20,  # Size by ROAS
        color=roi_metrics['ROI'],  # Color by ROI
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title="ROI %"),
        line=dict(width=2, color='white')
    ),
    text=roi_metrics['Channel'],
    textposition='top center',
    textfont=dict(size=10, color='black'),
    name='Channels'
))

# Add diagonal line (break-even)
max_val = max(roi_metrics['Spend'].max(), roi_metrics['Revenue'].max())
fig_roi.add_trace(go.Scatter(
    x=[0, max_val],
    y=[0, max_val],
    mode='lines',
    line=dict(color='red', width=2, dash='dash'),
    name='Break-even Line',
    showlegend=True
))

fig_roi.update_layout(
    title={
        'text': "Channel ROI Analysis: Spend vs Revenue<br><sub>Bubble size = ROAS | Color = ROI %</sub>",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 18}
    },
    xaxis_title="Total Spend ($)",
    yaxis_title="Revenue Generated ($)",
    height=600,
    font=dict(size=12),
    paper_bgcolor='#f8f9fa',
    hovermode='closest'
)

fig_roi.write_html('roi_bubble_chart.html')
print("✓ Created: roi_bubble_chart.html")

# ============================================================================
# 6. DROP-OFF ANALYSIS VISUALIZATION
# ============================================================================

# Calculate drop-off rates
drop_offs = []
stage_counts = [
    df['stage_1_landing'].sum(),
    df['stage_2_signup'].sum(),
    df['stage_3_product_view'].sum(),
    df['stage_4_add_to_cart'].sum(),
    df['stage_5_purchase'].sum()
]

stage_labels = ['Landing', 'Signup', 'Product View', 'Add to Cart', 'Purchase']

for i in range(len(stage_counts) - 1):
    users_lost = stage_counts[i] - stage_counts[i+1]
    drop_off_pct = (users_lost / stage_counts[i]) * 100
    drop_offs.append({
        'Stage': f"{stage_labels[i]} → {stage_labels[i+1]}",
        'Users Lost': users_lost,
        'Drop-off %': drop_off_pct
    })

drop_off_df = pd.DataFrame(drop_offs)

fig_dropoff = go.Figure()

fig_dropoff.add_trace(go.Bar(
    x=drop_off_df['Stage'],
    y=drop_off_df['Drop-off %'],
    marker_color=['#3498db', '#2ecc71', '#f39c12', '#e74c3c'],
    text=[f"{x:.1f}%" for x in drop_off_df['Drop-off %']],
    textposition='outside',
    name='Drop-off Rate'
))

fig_dropoff.update_layout(
    title={
        'text': "Drop-off Rate Analysis: Where Are We Losing Users?",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 18}
    },
    xaxis_title="Funnel Stage Transition",
    yaxis_title="Drop-off Rate (%)",
    height=500,
    font=dict(size=12),
    paper_bgcolor='#f8f9fa',
    showlegend=False
)

# Add annotation for highest drop-off
max_dropoff_idx = drop_off_df['Drop-off %'].idxmax()
max_dropoff = drop_off_df.iloc[max_dropoff_idx]

fig_dropoff.add_annotation(
    x=max_dropoff['Stage'],
    y=max_dropoff['Drop-off %'],
    text=f"⚠️ Highest Drop-off<br>{max_dropoff['Users Lost']:,.0f} users lost",
    showarrow=True,
    arrowhead=2,
    arrowsize=1,
    arrowwidth=2,
    arrowcolor="#e74c3c",
    ax=0,
    ay=-60,
    bgcolor="#ffcccc",
    bordercolor="#e74c3c"
)

fig_dropoff.write_html('dropoff_analysis.html')
print("✓ Created: dropoff_analysis.html")

# ============================================================================
# 7. STATIC VISUALIZATIONS (Matplotlib/Seaborn)
# ============================================================================

print("\nCreating static visualizations...")

# Figure 1: Funnel with conversion rates
fig, ax = plt.subplots(figsize=(12, 8))

y_pos = np.arange(len(stage_names))
colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6']

bars = ax.barh(y_pos, stage_values, color=colors, alpha=0.8, edgecolor='white', linewidth=2)

# Add value labels
for i, (bar, val) in enumerate(zip(bars, stage_values)):
    conv_rate = (val / stage_values[0]) * 100
    ax.text(val + 1000, bar.get_y() + bar.get_height()/2, 
            f'{val:,} ({conv_rate:.1f}%)', 
            va='center', fontsize=11, fontweight='bold')

ax.set_yticks(y_pos)
ax.set_yticklabels(stage_names, fontsize=12)
ax.set_xlabel('Number of Users', fontsize=12, fontweight='bold')
ax.set_title('Marketing Funnel: Conversion Flow Analysis', 
             fontsize=16, fontweight='bold', pad=20)
ax.grid(axis='x', alpha=0.3, linestyle='--')
ax.set_facecolor('#f8f9fa')
fig.patch.set_facecolor('white')

plt.tight_layout()
plt.savefig('static_funnel_chart.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Created: static_funnel_chart.png")
plt.close()

# Figure 2: Channel comparison
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Channel Performance Dashboard', fontsize=18, fontweight='bold', y=0.995)

channel_sorted = channel_metrics.sort_values('Conversion Rate', ascending=False)

# Conversion Rate
ax1 = axes[0, 0]
bars1 = ax1.bar(range(len(channel_sorted)), channel_sorted['Conversion Rate'], 
                color='#3498db', alpha=0.8, edgecolor='white', linewidth=2)
ax1.set_xticks(range(len(channel_sorted)))
ax1.set_xticklabels(channel_sorted['Channel'], rotation=45, ha='right')
ax1.set_ylabel('Conversion Rate (%)', fontweight='bold')
ax1.set_title('Conversion Rate by Channel', fontweight='bold', pad=10)
ax1.grid(axis='y', alpha=0.3, linestyle='--')
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.2f}%', ha='center', va='bottom', fontsize=9)

# Revenue
ax2 = axes[0, 1]
bars2 = ax2.bar(range(len(channel_sorted)), channel_sorted['Revenue'], 
                color='#2ecc71', alpha=0.8, edgecolor='white', linewidth=2)
ax2.set_xticks(range(len(channel_sorted)))
ax2.set_xticklabels(channel_sorted['Channel'], rotation=45, ha='right')
ax2.set_ylabel('Revenue ($)', fontweight='bold')
ax2.set_title('Revenue by Channel', fontweight='bold', pad=10)
ax2.grid(axis='y', alpha=0.3, linestyle='--')

# Sessions
ax3 = axes[1, 0]
bars3 = ax3.bar(range(len(channel_sorted)), channel_sorted['Sessions'], 
                color='#f39c12', alpha=0.8, edgecolor='white', linewidth=2)
ax3.set_xticks(range(len(channel_sorted)))
ax3.set_xticklabels(channel_sorted['Channel'], rotation=45, ha='right')
ax3.set_ylabel('Sessions', fontweight='bold')
ax3.set_title('Sessions by Channel', fontweight='bold', pad=10)
ax3.grid(axis='y', alpha=0.3, linestyle='--')

# Revenue per User
ax4 = axes[1, 1]
bars4 = ax4.bar(range(len(channel_sorted)), channel_sorted['Revenue/User'], 
                color='#9b59b6', alpha=0.8, edgecolor='white', linewidth=2)
ax4.set_xticks(range(len(channel_sorted)))
ax4.set_xticklabels(channel_sorted['Channel'], rotation=45, ha='right')
ax4.set_ylabel('Revenue per User ($)', fontweight='bold')
ax4.set_title('Revenue per User by Channel', fontweight='bold', pad=10)
ax4.grid(axis='y', alpha=0.3, linestyle='--')

for ax in axes.flat:
    ax.set_facecolor('#f8f9fa')

fig.patch.set_facecolor('white')
plt.tight_layout()
plt.savefig('static_channel_dashboard.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Created: static_channel_dashboard.png")
plt.close()

print("\n" + "="*80)
print("VISUALIZATION GENERATION COMPLETE")
print("="*80)
print("\nGenerated files:")
print("  Interactive (HTML):")
print("    - funnel_visualization.html")
print("    - channel_performance_dashboard.html")
print("    - channel_device_heatmap.html")
print("    - cohort_trends.html")
print("    - roi_bubble_chart.html")
print("    - dropoff_analysis.html")
print("  Static (PNG):")
print("    - static_funnel_chart.png")
print("    - static_channel_dashboard.png")
