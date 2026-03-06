import streamlit as st
import requests

st.title("🔎 Search Rentals")

query = st.text_input(
    "Mô tả phòng trọ mong muốn",
    "phòng trọ gần đại học"
)

max_price = st.number_input(
    "Max price",
    1000000,
    10000000,
    5000000
)

min_area = st.number_input(
    "Min area",
    10,
    100,
    20
)

if st.button("Search"):

    weights = st.session_state.get(
        "weights",
        [0.2,0.2,0.2,0.2,0.2]
    )

    response = requests.post(
        "http://127.0.0.1:8000/rentals/search",
        headers={
            "token": st.session_state["token"]
        },
        json={
            "query": query,
            "max_price": max_price,
            "min_area": min_area,
            "weights": weights
        }
    )

    results = response.json()

    st.session_state["results"] = results

    st.success("Search completed")