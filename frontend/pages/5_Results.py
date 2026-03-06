import streamlit as st

st.title("🏆 Recommended Rentals")

results = st.session_state.get("results",[])

if not results:
    st.warning("No results yet")
    st.stop()

for rental in results:

    with st.container():

        st.subheader(rental["title"])

        col1,col2,col3 = st.columns(3)

        col1.write("💰 Price:", rental["price"])
        col2.write("📐 Area:", rental["area"])
        col3.write("⭐ Score:", round(rental["score"],3))

        st.write(rental["description"])

        st.divider()