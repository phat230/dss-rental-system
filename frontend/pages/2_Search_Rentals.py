import streamlit as st

query = st.text_input("Search")

max_price = st.number_input("Max price", value=5000000)

min_area = st.number_input("Min area", value=20)

if st.button("Search"):

    st.session_state["query"]=query
    st.session_state["max_price"]=max_price
    st.session_state["min_area"]=min_area