
# Save the dataset
funnel_df.to_csv('marketing_funnel_data.csv', index=False)
print("✓ Saved: marketing_funnel_data.csv")

# Create a summary statistics file
print("\nGenerating data summary...")
print(f"\nFirst few rows preview:")
print(funnel_df.head())
print(f"\nColumn types:")
print(funnel_df.dtypes)
print(f"\nMissing values:")
print(funnel_df.isnull().sum())
