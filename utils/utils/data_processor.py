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
