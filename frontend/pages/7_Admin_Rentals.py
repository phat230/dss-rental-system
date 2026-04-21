import streamlit as st
import requests

API = "http://127.0.0.1:8000"

st.set_page_config(page_title="Quản lý danh mục phòng", layout="wide")

# ======================
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
# HEADER & LOAD DATA
# ======================
st.title("QUẢN LÝ DANH MỤC PHÒNG TRỌ")
st.write("Quản trị viên có thể xem danh sách, cập nhật thông số AHP hoặc xóa các phòng trọ khỏi hệ thống.")

try:
    res = requests.get(f"{API}/admin/rentals", headers=headers, timeout=5)
    rentals = res.json() if res.status_code == 200 else []
except:
    rentals = []

# ======================
# HIỂN THỊ DANH SÁCH (SỬA / XÓA)
# ======================
if not rentals:
    st.warning("Hiện không có phòng nào trong hệ thống hoặc Backend chưa kết nối.")
else:
    for r in rentals:
        # Tạo một khung viền bao quanh mỗi phòng
        with st.container(border=True):
            col_info, col_action = st.columns([4, 1])
            
            with col_info:
                st.markdown(f"**{r.get('title', 'Chưa có tiêu đề')}**")
                # Hiển thị tóm tắt các thông số quan trọng cho AHP
                price_formatted = f"{int(r.get('price', 0)):,}"
                st.write(f"Giá: {price_formatted} VNĐ | Diện tích: {r.get('area', 0)} m2 | Khoảng cách: {r.get('distance', 0)} km")
                st.write(f"Chất lượng: {r.get('quality', 5)}/9 | An ninh: {r.get('security', 5)}/9 | Khu vực: {r.get('district', 'N/A')}")
            
            with col_action:
                rental_id = r.get("_id")
                if rental_id:
                    # Nút sửa
                    if st.button("Sửa thông tin", key=f"edit_btn_{rental_id}", use_container_width=True):
                        st.session_state["edit_id"] = rental_id
                        st.session_state["edit_data"] = r
                        st.rerun()

                    # Nút xóa
                    if st.button("Xóa phòng", key=f"del_btn_{rental_id}", type="primary", use_container_width=True):
                        requests.delete(f"{API}/admin/delete-rental/{rental_id}", headers=headers)
                        # Nếu đang mở form sửa của đúng phòng này thì đóng lại
                        if "edit_id" in st.session_state and st.session_state["edit_id"] == rental_id:
                            del st.session_state["edit_id"]
                            del st.session_state["edit_data"]
                        st.rerun()

# ======================
# FORM CẬP NHẬT (Chỉ hiện khi bấm nút Sửa)
# ======================
if "edit_id" in st.session_state and "edit_data" in st.session_state:
    st.markdown("---")
    st.subheader("CẬP NHẬT THÔNG TIN PHÒNG TRỌ")
    data = st.session_state["edit_data"]
    
    with st.form("edit_form"):
        st.markdown("#### 1. Thông tin cơ bản & Liên hệ")
        u_title = st.text_input("Tiêu đề tin đăng", value=data.get("title", ""))
        
        col_a, col_b = st.columns(2)
        with col_a:
            u_owner = st.text_input("Người đăng / Chủ trọ", value=data.get("owner_name", ""))
            
            districts_list = ["Quận 1", "Quận 3", "Quận 5", "Quận 10", "Bình Thạnh", "Gò Vấp", "Thủ Đức", "Khác"]
            current_district = data.get("district", "Khác")
            if current_district not in districts_list:
                districts_list.append(current_district)
            
            u_district = st.selectbox("Quận / Huyện", options=districts_list, index=districts_list.index(current_district))
        
        with col_b:
            u_phone = st.text_input("Số điện thoại liên hệ", value=str(data.get("phone", "")))
            u_address = st.text_input("Địa chỉ chi tiết", value=data.get("address", ""))
        
        u_desc = st.text_area("Mô tả chi tiết", value=data.get("description", ""))

        st.markdown("#### 2. Chỉ số phục vụ thuật toán AHP")
        col_c, col_d, col_e = st.columns(3)
        with col_c:
            u_price = st.number_input("Giá thuê (VNĐ)", value=int(data.get("price", 3000000)), step=500000)
        with col_d:
            u_area = st.number_input("Diện tích (m2)", value=float(data.get("area", 20.0)), step=1.0)
        with col_e:
            u_distance = st.number_input("Khoảng cách trung tâm (km)", value=float(data.get("distance", 2.0)), step=0.5)

        col_f, col_g = st.columns(2)
        with col_f:
            u_quality = st.slider("Chất lượng phòng (Thang điểm Saaty 1-9)", 1, 9, value=int(data.get("quality", 5)))
        with col_g:
            u_security = st.slider("Mức độ an ninh (Thang điểm Saaty 1-9)", 1, 9, value=int(data.get("security", 5)))

        st.markdown("#### 3. Tọa độ Bản đồ")
        col_h, col_i = st.columns(2)
        with col_h:
            u_lat = st.number_input("Vĩ độ (Latitude)", format="%.6f", value=float(data.get("lat", 10.762622)))
        with col_i:
            u_lng = st.number_input("Kinh độ (Longitude)", format="%.6f", value=float(data.get("lng", 106.660172)))

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2, 2, 6])
        
        if c1.form_submit_button("Lưu thay đổi", type="primary"):
            payload = {
                "title": u_title,
                "owner_name": u_owner,
                "phone": u_phone,
                "district": u_district,
                "address": u_address,
                "description": u_desc,
                "price": u_price,
                "area": u_area,
                "distance": u_distance,
                "quality": u_quality,
                "security": u_security,
                "lat": u_lat,
                "lng": u_lng
            }
            requests.put(
                f"{API}/admin/update-rental/{st.session_state['edit_id']}",
                headers=headers,
                json=payload
            )
            del st.session_state["edit_id"]
            del st.session_state["edit_data"]
            st.rerun()
            
        if c2.form_submit_button("Hủy bỏ"):
            del st.session_state["edit_id"]
            del st.session_state["edit_data"]
            st.rerun()