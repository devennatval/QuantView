# Volatility: ATR & Rolling Standard Deviation

import matplotlib.pyplot as plt
from pandas import DataFrame
from pandas import Series
import pandas as pd
from utils.constants import Indicators, PriceFields
from utils.common import export_plot_image, indicator_column, indicator_label
import numpy as np

# Average True Range
def enrich_atr(df: DataFrame, period: int = 14):
    df = df.copy()

    high = df[PriceFields.HIGH]
    low = df[PriceFields.LOW]
    close = df[PriceFields.CLOSE]

    prev_close = close.shift(1)
    tr1 = (high - low).abs()
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()

    # Combine into a Series using max of all 3
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    atr = tr.rolling(window=period).mean()
    atr_col = indicator_column(Indicators.ATR, period)
    df[atr_col] = atr

    return df

def plot_atr(
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

    atr_col = indicator_column(Indicators.ATR, period)
    label = indicator_label(Indicators.ATR, period)

    ax.plot(df[atr_col], label=label, color='brown')
    ax.set_title(f'{symbol} {label}')
    ax.set_ylabel(Indicators.ATR)
    ax.grid()
    ax.legend()

    if save and standalone:
        export_plot_image(fig, symbol, label)

    if show and standalone:
        plt.tight_layout()
        plt.show()
    elif standalone:
        plt.close()

# N-Day Rolling Standard Deviation
def enrich_volatility_std(df: DataFrame, period: int = 20, annualize: bool = False):
    df = df.copy()
    returns = df[PriceFields.CLOSE].pct_change()
    vol = returns.rolling(window=period).std()

    if annualize:
        vol *= np.sqrt(252)

    vol_col = indicator_column(Indicators.VOLATILITY, period)
    df[vol_col] = vol

    return df

def plot_volatility_std(
    df: DataFrame,
    symbol: str,
    period: int = 20,
    annualize: bool = False,
    ax=None,
    save=False,
    show=True,
):
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=(14, 3))

    vol_col = indicator_column(Indicators.VOLATILITY, period)
    label = indicator_label(Indicators.VOLATILITY, period)
    if annualize:
        label += " (Annualized)"

    ax.plot(df[vol_col], label=label, color='teal')
    ax.set_title(f'{symbol} {label}')
    ax.set_ylabel('Volatility')
    ax.grid()
    ax.legend()

    if save and standalone:
        export_plot_image(fig, symbol, label)

    if show and standalone:
        plt.tight_layout()
        plt.show()
    elif standalone:
        plt.close()
