import streamlit as st
import requests

if "role" not in st.session_state:
    st.error("Vui lòng đăng nhập")
    st.stop()

if st.session_state["role"] != "admin":
    st.error("Chỉ admin được truy cập")
    st.stop()

st.title("⚙️ ADMIN DASHBOARD")

st.success(f"Xin chào Admin {st.session_state['name']}")

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
        "http://127.0.0.1:8000/admin/add-rental",
        headers={
            "token": st.session_state["token"]
        },
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
    else:
        st.error("Lỗi thêm phòng")