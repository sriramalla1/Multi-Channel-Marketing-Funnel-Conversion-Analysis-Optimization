
# Fill missing stage columns with 0
for stage_col in ['stage_2_signup', 'stage_3_product_view', 'stage_4_add_to_cart', 'stage_5_purchase']:
    funnel_df[stage_col] = funnel_df[stage_col].fillna(0).astype(int)

# Calculate overall funnel metrics
print("\n" + "="*60)
print("OVERALL FUNNEL PERFORMANCE")
print("="*60)

total_users = len(funnel_df)
stage_counts = {
    'Landing': funnel_df['stage_1_landing'].sum(),
    'Signup': funnel_df['stage_2_signup'].sum(),
    'Product_View': funnel_df['stage_3_product_view'].sum(),
    'Add_to_Cart': funnel_df['stage_4_add_to_cart'].sum(),
    'Purchase': funnel_df['stage_5_purchase'].sum()
}

for i, (stage, count) in enumerate(stage_counts.items()):
    conversion_rate = (count / total_users) * 100
    if i > 0:
        prev_stage_count = list(stage_counts.values())[i-1]
        stage_to_stage_rate = (count / prev_stage_count) * 100 if prev_stage_count > 0 else 0
        drop_off_rate = 100 - stage_to_stage_rate
        print(f"{stage:15s}: {count:6d} users ({conversion_rate:5.2f}%) | Stage conversion: {stage_to_stage_rate:5.2f}% | Drop-off: {drop_off_rate:5.2f}%")
    else:
        print(f"{stage:15s}: {count:6d} users ({conversion_rate:5.2f}%)")

print("\n" + "="*60)
print(f"Overall Conversion Rate (Landing → Purchase): {(stage_counts['Purchase']/stage_counts['Landing'])*100:.2f}%")
print(f"Total Revenue: ${funnel_df['purchase_value'].sum():,.2f}")
print(f"Average Order Value: ${funnel_df['purchase_value'].mean():.2f}")
print("="*60)
