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
# 📌 SIDEBAR MENU
# ======================
st.sidebar.title("⚙️ ADMIN MENU")

if st.sidebar.button("📊 Dashboard"):
    st.switch_page("pages/6_Admin_Dashboard.py")

if st.sidebar.button("🏠 Quản lý phòng"):
    st.switch_page("pages/7_Admin_Rentals.py")

if st.sidebar.button("👤 Quản lý user"):
    st.switch_page("pages/8_Admin_Users.py")

# ======================
# 📊 DASHBOARD
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
# ➕ FORM THÊM PHÒNG
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

location = st.text_input("Địa chỉ")

security = st.slider(
    "Mức độ an ninh",
    1,
    5
)

amenities = st.slider(
    "Tiện ích",
    1,
    5
)

# ======================
# 🖼️ UPLOAD ẢNH
# ======================
uploaded_file = st.file_uploader(
    "Upload ảnh",
    type=["jpg", "png"]
)

# Preview ảnh trước khi upload
if uploaded_file:
    st.image(uploaded_file, caption="Ảnh preview")

# ======================
# 🚀 SUBMIT
# ======================
if st.button("Thêm phòng trọ"):

    # validate
    if not title or not description or not location:
        st.warning("⚠️ Vui lòng nhập đầy đủ thông tin")
        st.stop()

    if not uploaded_file:
        st.warning("⚠️ Vui lòng chọn ảnh")
        st.stop()

    # ======================
    # 📤 UPLOAD ẢNH
    # ======================
    try:
        upload_res = requests.post(
            f"{API}/upload/image",
            files={"file": uploaded_file}
        )

        image_url = upload_res.json()["image_url"]

    except:
        st.error("❌ Lỗi upload ảnh")
        st.stop()

    # ======================
    # 📦 DATA GỬI BACKEND
    # ======================
    data = {
        "title": title,
        "description": description,
        "price": price,
        "area": area,
        "location": location,
        "security": security,
        "amenities": amenities,
        "image_url": image_url
    }

    # ======================
    # 🚀 GỬI API
    # ======================
    try:
        response = requests.post(
            f"{API}/admin/add-rental",
            headers=headers,
            json=data
        )

        if response.status_code == 200:
            st.success("✅ Thêm phòng thành công")
            st.image(image_url)
            st.rerun()
        else:
            st.error("❌ Lỗi thêm phòng")

    except:
        st.error("❌ Không kết nối được backend")

# ======================
# 📥 IMPORT EXCEL
# ======================
st.divider()
st.subheader("📊 Import dữ liệu từ Excel")

excel_file = st.file_uploader(
    "Upload file Excel",
    type=["xlsx"]
)

if st.button("Import Excel"):

    if not excel_file:
        st.warning("⚠️ Vui lòng chọn file Excel")
        st.stop()

    try:
        res = requests.post(
            f"{API}/import/excel",
            files={"file": excel_file}
        )

        if res.status_code == 200:
            st.success("✅ Import thành công")
            st.rerun()
        else:
            st.error("❌ Import thất bại")

    except:
        st.error("❌ Lỗi kết nối backend")