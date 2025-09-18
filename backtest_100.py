import json
import requests
import random
import time
from datetime import datetime, timedelta

# Load webhook config
with open("webhook_config.json", "r") as f:
    webhook_config = json.load(f)
WEBHOOK_URL = webhook_config["webhook_url"]

# Standard Fibonacci levels
FIB_LEVELS = {
    "-0.2": -0.2,
    "0": 0,
    "0.236": 0.236,
    "0.5": 0.5,
    "0.618": 0.618,
    "0.786": 0.786,
    "1": 1,
    "1.2": 1.2
}

def simulate_market_data():
    """Generate realistic market data with trends"""
    base_price = random.uniform(29000, 33000)
    trend = random.choice(["up", "down", "neutral"])
    
    if trend == "up":
        low = base_price - random.uniform(300, 800)
        high = base_price + random.uniform(800, 1500)
    elif trend == "down":
        low = base_price - random.uniform(800, 1500)
        high = base_price + random.uniform(300, 800)
    else:  # neutral
        low = base_price - random.uniform(500, 1000)
        high = base_price + random.uniform(500, 1000)
    
    return low, high, base_price

def generate_fibonacci_levels(low, high):
    """Generate standard Fibonacci retracement levels"""
    diff = high - low
    levels = {}
    for name, value in FIB_LEVELS.items():
        levels[name] = round(low + value * diff, 2)
    return levels

def is_session_exhausted(price_path, fib):
    """Check if price closed outside -0.2 or 1.2 fib levels (session end)"""
    for price in price_path:
        if price < fib["1.2"] or price > fib["-0.2"]:
            return True
    return False

def is_valid_fbo(price_path, fib, direction):
    """Enhanced FBO validation according to strategy rules"""
    zone_tests = 0
    rejection_confirmed = False
    
    support_zone = (fib["0"], fib["0.236"])
    resistance_zone = (fib["0.786"], fib["1"])
    
    for i in range(1, len(price_path)):
        prev_close = price_path[i-1]
        current_close = price_path[i]
        
        if direction == "long":
            # Check for tests of support zone (wick into zone)
            if support_zone[0] <= current_close <= support_zone[1]:
                zone_tests += 1
            # Check for rejection (wick below but close above)
            if current_close < support_zone[0] and prev_close > support_zone[0]:
                rejection_confirmed = True
                
        elif direction == "short":
            # Check for tests of resistance zone (wick into zone)
            if resistance_zone[0] <= current_close <= resistance_zone[1]:
                zone_tests += 1
            # Check for rejection (wick above but close below)
            if current_close > resistance_zone[1] and prev_close < resistance_zone[1]:
                rejection_confirmed = True
    
    return zone_tests >= 3 and rejection_confirmed

def determine_entry(price_path, fib, direction):
    """Find first candle open after FBO confirmation"""
    if direction == "long":
        zone = (fib["0"], fib["0.236"])
        for i in range(1, len(price_path)):
            if price_path[i] > zone[1]:  # Close above zone
                return round(price_path[i] + random.uniform(10, 50), 2)  # Next open
    else:
        zone = (fib["0.786"], fib["1"])
        for i in range(1, len(price_path)):
            if price_path[i] < zone[0]:  # Close below zone
                return round(price_path[i] - random.uniform(10, 50), 2)  # Next open
    return None

# Main backtest loop
time_pointer = datetime(2024, 1, 1, 9, 0)
for i in range(100):
    # 1. Generate market data
    low, high, base_price = simulate_market_data()
    fib = generate_fibonacci_levels(low, high)
    
    # 2. Simulate candle closes (50 candles)
    price_path = []
    current_price = base_price
    for _ in range(50):
        candle_close = current_price + random.uniform(-200, 200)
        price_path.append(round(candle_close, 2))
        current_price = candle_close
    
    # 3. Check session exhaustion (NEW CORRECTED LOGIC)
    if is_session_exhausted(price_path, fib):
        print(f"#{i+1}: Session exhausted (closed outside 1.2/-0.2 Fib)")
        time_pointer += timedelta(hours=1)
        continue
    
    # 4. Determine direction based on price action
    if max(price_path) > fib["0.786"] and min(price_path) < fib["0.236"]:
        direction = random.choice(["long", "short"])
    elif max(price_path) > fib["0.786"]:
        direction = "short"
    else:
        direction = "long"
    
    # 5. Validate FBO pattern
    if not is_valid_fbo(price_path, fib, direction):
        print(f"#{i+1}: Invalid FBO pattern")
        time_pointer += timedelta(hours=1)
        continue
    
    # 6. Determine entry price
    entry = determine_entry(price_path, fib, direction)
    if entry is None:
        print(f"#{i+1}: No valid entry point")
        time_pointer += timedelta(hours=1)
        continue
    
    # 7. Calculate stop loss and take profit
    if direction == "long":
        stop = round(fib["0"] - 0.1 * (fib["0.236"] - fib["0"]), 2)
        exit_price = round(entry + (entry - stop), 2)
    else:
        stop = round(fib["1"] + 0.1 * (fib["1"] - fib["0.786"]), 2)
        exit_price = round(entry - (stop - entry), 2)
    
    # 8. Prepare and send webhook
    payload = {
        "symbol": "BTCUSDT",
        "timestamp": time_pointer.strftime("%Y-%m-%d %H:%M"),
        "entry": entry,
        "stop": stop,
        "exit": exit_price,
        "signal": direction,
        "fib_levels": fib
    }
    
    print(f"🚀 #{i+1} {direction.upper()} | Entry: {entry} | SL: {stop} | TP: {exit_price}")
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=5)
        print(f"Webhook status: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Webhook error: {str(e)}")
    
    # 9. Move time forward and pause
    time_pointer += timedelta(hours=1)
    time.sleep(1.5)

print("Backtest completed!")














