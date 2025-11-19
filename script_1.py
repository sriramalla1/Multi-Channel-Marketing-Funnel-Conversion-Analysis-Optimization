
# Generate user data
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
    
    # Calculate cohort week (for time-based analysis)
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

users_df = pd.DataFrame(users_data)
print(f"✓ Generated {len(users_df)} user sessions")
print(f"\nChannel distribution:")
print(users_df['channel'].value_counts())
