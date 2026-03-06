import streamlit as st
import requests
import pandas as pd

st.title("📊 AHP Matrix Input")

criteria = ["Price","Location","Area","Security","Amenities"]

matrix = st.data_editor(
    pd.DataFrame(
        [
            [1,3,5,3,2],
            [1/3,1,2,2,2],
            [1/5,1/2,1,2,3],
            [1/3,1/2,1/2,1,2],
            [1/2,1/2,1/3,1/2,1]
        ],
        columns=criteria,
        index=criteria
    )
)

if st.button("Calculate AHP"):

    response = requests.post(
        "http://127.0.0.1:8000/ahp/calculate",
        json={
            "matrix": matrix.values.tolist()
        }
    )

    data = response.json()

    if "weights" in data:

        st.session_state["weights"] = data["weights"]

        st.success("AHP calculated")

        st.write("Weights:")

        st.bar_chart(data["weights"])

    else:
        st.error("Matrix inconsistency")