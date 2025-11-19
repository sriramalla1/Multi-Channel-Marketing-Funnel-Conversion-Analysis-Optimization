# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### Step 2: Generate Data

```bash
python 00_generate_data.py
```

**Expected output:**
- `marketing_funnel_data.csv` (75,000 rows, ~8MB)
- Console output showing funnel metrics

**Time:** ~30 seconds

### Step 3: Run Analysis Scripts

```bash
# Funnel analysis
python 01_funnel_analysis.py

# Attribution modeling
python 02_attribution_analysis.py

# Generate visualizations
python 03_visualizations.py
```

**Expected outputs:**
- 6 CSV files with analysis results
- 6 HTML interactive dashboards
- 2 PNG static charts

**Time:** ~2 minutes total

### Step 4: View Results

**Interactive Dashboards:**
Open these HTML files in your browser:
- `funnel_visualization.html` - Main funnel flow
- `channel_performance_dashboard.html` - Multi-metric channel view
- `channel_device_heatmap.html` - Conversion rate matrix
- `cohort_trends.html` - Time-series analysis
- `roi_bubble_chart.html` - Spend vs Revenue
- `dropoff_analysis.html` - Drop-off identification

**Data Files:**
Open these CSV files in Excel/Google Sheets:
- `channel_performance_metrics.csv`
- `cohort_analysis.csv`
- `attribution_model_comparison.csv`
- `channel_roi_metrics.csv`
- `budget_allocation_recommendations.csv`

---

## 📊 Understanding the Output

### Key Files Explained

**1. marketing_funnel_data.csv**
- Raw data with 75,000 user sessions
- Contains: user_id, channel, device, funnel stages, timestamps, revenue
- Use for: Custom analysis, filtering, deep dives

**2. channel_performance_metrics.csv**
| Column | Description |
|--------|-------------|
| Channel | Marketing channel name |
| Sessions | Total user sessions |
| Signups | Users who signed up |
| Purchases | Completed purchases |
| Signup Rate | % of sessions that signed up |
| Conversion Rate | % of sessions that purchased |
| Revenue | Total revenue generated |
| Revenue/User | Average revenue per session |

**3. channel_roi_metrics.csv**
| Column | Description |
|--------|-------------|
| Channel | Marketing channel name |
| Spend | Total marketing spend |
| Revenue | Revenue generated |
| ROAS | Return on ad spend (Revenue/Spend) |
| ROI | Return on investment % |
| CPA | Cost per acquisition |

**4. budget_allocation_recommendations.csv**
- Current vs Optimal budget split by channel
- Dollar amounts to shift between channels
- Projected revenue impact

---

## 🔍 Interpreting Results

### Funnel Metrics

**Overall Conversion Rate: 15.86%**
- **Meaning:** 15.86% of visitors complete a purchase
- **Benchmark:** Industry average is 2-5%
- **Assessment:** Strong performance

**Biggest Drop-off: Add to Cart → Purchase (42.35%)**
- **Meaning:** 42% of users abandon at checkout
- **Benchmark:** Industry average is 69%
- **Assessment:** Better than average but still opportunity

### Channel Performance

**High ROAS (4.0x+):**
- Channels generating $4+ for every $1 spent
- **Action:** Increase budget allocation

**Low ROAS (1.5x or below):**
- Channels barely breaking even
- **Action:** Reduce spend or optimize targeting

### Device Insights

**Desktop > Mobile conversion (3x gap):**
- **Meaning:** Mobile users struggle to convert
- **Action:** Prioritize mobile UX improvements

---

## 🛠️ Customization Options

### Modify Data Generation

Edit `00_generate_data.py` to change:

```python
# Number of users
NUM_USERS = 100000  # Change from 75000

# Date range
START_DATE = datetime(2023, 1, 1)  # Change year
END_DATE = datetime(2024, 12, 31)

# Channel distribution
CHANNELS = {
    'Organic Search': {'weight': 0.30, 'conversion_multiplier': 1.5},
    # Adjust weights and multipliers
}

# Base conversion rates
BASE_RATES = {
    'landing_to_signup': 0.45,  # Increase from 0.40
    'cart_to_purchase': 0.40,   # Increase from 0.33
}
```

### Adjust Attribution Models

Edit `02_attribution_analysis.py`:

