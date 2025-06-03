import pandas as pd
from cli.run import run_cli
from core.fetch import fetch_data
from core.plot import plot_multiple_indicators, plot_price
from utils.common import get_csv_data_path, save_csv


if __name__ == "__main__":
    # Example: python main.py --symbol BTC-USD --save
    run_cli()
