import streamlit as st
import requests

API = "http://127.0.0.1:8000"
headers = {"token": st.session_state["token"]}

st.title("👤 QUẢN LÝ USER")

res = requests.get(f"{API}/admin/users", headers=headers)
users = res.json()

for u in users:
    with st.container(border=True):
        st.write(f"👤 {u['name']} ({u['email']})")
        st.write("Role:", u["role"])

        if st.button("❌ Xóa", key=u["_id"]):
            requests.delete(
                f"{API}/admin/delete-user/{u['_id']}",
                headers=headers
            )
            st.rerun()