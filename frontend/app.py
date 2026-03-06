import streamlit as st
import numpy as np
from utils.api import calculate_ahp, search_rentals
from components.rental_card import render_rental_card

st.set_page_config(layout="wide")

st.title("⚡ SMART-RENT AI")
st.caption("HỆ HỖ TRỢ RA QUYẾT ĐỊNH ĐA TIÊU CHÍ")

# ---------------- SIDEBAR ----------------

st.sidebar.header("🎯 Ưu tiên của bạn")

price = st.sidebar.slider("Giá",1,9,3)
location = st.sidebar.slider("Vị trí",1,9,3)
area = st.sidebar.slider("Diện tích",1,9,3)

query = st.sidebar.text_input(
    "Tìm kiếm",
    "phòng trọ gần đại học"
)

# tạo matrix AHP
matrix = [
    [1, price/location, price/area],
    [location/price, 1, location/area],
    [area/price, area/location, 1]
]

if st.sidebar.button("PHÂN TÍCH & GỢI Ý"):

    ahp = calculate_ahp(matrix)

    st.session_state["weights"] = ahp["weights"]

    rentals = search_rentals(
        query,
        ahp["weights"]
    )

    st.session_state["rentals"] = rentals


# ---------------- WEIGHTS ----------------

if "weights" in st.session_state:

    st.sidebar.subheader("📊 Trọng số")

    labels = ["Price","Location","Area"]

    for i,w in enumerate(st.session_state["weights"]):

        st.sidebar.write(labels[i])
        st.sidebar.progress(w)


# ---------------- RESULTS ----------------

if "rentals" in st.session_state:

    rentals = st.session_state["rentals"]

    st.header("🏠 Danh sách đề xuất")

    page_size = 5

    if "page" not in st.session_state:
        st.session_state.page = 1

    start = (st.session_state.page-1)*page_size
    end = start + page_size

    for i,r in enumerate(rentals[start:end]):

        render_rental_card(
            r,
            best=(i==0 and st.session_state.page==1)
        )

    col1,col2 = st.columns(2)

    with col1:
        if st.button("← Trang trước"):
            st.session_state.page -= 1

    with col2:
        if st.button("Trang sau →"):
            st.session_state.page += 1