
# Create the funnel analysis script
funnel_analysis_code = '''"""
Multi-Channel Marketing Funnel Analysis
Author: Marketing Analytics Project
Description: Comprehensive funnel analysis with conversion metrics, drop-off analysis, and cohort analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

# Load data
print("Loading marketing funnel data...")
df = pd.read_csv('marketing_funnel_data.csv', parse_dates=['landing_timestamp', 'signup_timestamp', 
                                                             'product_view_timestamp', 'add_to_cart_timestamp',
                                                             'purchase_timestamp'])

print(f"Dataset loaded: {len(df):,} user sessions")
print(f"Date range: {df['landing_timestamp'].min().date()} to {df['landing_timestamp'].max().date()}")

# ============================================================================
# 1. OVERALL FUNNEL METRICS
# ============================================================================

print("\\n" + "="*80)
print("OVERALL FUNNEL PERFORMANCE ANALYSIS")
print("="*80)

stages = {
    'Landing': df['stage_1_landing'].sum(),
    'Signup': df['stage_2_signup'].sum(),
    'Product View': df['stage_3_product_view'].sum(),
    'Add to Cart': df['stage_4_add_to_cart'].sum(),
    'Purchase': df['stage_5_purchase'].sum()
}

funnel_metrics = []
stage_names = list(stages.keys())

for i, (stage, count) in enumerate(stages.items()):
    # Overall conversion rate
    overall_conv_rate = (count / stages['Landing']) * 100
    
    # Stage-to-stage conversion
    if i > 0:
        prev_count = stages[stage_names[i-1]]
        stage_conv_rate = (count / prev_count) * 100 if prev_count > 0 else 0
        drop_off = 100 - stage_conv_rate
    else:
        stage_conv_rate = 100.0
        drop_off = 0.0
    
    funnel_metrics.append({
        'Stage': stage,
        'Users': count,
        'Overall Conv Rate': f"{overall_conv_rate:.2f}%",
        'Stage Conv Rate': f"{stage_conv_rate:.2f}%",
        'Drop-off Rate': f"{drop_off:.2f}%"
    })
    
    print(f"\\n{stage}:")
    print(f"  Users: {count:,}")
    print(f"  Overall Conversion: {overall_conv_rate:.2f}%")
    if i > 0:
        print(f"  Stage Conversion: {stage_conv_rate:.2f}%")
        print(f"  Drop-off: {drop_off:.2f}%")
        print(f"  Users Lost: {prev_count - count:,}")

funnel_metrics_df = pd.DataFrame(funnel_metrics)

print("\\n" + "="*80)
print("KEY INSIGHTS:")
print("="*80)

# Identify biggest drop-off
drop_offs = []
for i in range(1, len(stage_names)):
    prev_count = stages[stage_names[i-1]]
    curr_count = stages[stage_names[i]]
    drop_off_pct = ((prev_count - curr_count) / prev_count) * 100
    drop_offs.append((f"{stage_names[i-1]} → {stage_names[i]}", drop_off_pct, prev_count - curr_count))

drop_offs.sort(key=lambda x: x[1], reverse=True)

print(f"\\n1. Biggest Drop-off Point: {drop_offs[0][0]}")
print(f"   - {drop_offs[0][1]:.2f}% drop-off rate")
print(f"   - {drop_offs[0][2]:,} users lost")
print(f"   → PRIORITY: Optimize this stage for maximum impact")

print(f"\\n2. Overall Conversion Rate: {(stages['Purchase']/stages['Landing'])*100:.2f}%")
print(f"   - Industry benchmark typically 2-5%")
print(f"   - Current performance: {'ABOVE' if (stages['Purchase']/stages['Landing'])*100 > 5 else 'WITHIN'} benchmark")

# Revenue metrics
total_revenue = df['purchase_value'].sum()
avg_order_value = df['purchase_value'].mean()
print(f"\\n3. Revenue Metrics:")
print(f"   - Total Revenue: ${total_revenue:,.2f}")
print(f"   - Average Order Value: ${avg_order_value:.2f}")
print(f"   - Revenue per Visitor: ${total_revenue/len(df):.2f}")

# ============================================================================
# 2. CHANNEL PERFORMANCE ANALYSIS
# ============================================================================

print("\\n\\n" + "="*80)
print("CHANNEL PERFORMANCE ANALYSIS")
print("="*80)

channel_metrics = []

for channel in df['channel'].unique():
    channel_data = df[df['channel'] == channel]
    
    total_users = len(channel_data)
    signups = channel_data['stage_2_signup'].sum()
    purchases = channel_data['stage_5_purchase'].sum()
    revenue = channel_data['purchase_value'].sum()
    
    signup_rate = (signups / total_users) * 100
    conv_rate = (purchases / total_users) * 100
    avg_revenue_per_user = revenue / total_users
    
    channel_metrics.append({
        'Channel': channel,
        'Sessions': total_users,
        'Signups': signups,
        'Purchases': purchases,
        'Signup Rate': signup_rate,
        'Conversion Rate': conv_rate,
        'Revenue': revenue,
        'Revenue/User': avg_revenue_per_user
    })

channel_df = pd.DataFrame(channel_metrics).sort_values('Conversion Rate', ascending=False)

print("\\nChannel Performance Summary:")
print(channel_df.to_string(index=False))

# Best and worst performers
best_channel = channel_df.iloc[0]
worst_channel = channel_df.iloc[-1]

print(f"\\n🏆 Best Performing Channel: {best_channel['Channel']}")
print(f"   - Conversion Rate: {best_channel['Conversion Rate']:.2f}%")
print(f"   - Revenue per User: ${best_channel['Revenue/User']:.2f}")

print(f"\\n⚠️  Worst Performing Channel: {worst_channel['Channel']}")
print(f"   - Conversion Rate: {worst_channel['Conversion Rate']:.2f}%")
print(f"   - Revenue per User: ${worst_channel['Revenue/User']:.2f}")
print(f"   → {((best_channel['Conversion Rate'] / worst_channel['Conversion Rate']) - 1) * 100:.1f}% performance gap")

# Save channel metrics
channel_df.to_csv('channel_performance_metrics.csv', index=False)
print("\\n✓ Saved: channel_performance_metrics.csv")

# ============================================================================
# 3. DEVICE PERFORMANCE ANALYSIS
# ============================================================================

print("\\n\\n" + "="*80)
print("DEVICE PERFORMANCE ANALYSIS")
print("="*80)

device_metrics = []

for device in df['device'].unique():
    device_data = df[df['device'] == device]
    
    total_users = len(device_data)
    purchases = device_data['stage_5_purchase'].sum()
    revenue = device_data['purchase_value'].sum()
    
    conv_rate = (purchases / total_users) * 100
    
    device_metrics.append({
        'Device': device,
        'Sessions': total_users,
        'Purchases': purchases,
        'Conversion Rate': conv_rate,
        'Revenue': revenue
    })

device_df = pd.DataFrame(device_metrics).sort_values('Conversion Rate', ascending=False)

print("\\nDevice Performance Summary:")
print(device_df.to_string(index=False))

# Device insights
desktop_conv = device_df[device_df['Device'] == 'Desktop']['Conversion Rate'].values[0]
mobile_conv = device_df[device_df['Device'] == 'Mobile']['Conversion Rate'].values[0]

print(f"\\n📱 Mobile vs Desktop Gap: {desktop_conv / mobile_conv:.2f}x")
print(f"   Desktop converts at {desktop_conv:.2f}% vs Mobile at {mobile_conv:.2f}%")
print(f"   → OPPORTUNITY: Mobile optimization could significantly boost revenue")

# ============================================================================
# 4. TIME-TO-CONVERT ANALYSIS
# ============================================================================

print("\\n\\n" + "="*80)
print("TIME-TO-CONVERT ANALYSIS")
print("="*80)

# Analyze users who completed purchase
purchasers = df[df['stage_5_purchase'] == 1].copy()

if len(purchasers) > 0:
    avg_journey_time = purchasers['total_journey_minutes'].mean()
    median_journey_time = purchasers['total_journey_minutes'].median()
    
    print(f"\\nAverage Journey Time: {avg_journey_time:.1f} minutes ({avg_journey_time/60:.1f} hours)")
    print(f"Median Journey Time: {median_journey_time:.1f} minutes ({median_journey_time/60:.1f} hours)")
    
    # Stage-specific timings
    print("\\nAverage Time Between Stages:")
    if 'landing_to_signup_minutes' in purchasers.columns:
        print(f"  Landing → Signup: {purchasers['landing_to_signup_minutes'].mean():.1f} minutes")
    if 'signup_to_product_minutes' in purchasers.columns:
        print(f"  Signup → Product View: {purchasers['signup_to_product_minutes'].mean():.1f} minutes")
    if 'product_to_cart_minutes' in purchasers.columns:
        print(f"  Product View → Add to Cart: {purchasers['product_to_cart_minutes'].mean():.1f} minutes")
    if 'cart_to_purchase_minutes' in purchasers.columns:
        print(f"  Add to Cart → Purchase: {purchasers['cart_to_purchase_minutes'].mean():.1f} minutes")

# ============================================================================
# 5. COHORT ANALYSIS
# ============================================================================

print("\\n\\n" + "="*80)
print("COHORT ANALYSIS (Monthly)")
print("="*80)

cohort_metrics = df.groupby('cohort_month').agg({
    'user_id': 'count',
    'stage_2_signup': 'sum',
    'stage_5_purchase': 'sum',
    'purchase_value': 'sum'
}).rename(columns={'user_id': 'Total_Users'})

cohort_metrics['Signup_Rate'] = (cohort_metrics['stage_2_signup'] / cohort_metrics['Total_Users']) * 100
cohort_metrics['Conversion_Rate'] = (cohort_metrics['stage_5_purchase'] / cohort_metrics['Total_Users']) * 100
cohort_metrics['Revenue_Per_User'] = cohort_metrics['purchase_value'] / cohort_metrics['Total_Users']

print("\\nMonthly Cohort Performance:")
print(cohort_metrics.to_string())

# Trend analysis
first_month_conv = cohort_metrics['Conversion_Rate'].iloc[0]
last_month_conv = cohort_metrics['Conversion_Rate'].iloc[-1]
improvement = ((last_month_conv - first_month_conv) / first_month_conv) * 100

print(f"\\n📈 Trend Analysis:")
print(f"   First Month Conversion: {first_month_conv:.2f}%")
print(f"   Last Month Conversion: {last_month_conv:.2f}%")
print(f"   Overall Change: {improvement:+.1f}%")

cohort_metrics.to_csv('cohort_analysis.csv')
print("\\n✓ Saved: cohort_analysis.csv")

# ============================================================================
# 6. SEGMENT ANALYSIS
# ============================================================================

print("\\n\\n" + "="*80)
print("DEMOGRAPHIC SEGMENT ANALYSIS")
print("="*80)

# Age group analysis
print("\\nAge Group Performance:")
age_metrics = df.groupby('age_group').agg({
    'user_id': 'count',
    'stage_5_purchase': 'sum',
    'purchase_value': 'sum'
})
age_metrics['Conversion_Rate'] = (age_metrics['stage_5_purchase'] / age_metrics['user_id']) * 100
age_metrics['Avg_Order_Value'] = age_metrics['purchase_value'] / age_metrics['stage_5_purchase']
print(age_metrics.to_string())

# Location analysis
print("\\nLocation Performance:")
location_metrics = df.groupby('location').agg({
    'user_id': 'count',
    'stage_5_purchase': 'sum',
    'purchase_value': 'sum'
})
location_metrics['Conversion_Rate'] = (location_metrics['stage_5_purchase'] / location_metrics['user_id']) * 100
print(location_metrics.to_string())

print("\\n\\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
print("\\nGenerated files:")
print("  - channel_performance_metrics.csv")
print("  - cohort_analysis.csv")
'''

with open('01_funnel_analysis.py', 'w') as f:
    f.write(funnel_analysis_code)

print("✓ Created: 01_funnel_analysis.py")
