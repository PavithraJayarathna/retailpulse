# RetailPulse — Source Data Contracts

## 1. Purpose

This document defines the expected structure and quality rules of source
datasets consumed by RetailPulse.

These contracts will later be enforced through automated validation.

---

## 2. Customers

Source: CRM  
Format: CSV  
File: customers.csv

| Column | Type | Required | Rule |
|---|---|---:|---|
| customer_id | string | Yes | Unique identifier |
| first_name | string | Yes | Non-empty |
| last_name | string | Yes | Non-empty |
| email | string | Yes | Valid email format |
| country | string | Yes | Standardizable country value |
| signup_date | date | Yes | Valid date |
| customer_status | string | Yes | Allowed status value |

Primary Key: customer_id

---

## 3. Products

Source: Product Management System  
Format: CSV  
File: products.csv

| Column | Type | Required | Rule |
|---|---|---:|---|
| product_id | string | Yes | Unique identifier |
| product_name | string | Yes | Non-empty |
| category | string | Yes | Valid category |
| unit_cost | decimal | Yes | >= 0 |
| list_price | decimal | Yes | >= 0 |
| active | boolean | Yes | True/False |

Primary Key: product_id

---

## 4. Orders

Source: E-Commerce Platform  
Format: CSV  
File: orders.csv

| Column | Type | Required | Rule |
|---|---|---:|---|
| order_id | string | Yes | Unique identifier |
| customer_id | string | Yes | References customer |
| order_timestamp | datetime | Yes | Valid timestamp |
| status | string | Yes | Allowed order status |
| currency | string | Yes | Supported currency code |
| channel | string | Yes | Valid sales channel |

Primary Key: order_id

Foreign Key:
customer_id → customers.customer_id

---

## 5. Order Items

Source: E-Commerce Platform  
Format: CSV  
File: order_items.csv

| Column | Type | Required | Rule |
|---|---|---:|---|
| order_item_id | string | Yes | Unique identifier |
| order_id | string | Yes | References order |
| product_id | string | Yes | References product |
| quantity | integer | Yes | > 0 |
| unit_price | decimal | Yes | >= 0 |
| discount_amount | decimal | Yes | >= 0 |

Primary Key: order_item_id

Foreign Keys:

order_id → orders.order_id

product_id → products.product_id

---

## 6. Payments

Source: Payment System  
Format: JSON  
File: payments.json

| Column | Type | Required | Rule |
|---|---|---:|---|
| payment_id | string | Yes | Unique identifier |
| order_id | string | Yes | References order |
| payment_timestamp | datetime | Yes | Valid timestamp |
| payment_method | string | Yes | Allowed method |
| amount | decimal | Yes | >= 0 |
| status | string | Yes | Allowed payment status |

Primary Key: payment_id

Multiple payment attempts may exist for one order.

---

## 7. Shipments

Source: Logistics System  
Format: CSV  
File: shipments.csv

| Column | Type | Required | Rule |
|---|---|---:|---|
| shipment_id | string | Yes | Unique identifier |
| order_id | string | Yes | References order |
| shipped_date | date | Conditional | Required once shipped |
| expected_delivery_date | date | Conditional | Required once scheduled |
| delivered_date | date | No | Null until delivered |
| carrier | string | Conditional | Required once shipped |
| shipping_country | string | Yes | Standardizable country |
| status | string | Yes | Allowed shipment status |

Primary Key: shipment_id

---

## 8. Returns

Source: Returns System  
Format: CSV  
File: returns.csv

| Column | Type | Required | Rule |
|---|---|---:|---|
| return_id | string | Yes | Unique identifier |
| order_item_id | string | Yes | References order item |
| return_date | date | Yes | Valid date |
| quantity | integer | Yes | > 0 |
| reason | string | Yes | Allowed return reason |
| refund_amount | decimal | Yes | >= 0 |
| status | string | Yes | Allowed return status |

Primary Key: return_id

Foreign Key:

order_item_id → order_items.order_item_id

---

## 9. Cross-Source Integrity Rules

RetailPulse should eventually validate that:

- Every order customer exists in the customer source.
- Every order item references an existing order.
- Every order item references an existing product.
- Returned quantity cannot exceed the associated purchased quantity.
- Payment records reference valid orders.
- Shipment records reference valid orders.
- Monetary values cannot contain impossible negative values unless explicitly permitted by a future business rule.
- Dates and timestamps must be parseable.
- Primary identifiers should not be null.