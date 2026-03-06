import streamlit as st
import requests

st.title("🔐 Login")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):

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

        st.success("Login successful!")

        # Redirect
        if data["role"] == "admin":
            st.switch_page("pages/6_Admin_Dashboard.py")
        else:
            st.switch_page("pages/4_Search_Rentals.py")

    else:
        st.error(data["error"])