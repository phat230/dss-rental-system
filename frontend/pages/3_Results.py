import streamlit as st
import requests

weights = st.session_state.get("weights",[0.5,0.3,0.2])

query = st.session_state.get("query","")

max_price = st.session_state.get("max_price",5000000)

min_area = st.session_state.get("min_area",20)

if st.button("Get Results"):

    res = requests.post(
        "http://localhost:8000/rentals/search",
        json={
            "query":query,
            "max_price":max_price,
            "min_area":min_area,
            "weights":weights
        }
    )

    rentals = res.json()

    for r in rentals:

        st.subheader(r["title"])
        st.write(r["description"])
        st.write("Price:",r["price"])
        st.write("Score:",r["score"])