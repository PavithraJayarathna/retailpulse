from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT /"data" / "raw" / "olist"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

INPUT_FILE = RAW_DATA_DIR / "olist_orders_dataset.csv"
OUTPUT_FILE = PROCESSED_DATA_DIR / "orders_clean.csv"

def load_orders():
    orders = pd.read_csv(INPUT_FILE)
    return orders

orders = load_orders()
print(orders.head())

def clean_orders(orders):
    cleaned = orders.copy()

    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for column in date_columns:
        cleaned[column] = pd.to_datetime(
            cleaned[column],
            errors="coerce",
        )

    cleaned["order_status"] = cleaned["order_status"].str.strip().str.lower()

    cleaned["missing_delivery_date_flag"]=((cleaned["order_status"]=="delivered") & (cleaned["order_delivered_customer_date"].isna()))
    cleaned["missing_approval_date_flag"] = ((cleaned["order_status"] == "delivered") & (cleaned["order_approved_at"].isna()))

    cleaned["delivery_days"]=(cleaned["order_delivered_customer_date"] - cleaned["order_purchase_timestamp"]).dt.days
    cleaned["delivery_delay_days"] = (cleaned["order_delivered_customer_date"]- cleaned["order_estimated_delivery_date"]).dt.days

    cleaned["late_delivery_flag"] = pd.NA
    valid_delivery = cleaned["delivery_delay_days"].notna()
    cleaned.loc[valid_delivery, "late_delivery_flag"] = (
    cleaned.loc[valid_delivery, "delivery_delay_days"] > 0
)

    return cleaned

def save_orders(orders):
    orders.to_csv(OUTPUT_FILE, index=False)

raw_orders = load_orders()
cleaned_orders = clean_orders(raw_orders)

save_orders(cleaned_orders)

print("\nCleaned orders saved successfully.")

#print(cleaned_orders.dtypes)
#print(cleaned_orders["order_status"].value_counts())
#print(cleaned_orders["missing_delivery_date_flag"].value_counts())
#print(cleaned_orders["missing_approval_date_flag"].value_counts())
#print(cleaned_orders[["order_purchase_timestamp","order_delivered_customer_date","delivery_days",]].head())

#negative_delivery = cleaned_orders[
    #cleaned_orders["delivery_days"] < 0
#]

#print("\nNegative delivery days:")
#print(len(negative_delivery))

#print(cleaned_orders["late_delivery_flag"].value_counts(dropna=False))
