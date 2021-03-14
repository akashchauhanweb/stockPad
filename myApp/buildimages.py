import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc

def graph(name):
    #graph
    style.use('ggplot')
    company = name + ".csv"
    df = pd.read_csv('C:/Users/akashweb/PycharmProjects/stockpadFinal/companydata/'+company, parse_dates=True, index_col=0)
    df['200ma'] = df['Adj Close'].rolling(window=200, min_periods=0).mean()

    ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)

    ax1.plot(df.index, df['Adj Close'])
    ax1.plot(df.index, df['200ma'])
    ax2.bar(df.index, df['Volume'])

    plt.savefig('C:/Users/akashweb/PycharmProjects/stockpadFinal/myApp/static/myApp/img/graph.png')

def candle(name):
    #candle
    style.use('ggplot')
    company = name + ".csv"
    df = pd.read_csv('C:/Users/akashweb/PycharmProjects/stockpadFinal/companydata/' + company, parse_dates=True, index_col=0)
    df_ohlc = df['Adj Close'].resample('10D').ohlc()
    df_volume = df['Volume'].resample('10D').sum()

    df_ohlc.reset_index(inplace=True)
    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

    ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
    ax1.xaxis_date()

    candlestick_ohlc(ax1, df_ohlc.values, width=3, colorup='g')
    ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)

    plt.savefig('C:/Users/akashweb/PycharmProjects/stockpadFinal/myApp/static/myApp/img/candle.png')

"""
def moving(name):
    #moving average graph
    style.use('ggplot')
    company = name + ".csv"
    df = pd.read_csv('C:/Users/akashweb/PycharmProjects/stockpadFinal/companydata/'+company, parse_dates=True)
    lst = []
    lst = df['Close']
    p = 0
    q = 0
    n = 0
    s1 = 0
    s2 = 0
    sb = []
    c = 0
    r = 0
    s3 = 0
    a3 = []
    m = 0
    while (n < 34):
        for i in range(p, p + 12):
            s1 = s1 + lst[i]
        for i in range(q, q + 26):
            s2 = s2 + lst[i]
        a1 = s1 / 12
        a2 = s2 / 26
        s1 = 0
        s2 = 0
        sb.append((a2 + a1) / 2)
        p = p + 1
        q = q + 1
        n = n + 1
    while (m < 34):
        for i in range(r, r + 9):
            s3 = s3 + lst[i]
        a3.append(s3 / 9)
        s3 = 0
        m = m + 1
        r = r + 1
    plt.plot(sb, 'b')
    plt.plot(a3, 'r')
    plt.savefig('C:/Users/akashweb/PycharmProjects/stockpadFinal/companydata/' + name + 'ma.png')
"""