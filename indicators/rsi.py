# Relative Strength Index

import matplotlib.pyplot as plt
from pandas import DataFrame
from utils.constants import Indicators, PriceFields
from utils.common import export_plot_image, indicator_column, indicator_label

def enrich_rsi(df: DataFrame, period: int = 14):
    df = df.copy()

    delta = df[PriceFields.CLOSE].diff()
    gain = delta.clip(lower=0, upper=100)
    loss = -delta.clip(upper=0, lower=-100)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss.replace(0, float('nan'))
    rsi_series = 100 - (100 / (1 + rs))

    indicator = indicator_column(Indicators.RSI, period)
    df[indicator] = rsi_series

    return df

def plot_rsi(
    df: DataFrame,
    symbol: str,
    period: int = 14,
    ax=None,
    save=False, 
    show=True,
):
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=(14, 3))

    column = indicator_column(Indicators.RSI, period)
    label = indicator_label(Indicators.RSI, period)

    ax.plot(df[column], color='purple', label=label)
    ax.axhline(70, color='red', linestyle='--')
    ax.axhline(30, color='green', linestyle='--')

    ax.set_title(f'{symbol} {label}')
    ax.set_ylabel(Indicators.RSI)
    ax.grid()
    ax.legend()

    if save and standalone:
        export_plot_image(fig, symbol, label)

    if show and standalone:
        plt.tight_layout()
        plt.show()
    elif standalone:
        plt.close()
