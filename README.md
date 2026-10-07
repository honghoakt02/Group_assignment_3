# HOSE V4: Quantitative Research Dashboard & Nested Walk-Forward Portfolio Optimization

> **Dự án Nghiên cứu Tài chính Định lượng (Quantitative Finance Thesis & Research Framework)**  
> **Chủ đề:** Hệ thống Đa nhân tố Kỹ thuật & Cơ bản kết hợp Khung Nested Walk-Forward, Tối ưu Danh mục (EW, MPT, MinVar, HRP) và Cơ chế Market Regime trên sàn HOSE (2021 – 2025).

---

## 📌 1. Cấu Trúc Dự Án (Project Architecture)

Dự án được cấu trúc theo mô hình phân tầng khoa học (**Decoupled Data-Centric Architecture**):
- **Tầng Dữ liệu (`data/`):** Lưu trữ toàn bộ 8 bộ dữ liệu thực nghiệm đã kiểm toán và metadata JSON/CSV, tách rời hoàn toàn khỏi giao diện người dùng để ngăn chặn hard-coding.
- **Tầng Giao diện (`frontend/`):** Dashboard tương tác hiện đại với thanh điều hướng 24 phân hệ, tích hợp Plotly.js, công thức toán KaTeX và trình duyệt dữ liệu gốc.
- **Tầng API Backend (`backend/`):** Dịch vụ FastAPI cung cấp RESTful API cho toàn bộ các tập dữ liệu thực nghiệm.
- **Tầng Scripts (`scripts/`):** Các script tiền xử lý dữ liệu và kiểm toán tính toàn vẹn dữ liệu tự động (*Data Validation Suite*).
- **Ứng dụng Streamlit (`app.py`):** Cung cấp thêm phương án triển khai 1-click trên Streamlit Community Cloud.

```text
hose-v4-dashboard/
├── data/                                    # Tầng lưu trữ dữ liệu thực nghiệm chuẩn
│   ├── metadata.json                        # Cấu hình tham số & thông tin tổng thể
│   ├── inventory.json                       # Bảng kiểm kê 40+ hạng mục dữ liệu thực tế
│   ├── 01_data_quality.csv                  # Chất lượng 95 mã cổ phiếu HOSE
│   ├── data_quality.json
│   ├── 02_time_split.csv                    # Phân chia Core Train / Val / Final Test
│   ├── time_split.json
│   ├── 03_core_threshold_trials.csv         # Lưới 9 cặp thử nghiệm BUY/EXIT trên Core Train
│   ├── core_threshold_trials.json
│   ├── 04_validation_selection_history.csv  # Lịch tái chọn Top 5 năm 2024 (Validation)
│   ├── val_selection_history.json
│   ├── 05_validation_models.csv             # Kết quả 5 mô hình trên tập Validation
│   ├── val_models.json
│   ├── 06_test_selection_history.csv        # Lịch tái chọn Top 5 năm 2025 (Final Test)
│   ├── test_selection_history.json
│   ├── 07_final_test_results.csv            # Báo cáo hiệu năng Out-Of-Sample 8 mô hình
│   ├── final_test_results.json
│   ├── 08_leakage_audit.csv                 # Ma trận kiểm toán chống nhìn trước tương lai
│   ├── leakage_audit.json
│   ├── sample_ranking.json                  # Chi tiết điểm xếp hạng Top 5 tại 2024-01-02
│   └── stock_features_sample.json           # Dữ liệu chỉ báo kỹ thuật mẫu (AAA cuối 2025)
├── frontend/                                # Giao diện Dashboard Web tương tác
│   ├── index.html                           # SPA Dashboard đầy đủ 24 mô-đun
│   ├── package.json                         # Cấu hình Vite & dependencies
│   └── src/                                 # Mã nguồn mở rộng React/TypeScript
├── backend/                                 # Dịch vụ API Backend (FastAPI)
│   ├── main.py                              # FastAPI REST API endpoints
│   └── requirements.txt                     # Thư viện cho Backend API
├── scripts/                                 # Bộ công cụ tiền xử lý & kiểm toán
│   ├── extract_data.py                      # Script trích xuất dữ liệu
│   └── validate_data.py                     # Bộ kiểm thử toàn vẹn dữ liệu
├── app.py                                   # Ứng dụng Streamlit đa năng (Deploy Streamlit Cloud)
├── requirements.txt                         # Thư viện cho Streamlit
├── package.json                             # Root npm scripts (npm run dev)
└── README.md                                # Tài liệu hướng dẫn chi tiết
```

---

## 📋 2. Bảng Kiểm Kê Dữ Liệu Thực Tế (Data Inventory)

Theo yêu cầu nghiêm ngặt của nghiên cứu khoa học: **Mọi số liệu phải lấy từ file gốc, không được nội suy hoặc bịa đặt**. Dưới đây là bảng kiểm kê chi tiết:

