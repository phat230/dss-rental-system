import streamlit as st
import requests

st.title("📝 Đăng ký tài khoản")

col1,col2,col3 = st.columns([1,2,1])

with col2:

    name = st.text_input("Tên người dùng")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm = st.text_input(
        "Nhập lại Password",
        type="password"
    )

    if st.button("Tạo tài khoản"):

        if password != confirm:
            st.error("Password không khớp")
            st.stop()

        response = requests.post(
            "http://127.0.0.1:8000/auth/register",
            json={
                "name": name,
                "email": email,
                "password": password
            }
        )

        data = response.json()

        if "message" in data:
            st.success("Tạo tài khoản thành công")
        else:
            st.error(data.get("error"))