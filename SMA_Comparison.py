#Plots a graph for selected Stock Closing Price with SMA Calculation
#Can compare with a second SMA window (optional)

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
print("Hi please select your stock: ")
print("1. Apple")
print("2. Google")
print("3. Intel")
print("4. AMD")
print("5. Nvidia")

option = input("You have selected option: ")

# Ask for SMA input
sma1 = int(input("Please enter SMA window: "))
compare = input("Do you want to compare with a second SMA window? (yes/no): ").strip().lower()

sma2 = None
if compare == "yes":
    sma2 = int(input("Enter the second SMA window: "))

# Function to plot stock with 1 or 2 SMAs
def plot_stock_with_smas(df, stock_name, color, sma1, sma2=None):
    # First SMA
    df[f"SMA{sma1}"] = df["Close"].rolling(window=sma1).mean()

    plt.figure(figsize=(12, 8))
    plt.title(f"{stock_name} Stock Closing Price with SMA(s)")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")

    # Plot Closing Price
    plt.plot(df.index, df["Close"], label="Daily Closing Price", color=color)

    # Plot first SMA
    plt.plot(df.index, df[f"SMA{sma1}"], label=f"{sma1}-Day SMA", color="red", linestyle="--")

    # Plot second SMA if provided
    if sma2:
        df[f"SMA{sma2}"] = df["Close"].rolling(window=sma2).mean()
        plt.plot(df.index, df[f"SMA{sma2}"], label=f"{sma2}-Day SMA", color="blue", linestyle="--")

    plt.grid(True)
    plt.legend()
    plt.show()

# Handle stock selection
if option == "1":
    print("You have selected Apple")
    plot_stock_with_smas(apple, "Apple", "black", sma1, sma2)

elif option == "2":
    print("You have selected Google")
    plot_stock_with_smas(google, "Google", "blue", sma1, sma2)

elif option == "3":
    print("You have selected Intel")
    plot_stock_with_smas(intel, "Intel", "purple", sma1, sma2)

elif option == "4":
    print("You have selected AMD")
    plot_stock_with_smas(amd, "AMD", "orange", sma1, sma2)

elif option == "5":
    print("You have selected Nvidia")
    plot_stock_with_smas(nvdia, "Nvidia", "green", sma1, sma2)

else:
    print("Invalid option. Please try again!")