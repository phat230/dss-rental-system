import streamlit as st
import requests

API = "http://127.0.0.1:8000"

# ======================
# ======================
# BẬT LẠI CHECK LOGIN CHUẨN
# ======================
if "token" not in st.session_state:
    st.error("⚠️ Vui lòng đăng nhập để tiếp tục!")
    st.stop()

if st.session_state.get("role") != "admin":
    st.error("🚫 Truy cập bị từ chối. Chỉ Admin mới được vào đây!")
    st.stop()

# Đã có token xịn từ trang Đăng nhập truyền sang
headers = {"token": st.session_state["token"]}

# ======================
# SIDEBAR MENU
# ======================
st.sidebar.title("ADMIN MENU")

if st.sidebar.button("Bảng điều khiển (Dashboard)", use_container_width=True):
    st.switch_page("pages/6_Admin_Dashboard.py")

if st.sidebar.button("Quản lý danh mục phòng", use_container_width=True):
    st.switch_page("pages/7_Admin_Rentals.py")

if st.sidebar.button("Quản lý người dùng", use_container_width=True):
    st.switch_page("pages/8_Admin_Users.py")

# ======================
# DASHBOARD HEADER
# ======================
st.title("ADMIN DASHBOARD")
st.success(f"Xin chào Quản trị viên: **{st.session_state.get('username', 'Admin')}**")

# ======================
# LOAD DATA TỪ BACKEND
# ======================
try:
    rentals = requests.get(f"{API}/admin/rentals", headers=headers).json()
    users = requests.get(f"{API}/admin/users", headers=headers).json()
except:
    st.error("Mất kết nối đến máy chủ Backend (FastAPI). Vui lòng kiểm tra lại!")
    rentals = []
    users = []

# ======================
# THỐNG KÊ NHANH (STATS)
# ======================
col1, col2 = st.columns(2)
with col1:
    st.metric("Tổng số phòng trọ trên hệ thống", len(rentals))
with col2:
    st.metric("Tổng số người dùng đăng ký", len(users))

# ======================
# FORM THÊM PHÒNG (ĐỒNG BỘ AHP)
# ======================
st.divider()
st.subheader("Thêm phòng trọ mới ")

with st.container():
    st.markdown("#### 1. Thông tin cơ bản & Liên hệ")
    title = st.text_input("Tiêu đề tin đăng", placeholder="VD: Căn hộ Studio Quận 2 Cũ - TP Thủ Đức")
    
    col_a, col_b = st.columns(2)
    with col_a:
        owner_name = st.text_input("Người đăng / Chủ trọ")
        district = st.selectbox("Quận / Huyện", ["Quận 1", "Quận 3", "Quận 5", "Quận 10", "Bình Thạnh", "Gò Vấp", "Thủ Đức", "Khác"])
    with col_b:
        phone = st.text_input("Số điện thoại liên hệ", placeholder="VD: 0901234567")
        address = st.text_input("Địa chỉ chi tiết")

    description = st.text_area("Mô tả chi tiết phòng trọ")

st.markdown("#### 2. Chỉ số phục vụ thuật toán AHP")
with st.container():
    col_c, col_d, col_e = st.columns(3)
    with col_c:
        price = st.number_input("Giá thuê (VNĐ)", min_value=500000, step=500000, value=3000000)
    with col_d:
        area = st.number_input("Diện tích (m2)", min_value=5.0, step=1.0, value=25.0)
    with col_e:
        distance = st.number_input("Khoảng cách trung tâm (km)", min_value=0.1, step=0.5, value=2.0)

    col_f, col_g = st.columns(2)
    with col_f:
        quality = st.slider("Chất lượng phòng (Thang điểm Saaty 1-9)", 1, 9, 5)
    with col_g:
        security = st.slider("Mức độ an ninh (Thang điểm Saaty 1-9)", 1, 9, 5)

st.markdown("#### 3. Tọa độ Bản đồ ")
with st.container():
    col_h, col_i = st.columns(2)
    with col_h:
        lat = st.number_input("Vĩ độ (Latitude)", format="%.6f", value=10.762622)
    with col_i:
        lng = st.number_input("Kinh độ (Longitude)", format="%.6f", value=106.660172)

st.markdown("#### 4. Hình ảnh minh họa")
uploaded_file = st.file_uploader("Kéo thả hoặc chọn ảnh (JPG, PNG)", type=["jpg", "png", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Ảnh xem trước", use_container_width=True)

# ======================
# XỬ LÝ SUBMIT THÊM PHÒNG
# ======================
if st.button("Lưu thông tin & Đồng bộ AHP", type="primary"):
    # Validate cơ bản
    if not title or not address or not phone:
        st.warning("Vui lòng nhập đầy đủ các thông tin bắt buộc (Tiêu đề, Địa chỉ, SĐT).")
        st.stop()

    image_url = "" # Mặc định nếu không có ảnh
    
    # Upload ảnh nếu có
    if uploaded_file:
        try:
            with st.spinner("Đang tải ảnh lên máy chủ..."):
                upload_res = requests.post(f"{API}/upload/image", files={"file": uploaded_file})
                image_url = upload_res.json().get("image_url", "")
        except:
            st.error("Có lỗi xảy ra trong quá trình upload ảnh!")
            st.stop()

    # Đóng gói Payload gửi lên Backend
    payload = {
        "title": title,
        "owner_name": owner_name,
        "phone": phone,
        "district": district,
        "address": address,
        "description": description,
        "price": price,
        "area": area,
        "distance": distance,
        "quality": quality,
        "security": security,
        "lat": lat,
        "lng": lng,
        "image_url": image_url
    }

    # Gửi request Insert vào DB
    try:
        with st.spinner("Đang lưu vào Cơ sở dữ liệu..."):
            response = requests.post(f"{API}/admin/add-rental", headers=headers, json=payload)
            
            if response.status_code == 200:
                st.success("Đã thêm phòng trọ thành công! Dữ liệu đã sẵn sàng cho thuật toán AHP.")
                st.rerun()
            else:
                st.error(f"Thêm phòng thất bại: {response.text}")
    except:
        st.error("Không kết nối được tới Backend.")

# ======================
# IMPORT EXCEL (NẠP DỮ LIỆU HÀNG LOẠT)
# ======================
st.divider()
with st.expander("NHẬP DỮ LIỆU NÂNG CAO TỪ TỆP EXCEL "):
    st.info("Mẹo: Đảm bảo file Excel của bạn có các cột tương ứng: title, price, area, distance, quality, security...")
    excel_file = st.file_uploader("Upload file Excel (.xlsx)", type=["xlsx"])

    if st.button("Bắt đầu tải lên & Xử lý"):
        if not excel_file:
            st.warning("Bạn chưa chọn file Excel nào!")
            st.stop()
            
        try:
            with st.spinner("Hệ thống đang đọc và import dữ liệu vào MongoDB..."):
                res = requests.post(f"{API}/import/excel", files={"file": excel_file})
                
                if res.status_code == 200:
                    st.success("Import dữ liệu hàng loạt thành công!")
                else:
                    st.error(f"Lỗi Import: {res.text}")
        except:
            st.error("Lỗi kết nối đến Backend xử lý file.")