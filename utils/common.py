from datetime import datetime
from pathlib import Path

from matplotlib import pyplot as plt

from .constants import Directories

def indicator_column(indicator: str, period: int) -> str:
    if period:
        return f"{indicator}{period}"
    
    return indicator

def indicator_label(indicator: str, period: int) -> str:
    if period:
        return f"{indicator} {period}"
    
    return indicator

def get_project_root(marker: str) -> Path:
    current = Path(__file__).resolve()
    while current != current.parent:
        if (current / marker).exists():
            return current
        current = current.parent
    raise FileNotFoundError(f"Could not find project root containing '{marker}' directory.")

def get_csv_data_path(name: str) -> Path:
    project_root = get_project_root(Directories.DATA)
    data_dir = project_root / Directories.DATA

    filename = f"{name}.csv" if not name.endswith(".csv") else name
    csv_path = data_dir / filename

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    return csv_path

def save_csv(df, symbol):
    project_root = get_project_root(Directories.DATA)
    data_dir = project_root / Directories.DATA

    filename = f"{symbol}.csv"
    filepath = data_dir / filename

    df.to_csv(filepath)
    print(f"Saved to {filepath}")

def resolve_plot_dir(symbol: str) -> Path:
    path = Path(Directories.FIGS) / symbol
    path.mkdir(parents=True, exist_ok=True)
    return path

def export_plot_image(fig, symbol: str, indicator: str):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dir_path = resolve_plot_dir(symbol)
    filename = f"{indicator}_{timestamp}.png"
    fig.savefig(dir_path / filename, bbox_inches="tight")
