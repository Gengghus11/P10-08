from flask import Flask, render_template, request, redirect, url_for
import yfinance as yf
import pandas as pd
import math
from collections import deque

app = Flask(__name__)

STOCKS = {
    "AAPL": "Apple",
    "GOOGL": "Google",
    "INTC": "Intel",
    "AMD": "AMD",
    "NVDA": "Nvidia",
}

# default value for inputs
DEFAULT_START = "2023-01-01"
DEFAULT_END = "2025-01-01"
DEFAULT_SMA = 5 

# fetch data from yfinance and ensure date is a column
def fetch_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end, progress=False)
    if not df.empty and "Date" not in df.columns:
        df = df.reset_index()
    return df

# calculate the max profit with multiple transactions allowed
def max_profit(prices):
    profit = 0.0
    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            profit += prices[i] - prices[i - 1]
    return float(profit)

# compute the sma 
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

# compute the steaks count of the stock graph
def compute_streak_stats(dates, closes):

    # check to see if there are more than 1 closing price, else there wont be a trend to identify with just 1 data
    if len(closes) < 2:
        return {
            "up_count": 0, 
            "up_total_days": 0, 
            "up_longest_len": 0,
            "up_longest_start": None, 
            "up_longest_end": None,
            "down_count": 0, 
            "down_total_days": 0, 
            "down_longest_len": 0,
            "down_longest_start": None,
            "down_longest_end": None,
            "current_dir": None, 
            "current_len": 0,
        }

    date_time = pd.to_datetime(dates).tolist()
    close_values = pd.to_numeric(closes, errors="coerce").tolist()

    segments = []
    current_direction = None
    current_start = None
    current_length = 0

    for i in range(1, len(close_values)):
        if close_values[i] is None or close_values[i-1] is None:
            step_direction = None
        else:
            if close_values[i] > close_values[i-1]:
                step_direction = "up"
            elif close_values[i] < close_values[i-1]:
                step_direction = "down"
            else:
                step_direction = None

        if step_direction is None:
            if current_direction is not None and current_length > 0:
                segments.append({
                    "direction": current_direction,
                    "start_index": current_start,
                    "end_index": i - 1,
                    "length": current_length
                })
            current_direction = None
            current_start = None
            current_length = 0
        else:
            if current_direction is None:
                current_direction = step_direction
                current_start = i - 1
                current_length = 1
            elif step_direction == current_direction:
                current_length += 1
            else:
                segments.append({
                    "direction": current_direction,
                    "start_index": current_start,
                    "end_index": i - 1,
                    "length": current_length
                })
                current_direction = step_direction
                current_start = i - 1
                current_length = 1

    if current_direction is not None and current_length > 0:
        segments.append({
            "direction": current_direction,
            "start_index": current_start,
            "end_index": len(close_values) - 1,
            "length": current_length
        })

    up_segments = []
    for s in segments:
        if s["direction"] == "up":
            up_segments.append(s)

    down_segments = []
    for s in segments:
        if s["direction"] == "down":
            down_segments.append(s)

    def longest(segments):
        if not segments:
            return 0, None, None
        longest_steaks = max(segments, key=lambda s: s["length"])
        return longest_steaks["length"], date_time[longest_steaks["start_index"]].strftime("%Y-%m-%d"), date_time[longest_steaks["end_index"]].strftime("%Y-%m-%d")

    up_longest_len, up_longest_start, up_longest_end = longest(up_segments)
    down_longest_len, down_longest_start, down_longest_end = longest(down_segments)

    up_total_days = 0
    for s in up_segments:
        if True:
            up_total_days += s["length"]

    down_total_days = 0
    for s in down_segments:
        if True:
            down_total_days += s["length"]

    current_dir = None
    current_len = 0
    if segments:
        last = segments[-1]
        if last["end_index"] == len(close_values) - 1:
            current_dir = last["direction"]
            current_len = last["length"]

    return {
        "up_count": len(up_segments),
        "up_total_days": up_total_days,
        "up_longest_len": up_longest_len,
        "up_longest_start": up_longest_start,
        "up_longest_end": up_longest_end,
        "down_count": len(down_segments),
        "down_total_days": down_total_days,
        "down_longest_len": down_longest_len,
        "down_longest_start": down_longest_start,
        "down_longest_end": down_longest_end,
        "current_dir": current_dir,
        "current_len": current_len,
    }

# routers
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ticker = request.form.get("ticker", "AAPL")
        start = request.form.get("start", DEFAULT_START)
        end = request.form.get("end", DEFAULT_END)
        sma_window = request.form.get("sma_window", str(DEFAULT_SMA))

        enable_sma2 = str(request.form.get("enable_sma2", "0")).strip().lower() in {"1", "true", "on", "yes", "y"}
        sma_window2 = request.form.get("sma_window2", "").strip() if enable_sma2 else ""

        return redirect(url_for(
            "stock",
            ticker=ticker,
            start=start,
            end=end,
            sma_window=sma_window,
            enable_sma2="1" if enable_sma2 else "0",
            sma_window2=sma_window2,
        ))

    return render_template(
        "index.html",
        tickers=STOCKS,
        default_start=DEFAULT_START,
        default_end=DEFAULT_END,
        selected_ticker="AAPL",
        default_sma_window=DEFAULT_SMA,
        default_enable_sma2=False,
        default_sma_window2=""
    )

