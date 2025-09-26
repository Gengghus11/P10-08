#Project: Apple Stock Trading Analysis

#Team: Team (P10-08):
#Voo Geng Loong (2500633)
#Chang Wen Lin Sarah (2501932)
#KHOR JUN KIT (2501028)
#AMOS TAY ZHI SHENG (2500527)

# We have to import the neccessary API and library need to open up stocks
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

apple = yf.download("AAPL", start = "2023-01-01", end = "2025-01-01")
google = yf.download("GOOGL", start = "2023-01-01", end = "2025-01-01")
intel = yf.download("INTC", start = "2023-01-01", end = "2025-01-01")
amd = yf.download("AMD", start = "2023-01-01", end = "2025-01-01")
nvdia = yf.download("NVDA", start = "2023-01-01", end = "2025-01-01")

#Selecting of Stock Trading Analysis
print("Hi please select your stock: ")
print("1. Apple")
print("2. Google")
print("3. Intel")
print("4. AMD")
print("5. Nvidia")

option = input("You have selected option: ")

if option == "1":
    print("You have selected Apple")
    print(apple.head())  # print only first 5 rows to avoid too long output

    # Apple Stock Price
    plt.figure(figsize=(14,10))
    plt.title("Apple Stock Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.plot(apple.index, apple["Open"], label="Open", color="blue", linestyle="--")
    plt.plot(apple.index, apple["High"], label="High", color="green")
    plt.plot(apple.index, apple["Low"], label="Low", color="red")
    plt.plot(apple.index, apple["Close"], label="Close", color="black")
    plt.grid(True)
    plt.legend()
    plt.show()

    # Apple On Balacne Volume (OBV)
    plt.figure(figsize=(14,10))
    apple["OBV"] = (np.sign(apple["Close"].diff()) * apple["Volume"]).fillna(0).cumsum()
    plt.plot(apple.index, apple["OBV"], label="OBV", color="brown")
    plt.grid(True)
    plt.legend()
    plt.show()

elif option == "2":
    print("You have selected Google")
    print(google)

    #Google Stock Price
    plt.figure(figsize=(14,10))
    plt.title("Google Stock Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.plot(google.index, google["Open"], label="Open", color="blue", linestyle="--")
    plt.plot(google.index, google["High"], label="High", color="green")
    plt.plot(google.index, google["Low"], label="Low", color="red")
    plt.plot(google.index, google["Close"], label="Close", color="black")
    plt.grid(True)
    plt.legend()
    plt.show()

    #Google On Balacne Volume (OBV)
    plt.figure(figsize=(14,10))
    google["OBV"] = (np.sign(google["Close"].diff()) * google["Volume"]).fillna(0).cumsum()
    plt.plot(google.index, google["OBV"], label="OBV", color="brown")
    plt.grid(True)
    plt.legend()
    plt.show()

elif option == "3":
    print("You have selected Intel")
    print(intel)

    #Intel Stock Price
    plt.figure(figsize=(14,10))
    plt.title("Intel Stock Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.plot(intel.index, intel["Open"], label="Open", color="blue", linestyle="--")
    plt.plot(intel.index, intel["High"], label="High", color="green")
    plt.plot(intel.index, intel["Low"], label="Low", color="red")
    plt.plot(intel.index, intel["Close"], label="Close", color="black")
    plt.grid(True)
    plt.legend()
    plt.show()

    #Intel On Balacne Volume (OBV)
    plt.figure(figsize=(14,10))
    intel["OBV"] = (np.sign(intel["Close"].diff()) * intel["Volume"]).fillna(0).cumsum()
    plt.plot(intel.index, intel["OBV"], label="OBV", color="brown")
    plt.grid(True)
    plt.legend()
    plt.show()

elif option == "4":
    print("You have selected AMD")
    print(amd)

    #AMD Stock Price
    plt.figure(figsize=(14,10))
    plt.title("AMD Stock Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.plot(amd.index, amd["Open"], label="Open", color="blue", linestyle="--")
    plt.plot(amd.index, amd["High"], label="High", color="green")
    plt.plot(amd.index, amd["Low"], label="Low", color="red")
    plt.plot(amd.index, amd["Close"], label="Close", color="black")
    plt.grid(True)
    plt.legend()
    plt.show()

    #AMD On Balacne Volume (OBV)
    plt.figure(figsize=(14,10))
    amd["OBV"] = (np.sign(amd["Close"].diff()) * amd["Volume"]).fillna(0).cumsum()
    plt.plot(amd.index, amd["OBV"], label="OBV", color="brown")
    plt.grid(True)
    plt.legend()
    plt.show()

elif option == "5":
    print("You have selected Nvidia")
    print(nvdia)

    #Nvdia Stock Price
    plt.figure(figsize=(14,10))
    plt.title("Apple Stock Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.plot(nvdia.index, nvdia["Open"], label="Open", color="blue", linestyle="--")
    plt.plot(nvdia.index, nvdia["High"], label="High", color="green")
    plt.plot(nvdia.index, nvdia["Low"], label="Low", color="red")
    plt.plot(nvdia.index, nvdia["Close"], label="Close", color="black")
    plt.grid(True)
    plt.legend()
    plt.show()

    #Nvdia On Balacne Volume (OBV)
    plt.figure(figsize=(14,10))
    nvdia["OBV"] = (np.sign(nvdia["Close"].diff()) * nvdia["Volume"]).fillna(0).cumsum()
    plt.plot(nvdia.index, ["OBV"], label="OBV", color="brown")
    plt.grid(True)
    plt.legend()
    plt.show()

else:
    print("Invalid option. Please try again!")