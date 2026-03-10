import streamlit as st
import time

# ==========================================
# 1. CHỐT CHẶN BẢO MẬT (GATEKEEPER)
# ==========================================


# --- 2. THIẾT LẬP CẤU HÌNH TRANG ---
st.set_page_config(page_title="Truy Xuất Bất Động Sản", layout="wide", initial_sidebar_state="expanded")

# --- KHỞI TẠO GIỎ HÀNG AHP (LƯU FULL DỮ LIỆU) ---
if "selected_houses_data" not in st.session_state:
    st.session_state["selected_houses_data"] = []

# --- 3. CSS TÙY CHỈNH ---
st.markdown("""
    <style>
    .main { background-color: #f8fafc; font-family: 'Inter', sans-serif; }
    h1 { color: #0f172a !important; font-weight: 800 !important; margin-bottom: 2rem; }
    
    .block-container { max-width: 1300px; padding-top: 2rem !important; padding-bottom: 4rem !important; }
    
    [data-testid="stForm"] {
        background-color: #ffffff; padding: 2.5rem; border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); border: 1px solid #e2e8f0;
        border-top: 4px solid #3b82f6; margin-bottom: 2rem;
    }

    .property-card {
        background-color: #ffffff; border-radius: 12px; overflow: hidden;
        border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        transition: transform 0.3s ease; height: 100%;
        display: flex; flex-direction: column; margin-bottom: 1rem;
    }
    .property-card:hover { transform: translateY(-5px); box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); }
    .prop-img { width: 100%; height: 200px; object-fit: cover; }
    .prop-content { padding: 1.5rem; flex-grow: 1; display: flex; flex-direction: column;}
    .prop-price { color: #3b82f6; font-size: 1.3rem; font-weight: 800; margin-bottom: 0.2rem; }
    .prop-title { color: #0f172a; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.8rem; height: 3rem; overflow: hidden;}
    .prop-specs { font-size: 0.85rem; color: #64748b; margin-bottom: 1rem; border-bottom: 1px dashed #e2e8f0; padding-bottom: 0.8rem;}
    
    div.stButton > button {
        width: 100%; background-color: #f1f5f9; color: #0f172a; border: 1px solid #cbd5e1; font-weight: 700; border-radius: 6px;
    }
    div.stButton > button:hover {
        background-color: #0f172a !important; color: white !important; border-color: #0f172a !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. DỮ LIỆU CƠ SỞ (22 BẤT ĐỘNG SẢN) ---
mock_database = [
    {"id": 1, "title": "Studio Cửa Sổ Lớn", "price": 3500000, "area": 25, "address": "Quận 10", "specs": "Gần ĐH Bách Khoa", "security": "Khá", "utility": "Cơ bản", "freedom": "Chung chủ", "img": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=600"},
    {"id": 2, "title": "Căn Hộ Mini Ban Công", "price": 4200000, "area": 30, "address": "Quận Tân Bình", "specs": "Full Nội Thất", "security": "Tốt", "utility": "Đầy đủ", "freedom": "Tự do", "img": "https://images.unsplash.com/photo-1502672260266-1c1c2f50ce3e?w=600"},
    {"id": 3, "title": "Phòng Trọ Gác Xép", "price": 2800000, "area": 20, "address": "Quận 11", "specs": "Tự do giờ giấc", "security": "Trung bình", "utility": "Ít", "freedom": "Tự do", "img": "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=600"},
    {"id": 4, "title": "Chung Cư Mini Hiện Đại", "price": 5500000, "area": 40, "address": "Quận 7", "specs": "Camera an ninh", "security": "Rất tốt", "utility": "Hiện đại", "freedom": "Tự do", "img": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=600"},
    {"id": 5, "title": "Ký Túc Xá Sleepbox", "price": 1500000, "area": 15, "address": "Quận 10", "specs": "Bao điện nước", "security": "Tốt", "utility": "Nhiều", "freedom": "Thấp", "img": "https://images.unsplash.com/photo-1536376072261-38c75010e6c9?w=600"},
    {"id": 6, "title": "Căn Hộ Dịch Vụ Cao Cấp", "price": 8500000, "area": 45, "address": "Quận 1", "specs": "Full dịch vụ", "security": "Tuyệt đối", "utility": "Full nội thất", "freedom": "Cao", "img": "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=600"},
    {"id": 7, "title": "Phòng Trọ Hàng Xanh", "price": 3200000, "area": 22, "address": "Bình Thạnh", "specs": "Không chung chủ", "security": "Khá", "utility": "Cơ bản", "freedom": "Tự do", "img": "https://images.unsplash.com/photo-1499916078039-922301b0eb9b?w=600"},
    {"id": 8, "title": "Studio Vinhome Central Park", "price": 12000000, "area": 38, "address": "Bình Thạnh", "specs": "Đẳng cấp 5 sao", "security": "Rất cao", "utility": "Sang trọng", "freedom": "Tự do", "img": "https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?w=600"},
    {"id": 9, "title": "Nhà Nguyên Căn Hẻm Nhỏ", "price": 7500000, "area": 55, "address": "Phú Nhuận", "specs": "1 trệt 1 lầu", "security": "Trung bình", "utility": "Không nội thất", "freedom": "Tuyệt đối", "img": "https://images.unsplash.com/photo-1513584684374-8bab748fbf90?w=600"},
    {"id": 10, "title": "Phòng Trọ Sinh Viên Giá Rẻ", "price": 2000000, "area": 18, "address": "Quận 9", "specs": "Gần khu công nghệ cao", "security": "Thấp", "utility": "Tối giản", "freedom": "23h đóng cửa", "img": "https://images.unsplash.com/photo-1554995207-c18c203602cb?w=600"},
    {"id": 11, "title": "Căn Hộ Duplex Trần Não", "price": 9500000, "area": 50, "address": "Quận 2", "specs": "Có gác rộng thoáng", "security": "Tốt", "utility": "Hiện đại", "freedom": "Tự do", "img": "https://images.unsplash.com/photo-1505691938895-1758d7feb511?w=600"},
    {"id": 12, "title": "Studio Minimalist Đa Kao", "price": 6800000, "area": 28, "address": "Quận 1", "specs": "Phong cách tối giản", "security": "Khá", "utility": "Đầy đủ", "freedom": "Tự do", "img": "https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?w=600"},
    {"id": 13, "title": "Căn Hộ Panorama View Sông", "price": 14000000, "area": 75, "address": "Quận 7", "specs": "View sông cực chill", "security": "Tuyệt đối", "utility": "Cao cấp", "freedom": "Tự do", "img": "https://images.unsplash.com/photo-1493209638045-3414a83937b1?w=600"},
    {"id": 14, "title": "Phòng Trọ Mới Xây Q.8", "price": 3000000, "area": 24, "address": "Quận 8", "specs": "Sạch sẽ thoáng mát", "security": "Khá", "utility": "Cơ bản", "freedom": "Tự do", "img": "https://images.unsplash.com/photo-1524061614234-8449637536ee?w=600"},
    {"id": 15, "title": "Penthouse Mini Sân Thượng", "price": 18000000, "area": 90, "address": "Quận 3", "specs": "Tiệc BBQ ngoài trời", "security": "Rất cao", "utility": "Full option", "freedom": "Tuyệt đối", "img": "https://images.unsplash.com/photo-1502672023488-70e25813eb80?w=600"},
    {"id": 16, "title": "Phòng Trọ Box 2 Người", "price": 2500000, "area": 18, "address": "Quận 5", "specs": "Gần ĐH Y Dược", "security": "Tốt", "utility": "Máy lạnh trung tâm", "freedom": "Trung bình", "img": "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=600"},
    {"id": 17, "title": "Studio Thiết Kế Loft", "price": 7200000, "area": 32, "address": "Quận 4", "specs": "Gần cầu Khánh Hội", "security": "Tốt", "utility": "Đầy đủ", "freedom": "Tự do", "img": "https://images.unsplash.com/photo-1522156373667-4c7234bbd804?w=600"},
    {"id": 18, "title": "Căn Hộ Sân Vườn Thảo Điền", "price": 16000000, "area": 100, "address": "Quận 2", "specs": "Yên tĩnh biệt lập", "security": "Rất cao", "utility": "Hồ bơi riêng", "freedom": "Tuyệt đối", "img": "https://images.unsplash.com/photo-1494438639946-1ebd1d20bf85?w=600"},
    {"id": 19, "title": "Phòng Trọ Gò Vấp Sạch", "price": 2700000, "area": 20, "address": "Gò Vấp", "specs": "Gần công viên", "security": "Khá", "utility": "Tủ lạnh riêng", "freedom": "Tự do", "img": "https://images.unsplash.com/photo-1499955085172-a104c9463ece?w=600"},
    {"id": 20, "title": "Căn Hộ Officetel Sun Avenue", "price": 10500000, "area": 42, "address": "TP. Thủ Đức", "specs": "Vừa ở vừa làm việc", "security": "Rất cao", "utility": "Thông minh", "freedom": "Tự do", "img": "https://images.unsplash.com/photo-1486304873000-2356438275de?w=600"},
    {"id": 21, "title": "Phòng Trọ Kín Q.6", "price": 2300000, "area": 18, "address": "Quận 6", "specs": "Khu dân cư ổn định", "security": "Trung bình", "utility": "Tối giản", "freedom": "Trung bình", "img": "https://images.unsplash.com/photo-1501183638710-841dd1904538?w=600"},
    {"id": 22, "title": "Studio Ánh Sáng Tân Phú", "price": 4800000, "area": 30, "address": "Quận Tân Phú", "specs": "Cửa sổ hướng Đông", "security": "Tốt", "utility": "Đầy đủ", "freedom": "Tự do", "img": "https://images.unsplash.com/photo-1512918583163-0133a656ad7e?w=600"}
]

def format_vnd(price):
    return "{:,.0f} VNĐ".format(price).replace(",", ".")

# --- 5. SIDEBAR: QUẢN LÝ ---
st.sidebar.markdown("### 📋 DANH SÁCH CHỌN (AHP)")
selected_list = st.session_state["selected_houses_data"]

if not selected_list:
    st.sidebar.info("Chưa có căn nào được chọn.")
else:
    for idx, house in enumerate(selected_list):
        st.sidebar.write(f"{idx+1}. {house['Ten']}")
    
    if st.sidebar.button("Làm mới danh sách"):
        st.session_state["selected_houses_data"] = []
        st.rerun()
    
    if len(selected_list) >= 2:
        if st.sidebar.button("TIẾN HÀNH PHÂN TÍCH AHP ➔", type="primary"):
            st.switch_page("pages/3_AHP_Input.py")
    else:
        st.sidebar.warning("Chọn ít nhất 2 căn.")

# --- 6. HEADER ---
st.markdown("<h1>TRUY XUẤT BẤT ĐỘNG SẢN</h1>", unsafe_allow_html=True)

# --- 7. TÌM KIẾM ---
with st.form("search_console"):
    search_query = st.text_input("Tìm kiếm theo khu vực, đặc điểm...", placeholder="VD: Quận 10, Ban công, Studio...")
    col_p, col_a = st.columns(2)
    with col_p: max_price = st.number_input("Ngân sách tối đa (VNĐ)", value=10000000, step=500000)
    with col_a: min_area = st.number_input("Diện tích tối thiểu (m²)", value=15, step=5)
    submitted = st.form_submit_button("TIẾN HÀNH TRUY XUẤT", use_container_width=True)

# --- 8. HIỂN THỊ ---
query = search_query.lower() if search_query else ""
filtered = [i for i in mock_database if i["price"] <= max_price and i["area"] >= min_area and (query in i["title"].lower() or query in i["address"].lower())]

if filtered:
    st.markdown(f"### Tìm thấy {len(filtered)} kết quả phù hợp")
    for i in range(0, len(filtered), 3):
        cols = st.columns(3, gap="large")
        for j in range(3):
            if i + j < len(filtered):
                prop = filtered[i + j]
                with cols[j]:
                    st.markdown(f"""
                        <div class="property-card">
                            <img class="prop-img" src="{prop['img']}">
                            <div class="prop-content">
                                <div class="prop-price">{format_vnd(prop['price'])}</div>
                                <div class="prop-title">{prop['title']}</div>
                                <div class="prop-specs"><b>{prop['area']} m²</b> • {prop['address']} • {prop['specs']}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Chọn vào AHP", key=f"btn_{prop['id']}"):
                        if not any(h['Ten'] == prop['title'] for h in st.session_state["selected_houses_data"]):
                            if len(st.session_state["selected_houses_data"]) < 5:
                                # ĐÓNG GÓI FULL DỮ LIỆU SANG TRANG 3
                                st.session_state["selected_houses_data"].append({
                                    "Ten": prop['title'],
                                    "Giá thuê": f"{prop['price']:,} VNĐ",
                                    "Vị trí": prop['address'],
                                    "Diện tích": f"{prop['area']} m²",
                                    "An ninh": prop['security'],
                                    "Tiện ích": prop['utility'],
                                    "Tự do": prop['freedom']
                                })
                                st.rerun()
                            else: st.error("Tối đa 5 căn.")
                        else: st.warning("Đã chọn căn này.")
else:
    st.warning("Không tìm thấy kết quả phù hợp với tiêu chí của bạn.")