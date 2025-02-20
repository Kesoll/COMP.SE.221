import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import seaborn as sns
import os
from dotenv import load_dotenv

class EnergyDataAnalyzer:
    """
    A class to analyze the correlation between electricity prices and wind power production.
    Uses Finnish energy data as an example.
    """

    def __init__(self):
        load_dotenv()  # Load environment variables
        self.price_base_url = "https://api.porssisahko.net/v1"
        self.fingrid_base_url = "https://data.fingrid.fi/api"
        self.fingrid_api_key = os.getenv("FINGRID_API_KEY", "your-api-key-here")

    def get_electricity_prices(self) -> pd.DataFrame:
        """
        Fetch hourly electricity prices from porssisahko.net using the latest-prices endpoint.
        """
        url = f"{self.price_base_url}/latest-prices.json"
        print(f"Requesting electricity prices from: {url}")

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            prices = pd.DataFrame(data['prices'])
            prices['startDate'] = pd.to_datetime(prices['startDate'])
            prices.set_index('startDate', inplace=True)
            return prices[['price']]
        else:
            raise Exception(f"Failed to fetch price data: {response.status_code}")

    def get_wind_power(self, start_time, end_time):
        dataset_id = 75  # Wind power generation dataset ID
        url = f"https://data.fingrid.fi/api/datasets/{dataset_id}/data"
        headers = {
            "x-api-key": self.fingrid_api_key,
            "Accept": "application/json"
        }
        params = {
            "startTime": start_time,
            "endTime": end_time,
            "format": "json",  # Ensure the format is JSON
        }

        response = requests.get(url, headers=headers, params=params)
        print(response.url)  # Print the URL for debugging

        if response.status_code == 200:
            response_json = response.json()
            print(response_json.keys())  # Print the keys of the response JSON for debugging

            # Assuming the data is under a specific key in the JSON
            if 'data' in response_json:
                wind_data = pd.DataFrame(response_json['data'])
                wind_data['startTime'] = pd.to_datetime(wind_data['startTime'])
                wind_data.set_index('startTime', inplace=True)
                return wind_data[['value']]
            else:
                raise Exception("Unexpected JSON structure: 'data' key not found")
        else:
            raise Exception(f"Failed to fetch wind data: {response.status_code}")



    def analyze_correlation(self, days: int = 7):
        """
        Analyze the correlation between electricity prices and wind power production
        for the specified number of days.
        """
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        # Format dates for API calls
        start_str = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_str = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        print(f"Fetching data from {start_str} to {end_str}")

        # Fetch data
        prices_df = self.get_electricity_prices()
        wind_df = self.get_wind_power(start_str, end_str)

        # Resample wind data to hourly intervals to match price data
        wind_df = wind_df.resample('H').mean()

        # Merge datasets
        combined_df = prices_df.join(wind_df, how='inner')

        # Calculate correlation
        correlation = combined_df['price'].corr(combined_df['value'])

        # Create visualization
        plt.figure(figsize=(12, 6))
        sns.scatterplot(data=combined_df, x='value', y='price')
        plt.title(f'Electricity Price vs Wind Power Production\nCorrelation: {correlation:.2f}')
        plt.xlabel('Wind Power Production (MW)')
        plt.ylabel('Electricity Price (€/MWh)')
        plt.tight_layout()

        return combined_df, correlation, plt

if __name__ == "__main__":
    analyzer = EnergyDataAnalyzer()
    df, corr, plot = analyzer.analyze_correlation(days=7)
    print(f"Correlation coefficient: {corr}")
    plot.show()
