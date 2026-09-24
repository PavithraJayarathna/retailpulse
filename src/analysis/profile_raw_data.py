from pathlib import Path

import pandas as pd


RAW_DATA_DIR = Path("data/raw/olist")


def profile_csv(file_path: Path) -> None:
    """Print basic structural information about a CSV file."""

    df = pd.read_csv(file_path)

    print("=" * 70)
    print(f"FILE: {file_path.name}")
    print(f"ROWS: {len(df):,}")
    print(f"COLUMNS: {len(df.columns)}")
    print("\nCOLUMN NAMES:")
    
    for column in df.columns:
        print(f"  - {column}")

    print("\nDATA TYPES:")
    print(df.dtypes)

    print("\nMISSING VALUES:")
    print(df.isna().sum())

    print("\nDUPLICATE ROWS:")
    print(df.duplicated().sum())

    print("\nUNIQUE VALUES PER COLUMN:")
    print(df.nunique())

    print()


def main() -> None:
    csv_files = sorted(RAW_DATA_DIR.glob("*.csv"))

    print(f"Found {len(csv_files)} CSV files.\n")

    for file_path in csv_files:
        profile_csv(file_path)


if __name__ == "__main__":
    main()
