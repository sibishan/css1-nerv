import os
import pprint
import yfinance as yf
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

# Use the 'Agg' backend for matplotlib to prevent interactive mode
matplotlib.use('Agg')

# Writes company profile information into a file for each symbol
def write_profiles(symbols):
    # Create 'profiles' directory if it doesn't exist
    if not os.path.exists('profiles'):
        os.makedirs('profiles')

    for symbol in symbols:
        # Get ticker information
        ticker = yf.Ticker(symbol)

        # Define file path for the profile
        filename = os.path.join('profiles', symbol + ".txt")

        # Write profile information to a text file
        with open(filename, 'w') as f:
            pprint.pprint(ticker.info, stream=f)

# Writes raw historical data into CSV file for each symbol
def write_raw_historical_data(symbols):
    # Create 'raw_historical_data' directory if it doesn't exist
    if not os.path.exists('raw_historical_data'):
        os.makedirs('raw_historical_data')

    for symbol in symbols:
        # Get historical data
        ticker = yf.Ticker(symbol)
        historical_data = ticker.history(period="max")

        # Define CSV file path for the historical data
        csv_filename = f"raw_historical_data/{symbol}_historical_data.csv"
        
        # Write historical data to a CSV file
        historical_data.to_csv(csv_filename)

# Generate statistics and plot and write them to a file for each symbol
def generate_plots_and_stats(symbols):
    # Ensure the 'plots' directory exists
    if not os.path.exists('plots'):
        os.makedirs('plots')
    
    # Ensure the 'raw_stats' directory exists
    if not os.path.exists('raw_stats'):
        os.makedirs('raw_stats')

    for symbol in symbols:
        # Read historical data from CSV file
        csv_filename = f"raw_historical_data/{symbol}_historical_data.csv"
        historical_data = pd.read_csv(csv_filename, index_col='Date', parse_dates=True)

        # Compute statistics
        stats = historical_data.describe()

        # Write statistics to a file
        stats_filename = f'raw_stats/{symbol}_raw_stats.txt'
        with open(stats_filename, 'w') as f:
            f.write(f"{symbol} Statistics\n")
            f.write(str(stats))

        # Plot closing prices over time
        plt.plot(historical_data.index, historical_data['Close'])
        plt.title(f'{symbol} Closing Prices')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'plots/{symbol}_closing_prices.png')
        plt.close()


ticker_symbols = ["ALL.AX", "ANZ.AX", "BHP.AX", "CBA.AX", "CSL.AX", "FMG.AX", "GMG.AX", 
                  "MQG.AX", "NAB.AX", "REA.AX", "RIO.AX", "TCL.AX", "TLS.AX", "WBC.AX", "WES.AX", "WOW.AX", "WDS.AX", "XRO.AX"]

write_profiles(ticker_symbols)
write_raw_historical_data(ticker_symbols)
generate_plots_and_stats(ticker_symbols)
