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
