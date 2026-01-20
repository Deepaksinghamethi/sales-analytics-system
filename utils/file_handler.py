def read_sales_data(file_path):
    records = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            parts = line.split("|")
            if len(parts) != 8:
                continue

            tid, date, pid, name, qty, price, cid, region = parts

            try:
                qty = int(qty)
                price = float(price.replace(",", ""))
            except:
                continue

            if qty <= 0 or price <= 0:
                continue

            records.append({
                "product": name,
                "quantity": qty,
                "revenue": qty * price
            })

    return records

