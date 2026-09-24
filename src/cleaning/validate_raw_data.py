from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data"/"raw"/"olist"

EXPECTED_FILES = [
    "olist_customers_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "product_category_name_translation.csv",
]

EXPECTED_COLUMNS = {
    "olist_customers_dataset.csv": [
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state",
    ],
    "olist_orders_dataset.csv": [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ],
}

PRIMARY_KEYS = {
    "olist_customers_dataset.csv": "customer_id",
    "olist_orders_dataset.csv": "order_id",
    "olist_products_dataset.csv": "product_id",
    "olist_sellers_dataset.csv": "seller_id",
}

FOREIGN_KEYS = [
    (
        "olist_orders_dataset.csv",
        "customer_id",
        "olist_customers_dataset.csv",
        "customer_id",
    ),
    (
        "olist_order_items_dataset.csv",
        "order_id",
        "olist_orders_dataset.csv",
        "order_id",
    ),
    (
        "olist_order_items_dataset.csv",
        "product_id",
        "olist_products_dataset.csv",
        "product_id",
    ),
    (
        "olist_order_items_dataset.csv",
        "seller_id",
        "olist_sellers_dataset.csv",
        "seller_id",
    ),
    (
        "olist_order_payments_dataset.csv",
        "order_id",
        "olist_orders_dataset.csv",
        "order_id",
    ),
]

def validate_files_exist() -> bool:
    all_valid = True

    for filename in EXPECTED_FILES:
        file_path = RAW_DATA_DIR / filename

        if file_path.exists():
            print(f"[PASS] {filename}")

        else:
            print(f"[FALL] Missing file: {filename}")
            all_valid = False

    return all_valid

def validate_columns() -> bool:
    all_valid = True

    for filename, expected_columns in EXPECTED_COLUMNS.items():
        file_path = RAW_DATA_DIR / filename
        df = pd.read_csv(file_path, nrows=0)

        missing_columns = [
            column
            for column in expected_columns
            if column not in df.columns
        ]

        if missing_columns:
            print(f"[FAIL] {filename}: missing columns {missing_columns}")
            all_valid = False
        else:
            print(f"[PASS] {filename}: required columns present")

    return all_valid

def validate_primary_keys() -> bool:
    all_valid = True

    for filename, primary_key in PRIMARY_KEYS.items():
        file_path = RAW_DATA_DIR / filename

        df = pd.read_csv(
            file_path,
            usecols=[primary_key],
        )

        null_count = df[primary_key].isna().sum()
        duplicate_count = df[primary_key].duplicated().sum()

        if null_count > 0:
            print(
                f"[FAIL] {filename}: "
                f"{primary_key} has {null_count} null values"
            )
            all_valid = False

        if duplicate_count > 0:
            print(
                f"[FAIL] {filename}: "
                f"{primary_key} has {duplicate_count} duplicates"
            )
            all_valid = False

        if null_count == 0 and duplicate_count == 0:
            print(
                f"[PASS] {filename}: "
                f"{primary_key} is unique and non-null"
            )

    return all_valid

def validate_foreign_keys() -> bool:
    all_valid = True

    for child_file, child_key, parent_file, parent_key in FOREIGN_KEYS:
        child_path = RAW_DATA_DIR / child_file
        parent_path = RAW_DATA_DIR / parent_file

        child_df = pd.read_csv(child_path, usecols=[child_key])
        parent_df = pd.read_csv(parent_path, usecols=[parent_key])

        orphan_mask = ~child_df[child_key].isin(parent_df[parent_key])
        orphan_count = orphan_mask.sum()

        if orphan_count > 0:
            print(
                f"[FAIL] {child_file}.{child_key}: "
                f"{orphan_count} values not found in "
                f"{parent_file}.{parent_key}"
            )
            all_valid = False
        else:
            print(
                f"[PASS] {child_file}.{child_key} -> "
                f"{parent_file}.{parent_key}"
            )

    return all_valid

def main() -> None:
    print("RetailPulse Raw Data Validation")
    print("=" * 40)

    files_valid = validate_files_exist()

    if not files_valid:
        print("\nValidation stopped: required files are missing.")
        return

    columns_valid = validate_columns()
    primary_keys_valid = validate_primary_keys()
    foreign_keys_valid = validate_foreign_keys()

    if (
        columns_valid
        and primary_keys_valid
        and foreign_keys_valid
    ):
        print("\nRaw data validation passed.")
    else:
        print("\nRaw data validation failed.")


if __name__ == "__main__":
    main()