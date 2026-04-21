import streamlit as st
import requests

API = "http://127.0.0.1:8000"

st.set_page_config(page_title="Quản lý người dùng", layout="wide")

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
# HEADER 
# ======================
st.title("QUẢN LÝ NGƯỜI DÙNG")
st.write("Quản trị viên có thể xem danh sách tài khoản đã đăng ký hoặc xóa người dùng khỏi hệ thống.")

# ======================
# LOAD DATA TỪ BACKEND
# ======================
try:
    res = requests.get(f"{API}/admin/users", headers=headers, timeout=5)
    users = res.json() if res.status_code == 200 else []
except:
    users = []

# ======================
# HIỂN THỊ DANH SÁCH (SỬA / XÓA)
# ======================
if not users:
    st.warning("Hiện không có người dùng nào trong hệ thống hoặc Backend chưa kết nối.")
else:
    for u in users:
        # Tạo khung viền bao quanh mỗi User cho chuyên nghiệp
        with st.container(border=True):
            col_info, col_action = st.columns([4, 1])
            
            with col_info:
                st.markdown(f"**Họ và tên:** {u.get('name', 'Chưa cập nhật')}")
                st.write(f"Email: {u.get('email', 'N/A')} | Phân quyền: {str(u.get('role', 'user')).upper()}")
            
            with col_action:
                user_id = u.get("_id")
                if user_id:
                    # Nút xóa tài khoản (màu đỏ - primary)
                    if st.button("Xóa tài khoản", key=f"del_user_{user_id}", type="primary", use_container_width=True):
                        try:
                            requests.delete(
                                f"{API}/admin/delete-user/{user_id}",
                                headers=headers
                            )
                            st.rerun()
                        except:
                            st.error("Lỗi kết nối khi thực hiện lệnh xóa.")