| Hạng mục | Trạng thái trong File V4 | Nguồn / Output cụ thể | Giá trị Thực tế |
| :--- | :---: | :--- | :--- |
| **Dataset** | Có | Cell 9 output | `HOSE - 01.01.2021 - 31.12.2025 (95 mã)` |
| **Số mã Ticker** | Có | Cell 9 output | `95 mã` |
| **Số dòng dữ liệu** | Có | Cell 9 output | `116,889 dòng` |
| **Số phiên giao dịch** | Có | Cell 9 output | `1,244 phiên` |
| **Khoảng thời gian** | Có | Cell 9 output | `04/01/2021 → 31/12/2025` |
| **Benchmark** | Có | Cell 19 output | `__MARKET_PROXY__` (Chỉ số tổng hợp tỷ trọng đều) |
| **Core Train** | Có | Cell 16 output | `04/01/2021 → 02/01/2024 (747 phiên, 60.05%)` |
| **Validation** | Có | Cell 16 output | `03/01/2024 → 31/12/2024 (249 phiên, 20.02%)` |
| **Final Test** | Có | Cell 16 output | `02/01/2025 → 31/12/2025 (248 phiên, 19.93%)` |
| **Ngưỡng BUY** | Có | Cell 27 output | `BUY = 5` (Khóa vĩnh viễn trên Core Train) |
| **Ngưỡng EXIT** | Có | Cell 27 output | `EXIT = 2` (Khóa vĩnh viễn trên Core Train) |
| **TOP_N** | Có | Cell 5 output | `5 cổ phiếu` |
| **Tần suất chọn Top N** | Có | Cell 5 output | `Q (Hàng quý)` |
| **Tần suất Rebalance** | Có | Cell 5 output | `M (Hàng tháng)` |
| **Trọng số Xếp hạng** | Có | Cell 5 code | Sharpe: 0.25, TA: 0.20, RS: 0.25, LowVol: 0.10, Liq: 0.05, Mom: 0.15 |
| **Phí giao dịch** | Có | Cell 5 code | `0.15% (0.0015)` |
| **Trượt giá (Slippage)**| Có | Cell 5 code | `0.05% (0.0005)` |
| **FA Point-in-time** | **Không có trong run** | Cell 13 output | `Chuyển TA-only do không có ngày công bố an toàn` |
| **Win Rate / Profit Factor**| **Không có trong output** | Cell 52 output | `N/A — dữ liệu chưa có trong file` |

---

## 🏆 3. Bảng Kết Quả Thực Nghiệm Out-Of-Sample (Năm 2025)

| Mô hình | Vai trò | Return [%] | CAGR [%] | Sharpe | Sortino | MaxDD [%] | Calmar | Turnover [%] | Tiền mặt TB [%] |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **DYN_EW_NO_REGIME** | *Pure Stock Selection Alpha* | **+56.79%** | **+57.23%** | **1.691** | **2.124** | -25.51% | 2.243 | 523.8% | 0.00% |
| **STATIC_EW_BH** | *Internal Benchmark Buy & Hold* | **+21.61%** | **+21.76%** | **0.980** | **1.132** | -17.65% | 1.233 | 99.9% | 0.00% |
| **VNINDEX_or_MarketBenchmark**| *Thị trường Chung* | **+14.21%** | **+14.30%** | **0.690** | **0.788** | -21.90% | 0.653 | — | — |
| **DIAG_DYN_MPT_LW_REGIME** | *Diagnostic MPT Shrinkage* | **+12.01%** | **+12.09%** | **0.577** | **0.589** | -22.31% | 0.542 | 1653.6% | 38.28% |
| **DIAG_DYN_BLEND50_REGIME** | *Diagnostic 50% MPT + 50% EW* | **+2.23%** | **+2.24%** | **0.215** | **0.207** | -24.28% | 0.092 | 1363.5% | 39.02% |
| **DIAG_DYN_HRP_REGIME** | *Diagnostic HRP Risk Parity* | **-0.28%** | **-0.28%** | **0.095** | **0.090** | -22.42% | -0.013 | 1171.3% | 38.95% |
| **DIAG_DYN_MINVAR_REGIME** | *Diagnostic Minimum Variance* | **-2.24%** | **-2.25%** | **-0.007** | **-0.007** | -21.53% | -0.105 | 1091.6% | 38.44% |
| **LOCKED_CHAMPION (DYN_EW_REGIME)**| *Khóa từ Validation (Official)* | **-7.41%** | **-7.45%** | **-0.222** | **-0.210** | -26.36% | -0.283 | 1089.5% | **39.77%** |

---

## 🚀 4. Hướng Dẫn Chạy Ứng Dụng (Running the Project)

### Cách 1: Chạy Frontend Dashboard Trực Tiếp
Frontend được đóng gói theo kiến trúc SPA đọc trực tiếp từ thư mục `data/`:
```bash
# Di chuyển vào thư mục dự án
cd hose-v4-dashboard

# Chạy bằng npx (nếu có Node.js)
npx serve frontend -p 3000

# Hoặc chạy bằng Python Simple Server (Bất kỳ máy nào có Python)
python -m http.server 3000 --directory frontend
```
Mở trình duyệt tại: `http://localhost:3000`

### Cách 2: Chạy API Backend (FastAPI)
```bash
cd hose-v4-dashboard
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --port 8000
```
API Documentation: `http://localhost:8000/docs`

### Cách 3: Chạy Streamlit Dashboard (Hoặc Deploy lên Streamlit Cloud)
```bash
cd hose-v4-dashboard
pip install -r requirements.txt
streamlit run app.py
```

---

## 🛡️ 5. Kiểm Toán Toàn Vẹn Dữ Liệu (Data Integrity Validation)

Để kiểm tra xem toàn bộ các bảng dữ liệu trong `data/` có khớp 100% với file notebook V4 hay không:
```bash
python scripts/validate_data.py
```
Kết quả kiểm tra:
- `PASS:` Phát hiện đủ các tập dữ liệu JSON & CSV.
- `PASS:` Tổng số phiên Core Train (747) + Validation (249) + Final Test (248) = 1,244 phiên.
- `PASS:` Lợi nhuận của `DYN_EW_NO_REGIME` khớp chính xác `+56.794123%`.
- `PASS:` Lợi nhuận của `LOCKED_CHAMPION` khớp chính xác `-7.409582%`.
- `PASS:` Tuyệt đối không có số liệu giả lập hay nội suy.
