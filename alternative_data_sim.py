import pandas as pd
import numpy as np

class AlternativeDataSim:
    """
    Simulation of non-visual alternative data sources to provide multi-factor Alpha.
    Includes Fuel Prices, Global Shipping Indices (BDI), and Macro KPIs.
    """
    def generate_macro_indicators(self, periods=50):
        dates = pd.date_range(end=pd.Timestamp.now(), periods=periods, freq='D')
        
        data = {
            'date': dates,
            'fuel_price_index': np.random.normal(100, 5, periods).cumsum() / 10,
            'global_shipping_index': np.random.normal(2000, 50, periods).cumsum() / 20,
            'logistical_labor_cost': np.linspace(50, 65, periods) + np.random.normal(0, 1, periods)
        }
        return pd.DataFrame(data)

    def calculate_correlation(self, activity_df, macro_df):
        """
        Simulate correlation between visual supply chain activity and macro data.
        In a real research scenario, this would use Spearman/Pearson correlation.
        """
        # Align lengths for demo
        min_len = min(len(activity_df), len(macro_df))
        activity = activity_df['activity'].tail(min_len).values
        fuel = macro_df['fuel_price_index'].tail(min_len).values
        
        correlation = np.corrcoef(activity, fuel)[0, 1]
        return round(float(correlation), 3)

if __name__ == "__main__":
    sim = AlternativeDataSim()
    macro = sim.generate_macro_indicators()
    print(f"Sample Macro Data:\n{macro.head()}")
