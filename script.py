
# First, let's create the synthetic dataset generation script
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
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

print("Starting synthetic data generation...")
print(f"Target users: {NUM_USERS}")
print(f"Date range: {START_DATE.date()} to {END_DATE.date()}")
