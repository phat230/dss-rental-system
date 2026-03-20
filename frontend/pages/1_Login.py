import streamlit as st
import requests
import time

st.set_page_config(page_title="Đăng Nhập Hệ Thống", layout="wide")

# sửa localhost -> 127.0.0.1
API_URL = "http://127.0.0.1:8000"

# Session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "username" not in st.session_state:
    st.session_state.username = None

# ==============================
# CSS
# ==============================

st.markdown("""
<style>
.main { background-color: #f8fafc; font-family: 'Inter', sans-serif; }

[data-testid="stForm"] {
    background-color: #ffffff;
    padding: 3rem 2.5rem;
    border-radius: 16px;
    box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05);
    border: 1px solid #e2e8f0;
    border-top: 6px solid #0f172a;
}

.stTextInput input {
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# LOGIN FORM
# ==============================

col1, col2, col3 = st.columns([1,1.3,1])

with col2:

    with st.form("login_form"):

        st.subheader("ĐĂNG NHẬP")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Đăng nhập")

        if submitted:

            if not email or not password:
                st.warning("Vui lòng nhập đầy đủ thông tin")
                st.stop()

            try:

                response = requests.post(
                    f"{API_URL}/auth/login",
                    json={
                        "email": email,
                        "password": password
                    },
                    timeout=30
                )

                st.write("Status:", response.status_code)
                st.write("Response:", response.text)

                data = response.json()

                if response.status_code == 200 and "token" in data:

                    st.session_state.logged_in = True
                    st.session_state.role = data["role"]
                    st.session_state.username = data["name"]
                    st.session_state.token = data["token"]

                    st.success("Đăng nhập thành công")
                    time.sleep(1)

                    if data["role"] == "admin":
                        st.switch_page("pages/6_Admin_Dashboard.py")
                    else:
                        st.switch_page("app.py")

                else:
                    st.error(data.get("error","Login failed"))

            except Exception as e:
                st.error(f"Lỗi kết nối backend: {e}")

    st.write("")

    if st.button("Chưa có tài khoản? Đăng ký"):
        st.switch_page("pages/2_Register.py")