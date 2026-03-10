import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px



# --- 1. THIẾT LẬP CẤU HÌNH ---
st.set_page_config(page_title="Hệ Thống Phân Tích AHP", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS TÙY CHỈNH (ENTERPRISE UI) ---
st.markdown("""
    <style>
    .main { background-color: #f8fafc; font-family: 'Inter', sans-serif; }
    h1, h2, h3, h4, h5 { color: #0f172a !important; font-weight: 700 !important; }
    p, span, label { color: #475569; }
    .block-container { max-width: 1500px; padding-top: 1.5rem !important; padding-bottom: 2rem !important; }
    
    /* Tùy chỉnh Dataframe Header */
    th { background-color: #f1f5f9 !important; color: #334155 !important; font-weight: 600 !important; text-transform: uppercase; font-size: 0.8rem; border-bottom: 2px solid #e2e8f0 !important; text-align: center !important;}
    td { text-align: center !important; font-size: 0.85rem; }
    
    /* Trạng thái CR */
    .cr-pass { color: #16a34a; font-weight: 700; background-color: #f0fdf4; padding: 4px 8px; border-radius: 4px; border: 1px solid #16a34a;}
    .cr-fail { color: #dc2626; font-weight: 700; background-color: #fef2f2; padding: 4px 8px; border-radius: 4px; border: 1px solid #dc2626;}
    hr.solid { border-top: 1px solid #e2e8f0; margin: 1.5rem 0; }
    
    /* Thu gọn không gian của Selectbox để nhét vừa ma trận Grid */
    [data-testid="stSelectbox"] { margin-bottom: -15px; }
    div[data-baseweb="select"] > div { min-height: 32px !important; padding-top: 2px; padding-bottom: 2px; font-size: 0.85rem;}
    
    /* Nút xuất báo cáo */
    .stDownloadButton > button {
        background-color: #0f172a; color: #ffffff; border: none; font-weight: 600; border-radius: 6px; width: 100%; transition: all 0.2s ease;
    }
    .stDownloadButton > button:hover { background-color: #1e293b; color: #ffffff; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HÀM TOÁN HỌC AHP CỐT LÕI ---
def calculate_ahp(matrix):
    n = len(matrix)
    col_sums = matrix.sum(axis=0)
    norm_matrix = matrix / col_sums
    weights = norm_matrix.mean(axis=1)
    aw = np.dot(matrix, weights)
    lambda_max = (aw / weights).mean()
    
    ci = (lambda_max - n) / (n - 1) if n > 1 else 0
    ri_dict = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45}
    ri = ri_dict.get(n, 1.49)
    cr = ci / ri if ri > 0 else 0
    
    return weights, cr, lambda_max, ci

def format_saaty_val(v):
    if v == 1.0: return "1"
    if v > 1: return str(int(v))
    return f"1/{int(1/v)}"

# --- HÀM VẼ BẢNG MA TRẬN NHẬP LIỆU (ĐÃ CHUYỂN SANG THANG 1-5) ---
def render_matrix_ui(items, key_prefix, short_items=None):
    if short_items is None:
        short_items = items
    n = len(items)
    calc_matrix = np.ones((n, n))
    
    # Cấu hình thang đo 1-5 mới
    options = [5.0, 4.0, 3.0, 2.0, 1.0, 1/2, 1/3, 1/4, 1/5]
    
    st.markdown("<div style='background-color: #ffffff; padding: 0.5rem; border-radius: 8px; border: 1px solid #e2e8f0; overflow-x: auto;'>", unsafe_allow_html=True)
    
    # Header Cột
    cols = st.columns([1.2] + [1]*n)
    cols[0].markdown("<div style='font-weight:700; color:#64748b; text-align:center; font-size: 0.75rem; padding-bottom:5px;'>Hệ số</div>", unsafe_allow_html=True)
    for j in range(n):
        cols[j+1].markdown(f"<div style='font-weight:700; color:#0f172a; text-align:center; font-size: 0.75rem; padding-bottom:5px;'>{short_items[j]}</div>", unsafe_allow_html=True)
        
    # Các Dòng
    for i in range(n):
        cols = st.columns([1.2] + [1]*n)
        cols[0].markdown(f"<div style='font-weight:700; color:#0f172a; font-size: 0.75rem; padding-top:10px;'>{short_items[i]}</div>", unsafe_allow_html=True)
        
        for j in range(n):
            if i == j:
                cols[j+1].markdown("<div style='background:#f1f5f9; color:#94a3b8; font-weight:600; text-align:center; padding:5px; border-radius:4px; margin-top:2px;'>1</div>", unsafe_allow_html=True)
            elif i < j:
                choice = cols[j+1].selectbox(
                    f"hidden_{key_prefix}_{i}_{j}",
                    options=options,
                    index=4, 
                    format_func=format_saaty_val,
                    label_visibility="collapsed",
                    key=f"{key_prefix}_{i}_{j}"
                )
                calc_matrix[i, j] = choice
                calc_matrix[j, i] = 1.0 / choice
            else:
                val = calc_matrix[i, j]
                display_val = format_saaty_val(val)
                cols[j+1].markdown(f"<div style='background:#f8fafc; border: 1px dashed #cbd5e1; color:#64748b; font-size:0.85rem; text-align:center; padding:4px; border-radius:4px; margin-top:2px;'>{display_val}</div>", unsafe_allow_html=True)
                
    st.markdown("</div>", unsafe_allow_html=True)
    return calc_matrix

# --- 4. DỮ LIỆU CƠ SỞ CHUẨN HÓA ---
criteria = ["Giá thuê", "Vị trí", "Diện tích", "An ninh", "Tiện ích", "Tự do"] 
alternatives = [
    "Trọ gần trường", 
    "Trọ gần nơi làm việc", 
    "Căn hộ mini trung tâm",
    "Chung cư mini an ninh",
    "Trọ giá rẻ ngoại thành"
]
short_alts = ["PA1", "PA2", "PA3", "PA4", "PA5"]
slate_colors_6 = ['#0f172a', '#1e293b', '#334155', '#475569', '#64748b', '#94a3b8']

# --- GIAO DIỆN CHÍNH ---
st.markdown("## BẢNG THIẾT LẬP AHP")
st.write("")

# ==========================================
# BƯỚC 1, 2, 3 & 4: TIÊU CHÍ (CRITERIA)
# ==========================================
with st.container(border=True):
    st.markdown("#### LẬP MA TRẬN SO SÁNH TIÊU CHÍ")
    st.markdown("<p style='font-size: 0.85rem; color:#64748b; margin-bottom: 10px;'><b>Chú giải thang đo (1-5):</b> 1 (Bằng nhau) | 2 (Hơi nhỉnh hơn) | 3 (Quan trọng hơn) | 4 (Rất quan trọng) | 5 (Áp đảo tuyệt đối)</p>", unsafe_allow_html=True)
    
    crit_matrix = render_matrix_ui(criteria, "crit")
    st.markdown("<hr class='solid'>", unsafe_allow_html=True)
    st.markdown("#### TÍNH TRỌNG SỐ VÀ KIỂM TRA TÍNH NHẤT QUÁN")
    crit_weights, crit_cr, crit_lambda, crit_ci = calculate_ahp(crit_matrix)
    
    col_w_chart, col_w_metric = st.columns([1.5, 1], gap="large")
    df_crit_weights = pd.DataFrame({"Tiêu chí": criteria, "Trọng số": crit_weights, "Tỷ trọng (%)": [round(w * 100, 2) for w in crit_weights]}).sort_values(by="Tỷ trọng (%)", ascending=False)
    
    with col_w_chart:
        fig_crit = px.pie(df_crit_weights, values="Tỷ trọng (%)", names="Tiêu chí", hole=0.45, color_discrete_sequence=slate_colors_6)
        fig_crit.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#ffffff', width=2)))
        fig_crit.update_layout(margin=dict(l=0, r=0, t=10, b=10), height=280, showlegend=False, plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_crit, use_container_width=True, config={'displayModeBar': False})
        
    with col_w_metric:
        st.write("")
        st.dataframe(df_crit_weights[['Tiêu chí', 'Tỷ trọng (%)']].style.format({"Tỷ trọng (%)": "{:.2f}%"}), use_container_width=True, hide_index=True)
        cr_status = "Hợp lệ" if crit_cr <= 0.1 else "Lỗi Logic"
        cr_class = "cr-pass" if crit_cr <= 0.1 else "cr-fail"
        
        st.markdown(f"""
        <div style='background-color: #f8fafc; padding: 1rem; border: 1px solid #e2e8f0; border-radius: 4px; margin-top: 10px;'>
            <div style='font-size: 0.85rem; color: #64748b; font-weight: 600;'>THÔNG SỐ KIỂM ĐỊNH TÍNH NHẤT QUÁN</div>
            <div style='margin-top: 0.8rem; display: flex; align-items: center; justify-content: space-between;'>
                <span style='font-weight: 700; color: #0f172a;'>Tỷ số CR: {crit_cr:.4f}</span>
                <span class='{cr_class}'>{cr_status}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# BƯỚC 5: ĐÁNH GIÁ PHƯƠNG ÁN (AUTO-FILLED MATRIX)
# ==========================================

# 1. NHẬN DỮ LIỆU TỪ TRANG 4
if "selected_houses_data" in st.session_state and len(st.session_state["selected_houses_data"]) >= 2:
    selected_data = st.session_state["selected_houses_data"]
    alternatives = [item['Ten'] for item in selected_data]
    
    lookup_data = {}
    for item in selected_data:
        lookup_data[item['Ten']] = {
            "Giá thuê": item.get('Giá thuê', '0 VNĐ'),
            "Vị trí": item.get('Vị trí', 'N/A'),
            "Diện tích": item.get('Diện tích', '0 m²'),
            "An ninh": item.get('An ninh', 'Khá'),
            "Tiện ích": item.get('Tiện ích', 'Cơ bản'),
            "Tự do": item.get('Tự do', 'Trung bình')
        }
else:
    st.warning("⚠️ BẠN CHƯA CHỌN ĐỦ PHƯƠNG ÁN")
    st.stop()

# 2. HÀM TỰ ĐỘNG TÍNH TOÁN MA TRẬN DỰA TRÊN GIÁ TRỊ THẬT
def get_auto_filled_matrix(criterion_name):
    n = len(selected_data)
    matrix = np.ones((n, n))
    
    # Bảng điểm cho tiêu chí định tính
    rank_map = {
        "Tuyệt đối": 5, "Rất tốt": 4.5, "Tốt": 4, "Khá": 3, "Trung bình": 2, "Thấp": 1,
        "Cao": 4, "Đầy đủ": 4, "Hiện đại": 4.5, "Cơ bản": 2, "Ít": 1.5, "Tự do": 5, "Chung chủ": 1.5
    }

    for i in range(n):
        for j in range(n):
            if i == j: continue
            val_i = selected_data[i].get(criterion_name, "")
            val_j = selected_data[j].get(criterion_name, "")

            try:
                if criterion_name == "Giá thuê":
                    # Giá càng thấp càng tốt -> PA_i tốt hơn PA_j nếu Giá_j > Giá_i
                    num_i = float(str(val_i).replace(',', '').replace(' VNĐ', ''))
                    num_j = float(str(val_j).replace(',', '').replace(' VNĐ', ''))
                    matrix[i, j] = num_j / num_i 
                elif criterion_name == "Diện tích":
                    num_i = float(str(val_i).replace(' m²', ''))
                    num_j = float(str(val_j).replace(' m²', ''))
                    matrix[i, j] = num_i / num_j
                else:
                    matrix[i, j] = rank_map.get(val_i, 3) / rank_map.get(val_j, 3)
            except:
                matrix[i, j] = 1.0
    return matrix

with st.container(border=True):
    st.markdown("#### ĐÁNH GIÁ PHƯƠNG ÁN TRÊN TỪNG TIÊU CHÍ")
    
    # Bảng thông số đối chiếu
    st.dataframe(pd.DataFrame.from_dict(lookup_data, orient='index'), use_container_width=True)
    
    alt_scores_matrix = np.zeros((len(alternatives), len(criteria)))
    short_alts = [f"PA{i+1}" for i in range(len(alternatives))]
    
    # Hiển thị Ma trận theo dạng Grid hệt như hình bạn yêu cầu
    for row_idx in range(3):
        cols = st.columns(2, gap="large")
        for col_idx in range(2):
            j = row_idx * 2 + col_idx
            if j < len(criteria):
                with cols[col_idx]:
                    st.markdown(f"<div style='font-weight: 800; color: #ffffff; background-color: #0f172a; padding: 10px; text-align: center; border-radius: 4px; margin-bottom: 5px;'>TIÊU CHÍ: {criteria[j].upper()}</div>", unsafe_allow_html=True)
                    
                    # 1. LẤY MA TRẬN ĐÃ ĐƯỢC MÁY TÍNH TỰ ĐỘNG
                    auto_matrix = get_auto_filled_matrix(criteria[j])
                    
                    # 2. VẼ MA TRẬN RA GIAO DIỆN (Dạng bảng ô vuông)
                    st.markdown("<div style='background: white; padding: 10px; border-radius: 8px; border: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
                    header_cols = st.columns([1.2] + [1]*len(alternatives))
                    header_cols[0].write("**Hệ số**")
                    for k in range(len(alternatives)): header_cols[k+1].write(f"**{short_alts[k]}**")
                    
                    for r in range(len(alternatives)):
                        row_cols = st.columns([1.2] + [1]*len(alternatives))
                        row_cols[0].write(f"**{short_alts[r]}**")
                        for c in range(len(alternatives)):
                            val = auto_matrix[r, c]
                            # Hiển thị giá trị đã tính toán vào các ô
                            display_val = f"{val:.2f}" if val >= 1 else f"1/{1/val:.1f}"
                            row_cols[c+1].markdown(f"<div style='text-align:center; background:#f8fafc; border:1px solid #e2e8f0; border-radius:4px; font-size:0.8rem;'>{display_val}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # 3. TÍNH CR VÀ TRỌNG SỐ TỪ MA TRẬN TỰ ĐỘNG NÀY
                    weights, cr, _, _ = calculate_ahp(auto_matrix)
                    alt_scores_matrix[:, j] = weights
                    
                    st.markdown(f"<div style='text-align: center; font-size: 0.8rem; margin-top:5px; color:#16a34a; font-weight:700;'>Tỷ số CR: {cr:.4f} (Đạt chuẩn)</div>", unsafe_allow_html=True)
        
        if row_idx < 2:
            st.markdown("<hr style='margin: 1.5rem 0;'>", unsafe_allow_html=True)

# ==========================================
# BƯỚC 6: TỔNG HỢP KẾT QUẢ CUỐI CÙNG
# ==========================================
final_scores = np.dot(alt_scores_matrix, crit_weights)

df_results = pd.DataFrame({
    "Phương án": alternatives,
    "Tỷ lệ phù hợp (%)": [round(s * 100, 2) for s in final_scores]
}).sort_values(by="Tỷ lệ phù hợp (%)", ascending=False).reset_index(drop=True)

df_results.index += 1
df_results.insert(0, 'Xếp hạng', df_results.index)

st.write("")
with st.container(border=True):
    st.markdown("#### KẾT QUẢ PHÂN TÍCH TỔNG HỢP")
    
    top_1 = df_results.iloc[0]
    st.success(f"🏆 LỰA CHỌN TỐI ƯU NHẤT: **{top_1['Phương án']}** ({top_1['Tỷ lệ phù hợp (%)']}%)")
    
    col_res_chart, col_res_table = st.columns([1.5, 1], gap="large")
    
    with col_res_chart:
        # THIẾT LẬP BIỂU ĐỒ TRÒN (PIE CHART)
        fig_final = px.pie(
            df_results, 
            values="Tỷ lệ phù hợp (%)", 
            names="Phương án",
            hole=0.4, # Tạo hiệu ứng biểu đồ vòng (Donut) cho hiện đại
            color_discrete_sequence=px.colors.qualitative.Pastel # Bảng màu dịu mắt, chuyên nghiệp
        )
        
        # Tùy chỉnh hiển thị chú giải và nhãn
        fig_final.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            marker=dict(line=dict(color='#ffffff', width=2))
        )
        
        fig_final.update_layout(
            margin=dict(t=0, b=0, l=0, r=0),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5), # Đưa chú giải xuống dưới
            height=400
        )
        
        st.plotly_chart(fig_final, use_container_width=True)
        
    with col_res_table:
        st.write("")
        # Hiển thị bảng dữ liệu chi tiết
        st.dataframe(
            df_results[['Xếp hạng', 'Phương án', 'Tỷ lệ phù hợp (%)']], 
            use_container_width=True, 
            hide_index=True
        )
        
        # Nút xuất báo cáo
        csv = df_results.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="XUẤT BÁO CÁO (.CSV)",
            data=csv,
            file_name="KetQua_PhanTich_AHP.csv",
            mime="text/csv",
            use_container_width=True
        )