@app.route("/stock")
def stock():
    ticker = request.args.get("ticker", "AAPL")
    start = request.args.get("start", DEFAULT_START)
    end = request.args.get("end", DEFAULT_END)

    try:
        sma_window = int(request.args.get("sma_window", DEFAULT_SMA))
    except (TypeError, ValueError):
        sma_window = DEFAULT_SMA
    sma_window = max(2, min(250, sma_window))

    enable_sma2 = str(request.args.get("enable_sma2", "0")).strip().lower() in {"1", "true", "on", "yes", "y"}
    sma_window2 = None
    if enable_sma2:
        try:
            sma_window2 = int(request.args.get("sma_window2", ""))
            sma_window2 = max(2, min(250, sma_window2))
        except (TypeError, ValueError):
            sma_window2 = None

    if ticker not in STOCKS:
        return redirect(url_for("index"))

    df = fetch_data(ticker, start, end)
    
    if df.empty:
        plot_data = None
        table_html = "<p>No data returned for that date range.</p>"
        last_close = None
        close_percentage_change = None
        max_profit_value = None

        # default streaks (0)
        streaks = compute_streak_stats(pd.Series(dtype="datetime64[ns]"), pd.Series(dtype="float"))
    else:
        # drop 1 column as yfinance render results in multiindex
        df_for_chart = df.copy()
        df_for_chart.columns = df_for_chart.columns.droplevel(1)

        # compute the percentage change based on the closing value
        last_close = float(df_for_chart["Close"].iloc[-1])
        first_close = float(df_for_chart["Close"].iloc[0])
        if first_close:
            close_percentage_change = ((last_close / first_close) - 1) * 100
        else:
            None

        # clean close series
        close_series = pd.to_numeric(df_for_chart["Close"], errors="coerce")

        # make numeric 
        daily_return_percentage = (close_series.pct_change() * 100.0)

        # values to be passed to chart.js
        daily_return_values = daily_return_percentage.tolist()                     

        # format the daily returns column to 2dp for a nicer visuals
        df["Daily Return (%)"] = daily_return_percentage.map(lambda x: f"{x:+.2f}%" if pd.notnull(x) else "")

        # computing the max profit based on the max_profit function defined earlier
        closing_prices = close_series.tolist()
        max_profit_value = max_profit(closing_prices)

        # call the compute_sma function and compute the sma
        sma_values = compute_sma(closing_prices, sma_window)

        plot_data = {
            "labels": pd.to_datetime(df_for_chart["Date"]).dt.strftime("%Y-%m-%d").tolist(),
            "datasets": [
                {"label": "Open",  "data": df_for_chart["Open"].tolist(),  "borderColor": "blue",  "fill": False, "tension": 0.1},
                {"label": "Close", "data": df_for_chart["Close"].tolist(), "borderColor": "black", "fill": False, "tension": 0.1},
                {"label": "High",  "data": df_for_chart["High"].tolist(),  "borderColor": "green", "fill": False, "tension": 0.1},
                {"label": "Low",   "data": df_for_chart["Low"].tolist(),   "borderColor": "red",   "fill": False, "tension": 0.1},
                {
                    "type": "bar",
                    "label": "Daily Return (%)",
                    "data": daily_return_values,
                    "yAxisID": "y1",
                    "borderColor": "teal",
                    "backgroundColor": "rgba(0, 128, 128, 0.35)",
                },
            ],
        }

        # count the number of valid sma points and only display the sma graph if there are more than 1 valid points
        valid_points = 0
        for i in sma_values:
            if i is not None:
                valid_points += 1

        if valid_points >= 1:
            plot_data["datasets"].append({
                "label": f"{sma_window}-day SMA",
                "data": sma_values,
                "borderColor": "orange",
                "fill": False,
                "tension": 0.1,
                "borderDash": [5, 5],
            })

        # check to the checbox for sma2 to see if it has been checked, if checked compute the second sma else pass
        if enable_sma2 and (sma_window2 is not None):
            sma_vals2 = compute_sma(closing_prices, sma_window2)
        
            # count the number of valid sma points and only display the sma graph if there are more than 1 valid points
            valid_points2 = 0
            for i in sma_vals2:
                if i is not None:
                    valid_points2 += 1

            if valid_points2 >= 1:
                plot_data["datasets"].append({
                    "label": f"{sma_window2}-day SMA",
                    "data": sma_vals2,
                    "borderColor": "purple",
                    "fill": False,
                    "tension": 0.1,
                    "borderDash": [8, 4],
                })

        # only display the most recent 10 tables else the table will be too lengthy
        table_html = (
            df[["Date", "Open", "Close", "High", "Low", "Volume", "Daily Return (%)"]]
            .tail(10)
            .to_html(classes="table table-striped", index=False)
        )

        # streaks data
        streaks = compute_streak_stats(df_for_chart["Date"], close_series)

    return render_template(
        "stock.html",
        ticker=ticker,
        name=STOCKS[ticker],
        start=start,
        end=end,
        plot_data=plot_data,
        table_html=table_html,
        last_close=last_close,
        close_percentage_change=close_percentage_change,
        max_profit_value=max_profit_value,
        sma_window=sma_window,
        enable_sma2=enable_sma2,
        sma_window2=sma_window2,
        up_streak_count=streaks["up_count"],
        up_total_days=streaks["up_total_days"],
        up_longest_len=streaks["up_longest_len"],
        up_longest_start=streaks["up_longest_start"],
        up_longest_end=streaks["up_longest_end"],
        down_streak_count=streaks["down_count"],
        down_total_days=streaks["down_total_days"],
        down_longest_len=streaks["down_longest_len"],
        down_longest_start=streaks["down_longest_start"],
        down_longest_end=streaks["down_longest_end"],
        current_streak_dir=streaks["current_dir"],
        current_streak_len=streaks["current_len"],
    )

if __name__ == "__main__":
    app.run(debug=True)