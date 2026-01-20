def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    """
    transactions = []

    for line in raw_lines:
        parts = line.split("|")

        # skip invalid rows
        if len(parts) != 8:
            continue

        try:
            quantity = int(parts[4])
            price = int(parts[5].replace(",", ""))

            if quantity <= 0 or price <= 0:
                continue

            transaction = {
                "TransactionID": parts[0],
                "Date": parts[1],
                "ProductID": parts[2],
                "ProductName": parts[3],
                "Quantity": quantity,
                "UnitPrice": price,
                "CustomerID": parts[6],
                "Region": parts[7]
            }

            transactions.append(transaction)

        except ValueError:
            continue

    return transactions
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    """
    valid_transactions = []
    invalid_count = 0

    summary = {
        "total_input": len(transactions),
        "invalid": 0,
        "filtered_by_region": 0,
        "filtered_by_amount": 0,
        "final_count": 0
    }

    # Available regions
    regions = set(t.get("Region") for t in transactions if "Region" in t)
    print("Available regions:", regions)

    for tx in transactions:
        try:
            # Required fields check
            required_keys = [
                "TransactionID", "ProductID", "CustomerID",
                "Quantity", "UnitPrice", "Region"
            ]

            if not all(key in tx for key in required_keys):
                invalid_count += 1
                continue

            # ID format validation
            if not tx["TransactionID"].startswith("T"):
                invalid_count += 1
                continue
            if not tx["ProductID"].startswith("P"):
                invalid_count += 1
                continue
            if not tx["CustomerID"].startswith("C"):
                invalid_count += 1
                continue

            # Quantity & Price validation
            if tx["Quantity"] <= 0 or tx["UnitPrice"] <= 0:
                invalid_count += 1
                continue

            amount = tx["Quantity"] * tx["UnitPrice"]

            # Region filter
            if region and tx["Region"] != region:
                summary["filtered_by_region"] += 1
                continue

            # Amount filter
            if min_amount and amount < min_amount:
                summary["filtered_by_amount"] += 1
                continue

            if max_amount and amount > max_amount:
                summary["filtered_by_amount"] += 1
                continue

            valid_transactions.append(tx)

        except Exception:
            invalid_count += 1

    summary["invalid"] = invalid_count
    summary["final_count"] = len(valid_transactions)

    return valid_transactions, invalid_count, summary
    def region_wise_sales(transactions):
    region_data = {}
    total_sales_all = 0

    # Calculate total sales per region
    for tx in transactions:
        region = tx["Region"]
        amount = tx["Quantity"] * tx["UnitPrice"]

        total_sales_all += amount

        if region not in region_data:
            region_data[region] = {
                "total_sales": 0,
                "transaction_count": 0
            }

        region_data[region]["total_sales"] += amount
        region_data[region]["transaction_count"] += 1

    # Add percentage
    for region in region_data:
        sales = region_data[region]["total_sales"]
        region_data[region]["percentage"] = round(
            (sales / total_sales_all) * 100, 2
        )

    # Sort by total_sales descending
    sorted_regions = dict(
        sorted(
            region_data.items(),
            key=lambda x: x[1]["total_sales"],
            reverse=True
        )
    )

    return sorted_regions
    def top_selling_products(transactions, n=5):
    product_data = {}

    for tx in transactions:
        product = tx["ProductName"]
        qty = tx["Quantity"]
        revenue = qty * tx["UnitPrice"]

        if product not in product_data:
            product_data[product] = {
                "quantity": 0,
                "revenue": 0
            }

        product_data[product]["quantity"] += qty
        product_data[product]["revenue"] += revenue

    # Convert to list of tuples
    product_list = [
        (product, data["quantity"], data["revenue"])
        for product, data in product_data.items()
    ]

    # Sort by quantity descending
    product_list.sort(key=lambda x: x[1], reverse=True)

    return product_list[:n]


