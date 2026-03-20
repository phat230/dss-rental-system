import streamlit as st
import requests

API = "http://127.0.0.1:8000"

# ======================
# 🔐 CHECK LOGIN
# ======================
if "role" not in st.session_state:
    st.error("Vui lòng đăng nhập")
    st.stop()

if st.session_state["role"] != "admin":
    st.error("Chỉ admin được truy cập")
    st.stop()

headers = {"token": st.session_state["token"]}

# ======================
# 📌 SIDEBAR MENU (PHẦN 5)
# ======================
st.sidebar.title("⚙️ ADMIN MENU")

if st.sidebar.button("📊 Dashboard"):
    st.switch_page("pages/6_Admin_Dashboard.py")

if st.sidebar.button("🏠 Quản lý phòng"):
    st.switch_page("pages/7_Admin_Rentals.py")

if st.sidebar.button("👤 Quản lý user"):
    st.switch_page("pages/8_Admin_Users.py")

# ======================
# 📊 DASHBOARD (PHẦN 4)
# ======================
st.title("📊 ADMIN DASHBOARD")

st.success(f"Xin chào Admin {st.session_state['username']}")

# ======================
# LOAD DATA
# ======================
try:
    rentals = requests.get(f"{API}/admin/rentals", headers=headers).json()
    users = requests.get(f"{API}/admin/users", headers=headers).json()
except:
    st.error("Không kết nối được backend")
    st.stop()

# ======================
# 📊 STATS
# ======================
col1, col2 = st.columns(2)

col1.metric("🏠 Tổng phòng", len(rentals))
col2.metric("👤 Tổng user", len(users))

# ======================
# 📋 DANH SÁCH NHANH
# ======================
st.subheader("🏠 Phòng mới nhất")

for r in rentals[:5]:
    st.write(f"• {r.get('title')} - {r.get('price')} VNĐ")

# ======================
# ➕ FORM THÊM PHÒNG (GIỮ LẠI CỦA BẠN)
# ======================
st.divider()
st.subheader("➕ Thêm phòng trọ mới")

title = st.text_input("Tiêu đề")
description = st.text_area("Mô tả")

price = st.number_input(
    "Giá",
    min_value=1000000,
    max_value=10000000
)

area = st.number_input(
    "Diện tích",
    min_value=10,
    max_value=100
)

security = st.slider(
    "Mức độ an ninh",
    1,
    5
)

if st.button("Thêm phòng trọ"):
    response = requests.post(
        f"{API}/admin/add-rental",
        headers=headers,
        json={
            "title": title,
            "description": description,
            "price": price,
            "area": area,
            "security": security
        }
    )

    if response.status_code == 200:
        st.success("Thêm phòng thành công")
        st.rerun()
    else:
        st.error("Lỗi thêm phòng")