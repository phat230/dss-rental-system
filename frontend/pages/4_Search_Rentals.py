import streamlit as st
import pandas as pd
import numpy as np
import requests

API = "http://127.0.0.1:8000"

# --- 1. CẤU HÌNH HỆ THỐNG ---
st.set_page_config(
    page_title="DSS - Tìm Kiếm Căn Hộ", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. CSS CHUẨN TẮC KÈ HOA ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 3.5rem !important; }
    
    .filter-container {
        background-color: var(--secondary-background-color);
        padding: 25px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.2);
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 30px;
    }
    .filter-title { font-weight: 700; margin-bottom: 15px; font-size: 18px; }
    .sub-text { opacity: 0.7; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. KHỞI TẠO SESSION STATE ---
if "token" not in st.session_state: st.session_state["token"] = None
if "name" not in st.session_state: st.session_state["name"] = "Khách hàng"

# =========================================================================
# 4. TOP NAVBAR 
# =========================================================================
nav_1, nav_2, nav_3, nav_4, nav_space, nav_auth = st.columns([1.5, 1.5, 1.5, 1.5, 3.5, 1.5])

with nav_1: st.page_link("app.py", label="Trang chủ")
with nav_2: st.page_link("pages/3_AHP_Input.py", label="Thuật toán")
with nav_3: st.page_link("pages/4_Search_Rentals.py", label="Tìm nhà")
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

st.markdown("<hr style='margin-top: 5px; margin-bottom: 30px; border-color: rgba(128,128,128,0.2);'>", unsafe_allow_html=True)

# =========================================================================
# 5. HÀM NỘI SUY (TƯƠNG THÍCH ĐA NGUỒN)
# =========================================================================
def get_price_desc(v): return f"{1 + (v - 1) * (9/8):.1f} Triệu" if pd.notna(v) else "N/A"
def get_area_desc(v): return f"{int(15 + (v - 1) * (85/8))} m2" if pd.notna(v) else "N/A"
def get_security_detail(v):
    if pd.isna(v): return "N/A"
    descs = {
        9: "Tuyệt đối: Bảo vệ 24/7", 8: "Rất cao: Khóa vân tay",
        7: "Cao: Camera hành lang", 6: "Tốt: Cổng vân tay",
        5: "Ổn định: Khu an ninh", 4: "Khá: Dân cư lâu năm",
        3: "Trung bình: Khóa cổng", 2: "Cơ bản: Cổng sắt", 1: "Tối giản"
    }
    return descs.get(int(v), "Bình thường")

# =========================================================================
# 6. GỘP DỮ LIỆU TỪ EXCEL & BACKEND API (FUSION DATA)
# =========================================================================
@st.cache_data(ttl=10) # Cache nhẹ để tránh gọi API liên tục gây lag
def load_and_merge_data():
    # 1. Tải dữ liệu Excel gốc
    try:
        df_excel = pd.read_excel("AHP11.xlsx", sheet_name="DuLieu_ThucTe_TPHCM")
    except:
        df_excel = pd.DataFrame()

    # 2. Tải dữ liệu từ Backend
    df_backend = pd.DataFrame()
    try:
        headers = {"token": st.session_state.get("token", "fake_token")}
        res = requests.get(f"{API}/admin/rentals", headers=headers, timeout=2)
        
        if res.status_code == 200:
            raw_data = res.json()
            if isinstance(raw_data, list) and len(raw_data) > 0:
                tmp = pd.DataFrame(raw_data)
                
                # Ánh xạ tên cột cho giống Excel
                tmp['Tên nhà'] = tmp.get('title', 'Phòng mới')
                tmp['Địa chỉ'] = tmp.get('location', 'Đang cập nhật')
                
                # CHUẨN HÓA TOÁN HỌC: Đổi VNĐ và m2 thực tế về thang điểm 1-9 để AHP tính được
                if 'price' in tmp.columns:
                    prices_m = pd.to_numeric(tmp['price'], errors='coerce') / 1000000
                    tmp['Giá'] = 1 + (prices_m - 1) * (8 / 9)
                    
                if 'area' in tmp.columns:
                    areas = pd.to_numeric(tmp['area'], errors='coerce')
                    tmp['Diện tích'] = 1 + (areas - 15) * (8 / 85)
                    
                if 'security' in tmp.columns:
                    tmp['An ninh'] = pd.to_numeric(tmp['security'], errors='coerce')
                    
                if 'amenities' in tmp.columns:
                    tmp['Chất lượng'] = pd.to_numeric(tmp['amenities'], errors='coerce')
                    
                # Tạo Khoảng cách ngẫu nhiên cho phòng backend vì admin form không có nhập
                np.random.seed(42)
                tmp['Khoảng cách'] = np.random.uniform(1.0, 9.0, size=len(tmp))
                
                cols_to_keep = ['Tên nhà', 'Địa chỉ', 'Giá', 'Diện tích', 'An ninh', 'Chất lượng', 'Khoảng cách']
                # Lưu lại cái ảnh ngầm bên trong để mốt đẩy sang trang 5
                if 'image_url' in tmp.columns:
                    cols_to_keep.append('image_url')
                    
                df_backend = tmp[[c for c in cols_to_keep if c in tmp.columns]].copy()
    except Exception as e:
        pass # Nếu backend sập thì im lặng xài tiếp excel

    # 3. Gộp 2 mảng dữ liệu (Cho Backend lên trước cho dễ thấy)
    if not df_excel.empty and not df_backend.empty:
        return pd.concat([df_backend, df_excel], ignore_index=True)
    elif not df_excel.empty:
        return df_excel.copy()
    elif not df_backend.empty:
        return df_backend.copy()
    else:
        return pd.DataFrame()

# Nạp dữ liệu
df = load_and_merge_data()

if df.empty:
    st.error("Hệ thống đang bảo trì: Không tìm thấy dữ liệu từ cả Excel và Backend!")
    st.stop()

# =========================================================================
# 7. BỘ LỌC TÌM KIẾM
# =========================================================================
st.markdown('<div class="filter-title">Bộ lọc tìm kiếm căn hộ</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    f_col1, f_col2, f_col3 = st.columns([2, 2, 2], gap="large")
    with f_col1:
        search_query = st.text_input("Tìm kiếm:", placeholder="Tên nhà hoặc địa chỉ...")
    with f_col2:
        p_max = st.slider("Ngân sách tối đa (Triệu):", 1.0, 10.0, 10.0, step=0.5)
    with f_col3:
        a_max = st.slider("Diện tích tối đa (m2):", 15, 100, 100)
    st.markdown('</div>', unsafe_allow_html=True)

df_f = df.copy()

if search_query and 'Tên nhà' in df_f.columns and 'Địa chỉ' in df_f.columns:
    df_f = df_f[df_f['Tên nhà'].astype(str).str.contains(search_query, case=False, na=False) | 
                df_f['Địa chỉ'].astype(str).str.contains(search_query, case=False, na=False)]

if 'Giá' in df_f.columns:
    v_max_p = 1 + (p_max - 1) * (8 / 9)
    df_f = df_f[df_f['Giá'] <= v_max_p]

if 'Diện tích' in df_f.columns:
    v_max_a = 1 + (a_max - 15) * (8 / 85)
    df_f = df_f[df_f['Diện tích'] <= v_max_a]

# =========================================================================
# 8. THUẬT TOÁN AHP VÀ MA TRẬN SAATY
# =========================================================================
if "ahp_weights" not in st.session_state or "ahp_criteria" not in st.session_state:
    st.info("💡 Hãy thực hiện Thuật toán AHP ở trang trước để hệ thống sắp xếp độ phù hợp cho bạn nhé!")
    
    if 'Giá' in df_f.columns: df_f['Giá thuê'] = df_f['Giá'].apply(get_price_desc)
    if 'Diện tích' in df_f.columns: df_f['Diện tích m2'] = df_f['Diện tích'].apply(get_area_desc)
    if 'An ninh' in df_f.columns: df_f['An ninh thực'] = df_f['An ninh'].apply(get_security_detail)
    
    # ĐÃ XÓA SẠCH CỘT "MÃ" TRONG BẢNG HIỂN THỊ
    display_cols = [c for c in ['Tên nhà', 'Địa chỉ', 'Giá thuê', 'Diện tích m2', 'An ninh thực'] if c in df_f.columns]
    st.dataframe(df_f[display_cols], use_container_width=True, hide_index=True)
else:
    w = st.session_state["ahp_weights"]
    cri = st.session_state["ahp_criteria"]
    weight_dict = dict(zip(cri, w))

    if not df_f.empty:
        # Tính điểm tổng hợp Score
        df_f['Score'] = 0.0
        for col in ['Giá', 'Khoảng cách', 'Chất lượng', 'An ninh', 'Diện tích']:
            if col in df_f.columns and col in weight_dict:
                c_min, c_max = df_f[col].min(), df_f[col].max()
                if c_max == c_min: c_max += 0.001
                
                if col in ['Giá', 'Khoảng cách']:
                    n_val = (c_max - df_f[col]) / (c_max - c_min)
                else:
                    n_val = (df_f[col] - c_min) / (c_max - c_min)
                    
                df_f['Score'] += n_val * weight_dict[col]

        df_res = df_f.sort_values('Score', ascending=False)
        
        # -------------------------------------------------------------------------
        # 1. BẢNG XẾP HẠNG TỔNG HỢP 
        # -------------------------------------------------------------------------
        st.markdown(f"#### 🏆 Tổng hợp: Đã tìm thấy **{len(df_res)}** căn hộ thỏa mãn bộ lọc")
        
        if 'Giá' in df_res.columns: df_res['Giá thuê'] = df_res['Giá'].apply(get_price_desc)
        if 'Diện tích' in df_res.columns: df_res['Diện tích m2'] = df_res['Diện tích'].apply(get_area_desc)
        if 'An ninh' in df_res.columns: df_res['An ninh thực'] = df_res['An ninh'].apply(get_security_detail)
        df_res['Phù hợp (%)'] = (df_res['Score'] * 100).round(1)

        # ĐÃ XÓA SẠCH CỘT "MÃ" TRONG BẢNG KẾT QUẢ AHP
        display_cols = [c for c in ['Tên nhà', 'Địa chỉ', 'Giá thuê', 'Diện tích m2', 'An ninh thực', 'Phù hợp (%)'] if c in df_res.columns]
        st.dataframe(df_res[display_cols], use_container_width=True, hide_index=True)
        
        st.markdown("<hr style='border-color: rgba(128,128,128,0.2); margin-top:30px; margin-bottom:30px;'>", unsafe_allow_html=True)

        # -------------------------------------------------------------------------
        # 2. MA TRẬN SAATY SO SÁNH CHÉO (CẤP 2)
        # -------------------------------------------------------------------------
        st.markdown("### 📊 Ma trận Saaty so sánh Phương án (Cấp độ 2)")
        st.markdown("<p class='sub-text' style='margin-bottom:20px;'>Hệ thống nội suy Ma trận vuông so sánh cặp dựa trên 5 phương án dẫn đầu để đảm bảo tính đồng nhất tuyệt đối trong đánh giá AHP.</p>", unsafe_allow_html=True)
        
        sorted_criteria = sorted(weight_dict.items(), key=lambda item: item[1], reverse=True)
        top_5_overall = df_res.head(5)
        global_names = top_5_overall['Tên nhà'].astype(str).tolist()
        
        legend_html = "<div style='font-size: 14px; opacity: 0.9; margin-bottom: 20px; padding: 15px; background-color: rgba(128,128,128,0.05); border-radius: 8px; border-left: 4px solid #3B82F6;'>"
        legend_html += "<b style='display:block; margin-bottom:8px; font-size:15px;'>Quy ước chung cho các Phương án (PA):</b>"
        for k in range(len(global_names)):
            legend_html += f"<b>PA{k+1}:</b> {global_names[k]} <br>"
        legend_html += "</div>"
        st.markdown(legend_html, unsafe_allow_html=True)
        
        for i in range(0, len(sorted_criteria), 2):
            cols = st.columns(2, gap="medium")
            for j in range(2):
                if i + j < len(sorted_criteria):
                    crit_name, crit_weight = sorted_criteria[i+j]
                    if crit_name in df_f.columns:
                        with cols[j]:
                            st.markdown(f"**🔹 Ma trận Tiêu chí: {crit_name}** <span style='color:#3B82F6; font-weight:bold;'>(Trọng số: {crit_weight*100:.1f}%)</span>", unsafe_allow_html=True)
                            
                            vals = top_5_overall[crit_name].tolist()
                            size = len(vals)
                            mat = np.ones((size, size))
                            
                            for r in range(size):
                                for c in range(size):
                                    vr = vals[r] if vals[r] != 0 else 0.001
                                    vc = vals[c] if vals[c] != 0 else 0.001
                                    
                                    if crit_name in ['Giá', 'Khoảng cách']:
                                        mat[r, c] = vc / vr 
                                    else:
                                        mat[r, c] = vr / vc 
                                        
                            short_names = [f"PA{k+1}" for k in range(size)]
                            df_mat = pd.DataFrame(mat, index=short_names, columns=short_names).round(2)
                            st.dataframe(df_mat, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)
if st.button("XEM CHI TIẾT BÁO CÁO", type="primary"):
    st.switch_page("pages/5_Results.py")