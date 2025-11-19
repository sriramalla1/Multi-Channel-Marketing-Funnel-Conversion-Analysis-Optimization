
# Generate funnel progression for each user
funnel_data = []

stages = ['Landing', 'Signup', 'Product_View', 'Add_to_Cart', 'Purchase']

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
        # Add time delay (1-30 minutes)
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
        
        # Add purchase value
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
        print(f"Processed {idx + 1} users...")

funnel_df = pd.DataFrame(funnel_data)
print(f"\n✓ Generated funnel progression for {len(funnel_df)} users")
print(f"\nDataset shape: {funnel_df.shape}")
