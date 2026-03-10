import streamlit as st
import time

st.set_page_config(page_title="Đăng Nhập Hệ Thống", layout="wide")

# --- 1. KHỞI TẠO DATABASE ẢO & SESSION ---
# Tạo một danh sách người dùng mặc định (nếu chưa có)
if "users_db" not in st.session_state:
    st.session_state["users_db"] = {
        "user": {"password": "user", "role": "User", "fullname": "Khách hàng cá nhân"},
        "admin": {"password": "admin", "role": "Admin", "fullname": "Quản trị viên"}
    }

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "role" not in st.session_state:
    st.session_state["role"] = None
if "username" not in st.session_state:
    st.session_state["username"] = None

# --- 2. CSS CAO CẤP ---
st.markdown("""
    <style>
    .main { background-color: #f8fafc; font-family: 'Inter', sans-serif; }
    [data-testid="stForm"] {
        background-color: #ffffff; padding: 3rem 2.5rem; border-radius: 16px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05); border: 1px solid #e2e8f0;
        border-top: 6px solid #0f172a;
    }
    .stTextInput input { border-radius: 8px; padding: 0.6rem 1rem; border: 1px solid #cbd5e1; }
    .stTextInput input:focus { border-color: #3b82f6; box-shadow: 0 0 0 1px #3b82f6; }
    
    [data-testid="stFormSubmitButton"] button {
        background-color: #0f172a; color: #ffffff; font-weight: 700; border-radius: 8px; 
        padding: 0.6rem 0; margin-top: 1rem; border: none; transition: all 0.3s;
    }
    [data-testid="stFormSubmitButton"] button:hover { background-color: #1e293b; transform: translateY(-2px); color: #ffffff;}
    
    div[data-testid="stVerticalBlock"] > div:nth-child(4) button {
        background-color: transparent; color: #3b82f6; border: 1px solid #cbd5e1;
        font-weight: 600; border-radius: 8px; padding: 0.5rem 0; transition: all 0.2s;
    }
    div[data-testid="stVerticalBlock"] > div:nth-child(4) button:hover { background-color: #f1f5f9; color: #1d4ed8; border-color: #94a3b8; }
    </style>
""", unsafe_allow_html=True)

# --- 3. GIAO DIỆN & LOGIC ĐĂNG NHẬP ---
if st.session_state["logged_in"]:
    st.success(f"Bạn đang đăng nhập với tư cách: **{st.session_state['username']}** ({st.session_state['role']})")
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        if st.button("VỀ TRANG CHỦ (GIỚI THIỆU)", use_container_width=True):
            st.switch_page("app.py")
        if st.button("VÀO TRANG PHÂN TÍCH AHP", use_container_width=True):
            st.switch_page("pages/3_AHP_Input.py")
        if st.button("ĐĂNG XUẤT", type="primary", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["role"] = None
            st.session_state["username"] = None
            st.rerun()
else:
    st.write("")
    st.write("")
    col1, col2, col3 = st.columns([1, 1.3, 1])
    
    with col2:
        with st.form("login_form"):
            st.markdown("<h2 style='color: #0f172a; text-align: center; font-weight: 800; margin-bottom: 0.5rem;'>CỔNG XÁC THỰC</h2>", unsafe_allow_html=True)
            st.markdown("<p style='color: #64748b; text-align: center; margin-bottom: 2rem;'>Vui lòng định danh để truy cập không gian làm việc</p>", unsafe_allow_html=True)
            
            login_user = st.text_input("Tên đăng nhập / Email")
            login_pass = st.text_input("Mật khẩu", type="password")
            st.markdown("<div style='font-size: 0.8rem; color: #94a3b8; margin-top: -10px; margin-bottom: 10px;'>*Tài khoản thử nghiệm: (user/user) hoặc (admin/admin).</div>", unsafe_allow_html=True)
            
            submitted = st.form_submit_button("XÁC THỰC & ĐĂNG NHẬP", use_container_width=True)
            
            if submitted:
                if not login_user or not login_pass:
                    st.warning("Vui lòng nhập đầy đủ thông tin.")
                else:
                    # LOGIC KIỂM TRA TỪ DATABASE ẢO
                    if login_user in st.session_state["users_db"]:
                        user_info = st.session_state["users_db"][login_user]
                        
                        if user_info["password"] == login_pass:
                            st.session_state["logged_in"] = True
                            st.session_state["role"] = user_info["role"]
                            st.session_state["username"] = user_info["fullname"]
                            
                            st.success(f"Xin chào {user_info['fullname']}! Đang truy cập hệ thống...")
                            time.sleep(1)
                            
                            if user_info["role"] == "Admin":
                                st.switch_page("pages/6_Admin_Dashboard.py")
                            else:
                                st.switch_page("app.py")
                        else:
                            st.error("Mật khẩu không chính xác. Vui lòng thử lại.")
                    else:
                        st.error("Tài khoản không tồn tại trên hệ thống.")
        
        st.write("")
        if st.button("Chưa có tài khoản? Khởi tạo hồ sơ mới", use_container_width=True):
            st.switch_page("pages/2_Register.py")