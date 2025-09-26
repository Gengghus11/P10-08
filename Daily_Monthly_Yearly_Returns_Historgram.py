#Plots graphs for selected Daily/Monthly/Yearly Returns + Histogram graph (optional)
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Download stock data
apple = yf.download("AAPL", start="2023-01-01", end="2025-01-01")
google = yf.download("GOOGL", start="2023-01-01", end="2025-01-01")
intel = yf.download("INTC", start="2023-01-01", end="2025-01-01")
amd = yf.download("AMD", start="2023-01-01", end="2025-01-01")
nvdia = yf.download("NVDA", start="2023-01-01", end="2025-01-01")

# Selecting Stock
print("Hi, please select your stock: ")
print("1. Apple")
print("2. Google")
print("3. Intel")
print("4. AMD")
print("5. Nvidia")

option = input("You have selected option: ")

# Calculate selected returns
def plot_returns(df, stock_name):
    print("Choose return frequency: ")
    print("1. Daily")
    print("2. Monthly")
    print("3. Yearly")
    freq_option = input("Enter option (1/2/3): ")

    if freq_option == "1":
        returns = df["Close"].pct_change()
        freq_name = "Daily"
    elif freq_option == "2":
        monthly_close = df["Close"].resample("M").last()
        returns = monthly_close.pct_change()
        freq_name = "Monthly"
    elif freq_option == "3":
        yearly_close = df["Close"].resample("Y").last()
        returns = yearly_close.pct_change()
        freq_name = "Yearly"
    else:
        print("Invalid option. Showing daily returns by default.")
        returns = df["Close"].pct_change()
        freq_name = "Daily"

    # Drop NA values for plotting
    returns = returns.dropna()

    # Display sample
    print(f"\nSample of {freq_name} Returns:")
    print(returns.head(10))

    # Plot line chart of returns
    plt.figure(figsize=(12, 6))
    plt.plot(returns.index, returns, color="green", alpha=0.7)
    plt.title(f"{stock_name} {freq_name} Returns")
    plt.xlabel("Date")
    plt.ylabel(f"{freq_name} Return (%)")
    plt.grid(True)
    plt.show()

    # Plot histogram of returns
    plt.figure(figsize=(10, 6))
    plt.hist(returns, bins=50, color="skyblue", edgecolor="black")
    plt.title(f"{stock_name} {freq_name} Returns Distribution")
    plt.xlabel(f"{freq_name} Return (%)")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()

# Handle stock selection
stocks = {
    "1": ("Apple", apple),
    "2": ("Google", google),
    "3": ("Intel", intel),
    "4": ("AMD", amd),
    "5": ("Nvidia", nvdia)}

if option in stocks:
    name, df = stocks[option]
    print(f"You have selected {name}")
    plot_returns(df, name)
else:
    print("Invalid option. Please try again!")