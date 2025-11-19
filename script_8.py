
# Create data generation script as separate file
data_gen_script = '''"""
Synthetic Marketing Funnel Data Generator
Author: Marketing Analytics Project
Description: Generate realistic multi-channel marketing funnel data for analysis
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# ============================================================================
# CONFIGURATION
# ============================================================================

NUM_USERS = 75000
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2024, 10, 31)

# Channel configurations with realistic conversion rates
CHANNELS = {
    'Organic Search': {'weight': 0.25, 'conversion_multiplier': 1.4},
    'Paid Search': {'weight': 0.20, 'conversion_multiplier': 1.1},
    'Social Media': {'weight': 0.20, 'conversion_multiplier': 0.7},
    'Email': {'weight': 0.15, 'conversion_multiplier': 1.8},
    'Direct': {'weight': 0.12, 'conversion_multiplier': 1.3},
    'Referral': {'weight': 0.08, 'conversion_multiplier': 1.2}
}

DEVICES = ['Desktop', 'Mobile', 'Tablet']
DEVICE_WEIGHTS = [0.45, 0.45, 0.10]

# Device-specific conversion multipliers
DEVICE_CONVERSION = {
    'Desktop': 1.3,
    'Mobile': 0.6,
    'Tablet': 0.9
}

# Funnel stage base conversion rates
BASE_RATES = {
    'landing_to_signup': 0.40,
    'signup_to_product_view': 0.62,
    'product_view_to_cart': 0.48,
    'cart_to_purchase': 0.33
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def generate_timestamp(start, end):
    """Generate random timestamp between start and end dates"""
    delta = end - start
    random_days = random.randint(0, delta.days)
    random_seconds = random.randint(0, 86400)
    return start + timedelta(days=random_days, seconds=random_seconds)

def calculate_conversion_probability(base_rate, channel_mult, device_mult, cohort_week):
    """Calculate conversion probability with various factors"""
    # Add slight improvement over time (learning/optimization effect)
    time_improvement = 1 + (cohort_week * 0.002)
    
    # Add some randomness
    random_factor = np.random.uniform(0.9, 1.1)
    
    prob = base_rate * channel_mult * device_mult * time_improvement * random_factor
    return min(prob, 0.95)  # Cap at 95%

# ============================================================================
# DATA GENERATION
# ============================================================================

print("="*80)
print("MARKETING FUNNEL DATA GENERATION")
print("="*80)
print(f"\\nGenerating {NUM_USERS:,} user sessions...")
print(f"Date range: {START_DATE.date()} to {END_DATE.date()}")
print(f"Channels: {len(CHANNELS)}")
print(f"Devices: {len(DEVICES)}")

# Generate base user sessions
users_data = []

for user_id in range(1, NUM_USERS + 1):
    # Select channel
    channel = random.choices(
        list(CHANNELS.keys()), 
        weights=[CHANNELS[ch]['weight'] for ch in CHANNELS.keys()]
    )[0]
    
    # Select device
    device = random.choices(DEVICES, weights=DEVICE_WEIGHTS)[0]
    
    # Generate landing timestamp
    landing_timestamp = generate_timestamp(START_DATE, END_DATE)
    
    # Calculate cohort week
    cohort_week = (landing_timestamp - START_DATE).days // 7
    
    # Demographics
    age_group = random.choices(
        ['18-24', '25-34', '35-44', '45-54', '55+'],
        weights=[0.15, 0.35, 0.25, 0.15, 0.10]
    )[0]
    
    location = random.choices(
        ['Urban', 'Suburban', 'Rural'],
        weights=[0.50, 0.35, 0.15]
    )[0]
    
    # Get multipliers
    channel_mult = CHANNELS[channel]['conversion_multiplier']
    device_mult = DEVICE_CONVERSION[device]
    
    users_data.append({
        'user_id': f'U{user_id:06d}',
        'channel': channel,
        'device': device,
        'age_group': age_group,
        'location': location,
        'landing_timestamp': landing_timestamp,
        'cohort_week': cohort_week,
        'channel_mult': channel_mult,
        'device_mult': device_mult
    })
    
    if user_id % 10000 == 0:
        print(f"  Generated {user_id:,} users...")

users_df = pd.DataFrame(users_data)
print(f"\\n✓ Generated {len(users_df):,} user sessions")

# Generate funnel progression
print("\\nGenerating funnel progression...")
funnel_data = []

for idx, user in users_df.iterrows():
    user_journey = {
        'user_id': user['user_id'],
        'channel': user['channel'],
        'device': user['device'],
        'age_group': user['age_group'],
        'location': user['location'],
        'cohort_week': user['cohort_week'],
        'cohort_month': user['landing_timestamp'].strftime('%Y-%m')
    }
    
    current_timestamp = user['landing_timestamp']
    
    # Stage 1: Landing (everyone lands)
    user_journey['stage_1_landing'] = 1
    user_journey['landing_timestamp'] = current_timestamp
    
    # Stage 2: Signup
    signup_prob = calculate_conversion_probability(
        BASE_RATES['landing_to_signup'],
        user['channel_mult'],
        user['device_mult'],
        user['cohort_week']
    )
    
    if random.random() < signup_prob:
        current_timestamp += timedelta(minutes=random.randint(1, 30))
        user_journey['stage_2_signup'] = 1
        user_journey['signup_timestamp'] = current_timestamp
        user_journey['landing_to_signup_minutes'] = (current_timestamp - user['landing_timestamp']).seconds / 60
    else:
        user_journey['stage_2_signup'] = 0
        user_journey['exit_stage'] = 'Landing'
        funnel_data.append(user_journey)
        continue
    
    # Stage 3: Product View
    product_view_prob = calculate_conversion_probability(
        BASE_RATES['signup_to_product_view'],
        user['channel_mult'],
        user['device_mult'],
        user['cohort_week']
    )
    
    if random.random() < product_view_prob:
        current_timestamp += timedelta(minutes=random.randint(2, 45))
        user_journey['stage_3_product_view'] = 1
        user_journey['product_view_timestamp'] = current_timestamp
        user_journey['signup_to_product_minutes'] = (current_timestamp - user_journey['signup_timestamp']).seconds / 60
    else:
        user_journey['stage_3_product_view'] = 0
        user_journey['exit_stage'] = 'Signup'
        funnel_data.append(user_journey)
        continue
    
    # Stage 4: Add to Cart
    cart_prob = calculate_conversion_probability(
        BASE_RATES['product_view_to_cart'],
        user['channel_mult'],
        user['device_mult'],
        user['cohort_week']
    )
    
    if random.random() < cart_prob:
        current_timestamp += timedelta(minutes=random.randint(3, 60))
        user_journey['stage_4_add_to_cart'] = 1
        user_journey['add_to_cart_timestamp'] = current_timestamp
        user_journey['product_to_cart_minutes'] = (current_timestamp - user_journey['product_view_timestamp']).seconds / 60
    else:
        user_journey['stage_4_add_to_cart'] = 0
        user_journey['exit_stage'] = 'Product_View'
        funnel_data.append(user_journey)
        continue
    
    # Stage 5: Purchase
    purchase_prob = calculate_conversion_probability(
        BASE_RATES['cart_to_purchase'],
        user['channel_mult'],
        user['device_mult'],
        user['cohort_week']
    )
    
    if random.random() < purchase_prob:
        current_timestamp += timedelta(minutes=random.randint(5, 90))
        user_journey['stage_5_purchase'] = 1
        user_journey['purchase_timestamp'] = current_timestamp
        user_journey['cart_to_purchase_minutes'] = (current_timestamp - user_journey['add_to_cart_timestamp']).seconds / 60
        
        # Add purchase value (lognormal distribution for realistic revenue)
        user_journey['purchase_value'] = round(np.random.lognormal(4.2, 0.6), 2)
        user_journey['exit_stage'] = 'Purchase'
    else:
        user_journey['stage_5_purchase'] = 0
        user_journey['exit_stage'] = 'Add_to_Cart'
    
    # Calculate total journey time
    if 'purchase_timestamp' in user_journey:
        user_journey['total_journey_minutes'] = (user_journey['purchase_timestamp'] - user['landing_timestamp']).seconds / 60
    
    funnel_data.append(user_journey)
    
    if (idx + 1) % 10000 == 0:
        print(f"  Processed {idx + 1:,} users...")

funnel_df = pd.DataFrame(funnel_data)

# Fill missing stage columns
for stage_col in ['stage_2_signup', 'stage_3_product_view', 'stage_4_add_to_cart', 'stage_5_purchase']:
    funnel_df[stage_col] = funnel_df[stage_col].fillna(0).astype(int)

print(f"\\n✓ Generated complete funnel data")

# ============================================================================
# SUMMARY STATISTICS
# ============================================================================

print("\\n" + "="*80)
print("DATA SUMMARY")
print("="*80)

print(f"\\nTotal records: {len(funnel_df):,}")
print(f"Date range: {funnel_df['landing_timestamp'].min()} to {funnel_df['landing_timestamp'].max()}")

print("\\nFunnel Performance:")
for i, stage in enumerate(['stage_1_landing', 'stage_2_signup', 'stage_3_product_view', 
                           'stage_4_add_to_cart', 'stage_5_purchase']):
    count = funnel_df[stage].sum()
    pct = (count / len(funnel_df)) * 100
    print(f"  {stage}: {count:,} users ({pct:.2f}%)")

print("\\nChannel Distribution:")
print(funnel_df['channel'].value_counts().to_string())

print("\\nDevice Distribution:")
print(funnel_df['device'].value_counts().to_string())

total_revenue = funnel_df['purchase_value'].sum()
print(f"\\nTotal Revenue: ${total_revenue:,.2f}")
print(f"Average Order Value: ${funnel_df['purchase_value'].mean():.2f}")

# ============================================================================
# SAVE DATA
# ============================================================================

output_file = 'marketing_funnel_data.csv'
funnel_df.to_csv(output_file, index=False)

print("\\n" + "="*80)
print(f"✓ Data saved to: {output_file}")
print("="*80)
print("\\nData generation complete!")
print("You can now run the analysis scripts:")
print("  1. python 01_funnel_analysis.py")
print("  2. python 02_attribution_analysis.py")
print("  3. python 03_visualizations.py")
'''

with open('00_generate_data.py', 'w') as f:
    f.write(data_gen_script)

print("✓ Created: 00_generate_data.py")
