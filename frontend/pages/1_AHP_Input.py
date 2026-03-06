import streamlit as st
import requests
import pandas as pd

st.title("AHP Matrix Input")

matrix = st.data_editor(
    pd.DataFrame([
        [1,3,5],
        [1/3,1,2],
        [1/5,1/2,1]
    ])
)

if st.button("Calculate"):

    res = requests.post(
        "http://localhost:8000/ahp/calculate",
        json={"matrix":matrix.values.tolist()}
    )

    data = res.json()

    st.write("Weights:", data["weights"])
    st.write("CR:", data["CR"])

    st.bar_chart(data["weights"])