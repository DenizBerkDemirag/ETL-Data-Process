import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_FILE = DATA_DIR / "raw" / "raw_orders_data.csv"


def read_data(file_path: Path) -> pd.DataFrame:
    """
    Read the data from the given file path.
    """
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error reading the file: {e}")
        return pd.DataFrame()