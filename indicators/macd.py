# Moving Average Convergence Divergence

import matplotlib.pyplot as plt
from pandas import DataFrame
from utils.constants import Indicators, PriceFields
from utils.common import export_plot_image, indicator_column, indicator_label

def enrich_macd(
    df: DataFrame,
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9,
):
    df = df.copy()

    fast_ema = df[PriceFields.CLOSE].ewm(span=fast_period, adjust=False).mean()
    slow_ema = df[PriceFields.CLOSE].ewm(span=slow_period, adjust=False).mean()

    macd_line = fast_ema - slow_ema
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    macd_hist = macd_line - signal_line

    macd_col = indicator_column(Indicators.MACD, f"{fast_period}_{slow_period}")
    signal_col = indicator_column(Indicators.MACD_SIGNAL, signal_period)
    hist_col = indicator_column(Indicators.MACD_HIST, signal_period)

    df[macd_col] = macd_line
    df[signal_col] = signal_line
    df[hist_col] = macd_hist

    return df

def plot_macd(
    df: DataFrame,
    symbol: str,
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9,
    ax=None,
    save=False,
    show=True,
):
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=(14, 4))

    macd_col = indicator_column(Indicators.MACD, f"{fast_period}_{slow_period}")
    signal_col = indicator_column(Indicators.MACD_SIGNAL, signal_period)
    hist_col = indicator_column(Indicators.MACD_HIST, signal_period)

    ax.plot(df[macd_col], label='MACD Line', color='blue')
    ax.plot(df[signal_col], label='Signal Line', color='orange')
    ax.bar(
        df.index,
        df[hist_col],
        label='Histogram',
        color=df[hist_col].apply(lambda x: 'green' if x >= 0 else 'red'),
        alpha=0.3,
    )

    ax.set_title(f'{symbol} MACD ({fast_period}, {slow_period}, {signal_period})')
    ax.set_ylabel(Indicators.MACD)
    ax.grid()
    ax.legend()

    if save and standalone:
        export_plot_image(fig, symbol, f"{Indicators.MACD}_{fast_period}_{slow_period}")

    if show and standalone:
        plt.tight_layout()
        plt.show()
    elif standalone:
        plt.close()
