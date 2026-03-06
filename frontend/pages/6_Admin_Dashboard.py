import streamlit as st
import requests

# kiểm tra login
if "role" not in st.session_state:
    st.error("Please login first")
    st.stop()

# kiểm tra admin
if st.session_state["role"] != "admin":
    st.error("Admin only")
    st.stop()

st.title("⚙️ Admin Dashboard")

st.write("Welcome Admin:", st.session_state.get("name"))

title = st.text_input("Title")
description = st.text_area("Description")

price = st.number_input(
    "Price",
    min_value=1000000,
    max_value=10000000
)

area = st.number_input(
    "Area",
    min_value=10,
    max_value=100
)

if st.button("Add Rental"):

    response = requests.post(
        "http://127.0.0.1:8000/admin/add-rental",
        headers={
            "Authorization": f"Bearer {st.session_state['token']}"
        },
        json={
            "title": title,
            "description": description,
            "price": price,
            "area": area
        }
    )

    data = response.json()

    if response.status_code == 200:
        st.success("Rental added successfully")
    else:
        st.error(data)