import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- 1. CẤU HÌNH HỆ THỐNG ---
st.set_page_config(
    page_title="DSS - Thuật toán AHP",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS CHUẨN TẮC KÈ HOA & KHỬ MÀU THANH TRƯỢT ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 3rem !important; padding-bottom: 2rem !important; }
    
    /* Box hướng dẫn tự đổi màu nền */
    .guide-box {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 30px;
        color: var(--text-color);
    }
    .guide-row { display: flex; flex-wrap: wrap; gap: 15px; font-size: 14px; }
    .highlight { font-weight: 700; color: var(--primary-color); }
    .sub-text { opacity: 0.7; font-size: 14px; color: var(--text-color); }

    /* ======================================================== */
    /* HACK CSS: THANH TRƯỢT TRUNG TÍNH + CỤC MỐC ĐỎ TINH TẾ    */
    /* ======================================================== */
    div[data-baseweb="slider"] > div > div > div {
        background: transparent !important; /* Tẩy phần vệt màu bị fill */
    }
    div[data-baseweb="slider"] > div > div {
        background-color: rgba(128, 128, 128, 0.25) !important; /* Thanh ngang màu xám nhạt */
    }
    div[data-baseweb="slider"] div[role="slider"] {
        background-color: #EF4444 !important; /* CỤC MỐC MÀU ĐỎ */
        border-radius: 50% !important; /* Vo tròn */
        width: 20px !important; /* Kích thước vừa phải */
        height: 20px !important; 
        border: 2px solid #FFFFFF !important; /* Viền trắng */
        box-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
        position: relative !important;
    }
    /* XÓA BỎ CÁI CHỮ 'SCALE' VÔ DUYÊN ĐI */
    div[data-baseweb="slider"] div[role="slider"]::after {
        content: none !important; 
    }
    div[data-baseweb="slider"] div[role="slider"]:hover {
        transform: scale(1.15);
    }
    /* ======================================================== */
    
    /* CSS cho đoạn text 2 đầu thanh trượt */
    .slider-edge-label {
        font-size: 12px;
        color: var(--text-color);
        opacity: 0.5;
        background-color: rgba(128,128,128,0.1);
        padding: 2px 6px;
        border-radius: 4px;
        margin-top: -10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. KHỞI TẠO SESSION STATE ---
if "token" not in st.session_state: st.session_state["token"] = None
if "name" not in st.session_state: st.session_state["name"] = "Khách hàng"
if "calculated" not in st.session_state: st.session_state["calculated"] = False
if "user_location" not in st.session_state: st.session_state["user_location"] = ""

# =========================================================================
# 4. TOP NAVBAR 
# =========================================================================
nav_1, nav_2, nav_3, nav_4, nav_space, nav_auth = st.columns([1.5, 1.5, 1.5, 1.5, 3.5, 1.5])

with nav_1: st.page_link("app.py", label="Trang chủ")
with nav_2: st.page_link("pages/3_AHP_Input.py", label="Thuật toán")
with nav_3: st.page_link("pages/4_Search_Rentals.py", label="Tìm kiếm")
with nav_4: st.page_link("pages/5_Results.py", label="Báo cáo")

if not st.session_state["token"]:
    with nav_auth:
        if st.button("Đăng nhập", use_container_width=True, key="top_login"):
            st.switch_page("pages/1_Login.py")
else:
    with nav_space:
        st.markdown(f"<div class='sub-text' style='margin-top: 8px; font-weight: 600; text-align: right;'>Chào, {st.session_state['name']}</div>", unsafe_allow_html=True)
    with nav_auth:
        if st.button("Thoát", use_container_width=True, key="top_logout"):
            st.session_state.clear()
            st.rerun()

st.markdown("<hr style='margin-top: 10px; margin-bottom: 30px; border-color: rgba(128,128,128,0.2);'>", unsafe_allow_html=True)

# =========================================================================
# 5. SIDEBAR
# =========================================================================
with st.sidebar:
    st.markdown("### Quản trị hệ thống")
    st.markdown("---")
    if st.session_state["token"]:
        st.write(f"Người dùng: `{st.session_state['name']}`")
        if st.button("Đăng xuất", use_container_width=True, key="side_logout"):
            st.session_state.clear()
            st.rerun()
    else:
        st.info("Vui lòng xác thực tài khoản.")
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.caption("Phiên bản v2.5 - Powered by AHP")

# =========================================================================
# 6. NỘI DUNG CHÍNH
# =========================================================================
st.markdown("<h2 style='font-weight: 800;'>Thiết lập Trọng số AHP</h2>", unsafe_allow_html=True)
st.markdown("<p class='sub-text' style='margin-bottom: 30px;'>Đánh giá mức độ quan trọng giữa các tiêu chí cốt lõi.</p>", unsafe_allow_html=True)

# --- BƯỚC 1: NHẬP VỊ TRÍ ---
st.markdown("<div style='font-weight: 700; font-size: 16px; margin-bottom: 10px;'>1. Nhập vị trí mong muốn (Trường học, công ty...):</div>", unsafe_allow_html=True)
user_loc = st.text_input("Vị trí của bạn", placeholder="Ví dụ: Đại học Bách Khoa, Quận 10...", label_visibility="collapsed")
st.session_state["user_location"] = user_loc

st.markdown("<br>", unsafe_allow_html=True)

# --- BƯỚC 2: CHỌN TIÊU CHÍ ---
st.markdown("<div style='font-weight: 700; font-size: 16px; margin-bottom: 10px;'>2. Lựa chọn tiêu chí đưa vào mô hình:</div>", unsafe_allow_html=True)
all_criteria = ["Giá", "Khoảng cách", "Chất lượng", "An ninh", "Diện tích"]
selected_criteria = st.multiselect("Lựa chọn tiêu chí", all_criteria, default=all_criteria, label_visibility="collapsed")

if len(selected_criteria) < 2:
    st.error("Cần tối thiểu 2 tiêu chí.")
    st.stop()

with st.expander("Bảng hướng dẫn thang điểm Saaty (1-9)", expanded=True):
    st.markdown("""
    <div class="guide-box">
        <div class="guide-row">
            <div style="flex: 1; min-width: 150px;"><span class="highlight">Mức 1:</span> Bằng nhau</div>
            <div style="flex: 1; min-width: 150px;"><span class="highlight">Mức 3:</span> Hơi quan trọng</div>
            <div style="flex: 1; min-width: 150px;"><span class="highlight">Mức 5:</span> Quan trọng rõ rệt</div>
            <div style="flex: 1; min-width: 150px;"><span class="highlight">Mức 7:</span> Rất quan trọng</div>
            <div style="flex: 1; min-width: 150px;"><span class="highlight">Mức 9:</span> Tuyệt đối</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- BƯỚC 3: SO SÁNH CẶP ---
st.markdown("<h4 style='font-weight: 700; margin-top: 20px;'>3. Khu vực thao tác (So sánh cặp)</h4>", unsafe_allow_html=True)

n = len(selected_criteria)
matrix = np.ones((n, n))
scale_values = [1/9, 1/8, 1/7, 1/6, 1/5, 1/4, 1/3, 1/2, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]

pairs = []
for i in range(n):
    for j in range(i + 1, n):
        pairs.append((i, j))

slider_cols = st.columns(2, gap="large")

for idx, (i, j) in enumerate(pairs):
    crit_a, crit_b = selected_criteria[i], selected_criteria[j]
    def format_slider(val, a=crit_a, b=crit_b):
        if val == 1.0: return "Bằng nhau"
        elif val > 1.0: return f"Mức {int(val)} (Ưu tiên {a})"
        else: return f"Mức {int(round(1/val))} (Ưu tiên {b})"

    with slider_cols[idx % 2]:
        st.markdown(f"**{crit_a}** vs **{crit_b}**")
        val = st.select_slider(
            label="Slider", label_visibility="collapsed",
            options=scale_values, value=1.0, format_func=format_slider, key=f"slider_{i}_{j}"
        )
        
        # BỔ SUNG TEXT 2 ĐẦU THANH TRƯỢT (GIỐNG ẢNH MẪU CỦA ÔNG)
        st.markdown(f"""
            <div style='display: flex; justify-content: space-between; margin-bottom: 20px;'>
                <span class='slider-edge-label'>Mức 9 (Ưu tiên {crit_b})</span>
                <span class='slider-edge-label'>Mức 9 (Ưu tiên {crit_a})</span>
            </div>
        """, unsafe_allow_html=True)
        
        matrix[i, j] = val
        matrix[j, i] = 1 / val

st.markdown("<br>", unsafe_allow_html=True)
_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    if st.button("XÁC NHẬN VÀ TÍNH TOÁN KẾT QUẢ", type="primary", use_container_width=True):
        if not user_loc.strip():
            st.warning("⚠️ Bạn nên nhập Vị trí mong muốn ở Bước 1 để hệ thống tính toán Khoảng cách chính xác hơn nhé!")
        st.session_state["calculated"] = True

# =========================================================================
# 7. HIỂN THỊ KẾT QUẢ 
# =========================================================================
if st.session_state["calculated"]:
    st.markdown("<hr style='border-color: rgba(128,128,128,0.2);'>", unsafe_allow_html=True)
    
    # === MA TRẬN SO SÁNH CẶP TIÊU CHÍ (CẤP 1) ===
    st.markdown("#####  Ma trận So sánh cặp Tiêu chí ")
    st.markdown("<p class='sub-text' style='margin-bottom: 15px;'>Ma trận thể hiện tỷ lệ ưu tiên giữa các tiêu chí do bạn vừa thiết lập.</p>", unsafe_allow_html=True)
    df_matrix = pd.DataFrame(matrix, index=selected_criteria, columns=selected_criteria).round(2)
    st.dataframe(df_matrix, use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    weights = (matrix / matrix.sum(axis=0)).mean(axis=1)
    lambda_max = (matrix.dot(weights) / weights).mean()
    ci = (lambda_max - n) / (n - 1)
    ri = {1: 0, 2: 0, 3: 0.58, 4: 0.9, 5: 1.12}.get(n, 1.12)
    cr = ci / ri

    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        st.markdown("##### Vector Trọng số (%)")
        st.dataframe(pd.DataFrame({"Tiêu chí": selected_criteria, "Trọng số (%)": weights * 100}).style.format({"Trọng số (%)": "{:.2f}%"}), use_container_width=True, hide_index=True)
        st.info(f"Chỉ số nhất quán CR = {cr:.4f}")
        
        if cr < 0.1:
            st.success("HỢP LỆ! Logic so sánh nhất quán.")
            st.session_state["ahp_weights"] = weights.tolist()
            st.session_state["ahp_criteria"] = selected_criteria
            if st.button("CHUYỂN SANG TÌM KIẾM", type="primary", use_container_width=True):
                st.switch_page("pages/4_Search_Rentals.py")
        else:
            st.error("KHÔNG HỢP LỆ! Vui lòng điều chỉnh lại thanh trượt (CR >= 0.1).")
    with c2:
        st.markdown("##### Biểu đồ Radar")
        radar_df = pd.DataFrame({"Trọng số": weights.tolist() + [weights[0]], "Tiêu chí": selected_criteria + [selected_criteria[0]]})
        fig = px.line_polar(radar_df, r="Trọng số", theta="Tiêu chí", line_close=True)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)