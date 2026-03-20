import streamlit as st
import pandas as pd
import numpy as np

# --- 1. CẤU HÌNH HỆ THỐNG ---
st.set_page_config(
    page_title="DSS - Tìm Kiếm Căn Hộ", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 3.5rem !important; }
    
    /* Box đổi màu tự động */
    .theme-card, .guide-box, .filter-container {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        color: var(--text-color);
    }
    
    .sub-text { opacity: 0.7; font-size: 14px; }
    .highlight { font-weight: 700; color: var(--primary-color); }
    </style>
    """, unsafe_allow_html=True)

# =========================================================================
# TOP NAVBAR (ĐỒNG BỘ 100% KÍCH THƯỚC CHO TẤT CẢ CÁC TRANG)
# =========================================================================
nav_1, nav_2, nav_3, nav_4, nav_space, nav_auth = st.columns([1.5, 1.5, 1.5, 1.5, 3.5, 1.5])

with nav_1: st.page_link("app.py", label="Trang chủ")
with nav_2: st.page_link("pages/3_AHP_Input.py", label="Thuật toán")
with nav_3: st.page_link("pages/4_Search_Rentals.py", label="Tìm kiếm")
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
# 4. HÀM NỘI SUY (MAPPING)
# =========================================================================
def get_price_desc(v): return f"{1 + (v - 1) * (9/8):.1f} Triệu"
def get_area_desc(v): return f"{int(15 + (v - 1) * (85/8))} m2"

def get_security_detail(v):
    v = int(v)
    descs = {
        9: "Tuyệt đối: Bảo vệ 24/7, Camera toàn khu, Thẻ từ thang máy",
        8: "Rất cao: Khóa vân tay, Cổng tự động, Camera an ninh",
        7: "Cao: Khu dân trí, Camera hành lang, Cửa khóa từ",
        6: "Tốt: Khóa cổng chung vân tay, Khu vực yên tĩnh",
        5: "Ổn định: Có cổng khóa riêng, Khu phố văn hóa",
        4: "Khá: Cổng chung khóa chìa, Dân cư lâu năm",
        3: "Trung bình: Khóa cổng ngoài, Cửa phòng gỗ",
        2: "Cơ bản: Nhà trong hẻm, Cổng sắt truyền thống",
        1: "Tối giản: Khu vực tự quản, Không có camera"
    }
    return descs.get(v, "Bình thường")

# =========================================================================
# 5. TẢI DỮ LIỆU & BỘ LỌC (THANH TRƯỢT MỘT ĐẦU)
# =========================================================================
try:
    df = pd.read_excel("AHP11.xlsx", sheet_name="DuLieu_ThucTe_TPHCM")
except:
    st.error("Không tìm thấy file AHP11.xlsx")
    st.stop()

st.markdown('<div class="filter-title">Bộ lọc tìm kiếm căn hộ</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    f_col1, f_col2, f_col3 = st.columns([2, 2, 2], gap="large")
    
    with f_col1:
        search_query = st.text_input("Tìm kiếm:", placeholder="Tên nhà hoặc địa chỉ...")
    
    with f_col2:
        p_range = st.slider("Ngân sách tối đa (Triệu):", 1.0, 10.0, 10.0, step=0.5)
    
    with f_col3:
        # ĐÃ SỬA: Khóa đầu trái 15, chỉ cho chỉnh đầu phải (Max Area)
        max_area = st.slider("Diện tích tối đa (Từ 15m² đến...):", 15, 100, 100)
    st.markdown('</div>', unsafe_allow_html=True)

# --- LOGIC LỌC ---
df_f = df.copy()
if search_query:
    df_f = df_f[df_f['Tên nhà'].str.contains(search_query, case=False, na=False) | 
                df_f['Địa chỉ'].str.contains(search_query, case=False, na=False)]

# Map ngược giá trị về 1-9
v_max_p = 1 + (p_range - 1) * (8 / 9)
v_max_a = 1 + (max_area - 15) * (8 / 85)

# Lọc: Mặc định tối thiểu luôn là thấp nhất (1 trong hệ 1-9 hoặc 15m2/1Tr)
df_f = df_f[(df_f['Giá'] <= v_max_p) & (df_f['Diện tích'] <= v_max_a)]

# =========================================================================
# 6. HIỂN THỊ KẾT QUẢ
# =========================================================================
if "ahp_weights" not in st.session_state:
    st.info("Hãy thực hiện AHP để xếp hạng kết quả.")
    df_f['Giá thuê'] = df_f['Giá'].apply(get_price_desc)
    df_f['Diện tích m2'] = df_f['Diện tích'].apply(get_area_desc)
    df_f['An ninh'] = df_f['An ninh'].apply(get_security_detail)
    st.dataframe(df_f[['Mã', 'Tên nhà', 'Địa chỉ', 'Giá thuê', 'Diện tích m2', 'An ninh']], use_container_width=True, hide_index=True)
else:
    w = st.session_state["ahp_weights"]
    if not df_f.empty:
        # Chuẩn hóa & Tính điểm
        for col, key in zip(['Giá', 'Chất lượng', 'An ninh', 'Diện tích'], ['G_n', 'CL_n', 'AN_n', 'DT_n']):
            if col == 'Giá':
                df_f[key] = (df_f[col].max() - df_f[col]) / (df_f[col].max() - df_f[col].min() + 0.001)
            else:
                df_f[key] = (df_f[col] - df_f[col].min()) / (df_f[col].max() - df_f[col].min() + 0.001)

        df_f['Score'] = (df_f['G_n']*w[0] + df_f['CL_n']*w[2] + df_f['AN_n']*w[3] + df_f['DT_n']*w[4])
        df_res = df_f.sort_values('Score', ascending=False)

        # Định dạng hiển thị
        df_res['Giá thuê'] = df_res['Giá'].apply(get_price_desc)
        df_res['Diện tích m2'] = df_res['Diện tích'].apply(get_area_desc)
        df_res['An ninh'] = df_res['An ninh'].apply(get_security_detail)
        df_res['Phù hợp (%)'] = (df_res['Score'] * 100).round(1)

        st.markdown(f"#### Tìm thấy **{len(df_res)}** căn hộ (15m² - {max_area}m²):")
        st.dataframe(
            df_res[['Mã', 'Tên nhà', 'Địa chỉ', 'Giá thuê', 'Diện tích m2', 'An ninh', 'Phù hợp (%)']],
            use_container_width=True, hide_index=True
        )
    else:
        st.warning("Không có căn hộ nào nằm trong khoảng diện tích và giá này.")

if st.button("XEM CHI TIẾT BÁO CÁO", type="primary"):
    st.switch_page("pages/5_Results.py")