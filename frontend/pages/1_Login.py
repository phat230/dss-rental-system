import streamlit as st
import requests

st.set_page_config(page_title="Login")

st.title("🔐 Đăng nhập hệ thống")

col1,col2,col3 = st.columns([1,2,1])

with col2:

    email = st.text_input("📧 Email")

    password = st.text_input(
        "🔑 Password",
        type="password"
    )

    if st.button("Đăng nhập"):

        response = requests.post(
            "http://127.0.0.1:8000/auth/login",
            json={
                "email": email,
                "password": password
            }
        )

        data = response.json()

        if "token" in data:

            st.session_state["token"] = data["token"]
            st.session_state["role"] = data["role"]
            st.session_state["name"] = data["name"]

            st.success("Đăng nhập thành công")

            if data["role"] == "admin":
                st.switch_page("pages/6_Admin_Dashboard.py")
            else:
                st.switch_page("pages/4_Search_Rentals.py")

        else:
            st.error(data["error"])