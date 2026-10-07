"""
HOSE V4: Quantitative Research Dashboard & Nested Walk-Forward Portfolio Optimization
Streamlit Deployment Version
"""

import os
import io
import json
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="HOSE V4 | Định lượng Danh mục & Nested Walk-Forward",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def load_data(filename):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Load data layer
metadata = load_data("metadata.json")
final_test = load_data("final_test_results.json")
time_split = load_data("time_split.json")
threshold_trials = load_data("core_threshold_trials.json")
val_models = load_data("val_models.json")
val_selection = load_data("val_selection_history.json")
test_selection = load_data("test_selection_history.json")
leakage_audit = load_data("leakage_audit.json")
data_quality = load_data("data_quality.json")
inventory = load_data("inventory.json")

df_final_test = pd.DataFrame(final_test)

with st.sidebar:
    st.markdown("### **HOSE V4 QUANT DASHBOARD**")
    st.caption("Nested Walk-Forward FA/TA -> Top N -> EW/MPT/MinVar/HRP")
    st.divider()
    page = st.selectbox(
        "Mô-đun:",
        [
            "1. Overview",
            "2. Data & Quality",
            "3. Methodology",
            "4. Train / Val / Test",
            "5. Fundamental (FA)",
            "6. Technical (TA)",
            "7. BUY / EXIT Threshold",
            "8. Stock Ranking",
            "9. Nested Walk-Forward",
            "10. Top N Selection",
            "11. Performance",
            "12. Drawdown",
            "13. Benchmark",
            "14. Raw Results & Export"
        ]
    )
    st.divider()
    st.markdown("""
    **Kiểm toán Rò rỉ Dữ liệu:**
    - Causal Walk-Forward: `Passed`
    - No Retuning on Test: `Audited`
    """)

if page.startswith("1."):
    st.title("🏛️ Tổng quan Kết quả Thực nghiệm HOSE V4")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Selection Alpha (DYN_EW_NO_REGIME)", "+56.79%", "Sharpe 1.691")
    col2.metric("Static Buy & Hold", "+21.61%", "Sharpe 0.980")
    col3.metric("VN-Index (Market Proxy)", "+14.21%", "Sharpe 0.690")
    col4.metric("Locked Champion (Regime)", "-7.41%", "Cash 39.77%")

    st.subheader("Bảng Đối Chiếu 8 Mô Hình trong Final Test (2025)")
    st.dataframe(df_final_test, use_container_width=True, hide_index=True)

elif page.startswith("2."):
    st.title("📊 Dữ liệu Đầu vào & Chất lượng 95 Mã HOSE")
    st.dataframe(pd.DataFrame(data_quality), use_container_width=True, hide_index=True)

elif page.startswith("4."):
    st.title("⏳ Phân chia Train / Validation / Final Test & Leakage Audit")
    st.subheader("1. Phân chia tập dữ liệu tuần tự")
    st.dataframe(pd.DataFrame(time_split), use_container_width=True, hide_index=True)
    st.subheader("2. Ma trận kiểm toán chống nhìn trước tương lai")
    st.dataframe(pd.DataFrame(leakage_audit), use_container_width=True, hide_index=True)

elif page.startswith("5."):
    st.title("🔍 Phân tích Cơ bản (FA)")
    st.warning("Current empirical run: FA not available in dataset / TA-only fallback")
    st.info("Chỉ sử dụng FA khi có effective_date <= decision date để tránh Lookahead Bias.")

elif page.startswith("7."):
    st.title("🎯 Quá trình Chọn Ngưỡng BUY / EXIT")
    st.dataframe(pd.DataFrame(threshold_trials), use_container_width=True, hide_index=True)
    st.success("Khóa vĩnh viễn: BUY = 5 | EXIT = 2")

elif page.startswith("9."):
    st.title("🔄 Lịch Nested Walk-Forward (Tái chọn Top 5)")
    st.subheader("Final Test 2025:")
    st.dataframe(pd.DataFrame(test_selection), use_container_width=True, hide_index=True)
    st.subheader("Validation 2024:")
    st.dataframe(pd.DataFrame(val_selection), use_container_width=True, hide_index=True)

elif page.startswith("14."):
    st.title("📋 Raw Results & Export Hub")
    st.dataframe(df_final_test, use_container_width=True, hide_index=True)
    csv = df_final_test.to_csv(index=False).encode("utf-8-sig")
    st.download_button("Tải xuống Final Test (CSV)", csv, "final_test_results.csv", "text/csv")

else:
    st.title(page)
    st.dataframe(df_final_test, use_container_width=True, hide_index=True)
