import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- 1. CẤU HÌNH HỆ THỐNG ---
st.set_page_config(
    page_title="DSS - Thuật toán AHP",
    layout="wide",
    initial_sidebar_state="expanded" # ĐÃ KHÔI PHỤC SIDEBAR
)

# --- 2. CSS CHUYÊN NGHIỆP ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] { 
        font-family: 'Inter', sans-serif; 
        background-color: #FAFAFA; 
        color: #1A1F36;
    }

    .block-container { padding-top: 3rem !important; padding-bottom: 2rem !important; }

    /* Custom CSS cho khối hướng dẫn */
    .guide-box {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 30px;
    }
    .guide-row { display: flex; flex-wrap: wrap; gap: 15px; font-size: 14px; color: #334155; }
    .guide-item { flex: 1; min-width: 180px; }
    .highlight { font-weight: 700; color: #0061FF; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. KHỞI TẠO SESSION STATE ---
if "token" not in st.session_state:
    st.session_state["token"] = None
if "name" not in st.session_state:
    st.session_state["name"] = "Khách hàng"
if "role" not in st.session_state:
    st.session_state["role"] = "Viewer"

# =========================================================================
# TOP NAVBAR (ĐỒNG BỘ 100% KÍCH THƯỚC CHO TẤT CẢ CÁC TRANG)
# =========================================================================
nav_1, nav_2, nav_3, nav_4, nav_space, nav_auth = st.columns([1.5, 1.5, 1.5, 1.5, 3.5, 1.5])

with nav_1: st.page_link("app.py", label="Trang chủ")
with nav_2: st.page_link("pages/3_AHP_Input.py", label="Thuật toán")
with nav_3: st.page_link("pages/4_Search_Rentals.py", label="Tìm nhà")
with nav_4: st.page_link("pages/5_Results.py", label="Báo cáo")

if not st.session_state.get("token"):
    with nav_auth:
        if st.button("Đăng nhập", use_container_width=True, key="top_login"):
            st.switch_page("pages/1_Login.py")
else:
    with nav_space:
        name = st.session_state.get('name', 'Khách hàng')
        st.markdown(f"<div style='margin-top: 8px; font-weight: 600; text-align: right; color: #4B5563;'>Chào, {name}</div>", unsafe_allow_html=True)
    with nav_auth:
        if st.button("Thoát", use_container_width=True, key="top_logout"):
            st.session_state.clear()
            st.rerun()

st.markdown("<hr style='margin-top: 5px; margin-bottom: 30px; border-color: #E5E7EB;'>", unsafe_allow_html=True)
# =========================================================================
# 5. SIDEBAR TRUYỀN THỐNG (ĐÃ KHÔI PHỤC)
# =========================================================================
with st.sidebar:
    st.markdown("### Quản trị hệ thống")
    st.markdown("---")
    if st.session_state["token"]:
        st.write(f"Người dùng: `{st.session_state['name']}`")
        st.write(f"Vai trò: `{st.session_state['role']}`")
        if st.button("Đăng xuất", use_container_width=True, key="side_logout"):
            st.session_state.clear()
            st.rerun()
    else:
        st.info("Vui lòng xác thực tài khoản.")
        if st.button("Đăng nhập", use_container_width=True, key="side_login"):
            st.switch_page("pages/1_Login.py")
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.caption("Phiên bản v2.5 - Powered by AHP")


# =========================================================================
# 6. NỘI DUNG CHÍNH: THIẾT LẬP AHP (ĐÃ THÊM DIỆN TÍCH)
# =========================================================================

st.markdown("<h2 style='font-weight: 800; color: #111827; margin-bottom: 5px;'>Thiết lập Trọng số AHP</h2>", unsafe_allow_html=True)
st.markdown("<p style='color: #4B5563; font-size: 15px; margin-bottom: 20px;'>Đánh giá mức độ quan trọng giữa 5 tiêu chí cốt lõi.</p>", unsafe_allow_html=True)

# THÊM DIỆN TÍCH VÀO DANH SÁCH TIÊU CHÍ
all_criteria = ["Giá", "Khoảng cách", "Chất lượng", "An ninh", "Diện tích"]
selected_criteria = st.multiselect(
    "1. Lựa chọn tiêu chí đưa vào mô hình:", 
    all_criteria, 
    default=["Giá", "Khoảng cách", "Chất lượng", "An ninh", "Diện tích"]
)

if len(selected_criteria) < 2:
    st.error("Hệ thống yêu cầu tối thiểu 2 tiêu chí.")
    st.stop()

# Khu vực 2: Khối Hướng dẫn
with st.expander("Bảng hướng dẫn thang điểm Saaty (1-9)", expanded=True):
    st.markdown("""
    <div class="guide-box">
        <div class="guide-row">
            <div class="guide-item"><span class="highlight">Mức 1:</span> Bằng nhau</div>
            <div class="guide-item"><span class="highlight">Mức 3:</span> Hơi quan trọng</div>
            <div class="guide-item"><span class="highlight">Mức 5:</span> Quan trọng rõ rệt</div>
            <div class="guide-item"><span class="highlight">Mức 7:</span> Rất quan trọng</div>
            <div class="guide-item"><span class="highlight">Mức 9:</span> Tuyệt đối</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<h4 style='font-weight: 700; color: #111827; margin-top: 30px; margin-bottom: 20px;'>2. Khu vực thao tác (So sánh cặp)</h4>", unsafe_allow_html=True)

n = len(selected_criteria)
matrix = np.ones((n, n))
scale_values = [1/9, 1/8, 1/7, 1/6, 1/5, 1/4, 1/3, 1/2, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]

pairs = []
for i in range(n):
    for j in range(i + 1, n):
        pairs.append((i, j))

slider_cols = st.columns(2, gap="large")

for idx, (i, j) in enumerate(pairs):
    crit_a = selected_criteria[i]
    crit_b = selected_criteria[j]
    
    def format_slider(val, a=crit_a, b=crit_b):
        if val == 1.0: return "Bằng nhau"
        elif val > 1.0: return f"Mức {int(val)} (Ưu tiên {a})"
        else: return f"Mức {int(round(1/val))} (Ưu tiên {b})"

    with slider_cols[idx % 2]:
        st.markdown(f"<div style='font-size: 15px; font-weight: 600; color: #111827;'>{crit_a} vs {crit_b}</div>", unsafe_allow_html=True)
        val = st.select_slider(
            label="Slider", label_visibility="collapsed",
            options=scale_values, value=1.0, format_func=format_slider, key=f"slider_{i}_{j}"
        )
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
        matrix[i, j] = val
        matrix[j, i] = 1 / val

# --- MA TRẬN HEATMAP ---
st.markdown("<h4 style='font-weight: 700; color: #111827; margin-top: 10px; margin-bottom: 15px;'>3. Ma trận So sánh cặp</h4>", unsafe_allow_html=True)
matrix_df = pd.DataFrame(matrix, index=selected_criteria, columns=selected_criteria)
st.dataframe(matrix_df.style.format("{:.2f}").background_gradient(cmap='Blues', axis=None), use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)
_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    btn_calc = st.button("XÁC NHẬN VÀ TÍNH TOÁN KẾT QUẢ", type="primary", use_container_width=True)

# =========================================================================
# 7. KẾT QUẢ (FIX LỖI NÚT BẤM BẰNG SESSION STATE)
# =========================================================================

# Tạo một biến flag trong session_state để giữ trạng thái đã tính toán xong
if "calculated" not in st.session_state:
    st.session_state["calculated"] = False

if btn_calc:
    st.session_state["calculated"] = True

if st.session_state["calculated"]:
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # --- LOGIC TÍNH TOÁN ---
    column_sums = matrix.sum(axis=0)
    norm_matrix = matrix / column_sums
    weights = norm_matrix.mean(axis=1)
    
    lambda_max = (matrix.dot(weights) / weights).mean()
    ci = (lambda_max - n) / (n - 1)
    ri_dict = {1: 0, 2: 0, 3: 0.58, 4: 0.9, 5: 1.12}
    cr = ci / ri_dict.get(n, 1.12)

    res_c1, res_c2 = st.columns([1, 1], gap="large")
    
    with res_c1:
        st.write("##### Bảng Vector Trọng số (%)")
        st.dataframe(pd.DataFrame({"Tiêu chí": selected_criteria, "Trọng số (%)": weights * 100}).style.format({"Trọng số (%)": "{:.2f}%"}).background_gradient(cmap='Blues'), use_container_width=True, hide_index=True)
        
        st.write("##### Kiểm định CR")
        st.info(f"CR = {cr:.4f}")
        
        if cr < 0.1:
            st.success("HỢP LỆ!")
            # Lưu vào session để trang 4 dùng được
            st.session_state["ahp_weights"] = weights.tolist()
            st.session_state["ahp_criteria"] = selected_criteria
            
            # NÚT CHUYỂN TRANG BÂY GIỜ SẼ CHẠY ĐÚNG
            if st.button("TÌM KIẾM KẾT QUẢ", type="primary", use_container_width=True):
                st.switch_page("pages/4_Search_Rentals.py")
        else:
            st.error("KHÔNG HỢP LỆ! Vui lòng điều chỉnh lại logic.")

    with res_c2:
        st.write("##### Biểu đồ Radar")
        radar_df = pd.DataFrame({"Trọng số": weights.tolist() + [weights[0]], "Tiêu chí": selected_criteria + [selected_criteria[0]]})
        fig = px.line_polar(radar_df, r="Trọng số", theta="Tiêu chí", line_close=True)
        fig.update_traces(fill='toself', line_color='#0061FF')
        st.plotly_chart(fig, use_container_width=True)