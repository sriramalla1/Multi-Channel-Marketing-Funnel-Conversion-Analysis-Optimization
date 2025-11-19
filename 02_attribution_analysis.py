"""
Multi-Touch Attribution Analysis
Author: Marketing Analytics Project
Description: Compare different attribution models and analyze channel contribution to conversions
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Load data
print("Loading marketing funnel data...")
df = pd.read_csv('marketing_funnel_data.csv', parse_dates=['landing_timestamp'])

# Filter to only purchasers for attribution analysis
purchasers = df[df['stage_5_purchase'] == 1].copy()
print(f"Analyzing {len(purchasers):,} conversions across {df['channel'].nunique()} channels")

# ============================================================================
# 1. ATTRIBUTION MODEL IMPLEMENTATIONS
# ============================================================================

print("\n" + "="*80)
print("MULTI-TOUCH ATTRIBUTION MODELING")
print("="*80)

# In this simplified version, each user has one touchpoint (their acquisition channel)
# In real-world scenarios, users would have multiple touchpoints across their journey

def first_touch_attribution(channel_data):
    """First-touch: 100% credit to first interaction"""
    return channel_data.groupby('channel').agg({
        'user_id': 'count',
        'purchase_value': 'sum'
    }).rename(columns={'user_id': 'Conversions', 'purchase_value': 'Revenue'})

def last_touch_attribution(channel_data):
    """Last-touch: 100% credit to last interaction before conversion"""
    # In single-touch data, this equals first-touch
    return first_touch_attribution(channel_data)

def linear_attribution(channel_data):
    """Linear: Equal credit across all touchpoints"""
    # In single-touch data, this equals first-touch
    # In multi-touch, would divide credit equally
    return first_touch_attribution(channel_data)

def time_decay_attribution(channel_data, decay_rate=0.5):
    """Time-decay: More recent touchpoints get more credit"""
    # Simplified: adjust credit based on conversion speed
    results = []
    for channel in channel_data['channel'].unique():
        channel_df = channel_data[channel_data['channel'] == channel]

        # Weight by recency (faster conversions get slightly more weight)
        avg_time = channel_df['total_journey_minutes'].mean()
        time_weight = 1 / (1 + avg_time / 100)  # Normalize

        conversions = len(channel_df)
        revenue = channel_df['purchase_value'].sum() * time_weight

        results.append({
            'channel': channel,
            'Conversions': conversions,
            'Revenue': revenue
        })

    return pd.DataFrame(results).set_index('channel')

def position_based_attribution(channel_data, first_weight=0.4, last_weight=0.4):
    """Position-based (U-shaped): 40% first, 40% last, 20% middle"""
    # Simplified version for single-touch
    return first_touch_attribution(channel_data)

# ============================================================================
# 2. CALCULATE ATTRIBUTION FOR EACH MODEL
# ============================================================================

print("\nCalculating attribution models...")

# First-Touch Attribution
first_touch = first_touch_attribution(purchasers)
first_touch['Attribution_Model'] = 'First-Touch'

# Last-Touch Attribution
last_touch = last_touch_attribution(purchasers)
last_touch['Attribution_Model'] = 'Last-Touch'

# Linear Attribution
linear = linear_attribution(purchasers)
linear['Attribution_Model'] = 'Linear'

# Time-Decay Attribution
time_decay = time_decay_attribution(purchasers)
time_decay['Attribution_Model'] = 'Time-Decay'

# Position-Based Attribution
position_based = position_based_attribution(purchasers)
position_based['Attribution_Model'] = 'Position-Based'

# ============================================================================
# 3. COMPARE ATTRIBUTION MODELS
# ============================================================================

print("\n" + "="*80)
print("ATTRIBUTION MODEL COMPARISON")
print("="*80)

# Combine all models
all_models = pd.concat([
    first_touch.reset_index(),
    last_touch.reset_index(),
    linear.reset_index(),
    time_decay.reset_index(),
    position_based.reset_index()
])

# Calculate revenue share for each model
attribution_comparison = all_models.pivot(index='channel', columns='Attribution_Model', values='Revenue')
attribution_comparison = attribution_comparison.fillna(0)

# Calculate percentage of total revenue
for col in attribution_comparison.columns:
    total = attribution_comparison[col].sum()
    attribution_comparison[f'{col}_Pct'] = (attribution_comparison[col] / total) * 100

print("\nRevenue Attribution by Model:")
print(attribution_comparison.to_string())

# Save attribution comparison
attribution_comparison.to_csv('attribution_model_comparison.csv')
print("\n✓ Saved: attribution_model_comparison.csv")

# ============================================================================
# 4. CALCULATE ROI/ROAS BY CHANNEL
# ============================================================================

print("\n\n" + "="*80)
print("ROI/ROAS ANALYSIS BY CHANNEL")
print("="*80)

# Simulate marketing spend by channel (cost per acquisition varies by channel)
# These are realistic industry averages
cpa_by_channel = {
    'Organic Search': 15,    # Lower cost (SEO investment amortized)
    'Paid Search': 35,       # Higher CPC
    'Social Media': 28,      # Mid-range
    'Email': 5,              # Very low marginal cost
    'Direct': 8,             # Brand awareness spillover
    'Referral': 12           # Partnership costs
}

roi_metrics = []

for channel in df['channel'].unique():
    channel_data = df[df['channel'] == channel]

    total_sessions = len(channel_data)
    conversions = channel_data['stage_5_purchase'].sum()
    revenue = channel_data['purchase_value'].sum()

    # Calculate spend
    cost_per_session = cpa_by_channel.get(channel, 20)
    total_spend = total_sessions * cost_per_session

    # Calculate metrics
    cpa = total_spend / conversions if conversions > 0 else 0
    roas = revenue / total_spend if total_spend > 0 else 0
    roi = ((revenue - total_spend) / total_spend) * 100 if total_spend > 0 else 0

    roi_metrics.append({
        'Channel': channel,
        'Sessions': total_sessions,
        'Spend': total_spend,
        'Revenue': revenue,
        'Conversions': conversions,
        'CPA': cpa,
        'ROAS': roas,
        'ROI': roi
    })

roi_df = pd.DataFrame(roi_metrics).sort_values('ROAS', ascending=False)

print("\nChannel ROI/ROAS Performance:")
for _, row in roi_df.iterrows():
    print(f"\n{row['Channel']}:")
    print(f"  Total Spend: ${row['Spend']:,.2f}")
    print(f"  Revenue Generated: ${row['Revenue']:,.2f}")
    print(f"  ROAS: {row['ROAS']:.2f}x (${row['ROAS']:.2f} revenue per $1 spend)")
    print(f"  ROI: {row['ROI']:.1f}%")
    print(f"  CPA: ${row['CPA']:.2f} (cost per acquisition)")

# Save ROI metrics
roi_df.to_csv('channel_roi_metrics.csv', index=False)
print("\n✓ Saved: channel_roi_metrics.csv")

# ============================================================================
# 5. BUDGET ALLOCATION RECOMMENDATIONS
# ============================================================================

print("\n\n" + "="*80)
print("BUDGET ALLOCATION OPTIMIZATION")
print("="*80)

# Current budget allocation (based on session volume)
total_spend = roi_df['Spend'].sum()
roi_df['Current_Budget_Share'] = (roi_df['Spend'] / total_spend) * 100

# Optimal allocation based on ROAS
# Weight by ROAS squared to heavily favor high performers
roi_df['ROAS_Weight'] = roi_df['ROAS'] ** 2
total_roas_weight = roi_df['ROAS_Weight'].sum()
roi_df['Optimal_Budget_Share'] = (roi_df['ROAS_Weight'] / total_roas_weight) * 100

# Calculate budget shift
roi_df['Budget_Change'] = roi_df['Optimal_Budget_Share'] - roi_df['Current_Budget_Share']
roi_df['Dollar_Change'] = (roi_df['Budget_Change'] / 100) * total_spend

print("\nCurrent vs Optimal Budget Allocation:")
print(roi_df[['Channel', 'Current_Budget_Share', 'Optimal_Budget_Share', 'Budget_Change', 'Dollar_Change']].to_string(index=False))

print("\n" + "-"*80)
print("RECOMMENDATIONS:")
print("-"*80)

# Channels to increase
increase_channels = roi_df[roi_df['Budget_Change'] > 5].sort_values('Budget_Change', ascending=False)
if len(increase_channels) > 0:
    print("\n🚀 INCREASE INVESTMENT:")
    for _, channel in increase_channels.iterrows():
        print(f"   {channel['Channel']}: {channel['Budget_Change']:+.1f}% (${channel['Dollar_Change']:+,.0f})")
        print(f"      Current ROAS: {channel['ROAS']:.2f}x - High return justifies more spend")

# Channels to decrease
decrease_channels = roi_df[roi_df['Budget_Change'] < -5].sort_values('Budget_Change')
if len(decrease_channels) > 0:
    print("\n⚠️  DECREASE INVESTMENT:")
    for _, channel in decrease_channels.iterrows():
        print(f"   {channel['Channel']}: {channel['Budget_Change']:+.1f}% (${channel['Dollar_Change']:+,.0f})")
        print(f"      Current ROAS: {channel['ROAS']:.2f}x - Underperforming, reallocate budget")

# Projected impact
current_total_revenue = roi_df['Revenue'].sum()
weighted_roas = (roi_df['ROAS'] * roi_df['Optimal_Budget_Share'] / 100).sum()
projected_revenue = total_spend * weighted_roas
revenue_lift = ((projected_revenue - current_total_revenue) / current_total_revenue) * 100

print(f"\n💡 PROJECTED IMPACT:")
print(f"   Current Revenue: ${current_total_revenue:,.2f}")
print(f"   Projected Revenue (optimized): ${projected_revenue:,.2f}")
print(f"   Expected Lift: {revenue_lift:+.1f}%")

# Save allocation recommendations
roi_df[['Channel', 'Spend', 'Revenue', 'ROAS', 'ROI', 'Current_Budget_Share', 
        'Optimal_Budget_Share', 'Budget_Change', 'Dollar_Change']].to_csv('budget_allocation_recommendations.csv', index=False)
print("\n✓ Saved: budget_allocation_recommendations.csv")

# ============================================================================
# 6. ATTRIBUTION IMPACT ON DECISIONS
# ============================================================================

print("\n\n" + "="*80)
print("ATTRIBUTION MODEL IMPACT ON DECISIONS")
print("="*80)

print("\nHow attribution model choice affects channel credit:")
print("\n(Note: In single-touch journeys, most models yield similar results)")
print("(In multi-touch scenarios, differences would be more pronounced)")

# Compare top 3 channels across models
print("\nTop 3 Channels by Revenue (First-Touch Model):")
top3_first = first_touch.nlargest(3, 'Revenue')[['Revenue', 'Conversions']]
for channel, row in top3_first.iterrows():
    print(f"  {channel}: ${row['Revenue']:,.2f} ({row['Conversions']} conversions)")

print("\nKey Insight:")
print("In real multi-touch attribution scenarios:")
print("  • First-Touch favors awareness channels (upper funnel)")
print("  • Last-Touch favors conversion channels (lower funnel)")
print("  • Linear gives balanced view of all touchpoints")
print("  • Time-Decay emphasizes recent interactions")
print("  • Position-Based (40-20-40) balances first and last touch")

print("\n" + "="*80)
print("ATTRIBUTION ANALYSIS COMPLETE")
print("="*80)
print("\nGenerated files:")
print("  - attribution_model_comparison.csv")
print("  - channel_roi_metrics.csv")
print("  - budget_allocation_recommendations.csv")