```python
# Change CPA assumptions
cpa_by_channel = {
    'Organic Search': 20,   # Adjust costs
    'Paid Search': 40,
    # ...
}

# Adjust time-decay rate
time_decay = time_decay_attribution(purchasers, decay_rate=0.7)
```

### Customize Visualizations

Edit `03_visualizations.py`:

```python
# Change color schemes
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']

# Adjust figure sizes
fig.update_layout(height=800, width=1200)

# Modify chart titles
title_text="Your Custom Title Here"
```

---

## 📈 Advanced Usage

### Filter Data for Specific Segments

```python
import pandas as pd

df = pd.read_csv('marketing_funnel_data.csv')

# Analyze only mobile users
mobile_df = df[df['device'] == 'Mobile']

# Analyze specific channel
email_df = df[df['channel'] == 'Email']

# Analyze specific month
jan_df = df[df['cohort_month'] == '2024-01']

# Analyze purchasers only
purchasers = df[df['stage_5_purchase'] == 1]
```

### Calculate Custom Metrics

```python
# Conversion rate by segment
segment_conv = df.groupby('age_group')['stage_5_purchase'].mean() * 100

# Revenue by device and channel
revenue_matrix = df.pivot_table(
    values='purchase_value',
    index='channel',
    columns='device',
    aggfunc='sum'
)

# Average time to purchase by channel
avg_time = df[df['stage_5_purchase']==1].groupby('channel')['total_journey_minutes'].mean()
```

### Export Custom Reports

```python
# Create custom summary
summary = df.groupby(['channel', 'device']).agg({
    'user_id': 'count',
    'stage_5_purchase': 'sum',
    'purchase_value': 'sum'
}).reset_index()

summary.to_csv('custom_summary.csv', index=False)
```

---

## 🐛 Troubleshooting

### Common Issues

**1. Module not found error**
```bash
pip install [missing-package]
```

**2. Data file not found**
```bash
# Make sure you ran data generation first
python 00_generate_data.py
```

**3. Charts not displaying**
- For HTML files: Open directly in browser (Chrome, Firefox, Safari)
- For PNG files: Use image viewer or presentation software

**4. Script runs but no output**
- Check that all previous scripts completed successfully
- Verify CSV files exist in same directory

**5. Memory error (large datasets)**
```python
# Reduce dataset size in 00_generate_data.py
NUM_USERS = 50000  # Instead of 75000
```

---

## 💡 Tips for Portfolio Presentation

### 1. Create a Highlights Folder
```bash
mkdir portfolio_highlights
cp funnel_visualization.html portfolio_highlights/
cp channel_performance_dashboard.html portfolio_highlights/
cp executive_summary.md portfolio_highlights/
cp static_funnel_chart.png portfolio_highlights/
```

### 2. Screenshot Key Insights
- Open HTML dashboards in browser
- Take screenshots of most impactful visualizations
- Annotate with key findings
- Add to portfolio presentation

### 3. Prepare 3-Minute Summary
**Structure:**
1. Problem statement (30 sec)
2. Analysis approach (30 sec)
3. Key findings (60 sec)
4. Recommendations & impact (60 sec)

### 4. Link to GitHub
```markdown
[View Complete Analysis](https://github.com/yourusername/marketing-funnel-analysis)
```

---

## 📚 Next Steps

**Immediate:**
1. ✅ Run all scripts successfully
2. ✅ Review output files
3. ✅ Read executive_summary.md
4. ✅ Explore interactive dashboards

**Within a Week:**
1. Customize analysis for your portfolio niche
2. Add custom visualizations
3. Write blog post explaining methodology
4. Practice presentation of findings

**For Interviews:**
1. Prepare to explain technical decisions
2. Be ready to discuss alternative approaches
3. Have examples of actionable recommendations
4. Demonstrate understanding of business impact

---

## 🆘 Need Help?

**Documentation:**
- README.md - Project overview
- executive_summary.md - Business insights
- technical_methodology.md - Technical details

**Code Comments:**
- Each script has inline documentation
- Functions have docstrings
- Complex logic explained

**Common Questions:**
Q: Can I use real data instead of synthetic?
A: Yes! Replace 00_generate_data.py with your data loader. Ensure columns match expected format.

Q: How do I add more channels?
A: Edit CHANNELS dictionary in 00_generate_data.py

Q: Can I change the funnel stages?
A: Yes, but requires modifying analysis scripts to match new stage structure

---

**Happy Analyzing! 🎉**
