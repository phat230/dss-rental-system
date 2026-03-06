import streamlit as st

st.set_page_config(
    page_title="DSS Rental System",
    layout="wide"
)

st.title(" DSS Hệ Hỗ Trợ Quyết Định Thuê Nhà")

if "token" not in st.session_state:
    st.warning("Bạn cần đăng nhập trước")
    st.stop()

st.sidebar.write(" Xin chào:", st.session_state["name"])
st.sidebar.write("Role:", st.session_state["role"])

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()

st.write("Chọn chức năng bên menu bên trái.")