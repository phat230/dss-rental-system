import streamlit as st
import folium
from streamlit_folium import st_folium


def render_rental_card(rental, best=False):

    col1, col2 = st.columns([1,3])

    with col1:
        st.image(
            "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2",
            use_column_width=True
        )

    with col2:

        if best:
            st.markdown("### ⭐ Best Match")

        st.subheader(rental["title"])

        st.write(rental["description"])

        st.write(f"💰 Price: {rental['price']}")
        st.write(f"📏 Area: {rental['area']}")

        if st.button(f"📍 Xem bản đồ {rental['id']}"):

            m = folium.Map(
                location=[10.7769,106.7009],
                zoom_start=14
            )

            folium.Marker(
                [10.7769,106.7009],
                popup=rental["title"]
            ).add_to(m)

            st_folium(m, height=250)