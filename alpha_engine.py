import pandas as pd
import numpy as np

class AlphaEngine:
    def __init__(self, historical_baseline=None):
        """
        Engine for calculating 'Qualitative Alpha' from freight activity.
        """
        self.baseline = historical_baseline or 10.0 # Standard mean activity

    def calculate_activity_index(self, window_data):
        """
        Calculate an index score based on current vs baseline activity.
        """
        if window_data.empty:
            return 0.0
        
        current_mean = window_data['activity'].mean()
        index = (current_mean / self.baseline) * 100
        return round(index, 2)

    def detect_trends(self, full_history):
        """
        Analyze if supply chain velocity is accelerating or decelerating.
        """
        if len(full_history) < 20:
            return "Neutral (Insufficient Data)"
        
        # Simple slope of activity counts
        activities = full_history['activity'].values
        slope = np.polyfit(np.arange(len(activities)), activities, 1)[0]
        
        if slope > 0.1:
            return "Bullish (Increasing Logistics Velocity)"
        elif slope < -0.1:
            return "Bearish (Decelerating Volume)"
        return "Stable"

    def get_alpha_signal(self, current_index, trend):
        """
        Generate a qualitative alpha recommendation.
        """
        if current_index > 120 and "Bullish" in trend:
            return "Strong Expansion - Positive Alpha Catalyst"
        elif current_index < 80 and "Bearish" in trend:
            return "Logistical Contraction - Negative Alpha Outlook"
        return "Market-Weight Logistical Flow"

if __name__ == "__main__":
    # Test engine
    engine = AlphaEngine()
    test_df = pd.DataFrame({'activity': [10, 12, 11, 14, 15, 13, 16]})
    idx = engine.calculate_activity_index(test_df)
    print(f"Test Index: {idx}")
