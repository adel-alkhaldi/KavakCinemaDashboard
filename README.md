# Kavak Cinema Recovery Dashboard

An interactive Streamlit dashboard for simulating and analyzing profit recovery initiatives at Kavak Cinema.

## Features
- **Interactive Levers**: Adjust parameters to simulate different operational scenarios
- **Real-Time Calculations**: Instant profit impact analysis across 4 strategic initiatives
- **Visual Analytics**: Waterfall charts and metric cards for clear performance tracking
- **Deep Dive Tabs**: Detailed breakdowns for each operational initiative

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the dashboard**:
   ```bash
   streamlit run app.py / python -m streamlit run app.py
   ```

3. **Open in browser**: The app will automatically open at `http://localhost:8501`

## Strategic Initiatives

1. **Combo Promotions**: Bundle Ticket + Popcorn + Soda with discount incentives
2. **Delivery App Integration**: Expand F&B sales through delivery platforms like Talabat
3. **Food Quality Control**: Improve food quality to boost in-cinema purchase rates
4. **Operational Efficiencies**: Streamline concession operations and reduce overhead

## Configuration

All baseline metrics and profit calculations are defined in `app.py`. Modify the constants at the top of the file to adjust baseline data:
- `BASELINE_PROFIT`: Starting profit reference point
- `TOTAL_CUSTOMERS`: Total customer transactions
- `PROFIT_*`: Individual product profit margins

## Requirements
- Python 3.8+
- streamlit
- pandas
- plotly
