import streamlit as st
import requests

API = "http://127.0.0.1:8000"

st.title("🏠 QUẢN LÝ PHÒNG TRỌ")

# ======================
# 🔐 CHECK LOGIN
# ======================
if "token" not in st.session_state:
    st.error("Vui lòng đăng nhập lại")
    st.stop()

if st.session_state.get("role") != "admin":
    st.error("Không có quyền truy cập")
    st.stop()

headers = {"token": st.session_state["token"]}

# ======================
# LOAD DATA
# ======================
try:
    res = requests.get(f"{API}/admin/rentals", headers=headers, timeout=10)
    
    if res.status_code != 200:
        st.error("Lỗi API")
        st.write(res.text)
        st.stop()

    rentals = res.json()

    # ❗ FIX LỖI CHÍNH: đảm bảo là list
    if not isinstance(rentals, list):
        st.error("Dữ liệu không hợp lệ từ server")
        st.write(rentals)
        st.stop()

except Exception as e:
    st.error(f"Lỗi kết nối backend: {e}")
    st.stop()

# ======================
# TABLE
# ======================
if not rentals:
    st.info("Chưa có phòng trọ nào")
else:
    for r in rentals:
        with st.container(border=True):

            # ❗ dùng .get an toàn
            st.subheader(r.get("title", "Không có tiêu đề"))

            col1, col2, col3 = st.columns(3)

            col1.markdown(f"**💰 Giá:** {r.get('price', 'N/A')} VNĐ")
            col2.markdown(f"**📐 Diện tích:** {r.get('area', 'N/A')} m²")
            col3.markdown(f"**🔒 An ninh:** {r.get('security', 'N/A')}/5")

            colA, colB = st.columns(2)

            # ❗ tránh lỗi key None
            rental_id = r.get("_id")

            if rental_id:
                if colA.button("🗑 Xóa", key=f"delete_{rental_id}"):
                    requests.delete(
                        f"{API}/admin/delete-rental/{rental_id}",
                        headers=headers
                    )
                    st.rerun()

                if colB.button("✏️ Sửa", key=f"edit_{rental_id}"):
                    st.session_state["edit_id"] = rental_id
                    st.session_state["edit_data"] = r

# ======================
# ADD NEW
# ======================
st.divider()
st.subheader("➕ Thêm phòng")

title = st.text_input("Title")
price = st.number_input("Price", min_value=0)
area = st.number_input("Area", min_value=0)
security = st.slider("Security", 1, 5)

if st.button("Thêm"):
    if not title:
        st.warning("Vui lòng nhập tiêu đề")
    else:
        try:
            res = requests.post(
                f"{API}/admin/add-rental",
                headers=headers,
                json={
                    "title": title,
                    "price": price,
                    "area": area,
                    "security": security
                },
                timeout=10
            )

            if res.status_code == 200:
                st.success("Đã thêm phòng")
                st.rerun()
            else:
                st.error("Lỗi thêm phòng")
                st.write(res.text)

        except Exception as e:
            st.error(f"Lỗi kết nối backend: {e}")