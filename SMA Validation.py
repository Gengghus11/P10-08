import math
from collections import deque

# SMA function from main code (Line 40)
def compute_sma(prices, k: int):
    n = len(prices)
    if n == 0:
        return []
    if k <= 1:
        out = []
        for x in prices:
            if x is None or (isinstance(x, float) and math.isnan(x)):
                out.append(None)
            else:
                out.append(float(x))
        return out
    
    res = [None] * n
    q = deque()
    window_sum, nan_count = 0.0, 0

    for i, x in enumerate(prices):
        q.append(x)
        if x is None or (isinstance(x, float) and math.isnan(x)):
            nan_count += 1
        else:
            window_sum += float(x)
        if len(q) > k:
            old = q.popleft()
            if old is None or (isinstance(old, float) and math.isnan(old)):
                nan_count -= 1
            else:
                window_sum -= float(old)
        if len(q) == k and nan_count == 0:
            res[i] = window_sum / k

    return res

#Test case ([closing price], sma_window): Input different closing prices and sma window and run code
# Test case 1: [10, 20, 30, 40, 50], 3
# Test case 2: [185.64, 184.25, 181.91, 181.18, 185.56], 3
# Test case 3: [10, 20, 30], 5
# Test case 4: [10, None, 30, 40, 50], 3
# Test case 5: [0, 0, 10, 20, 30], 3
closing_prices = [10, 20, 30]
sma_window = 5

# call the compute_sma function and compute the sma from main code (Line 300)
sma_values = compute_sma(closing_prices, sma_window)

print("Code SMA result:", sma_values)

# Validate with pandas
import pandas as pd

# Compute SMA using pandas
series = pd.Series(closing_prices)
pandas_sma = series.rolling(window=sma_window, min_periods=sma_window).mean().tolist()

print("Pandas SMA result:", pandas_sma)