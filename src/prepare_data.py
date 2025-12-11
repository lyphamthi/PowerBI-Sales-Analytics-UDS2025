from pathlib import Path
import pandas as pd

# 1. ĐƯỜNG DẪN THƯ MỤC DỮ LIỆU
RAW_DIR = Path("data/raw")
PROC_DIR = Path("data/processed")
PROC_DIR.mkdir(parents=True, exist_ok=True)

# 2. ĐỌC CÁC FILE EXCEL GỐC
print("Đang đọc dữ liệu...")

product = pd.read_excel(RAW_DIR / "1. Product_Lookup.xlsx")
territory = pd.read_excel(RAW_DIR / "2. Territory_Lookup.xlsx")
warehouse = pd.read_excel(RAW_DIR / "3. Warehouse_Lookup.xlsx")
employee = pd.read_excel(RAW_DIR / "4. Employee_Lookup.xlsx")

orders = pd.read_excel(
    RAW_DIR / "5. Orders.xlsx",
    parse_dates=["OrderDate", "DeliveryDate"]  # nếu tên cột khác thì sửa lại
)
sales = pd.read_excel(
    RAW_DIR / "6. Sales Data.xlsx",
    parse_dates=["SalesDate"]
)
cancel = pd.read_excel(
    RAW_DIR / "7. Cancellation.xlsx",
    parse_dates=["CancelDate"]
)

print("Đọc xong các file Excel.")

# ============= CHUẨN HÓA CỘT GIÁ & KHỐI LƯỢNG =============
# In ra thử xem Product_Lookup có những cột gì
print("Các cột trong Product_Lookup:", list(product.columns))

# Tìm cột giá (chứa từ 'price' hoặc 'giá')
price_candidates = [
    c for c in product.columns
    if "price" in str(c).lower() or "giá" in str(c).lower()
]

if not price_candidates:
    raise ValueError(
        f"Không tìm thấy cột giá trong Product_Lookup. "
        f"Các cột hiện có: {list(product.columns)}"
    )

price_col = price_candidates[0]  # lấy cột đầu tiên tìm được

# Tìm cột khối lượng (chứa 'volume' hoặc 'khối' hoặc 'weight')
volume_candidates = [
    c for c in product.columns
    if "volume" in str(c).lower()
    or "khối" in str(c).lower()
    or "weight" in str(c).lower()
]

if not volume_candidates:
    raise ValueError(
        f"Không tìm thấy cột khối lượng trong Product_Lookup. "
        f"Các cột hiện có: {list(product.columns)}"
    )

volume_col = volume_candidates[0]

# Đổi tên về chuẩn chung để các phần sau dùng
product = product.rename(columns={
    price_col: "Price",
    volume_col: "ProductVolume"
})

print(f"Đã map cột giá: '{price_col}' -> 'Price'")
print(f"Đã map cột khối lượng: '{volume_col}' -> 'ProductVolume'")

date_cols = []

for df, cols in [
    (orders, ["OrderDate", "DeliveryDate"]),
    (sales, ["SalesDate"]),
    (cancel, ["CancelDate"])
]:
    for c in cols:
        if c in df.columns:
            date_cols.append(df[c])

all_dates = pd.concat(date_cols).dropna().drop_duplicates()
dim_date = pd.DataFrame({"Date": all_dates})
dim_date["DateKey"] = dim_date["Date"].dt.strftime("%Y%m%d").astype(int)
dim_date["Year"] = dim_date["Date"].dt.year
dim_date["Month"] = dim_date["Date"].dt.month
dim_date["MonthName"] = dim_date["Date"].dt.strftime("%b")
dim_date["YearMonth"] = dim_date["Date"].dt.strftime("%Y-%m")

# map Date -> DateKey để dùng lại
date_map = dim_date.set_index("Date")["DateKey"]


# 4. LƯU CÁC DIMENSION

dim_product = product.copy()
dim_territory = territory.copy()
dim_warehouse = warehouse.copy()
dim_employee = employee.copy()

dim_product.to_csv(PROC_DIR / "dim_product.csv", index=False)
dim_territory.to_csv(PROC_DIR / "dim_territory.csv", index=False)
dim_warehouse.to_csv(PROC_DIR / "dim_warehouse.csv", index=False)
dim_employee.to_csv(PROC_DIR / "dim_employee.csv", index=False)
dim_date.to_csv(PROC_DIR / "dim_date.csv", index=False)

print("Đã tạo và lưu các bảng dimension.")

# 5. FACT_ORDERS

fact_orders = orders.merge(
    product[["ProductID", "ProductVolume", "Price"]],
    on="ProductID",
    how="left"
)

# Giá trị đơn hàng tiềm năng (Revenue nếu bán hết)
fact_orders["OrderValuePotential"] = fact_orders["OrderQty"] * fact_orders["Price"]

# Thêm khóa ngày
fact_orders["OrderDateKey"] = fact_orders["OrderDate"].map(date_map)
fact_orders["DeliveryDateKey"] = fact_orders["DeliveryDate"].map(date_map)

fact_orders.to_csv(PROC_DIR / "fact_orders.csv", index=False)

print("Đã tạo fact_orders.")

# 6. FACT_SALES
fact_sales = sales.merge(
    product[["ProductID", "ProductVolume", "Price"]],
    on="ProductID",
    how="left"
)

fact_sales["SalesRevenue"] = fact_sales["SalesQty"] * fact_sales["Price"]
fact_sales["ShippingCost"] = fact_sales["SalesQty"] * 2000  # giả định 2,000 VND / đơn vị
fact_sales["GrossProfit"] = fact_sales["SalesRevenue"] - fact_sales["ShippingCost"]

# OnTimeFlag nếu có cột OnTimeRate
if "OnTimeRate" in fact_sales.columns:
    fact_sales["OnTimeFlag"] = (fact_sales["OnTimeRate"] > 91).astype(int)

fact_sales["SalesDateKey"] = fact_sales["SalesDate"].map(date_map)

fact_sales.to_csv(PROC_DIR / "fact_sales.csv", index=False)

print("Đã tạo fact_sales.")

# 7. FACT_CANCELLATION

fact_cancel = cancel.merge(
    product[["ProductID", "ProductVolume", "Price"]],
    on="ProductID",
    how="left"
)

fact_cancel["CancelDateKey"] = fact_cancel["CancelDate"].map(date_map)

fact_cancel.to_csv(PROC_DIR / "fact_cancellation.csv", index=False)

print("Đã tạo fact_cancellation.")


# 8. AGG MONTHLY SALES (CHO FORECAST)

monthly_sales = (
    fact_sales
    .groupby(fact_sales["SalesDate"].dt.to_period("M"))
    .agg(
        Revenue=("SalesRevenue", "sum"),
        Volume=("SalesVolume", "sum")
    )
    .reset_index()
)

monthly_sales["SalesMonth"] = monthly_sales["SalesDate"].dt.to_timestamp()
monthly_sales.to_csv(PROC_DIR / "agg_monthly_sales.csv", index=False)

print("Hoàn thành! Dữ liệu đã được lưu trong thư mục data/processed.")
