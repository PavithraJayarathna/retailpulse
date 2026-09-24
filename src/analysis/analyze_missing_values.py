from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw" / "olist"


orders_path = RAW_DATA_DIR / "olist_orders_dataset.csv"
orders = pd.read_csv(orders_path)

#print(orders.head( ))
#print(orders["order_status"])
#print(orders["order_status"].value_counts())
#print(orders["order_delivered_customer_date"].isna())

missing_rows = orders[orders["order_delivered_customer_date"].isna()]
print(len(missing_rows))

print(missing_rows["order_status"].value_counts())

delivered_missing_dates = orders[(orders["order_status"]== "delivered" )& ( orders["order_delivered_customer_date"].isna())]
print(delivered_missing_dates)

missing_approval = orders[
    orders["order_approved_at"].isna()
]

print("\nMissing approval dates:")
print(len(missing_approval))
print(missing_approval["order_status"].value_counts())