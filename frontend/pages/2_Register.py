import streamlit as st
import requests

st.title("📝 Register")

name = st.text_input("Name")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Create Account"):

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
        st.success("Account created successfully")
    else:
        st.error(data.get("error","Register failed"))