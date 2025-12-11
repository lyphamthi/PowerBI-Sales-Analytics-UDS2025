# PowerBI-Sales-Analytics-UDS2025
Sales dashboard project using Power BI: revenue analysis, profit analysis, cancellation rate, forecasting.
📊 PowerBI Sales Analytics Dashboard – UDS 2025

Một dự án phân tích dữ liệu bán hàng sử dụng Power BI nhằm hỗ trợ doanh nghiệp ABC Furniture theo dõi doanh thu, chi phí vận chuyển, lợi nhuận gộp, hành vi hủy đơn và dự báo doanh thu năm 2025.

✨ 1. Giới thiệu dự án

Dự án này được xây dựng dựa trên bộ dữ liệu của cuộc thi UEB Data Showdown 2025, gồm:

Orders (đơn hàng)

Sales (xuất kho)

Cancellation (hủy đơn)

Product lookup

Employee lookup

Territory & Warehouse lookup

Sau khi xử lý bằng Python, dữ liệu được mô hình hoá (Star Schema) và trình bày bằng Power BI.

🎯 2. Mục tiêu phân tích

Dashboard cung cấp các phân tích chính:

Phần 1 – Bắt buộc

Tổng doanh thu & tổng khối lượng hàng theo tháng

Chi phí vận chuyển & lợi nhuận gộp

Xu hướng theo thời gian

So sánh vùng miền

Top/Bottom sản phẩm

Dự báo đơn hàng 2025

Phần 2 – Chuyên sâu

(Chọn 1 trong 4 yêu cầu, ở đây chọn Chiến lược sản phẩm)

Phân tích Regular vs Season

Profitability & Cancel Rate

Đề xuất chiến lược giá/ưu tiên kho

🧹 3. Quy trình thực hiện
(1) Data Cleaning (Python)

Chuẩn hoá format ngày

Ghép bảng dim + fact

Tạo bảng processed dùng cho Power BI

Remove duplicates, xử lý missing values

(2) Data Modeling (Power BI)

Sử dụng Star Schema:

      dim_date       dim_product       dim_territory
          \             |                   /
           \            |                  /
              ---- fact_sales ----
              ---- fact_orders ----
              ---- fact_cancellation ----

(3) Dashboard

Gồm 2 trang:

Trang 1: Tổng quan doanh thu – chi phí – lợi nhuận – vùng miền

Trang 2: Profit Analysis + Forecast 2025

📸 4. Dashboard Preview
Trang 1 – Sales Overview

(Thêm hình screenshot dashboard của bạn vào thư mục /screenshots và đặt tên như dưới đây)

![Dashboard Overview](screenshots/dashboard_overview.png)

Trang 2 – Profitability & Forecast
![Profit Analysis](screenshots/profit_analysis.png)
![Forecast](screenshots/forecast.png)

📈 5. Các chỉ số & insight chính

Tổng doanh thu: 79B VND

Tổng chi phí vận chuyển: 97M VND

Lợi nhuận gộp: 78B VND

Vùng doanh thu cao nhất: Miền Nam

Nhóm sản phẩm lãi tốt nhất: Regular

Season có tỉ lệ hủy cao hơn → khuyến nghị tối ưu kho & dự báo nhu cầu

🔮 6. Forecast 2025

Sử dụng Power BI Analytics (Forecast):

Dự báo theo YearMonth

Confidence interval 95%

Nhận định: Quý 1/2025 có xu hướng giảm nhẹ, cần tăng chương trình kích cầu.

🛠 7. Công cụ sử dụng
Công cụ	Mục đích
Power BI	Dashboard, modeling, DAX, forecasting
Python (Pandas)	Data cleaning & preprocessing
Excel	Raw data
GitHub	Lưu trữ & portfolio
📁 8. Cấu trúc repo
PowerBI-Sales-Analytics-UDS2025/
│
├── processed/                 # Data sau xử lý bằng Python
├── screenshots/               # Ảnh dashboard preview
├── Sales_Analytics.pbix       # File Power BI chính
└── README.md                  # Tài liệu mô tả
🚀 9. Cách mở dự án

Tải file .pbix về

Mở bằng Power BI Desktop

Kiểm tra Data Source → processed/*.csv

Refresh để load lại dữ liệu

👤 10. Tác giả

Nguyễn Viết Lãm
Data Analyst | Power BI | SQL | Python
📧 lyphamthi138@gmail.com 

🌐 GitHub: https://github.com/lyphamthi
