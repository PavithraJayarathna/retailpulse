# RetailPulse — Data Model

## 1. Overview

RetailPulse separates operational source data from the analytical data model.

Operational data represents business transactions from systems such as customer management, ordering, payments, logistics, and returns.

The analytical layer will transform this data into a model optimized for reporting and analytics.

## 2. Operational Entities

Initial source entities:

- Customers
- Orders
- Order Items
- Products
- Categories
- Payments
- Shipments
- Returns

## 3. Core Relationships

- One customer can place many orders.
- One order can contain many order items.
- Each order item references one product.
- A product belongs to a product category.
- Orders can have associated payment records.
- Orders can have shipment information.
- Products or order items may be associated with returns.

Exact payment, shipment, and return cardinalities will be finalized when the source schemas are defined.

## 4. Analytical Model

RetailPulse will use a dimensional analytical model for business intelligence.

### Fact Sales

The primary sales fact table will contain measurable sales events.

Potential measures include:

- Quantity
- Gross Sales
- Discount Amount
- Net Revenue
- Cost of Goods Sold
- Gross Profit

### Dimensions

Initial dimensions may include:

- Dim Date
- Dim Customer
- Dim Product
- Dim Location
- Dim Channel
- Dim Promotion

The final dimensions will be determined by the analytical requirements and available source data.

## 5. Fact Table Grain

The planned grain of Fact Sales is:

> One row represents one product line within a qualifying order.

Defining the grain before implementing the warehouse helps prevent aggregation and double-counting errors.

## 6. Conceptual Star Schema

                     Dim Date
                        |
                        |
Dim Customer ------ Fact Sales ------ Dim Product
                        |
                        |
                   Dim Location

Additional dimensions will be introduced only when required by the business questions.