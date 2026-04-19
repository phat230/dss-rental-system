import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Import thư viện bản đồ Folium
try:
    import folium
    from streamlit_folium import st_folium
except ImportError:
    st.error("Hệ thống yêu cầu thư viện bản đồ. Vui lòng mở Terminal và chạy lệnh: pip install folium streamlit-folium")
    st.stop()

# Import thư viện AI Gemini
try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

# --- 1. CẤU HÌNH HỆ THỐNG ---
st.set_page_config(
    page_title="DSS - Báo Cáo Chi Tiết", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. CSS CHUẨN TẮC KÈ HOA & ĐỘ LẠI BẢNG XẾP HẠNG ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 3.5rem !important; }
    
    .card-rank-1 { background: linear-gradient(135deg, #1E3A8A, #3B82F6); color: #FFFFFF; }
    .card-rank-2 { background: linear-gradient(135deg, #065F46, #10B981); color: #FFFFFF; }
    .card-rank-3 { background: linear-gradient(135deg, #7E22CE, #A855F7); color: #FFFFFF; }
    
    .color-card {
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .card-title { font-size: 20px; font-weight: 800; margin-bottom: 5px; color: #FFFFFF; text-shadow: 1px 1px 2px rgba(0,0,0,0.2); }
    .card-price { font-size: 24px; font-weight: 800; color: #FDE047; margin-bottom: 15px; text-shadow: 1px 1px 2px rgba(0,0,0,0.3); } 
    .card-detail { font-size: 14px; margin-bottom: 8px; border-bottom: 1px dashed rgba(255, 255, 255, 0.3); padding-bottom: 8px; color: #F8FAFC; }
    .card-score { font-size: 16px; font-weight: 800; color: #FFFFFF; margin-top: 15px; text-align: center; background: rgba(0,0,0,0.25); padding: 10px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); }
    
    .badge { position: absolute; top: 0; right: 0; background: #EF4444; color: white; padding: 6px 16px; font-weight: 800; border-bottom-left-radius: 16px; box-shadow: -2px 2px 5px rgba(0,0,0,0.2); }

    /* ======================================================== */
    /* HACK CSS: NÂNG CẤP BẢNG XẾP HẠNG THÀNH MENU HIỆN ĐẠI     */
    /* ======================================================== */
    div[role="radiogroup"] > label {
        background-color: rgba(128, 128, 128, 0.03);
        border: 1px solid rgba(128, 128, 128, 0.15);
        border-radius: 10px;
        padding: 14px 16px !important;
        margin-bottom: 10px !important;
        transition: all 0.2s ease-in-out;
        cursor: pointer;
    }
    div[role="radiogroup"] > label:hover {
        background-color: rgba(59, 130, 246, 0.05);
        border-color: #3B82F6;
        transform: translateX(6px); 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    div[role="radiogroup"] > label div {
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    div[data-baseweb="radio"] > div {
        background-color: #3B82F6 !important;
    }
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
with nav_3: st.page_link("pages/4_Search_Rentals.py", label="Tìm kiếm")
with nav_4: st.page_link("pages/5_Results.py", label="Báo cáo")

if not st.session_state.get("token"):
    with nav_auth:
        if st.button("Đăng nhập", use_container_width=True, key="top_login"):
            st.switch_page("pages/1_Login.py")
else:
    with nav_space:
        name = st.session_state.get('name', 'Khách hàng')
        st.markdown(f"<div style='margin-top: 8px; font-weight: 600; text-align: right; color: var(--text-color); opacity: 0.7;'>Chào, {name}</div>", unsafe_allow_html=True)
    with nav_auth:
        if st.button("Thoát", use_container_width=True, key="top_logout"):
            st.session_state.clear()
            st.rerun()

st.markdown("<hr style='margin-top: 5px; margin-bottom: 30px; border-color: rgba(128,128,128,0.2);'>", unsafe_allow_html=True)

# =========================================================================
# 5. HÀM NỘI SUY AN TOÀN
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
# 6. KIỂM TRA AHP & TẢI DỮ LIỆU
# =========================================================================
st.markdown("<h2 style='font-weight: 800; margin-bottom: 5px;'>Báo Cáo Phân Tích Phương Án</h2>", unsafe_allow_html=True)
st.markdown("<p style='margin-bottom: 30px; opacity: 0.7;'>Đánh giá và so sánh chuyên sâu các căn hộ tốt nhất dựa trên cấu trúc trọng số của bạn.</p>", unsafe_allow_html=True)

if "ahp_weights" not in st.session_state or "ahp_criteria" not in st.session_state:
    st.warning("Hệ thống chưa nhận được cấu hình AHP. Vui lòng quay lại bước 'Thuật toán'.")
    st.stop()

try:
    df = pd.read_excel("AHP11.xlsx", sheet_name="DuLieu_ThucTe_TPHCM")
except Exception as e:
    st.error(f"Lỗi tải dữ liệu: Không tìm thấy file AHP11.xlsx ({e})")
    st.stop()

# =========================================================================
# 7. TÍNH TOÁN DSS
# =========================================================================
w = st.session_state["ahp_weights"]
cri = st.session_state["ahp_criteria"]
weight_dict = dict(zip(cri, w))

df = df.copy()
df['Score'] = 0.0

for col in ['Giá', 'Khoảng cách', 'Chất lượng', 'An ninh', 'Diện tích']:
    if col in df.columns and col in weight_dict:
        c_min, c_max = df[col].min(), df[col].max()
        if c_max == c_min: c_max += 0.001 
        if col in ['Giá', 'Khoảng cách']: n_val = (c_max - df[col]) / (c_max - c_min)
        else: n_val = (df[col] - c_min) / (c_max - c_min)
        df['Score'] += n_val * weight_dict[col]

df_sorted = df.sort_values('Score', ascending=False).reset_index(drop=True)
top_3 = df_sorted.head(3)
top_10 = df_sorted.head(10).copy()

if 'Tên nhà' not in top_10.columns: top_10['Tên nhà'] = [f"Nhà {i+1}" for i in range(len(top_10))]
top_10['Tên nhà an toàn'] = top_10['Tên nhà'].astype(str)

# =========================================================================
# 8. HIỂN THỊ THẺ TOP 3 ĐA SẮC
# =========================================================================
st.markdown("#### Top 3 Căn Hộ Tối Ưu Nhất")
cols = st.columns(3, gap="large")

card_classes = ["card-rank-1", "card-rank-2", "card-rank-3"]
badge_texts = ["LỰA CHỌN SỐ 1", "HẠNG 2", "HẠNG 3"]

for i in range(3):
    if i >= len(top_3): break
    row = top_3.iloc[i]
    
    with cols[i]:
        st.markdown(f"""
        <div class="color-card {card_classes[i]}">
            <div class="badge">{badge_texts[i]}</div>
            <div class="card-title">{row.get('Tên nhà', f'Nhà {i+1}')}</div>
            <div style="font-size: 13px; margin-bottom: 10px; min-height: 40px; color: #E2E8F0;">{row.get('Địa chỉ', 'Đang cập nhật')}</div>
            <div class="card-price">{get_price_desc(row.get('Giá', 1))} / Tháng</div>
            <div class="card-detail"><b>Diện tích:</b> {get_area_desc(row.get('Diện tích', 15))}</div>
            <div class="card-detail" style="border-bottom: none;"><b>An ninh:</b> {get_security_detail(row.get('An ninh', 1))}</div>
            <div class="card-score">ĐIỂM ĐÁNH GIÁ: {row.get('Score', 0) * 100:.1f} / 100</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br><hr style='border-color: rgba(128,128,128,0.2);'><br>", unsafe_allow_html=True)

# =========================================================================
# 9. TRỢ LÝ AI CHATBOT (HYBRID ENGINE - KHÔNG CẦN API KEY)
# =========================================================================
st.markdown("#### 🤖 Cố Vấn AI Thông Minh (DSS Copilot)")
st.markdown("<p style='color: var(--text-color); opacity: 0.7; margin-bottom: 15px; font-size: 14px;'>Trợ lý ảo tích hợp công nghệ phân tích dữ liệu tự nhiên. Bạn có thể chọn câu hỏi gợi ý bên dưới.</p>", unsafe_allow_html=True)

# BIẾN NÀY KỆ NÓ, KHÔNG CẦN CHẠM VÀO NẾU DÙNG OFFLINE
api_key = "DÁN_API_KEY_CỦA_ÔNG_VÀO_ĐÂY"

n1_name = top_3.iloc[0].get('Tên nhà', 'Hạng 1') if len(top_3) > 0 else 'Hạng 1'

if "ai_chat_msgs" not in st.session_state:
    st.session_state.ai_chat_msgs = [
        {"role": "assistant", "avatar": "🤖", "content": f"Chào bạn! Tôi là **DSS Copilot**. Dựa trên phân tích thuật toán, căn **{n1_name}** đang là chân ái của bạn. Bạn muốn tôi so sánh chi tiết, tìm nhà rẻ nhất, hay phân tích an ninh không?"}
    ]

chat_container = st.container(height=380)
with chat_container:
    for msg in st.session_state.ai_chat_msgs:
        with st.chat_message(msg["role"], avatar=msg.get("avatar", "🧑‍💻")):
            st.markdown(msg["content"])

st.markdown("<div style='margin-top: 10px; margin-bottom: 5px; font-size: 13px; color: #3B82F6; font-weight: 800;'>💡 HỎI NHANH AI:</div>", unsafe_allow_html=True)

q_cols = st.columns(3)
quick_prompts = [
    "⚖️ So sánh chi tiết Hạng 1 và Hạng 2",
    "💰 Căn nào có giá thuê cực rẻ trong Top 10?",
    "🛡️ Phân tích an ninh của căn Hạng 1"
]

chosen_quick_prompt = None
for i, q in enumerate(quick_prompts):
    if q_cols[i].button(q, use_container_width=True):
        chosen_quick_prompt = q.replace("⚖️ ", "").replace("💰 ", "").replace("🛡️ ", "")

prompt = st.chat_input("Hỏi DSS Copilot (VD: Xung quanh căn hạng 1 có tiện ích gì không?)...")
final_prompt = chosen_quick_prompt or prompt

# --- BỘ NÃO OFFLINE THÔNG MINH ---
def get_offline_brain_response(p, df_10):
    p = str(p).lower()
    h1 = df_10.iloc[0] if len(df_10) > 0 else None
    h2 = df_10.iloc[1] if len(df_10) > 1 else None
    
    if "so sánh" in p:
        if h1 is not None and h2 is not None:
            return f"**⚖️ BÁO CÁO SO SÁNH:**\n\n* **🥇 {h1.get('Tên nhà', 'Hạng 1')} (Độ phù hợp: {(h1.get('Score', 0)*100):.1f}%):** Mức giá {get_price_desc(h1.get('Giá', 1))}, Diện tích {get_area_desc(h1.get('Diện tích', 15))}. Ưu điểm: Điểm số AHP cao nhất, tối ưu toàn diện các tiêu chí của bạn.\n* **🥈 {h2.get('Tên nhà', 'Hạng 2')} (Độ phù hợp: {(h2.get('Score', 0)*100):.1f}%):** Mức giá {get_price_desc(h2.get('Giá', 1))}, Diện tích {get_area_desc(h2.get('Diện tích', 15))}. Ưu điểm: Là phương án dự phòng xuất sắc nếu căn Hạng 1 đã có người thuê.\n\n👉 **Lời khuyên:** Vẫn ưu tiên chốt căn Hạng 1 vì nó sát với nhu cầu toán học của bạn nhất."
        return "Xin lỗi, không đủ dữ liệu để so sánh."
        
    elif "rẻ" in p or "giá" in p:
        if 'Giá' in df_10.columns:
            best_idx = df_10['Giá'].idxmin()
            best_h = df_10.iloc[best_idx]
            return f"💰 **PHÂN TÍCH TÀI CHÍNH:**\n\nCăn có giá thuê tốt nhất trong danh sách Top 10 là **{best_h.get('Tên nhà', 'N/A')}** (Đang xếp Hạng {best_idx+1}).\n\n💵 Mức giá cực kỳ sinh viên: chỉ **{get_price_desc(best_h.get('Giá', 1))} / Tháng**. Nếu bạn đặt nặng vấn đề tiết kiệm ngân sách, hãy cân nhắc đi xem căn này ngay!"
        return "Xin lỗi, hệ thống chưa có đủ dữ liệu về giá."
        
    elif "an ninh" in p:
        if h1 is not None:
            return f"🛡️ **ĐÁNH GIÁ AN NINH (HẠNG 1):**\n\nTheo hồ sơ, căn **{h1.get('Tên nhà', 'N/A')}** sở hữu hệ thống: **{get_security_detail(h1.get('An ninh', 1))}**. Với trang bị bảo vệ mức độ này, bạn hoàn toàn có thể yên tâm sinh sống lâu dài."
        return "Không có dữ liệu an ninh."
        
    else:
        if h1 is not None:
            return f"🤖 **DSS Copilot:** Câu hỏi rất tinh tế! Dựa trên tổng hợp mô hình AHP, tôi vẫn khuyến nghị mạnh mẽ căn **{h1.get('Tên nhà', '')}**. Nó đạt mức độ lý tưởng {(h1.get('Score', 0)*100):.1f}%. Bạn có muốn tôi phân tích sâu hơn về tài chính hay an ninh của nó không?"
        return "Hệ thống đang thu thập thêm dữ liệu."

if final_prompt:
    st.session_state.ai_chat_msgs.append({"role": "user", "avatar": "🧑‍💻", "content": final_prompt})
    
    with chat_container:
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(final_prompt)
            
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Đang phân tích dữ liệu đa chiều..."):
                if api_key == "DÁN_API_KEY_CỦA_ÔNG_VÀO_ĐÂY" or not api_key or not HAS_GENAI:
                    ans = get_offline_brain_response(final_prompt, top_10)
                    st.markdown(ans)
                    st.session_state.ai_chat_msgs.append({"role": "assistant", "avatar": "🤖", "content": ans})
                else:
                    try:
                        context_data = "Thông tin 10 căn nhà tốt nhất:\n"
                        for idx, row in top_10.iterrows():
                            context_data += f"- Hạng {idx+1}: {row.get('Tên nhà', '')}, Giá: {get_price_desc(row.get('Giá', 1))}, Diện tích: {get_area_desc(row.get('Diện tích', 15))}, An ninh: {get_security_detail(row.get('An ninh', 1))}, Điểm: {(row.get('Score', 0)*100):.1f}/100.\n"
                        
                        system_prompt = f"{context_data}\nKhách hỏi: \"{final_prompt}\"\nBạn là chuyên gia BĐS, hãy tư vấn ngắn gọn, chuyên nghiệp."
                        
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        response = model.generate_content(system_prompt)
                        ans = response.text
                        st.markdown(ans)
                        st.session_state.ai_chat_msgs.append({"role": "assistant", "avatar": "🤖", "content": ans})
                    except Exception:
                        ans = get_offline_brain_response(final_prompt, top_10)
                        st.markdown(ans)
                        st.session_state.ai_chat_msgs.append({"role": "assistant", "avatar": "🤖", "content": ans})
    st.rerun()

# =========================================================================
# 10. BIỂU ĐỒ PHÂN TÍCH CHUYÊN SÂU
# =========================================================================
st.markdown("<hr style='border-color: rgba(128,128,128,0.2); margin-top: 30px; margin-bottom: 30px;'>", unsafe_allow_html=True)
chart_col1, chart_col2 = st.columns([1.5, 1], gap="large")

with chart_col1:
    st.markdown("#### Tương quan Điểm số Top 10")
    bar_names = [row.get('Tên nhà', f'Nhà {i+1}') for i, row in top_10.iterrows()]
    bar_df = pd.DataFrame({'Tên nhà': bar_names, 'Score': (top_10['Score'] * 100).round(1)}).sort_values('Score', ascending=True)
    fig_bar = px.bar(bar_df, x='Score', y='Tên nhà', orientation='h', text='Score')
    fig_bar.update_traces(marker_color='#3B82F6', textposition='outside')
    fig_bar.update_layout(xaxis_title="Điểm Phù Hợp (%)", yaxis_title="", margin=dict(l=0, r=20, t=20, b=0), xaxis=dict(range=[0, 110]), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_bar, use_container_width=True)

with chart_col2:
    st.markdown("#### Sơ đồ Cấu trúc Trọng số")
    pie_data = pd.DataFrame({"Tiêu chí": cri, "Trọng số": w})
    fig_pie = px.pie(pie_data, values='Trọng số', names='Tiêu chí', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_pie.update_traces(textinfo='percent', textposition='inside')
    fig_pie.update_layout(showlegend=True, legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5), margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("<br><hr style='border-color: rgba(128,128,128,0.2);'><br>", unsafe_allow_html=True)

# =========================================================================
# 11. BẢN ĐỒ INTERACTIVE & THẺ CHI TIẾT (FIXED FULL QUẬN SÀI GÒN)
# =========================================================================
st.markdown("#### Khảo sát Vị trí Địa lý & Hồ sơ Phương án")
st.markdown("<p class='sub-text' style='margin-bottom: 25px;'>Nhấn vào danh sách hoặc các mốc trên bản đồ để xem hồ sơ năng lực chi tiết của từng căn.</p>", unsafe_allow_html=True)

np.random.seed(42)

# --- BẢN VÁ LỖI: FULL TỌA ĐỘ 22 QUẬN HUYỆN TPHCM ---
def get_lat_lon(district):
    coords = {
        'quận 1': (10.7756, 106.7019), 'quận 2': (10.7872, 106.7495),
        'quận 3': (10.7843, 106.6817), 'quận 4': (10.7580, 106.7061),
        'quận 5': (10.7540, 106.6633), 'quận 6': (10.7480, 106.6343),
        'quận 7': (10.7339, 106.7161), 'quận 8': (10.7241, 106.6286),
        'quận 9': (10.8428, 106.8286), 'quận 10': (10.7743, 106.6669),
        'quận 11': (10.7628, 106.6433), 'quận 12': (10.8671, 106.6413),
        'phú nhuận': (10.7998, 106.6803), 'bình thạnh': (10.8105, 106.7091),
        'tân bình': (10.8015, 106.6526), 'tân phú': (10.7901, 106.6262),
        'gò vấp': (10.8386, 106.6659), 'thủ đức': (10.8494, 106.7537),
        'bình tân': (10.7653, 106.6038), 'nhà bè': (10.6953, 106.7265),
        'hóc môn': (10.8837, 106.5945), 'bình chánh': (10.6874, 106.5940)
    }
    
    # Tìm kiếm theo chuỗi mờ (Tránh lỗi do nhập liệu excel sai)
    dist_str = str(district).lower()
    base_lat, base_lon = 10.7769, 106.7009 # Mặc định
    
    for k, v in coords.items():
        if k in dist_str:
            base_lat, base_lon = v
            break
            
    # Thêm nhiễu ngẫu nhiên để các chấm không đè lên nhau hoàn toàn
    return base_lat + np.random.uniform(-0.015, 0.015), base_lon + np.random.uniform(-0.015, 0.015)
# ----------------------------------------------------

lats, lons = [], []
for d in top_10.get('Quận/Khu vực', pd.Series([''] * len(top_10))):
    lt, ln = get_lat_lon(d)
    lats.append(lt)
    lons.append(ln)
top_10['lat'] = lats
top_10['lon'] = lons

radio_options = [f"Hạng {i+1}: {row.get('Tên nhà', f'Nhà {i+1}')}" for i, row in top_10.iterrows()]
if "map_selected_option" not in st.session_state or st.session_state["map_selected_option"] not in radio_options:
    st.session_state["map_selected_option"] = radio_options[0] if radio_options else ""

map_col1, map_col2, map_col3 = st.columns([1.2, 2.6, 1.2], gap="medium")

with map_col1:
    st.markdown("<div style='font-weight:900; font-size:18px; margin-bottom:15px; color: var(--text-color);'>🏆 Bảng Xếp Hạng</div>", unsafe_allow_html=True)
    list_container = st.container(height=405)
    with list_container:
        if radio_options:
            selected_option = st.radio("Chọn nhà:", radio_options, key="map_selected_option", label_visibility="collapsed")
            selected_rank = int(selected_option.split(":")[0].replace("Hạng ", ""))
            selected_idx = selected_rank - 1
            selected_row = top_10.iloc[selected_idx]
        else:
            st.error("Không có dữ liệu")
            st.stop()

with map_col2:
    m = folium.Map(location=[10.7769, 106.7009], zoom_start=12, tiles="CartoDB positron")
    for idx, row in top_10.iterrows():
        rank = idx + 1
        bg_color = "#EF4444" if rank == selected_rank else "#3B82F6" 
        icon_html = f'''<div style="font-size: 13px; font-weight: 800; background-color: {bg_color}; color: white; border-radius: 50%; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);">{rank}</div>'''
        
        safe_name = row.get('Tên nhà', f'Nhà {rank}')
        folium.Marker(location=[row['lat'], row['lon']], tooltip=f"Hạng {rank}: {safe_name}", icon=folium.DivIcon(html=icon_html, icon_size=(28,28), icon_anchor=(14,14))).add_to(m)

    map_data = st_folium(m, use_container_width=True, height=440, returned_objects=["last_object_clicked_tooltip"])
    if map_data and map_data.get("last_object_clicked_tooltip"):
        clicked_tooltip = map_data["last_object_clicked_tooltip"]
        if clicked_tooltip != st.session_state["map_selected_option"]:
            st.session_state["map_selected_option"] = clicked_tooltip
            st.rerun()

with map_col3:
    st.markdown("<div style='font-weight:900; font-size:18px; margin-bottom:15px; color: var(--text-color);'>📑 Hồ sơ Năng lực</div>", unsafe_allow_html=True)
    
    score_val = selected_row.get('Score', 0) * 100
    
    dia_chi_goc = str(selected_row.get('Địa chỉ', ''))
    khu_vuc_chuan = str(selected_row.get('Quận/Khu vực', 'N/A'))
    danh_sach_quan_huyen = ['Quận 1', 'Quận 2', 'Quận 3', 'Quận 4', 'Quận 5', 'Quận 6', 'Quận 7', 'Quận 8', 'Quận 9', 'Quận 10', 'Quận 11', 'Quận 12', 'Phú Nhuận', 'Bình Thạnh', 'Tân Bình', 'Tân Phú', 'Gò Vấp', 'Thủ Đức', 'Bình Tân', 'Nhà Bè', 'Hóc Môn', 'Bình Chánh']
    
    for q in danh_sach_quan_huyen:
        if q.lower() in dia_chi_goc.lower():
            khu_vuc_chuan = q
            break
            
    raw_html = f"""
    <div style="background-color: var(--secondary-background-color); border: 1px solid rgba(128,128,128,0.2); border-radius: 16px; padding: 20px; box-shadow: 0 8px 16px rgba(0,0,0,0.05); height: 440px; position: relative;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <span style="background: linear-gradient(135deg, #EF4444, #F59E0B); color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 800; box-shadow: 0 2px 4px rgba(239, 68, 68, 0.3);">HẠNG {selected_rank}</span>
            <span style="font-size: 18px; font-weight: 900; color: var(--primary-color);">{score_val:.1f} ĐIỂM</span>
        </div>
        <div style="font-weight: 800; font-size: 18px; margin-bottom: 5px; line-height: 1.3; color: var(--text-color);">{selected_row.get('Tên nhà', f'Nhà {selected_rank}')}</div>
        <div style="font-size: 13px; color: var(--text-color); opacity: 0.6; margin-bottom: 20px;">📍 {dia_chi_goc}</div>
        <div style="background: rgba(128,128,128,0.05); padding: 15px; border-radius: 12px; border: 1px solid rgba(128,128,128,0.1); margin-bottom: 15px;">
            <div style="font-size: 22px; font-weight: 900; color: #10B981; margin-bottom: 5px;">{get_price_desc(selected_row.get('Giá', 1))} <span style="font-size: 12px; color: var(--text-color); opacity: 0.5; font-weight: normal;">/ Tháng</span></div>
            <div style="display: flex; justify-content: space-between; font-size: 13px; padding-top: 10px; border-top: 1px dashed rgba(128,128,128,0.2); color: var(--text-color); opacity: 0.8;">
                <span>📐 Diện tích: <b>{get_area_desc(selected_row.get('Diện tích', 15))}</b></span>
                <span>Khu vực: <b>{khu_vuc_chuan}</b></span>
            </div>
        </div>
        <div style="font-size: 13px; font-weight: 600; margin-bottom: 5px; color: var(--text-color);">🛡️ Hệ thống An ninh:</div>
        <div style="font-size: 13px; margin-bottom: 25px; opacity: 0.8; color: var(--text-color);">{get_security_detail(selected_row.get('An ninh', 1))}</div>
        <div style="position: absolute; bottom: 25px; left: 20px; right: 20px;">
            <div style="display: flex; justify-content: space-between; font-size: 12px; font-weight: 700; margin-bottom: 6px; color: var(--text-color); opacity: 0.8;">
                <span>ĐỘ PHÙ HỢP DSS:</span>
                <span style="color: var(--primary-color);">{score_val:.1f}%</span>
            </div>
            <div style="background: rgba(128,128,128,0.2); border-radius: 6px; width: 100%; height: 8px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #3B82F6, #1D4ED8); width: {score_val}%; height: 100%; border-radius: 6px; transition: width 0.5s ease-in-out;"></div>
            </div>
        </div>
    </div>
    """
    
    clean_html = "".join([line.strip() for line in raw_html.split("\n")])
    st.markdown(clean_html, unsafe_allow_html=True)

st.markdown("<br><hr style='border-color: rgba(128,128,128,0.2);'><br>", unsafe_allow_html=True)

# =========================================================================
# 12. BẢNG DỮ LIỆU TỔNG HỢP & XUẤT FILE
# =========================================================================
st.markdown("#### Bảng Báo Cáo Tổng Hợp Kế Hoạch Đề Xuất", unsafe_allow_html=True)

cols_to_get = ['Mã', 'Tên nhà', 'Địa chỉ', 'Giá', 'Diện tích', 'An ninh', 'Score']
available_cols = [c for c in cols_to_get if c in df_sorted.columns]
report_df = df_sorted[available_cols].copy()

if 'Giá' in report_df.columns: report_df['Giá thuê'] = report_df['Giá'].apply(get_price_desc)
if 'Diện tích' in report_df.columns: report_df['Diện tích thực'] = report_df['Diện tích'].apply(get_area_desc)
if 'An ninh' in report_df.columns: report_df['Hệ thống an ninh'] = report_df['An ninh'].apply(get_security_detail)
if 'Score' in report_df.columns: report_df['Điểm số (%)'] = (report_df['Score'] * 100).round(2)

display_cols = [c for c in ['Mã', 'Tên nhà', 'Địa chỉ', 'Giá thuê', 'Diện tích thực', 'Hệ thống an ninh', 'Điểm số (%)'] if c in report_df.columns]
display_report = report_df[display_cols]

st.dataframe(display_report, use_container_width=True, hide_index=True)

csv = display_report.to_csv(index=False).encode('utf-8-sig')
st.markdown("<br>", unsafe_allow_html=True)
st.download_button(label="TẢI XUỐNG BÁO CÁO (CSV)", data=csv, file_name='Bao_Cao_Nha_Tro_TPHCM.csv', mime='text/csv', type="primary")