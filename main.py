print("Sales Analytics System")
from utils.file_handler import read_sales_data
from utils.data_processor import analyze_sales
from utils.api_handler import fetch_product_info

def main():
    records = read_sales_data("data/sales_data.txt")

    total_qty, total_revenue, product_wise = analyze_sales(records)

    print("TOTAL VALID RECORDS:", len(records))
    print("TOTAL QUANTITY SOLD:", total_qty)
    print("TOTAL REVENUE:", total_revenue)

    print("\nPRODUCT WISE REVENUE:")
    for product, revenue in product_wise.items():
        info = fetch_product_info(product)
        print(product, "-", revenue, "-", info["category"])

if __name__ == "__main__":
    main()

