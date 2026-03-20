import streamlit as st
import requests
import time

st.set_page_config(page_title="Đăng Ký", layout="wide")

API_URL = "http://127.0.0.1:8000"

col1, col2, col3 = st.columns([1,1.3,1])

with col2:

    with st.form("register_form"):

        st.subheader("ĐĂNG KÝ TÀI KHOẢN")

        fullname = st.text_input("Họ và tên")
        email = st.text_input("Email")
        password = st.text_input("Mật khẩu", type="password")
        confirm = st.text_input("Xác nhận mật khẩu", type="password")

        submitted = st.form_submit_button("Đăng ký")

        if submitted:

            if not fullname or not email or not password:
                st.warning("Vui lòng nhập đầy đủ thông tin")

            elif password != confirm:
                st.error("Mật khẩu không khớp")

            elif len(password) < 6:
                st.warning("Mật khẩu phải >= 6 ký tự")

            else:

                try:

                    response = requests.post(
                        f"{API_URL}/auth/register",
                        json={
                            "name": fullname,
                            "email": email,
                            "password": password
                        },
                        timeout=5
                    )

                    st.write("Status:", response.status_code)
                    st.write("Response:", response.text)

                    data = response.json()

                    if response.status_code == 200:

                        st.success("Đăng ký thành công")
                        time.sleep(1)

                        st.switch_page("pages/1_Login.py")

                    else:
                        st.error(data.get("error","Register failed"))

                except Exception as e:
                    st.error(f"Lỗi kết nối backend: {e}")

    st.write("")

    if st.button("Đã có tài khoản? Đăng nhập"):
        st.switch_page("pages/1_Login.py")