def analyze_sales(records):
    total_qty = 0
    total_revenue = 0
    product_wise = {}

    for r in records:
        total_qty += r["quantity"]
        total_revenue += r["revenue"]

        product_wise.setdefault(r["product"], 0)
        product_wise[r["product"]] += r["revenue"]

    return total_qty, total_revenue, product_wise
