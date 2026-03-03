import pandas as pd
import numpy as np
from scipy import stats

class AlphaEngine:
    def __init__(self, historical_baseline=15.0):
        """
        Research-grade Alpha Engine with statistical anomaly detection.
        """
        self.baseline = historical_baseline
        self.window_size = 30 # Rolling window for Z-Score calculation

    def calculate_z_score(self, current_value, history):
        """
        Determine how many standard deviations the current activity is from the mean.
        Standard research method for identifying supply chain shocks.
        """
        if len(history) < 5:
            return 0.0
        
        mean = history['activity'].mean()
        std = history['activity'].std()
        
        if std == 0:
            return 0.0
            
        z_score = (current_value - mean) / std
        return round(float(z_score), 3)

    def calculate_activity_index(self, window_data):
        if window_data.empty:
            return 0.0
        current_mean = window_data['activity'].mean()
        index = (current_mean / self.baseline) * 100
        return round(index, 2)

    def detect_trends(self, full_history):
        if len(full_history) < 10:
            return "Stabilizing..."
        
        activities = full_history['activity'].values
        # Using linear regression to detect velocity changes
        x = np.arange(len(activities))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, activities)
        
        if slope > 0.1 and p_value < 0.05:
            return "Statistically Significant Expansion"
        elif slope < -0.1 and p_value < 0.05:
            return "Statistically Significant Contraction"
        return "Neutral / Sideways Volume"

    def get_alpha_signal(self, z_score, trend):
        """
        Multi-factor alpha generation.
        """
        if z_score > 2.0 and "Expansion" in trend:
            return "ALPHA BUY: Supply Chain Hyper-Velocity"
        elif z_score < -2.0 and "Contraction" in trend:
            return "ALPHA SELL: Terminal Paralysis / Shock"
        elif abs(z_score) > 3.0:
            return "RESEARCH ALERT: Logistical Outlier Detected"
        return "Market Weight"

if __name__ == "__main__":
    # Test engine
    engine = AlphaEngine()
    test_df = pd.DataFrame({'activity': [10, 12, 11, 14, 15, 13, 16]})
    idx = engine.calculate_activity_index(test_df)
    print(f"Test Index: {idx}")
