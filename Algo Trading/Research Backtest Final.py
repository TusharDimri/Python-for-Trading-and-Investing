import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# List of top 10 Indian companies by market cap
indian_companies = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS']

num_trades = 0
num_winning_trades = 0
num_losing_trades = 0
entry_points = []
exit_points = []
stop_loss_arr = []
target_arr = []

def ATR(DF, n=14):
    df = DF.copy()
    df["H-L"] = df["High"] - df["Low"]
    df["H-PC"] = df["High"] - df["Adj Close"].shift(1)
    df["L-PC"] = df["Low"] - df["Adj Close"].shift(1)
    df["True Range"] = df[["H-L", "H-PC", "L-PC"]].max(axis=1, skipna=False)
    df["ATR"] = df["True Range"].ewm(com=n, min_periods=n).mean()
    return df["ATR"]

for ticker in indian_companies:
    data = yf.download(ticker, start='2018-07-18', end='2023-07-18', interval='1d')
    data.reset_index(inplace=True)

    data['MovingAverage'] = data['Adj Close'].rolling(window=50).mean()

    X = np.arange(len(data)).reshape(-1, 1)
    y = data['Adj Close'].values.reshape(-1, 1)
    regression = LinearRegression().fit(X, y)
    regression_line = regression.predict(X)

    # Calculate standard deviation
    std_dev = np.std(y - regression_line)

    # Calculate upper and lower bounds
    upper_bound = regression_line + 2 * std_dev
    lower_bound = regression_line - 2 * std_dev

    ATR_array = ATR(data)

    for i in range(1, len(data)):
        # Short Trade
        if data['Adj Close'][i - 1] < upper_bound[i - 1] and data['Adj Close'][i] >= upper_bound[i]:
            entry_price = data['Adj Close'][i]
            entry_points.append(entry_price)
            stop_loss = entry_price + 3 * ATR_array[i]
            stop_loss_arr.append(stop_loss)
            target = entry_price - (stop_loss - entry_price)
            target_arr.append(target)

            for j in range(i+1, len(data)):
                if data['High'][j] > stop_loss and data['Low'][j] < stop_loss:
                    exit_points.append(stop_loss)
                    num_trades += 1
                    num_losing_trades += 1
                    break
                elif data['High'][j] > target and data['Low'][j] < target:
                    exit_points.append(target)
                    num_trades += 1
                    num_winning_trades += 1
                    break
                elif j == (len(data) - 1):
                    exit_points.append("Trade Still Active")
                    num_trades += 1

        # Long Trade
        if data['Adj Close'][i - 1] > lower_bound[i - 1] and data['Adj Close'][i] <= lower_bound[i]:
            entry_price = data['Adj Close'][i]
            entry_points.append(entry_price)
            stop_loss = entry_price - 3 * ATR_array[i]
            stop_loss_arr.append(stop_loss)
            target = entry_price + (entry_price - stop_loss)
            target_arr.append(target)

            for j in range(i+1, len(data)):
                if data['High'][j] > stop_loss and data['Low'][j] < stop_loss:
                    exit_points.append(stop_loss)
                    num_trades += 1
                    num_losing_trades += 1
                    break
                elif data['High'][j] > target and data['Low'][j] < target:
                    exit_points.append(target)
                    num_trades += 1
                    num_winning_trades += 1
                    break
                elif j == (len(data) - 1):
                    exit_points.append("Trade Still Active")
                    num_trades += 1
                    
    
    # Plot the data, regression line, and bounds
    plt.figure(figsize=(12, 6))
    plt.plot(data['Date'], data['Adj Close'], label='Stock Price')
    plt.plot(data['Date'], data['MovingAverage'], label='Moving Average (50)')
    plt.plot(data['Date'], regression_line, label='Regression Line')
    plt.plot(data['Date'], upper_bound, 'r--', label='Upper Bound')
    plt.plot(data['Date'], lower_bound, 'r--', label='Lower Bound')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Linear Regression with 50-Period Moving Average')
    plt.legend()
    plt.grid(True)
    plt.show()

# Print the results
print("Number of Trades:", num_trades)
print("Number of Winning Trades:", num_winning_trades)
print("Number of Losing Trades:", num_losing_trades)

