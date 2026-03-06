import streamlit as st

st.set_page_config(
    page_title="DSS Rental System",
    layout="wide"
)

st.title("🏠 HỆ HỖ TRỢ RA QUYẾT ĐỊNH THUÊ NHÀ")

st.markdown("""
Hệ thống hỗ trợ người dùng **tìm kiếm và lựa chọn nhà trọ phù hợp**
dựa trên phương pháp **AHP (Analytic Hierarchy Process)**.

### Chức năng hệ thống
- 🔐 Đăng nhập / Đăng ký
- 📊 Tính trọng số tiêu chí bằng AHP
- 🔎 Tìm kiếm phòng trọ phù hợp
- 🏆 Xếp hạng phòng trọ tốt nhất
- ⚙️ Admin quản lý dữ liệu nhà trọ
""")

if "token" not in st.session_state:
    st.warning("⚠️ Bạn cần đăng nhập trước")
    st.stop()

st.sidebar.title("👤 Thông tin người dùng")

st.sidebar.write("Tên:", st.session_state["name"])
st.sidebar.write("Role:", st.session_state["role"])

if st.sidebar.button("🚪 Logout"):
    st.session_state.clear()
    st.rerun()

st.success("Chọn chức năng trong menu bên trái.")