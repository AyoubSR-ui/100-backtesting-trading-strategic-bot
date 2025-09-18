from binance.client import Client
import pandas as pd
from datetime import datetime

# Initialize the client (no API keys needed for public data)
client = Client()

# Define your custom date range
symbol = "BTCUSDT"
interval = Client.KLINE_INTERVAL_1HOUR
start_date = "1 Jan, 2023"
end_date = "10 Jan, 2023"

# Fetch historical data
klines = client.get_historical_klines(symbol, interval, start_str=start_date, end_str=end_date)

# Convert to DataFrame
df = pd.DataFrame(klines, columns=[
    "timestamp", "open", "high", "low", "close", "volume",
    "close_time", "quote_asset_volume", "number_of_trades",
    "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
])

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
df.set_index("timestamp", inplace=True)

# Save to CSV if needed
df.to_csv("BTCUSDT_1H_custom_range.csv")
print("✅ Data saved to CSV.")
