import streamlit as st
import time

st.set_page_config(page_title="Đăng Ký Tài Khoản", layout="wide")

# KHỞI TẠO DATABASE ẢO (Đồng bộ với trang Login)
if "users_db" not in st.session_state:
    st.session_state["users_db"] = {
        "user": {"password": "user", "role": "User", "fullname": "Khách hàng cá nhân"},
        "admin": {"password": "admin", "role": "Admin", "fullname": "Quản trị viên"}
    }

st.markdown("""
    <style>
    .main { background-color: #f8fafc; font-family: 'Inter', sans-serif; }
    
    [data-testid="stForm"] {
        background-color: #ffffff; padding: 3rem 2.5rem; border-radius: 16px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05); border: 1px solid #e2e8f0;
        border-top: 6px solid #3b82f6;
    }
    .stTextInput input { border-radius: 8px; padding: 0.6rem 1rem; border: 1px solid #cbd5e1; }
    .stTextInput input:focus { border-color: #3b82f6; box-shadow: 0 0 0 1px #3b82f6; }
    
    [data-testid="stFormSubmitButton"] button {
        background-color: #3b82f6; color: #ffffff; font-weight: 700; border-radius: 8px; 
        padding: 0.6rem 0; margin-top: 1rem; border: none; transition: all 0.3s;
    }
    [data-testid="stFormSubmitButton"] button:hover { background-color: #2563eb; transform: translateY(-2px); color: #ffffff;}
    
    div[data-testid="stVerticalBlock"] > div:nth-child(4) button {
        background-color: transparent; color: #475569; border: 1px solid #cbd5e1;
        font-weight: 600; border-radius: 8px; padding: 0.5rem 0; transition: all 0.2s;
    }
    div[data-testid="stVerticalBlock"] > div:nth-child(4) button:hover { background-color: #f1f5f9; color: #0f172a; border-color: #94a3b8; }
    </style>
""", unsafe_allow_html=True)

st.write("")
st.write("")
col1, col2, col3 = st.columns([1, 1.3, 1])

with col2:
    with st.form("register_form"):
        st.markdown("<h2 style='color: #0f172a; text-align: center; font-weight: 800; margin-bottom: 0.5rem;'>KHỞI TẠO HỒ SƠ</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748b; text-align: center; margin-bottom: 2rem;'>Thiết lập tài khoản để lưu trữ phân tích cá nhân</p>", unsafe_allow_html=True)
        
        reg_fullname = st.text_input("Họ và tên đầy đủ")
        reg_email = st.text_input("Tên đăng nhập / Địa chỉ Email")
        reg_pass = st.text_input("Mật khẩu bảo mật", type="password")
        reg_pass_confirm = st.text_input("Xác nhận lại mật khẩu", type="password")
        
        submitted = st.form_submit_button("GỬI YÊU CẦU ĐĂNG KÝ", use_container_width=True)
        
        if submitted:
            if not reg_fullname or not reg_email or not reg_pass:
                st.warning("Vui lòng điền đầy đủ các trường thông tin.")
            elif reg_pass != reg_pass_confirm:
                st.error("Mật khẩu xác nhận không trùng khớp.")
            elif len(reg_pass) < 6:
                st.warning("Mật khẩu phải bao gồm ít nhất 6 ký tự.")
            elif reg_email in st.session_state["users_db"]:
                # Kiểm tra xem tài khoản đã tồn tại chưa
                st.error("Email/Tên đăng nhập này đã được đăng ký. Vui lòng chọn tên khác!")
            else:
                # LƯU TÀI KHOẢN MỚI VÀO DATABASE ẢO
                st.session_state["users_db"][reg_email] = {
                    "password": reg_pass,
                    "role": "User", # Mặc định người đăng ký mới là User
                    "fullname": reg_fullname
                }
                
                st.success("Tài khoản đã được khởi tạo thành công!")
                st.info("Hệ thống đang tự động chuyển hướng về trang Đăng nhập...")
                time.sleep(2)
                st.switch_page("pages/1_Login.py")
                
    st.write("")
    if st.button("Đã có tài khoản? Trở về trang Đăng nhập", use_container_width=True):
        st.switch_page("pages/1_Login.py")