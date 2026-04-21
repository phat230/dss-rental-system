import streamlit as st

# --- 1. CẤU HÌNH HỆ THỐNG ---
st.set_page_config(
    page_title="DSS Rental Analytics",
    layout="wide",
    initial_sidebar_state="expanded" # Giữ Sidebar mở
)

# --- 2. CSS CHUYÊN NGHIỆP ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] { 
        font-family: 'Inter', sans-serif; 
        background-color: #FAFAFA; 
        color: #1A1F36;
    }

    /* Hiệu ứng chữ Gradient cho Tiêu đề chính */
    .gradient-text {
        background: linear-gradient(135deg, #0061FF 0%, #60EFFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 16px;
    }
    
    .subtitle { font-size: 18px; color: #4B5563; line-height: 1.7; margin-bottom: 30px; }
    
    /* Thẻ So Sánh & Đối tượng */
    .vs-card { background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px; padding: 30px; height: 100%; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }
    .vs-title-bad { color: #DC2626; font-weight: 700; font-size: 20px; margin-bottom: 15px; border-bottom: 2px solid #FCA5A5; padding-bottom: 10px;}
    .vs-title-good { color: #059669; font-weight: 700; font-size: 20px; margin-bottom: 15px; border-bottom: 2px solid #6EE7B7; padding-bottom: 10px;}
    .audience-card { background: #FFFFFF; border-radius: 8px; overflow: hidden; border: 1px solid #E5E7EB; transition: transform 0.3s ease; height: 100%;}
    .audience-card:hover { transform: translateY(-5px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }
    .audience-content { padding: 20px; }
    .audience-title { font-weight: 700; font-size: 18px; color: #111827; margin-bottom: 8px; }
    .audience-desc { font-size: 14px; color: #4B5563; line-height: 1.5; }
    
    /* Tùy chỉnh Nút bấm Top Navbar */
    .nav-link-text { font-weight: 600; color: #4B5563; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. KHỞI TẠO SESSION STATE ---
if "token" not in st.session_state:
    st.session_state["token"] = None
if "name" not in st.session_state:
    st.session_state["name"] = "Khách hàng"
if "role" not in st.session_state:
    st.session_state["role"] = "Viewer"

# =========================================================================
# TOP NAVBAR (ĐỒNG BỘ 100% KÍCH THƯỚC CHO TẤT CẢ CÁC TRANG)
# =========================================================================
nav_1, nav_2, nav_3, nav_4, nav_space, nav_auth = st.columns([1.5, 1.5, 1.5, 1.5, 3.5, 1.5])

with nav_1: st.page_link("app.py", label="Trang chủ")
with nav_2: st.page_link("pages/3_AHP_Input.py", label="Thuật toán")
with nav_3: st.page_link("pages/4_Search_Rentals.py", label="Tìm kiếm")
with nav_4: st.page_link("pages/5_Results.py", label="Báo cáo")

if not st.session_state.get("token"):
    with nav_auth:
        if st.button("Đăng nhập", use_container_width=True, key="top_login"):
            st.switch_page("pages/1_Login.py")
else:
    with nav_space:
        name = st.session_state.get('name', 'Khách hàng')
        st.markdown(f"<div style='margin-top: 8px; font-weight: 600; text-align: right; color: #4B5563;'>Chào, {name}</div>", unsafe_allow_html=True)
    with nav_auth:
        if st.button("Thoát", use_container_width=True, key="top_logout"):
            st.session_state.clear()
            st.rerun()

st.markdown("<hr style='margin-top: 5px; margin-bottom: 30px; border-color: #E5E7EB;'>", unsafe_allow_html=True)
# =========================================================================
# 5. SIDEBAR TRUYỀN THỐNG (Đồng bộ với Top Navbar)
# =========================================================================
with st.sidebar:
    st.markdown("### Quản trị hệ thống")
    st.markdown("---")
    
    if st.session_state["token"]:
        # Đã đăng nhập
        st.write(f"Người dùng: `{st.session_state['name']}`")
        st.write(f"Vai trò: `{st.session_state['role']}`")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Đăng xuất", use_container_width=True, key="side_logout"):
            st.session_state.clear()
            st.rerun()
    else:
        # Chưa đăng nhập
        st.info("Vui lòng xác thực tài khoản.")
        if st.button("Đăng nhập", use_container_width=True, key="side_login"):
            st.switch_page("pages/1_Login.py")
        if st.button("Tạo tài khoản", use_container_width=True, key="side_reg"):
            st.switch_page("pages/2_Register.py")
            
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.caption("Phiên bản v2.5 - Powered by AHP")


# =========================================================================
# 6. NỘI DUNG CHÍNH (MAIN PAGE)
# =========================================================================

if not st.session_state["token"]:
    # --- GIAO DIỆN LANDING PAGE (KHI CHƯA ĐĂNG NHẬP) ---
    h_col1, h_col2 = st.columns([1.2, 1], gap="large")
    with h_col1:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="gradient-text">Quyết Định Thuê Nhà Dựa Trên Dữ Liệu Thực Tế.</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Đừng để cảm tính đánh lừa bạn. Hệ thống DSS sử dụng thuật toán Phân tích phân cấp (AHP) giúp bạn tìm ra căn hộ hoàn hảo nhất dựa trên chính mức độ ưu tiên của bạn về Giá cả, Vị trí và Tiện ích.</div>', unsafe_allow_html=True)
        
        # --- ĐÃ THÊM NÚT ĐĂNG NHẬP NGAY CÙNG HÀNG & KÍCH THƯỚC ---
        btn_action1, btn_action2, _ = st.columns([1, 1, 0.5]) 
        with btn_action1:
            if st.button("BẮT ĐẦU TRẢI NGHIỆM", type="primary", use_container_width=True, key="hero_start"):
                st.switch_page("pages/2_Register.py")
        with btn_action2:
            if st.button("ĐĂNG NHẬP NGAY", use_container_width=True, key="hero_login"):
                st.switch_page("pages/1_Login.py")
                
    with h_col2:
        st.image("https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=800&q=80", caption="Tối ưu hóa lựa chọn không gian sống", use_container_width=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    # Bài toán & Giải pháp
    st.markdown("<h2 style='text-align: center; font-weight: 800; color: #111827;'>Tại sao bạn cần Hệ thống DSS?</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #4B5563; font-size: 16px; margin-bottom: 40px;'>Tìm nhà là một quyết định tốn kém. Hãy xem sự khác biệt giữa việc phó mặc cho cảm tính và sử dụng thuật toán khoa học.</p>", unsafe_allow_html=True)
    
    vs_col1, vs_col2 = st.columns(2, gap="large")
    with vs_col1:
        st.markdown("""
        <div class="vs-card">
            <div class="vs-title-bad">Lựa chọn theo Bản năng & Cảm tính</div>
            <ul style="color: #4B5563; line-height: 1.8; font-size: 15px;">
                <li><b>Rơi vào "Ma trận" thông tin:</b> Dễ bị ngợp và rối trí khi phải lướt xem hàng chục, hàng trăm tin đăng cho thuê mập mờ trên mạng xã hội.</li>
                <li><b>Bị thao túng bởi hình ảnh:</b> Thường đưa ra quyết định sai lầm do bị hấp dẫn bởi "ảnh mạng" trang trí đẹp mắt, mà bỏ qua các yếu tố cốt lõi như tình trạng ngập nước, an ninh khu vực.</li>
                <li><b>Mâu thuẫn trong nhu cầu:</b> Muốn nhà ở trung tâm nhưng lại muốn giá rẻ, dẫn đến việc đi xem nhà nhiều ngày nhưng không chốt được căn nào.</li>
                <li><b>Rủi ro tài chính cao:</b> Dễ phải bỏ tiền cọc chuyển đi sớm vì phát hiện ra những bất tiện không lường trước (hàng xóm ồn ào, phí quản lý quá cao).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with vs_col2:
        st.markdown("""
        <div class="vs-card">
            <div class="vs-title-good">Lựa chọn bằng Thuật toán AHP</div>
            <ul style="color: #4B5563; line-height: 1.8; font-size: 15px;">
                <li><b>Lượng hóa mọi tiêu chí:</b> Biến các khái niệm mơ hồ thành điểm số cụ thể. Bạn tự định giá xem "An ninh" quan trọng gấp mấy lần "Giá thuê".</li>
                <li><b>Kiểm soát tính logic:</b> Hệ thống có thang đo Chỉ số Nhất quán (CR). Nếu bạn thiết lập ưu tiên mâu thuẫn, thuật toán sẽ lập tức cảnh báo để bạn điều chỉnh lại.</li>
                <li><b>Tối ưu hóa thời gian:</b> Thay vì kẻ bảng Excel so sánh thủ công, bạn chỉ cần nhập điểm, hệ thống sẽ tính toán Vector ưu tiên một cách tự động.</li>
                <li><b>Xuất báo cáo minh bạch:</b> Căn nhà phù hợp nhất với cấu hình của bạn sẽ được xếp hạng cao nhất dựa trên toán học, giúp bạn tự tin ra quyết định.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # ĐỐI TƯỢNG (BẢN CHI TIẾT SÂU SẮC)
    st.markdown("<h2 style='text-align: center; font-weight: 800; color: #111827;'>Hệ thống này dành cho ai?</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #4B5563; font-size: 16px; margin-bottom: 50px;'>Mỗi tệp khách hàng có một định nghĩa riêng về \"Căn hộ hoàn hảo\". Thuật toán AHP linh hoạt đáp ứng mọi lăng kính cá nhân.</p>", unsafe_allow_html=True)
    
    aud_col1, aud_col2, aud_col3 = st.columns(3, gap="medium")
    
    with aud_col1:
        st.markdown("""
        <div class="audience-card">
            <img src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=600&q=80" style="width:100%; height:220px; object-fit:cover;">
            <div class="audience-content">
                <div class="audience-title">Sinh Viên & Người Đi Làm Trẻ</div>
                <div class="audience-desc" style="text-align: justify; margin-top: 10px;">
                    <b style="color:#111827;">Bối cảnh thực tế:</b> Nhóm khách hàng này thường phải đối mặt với bài toán nan giải: Ngân sách thuê nhà bị giới hạn cứng mỗi tháng, nhưng lại đòi hỏi khắt khe về vị trí nhằm tiết kiệm thời gian di chuyển. Sự đánh đổi giữa "nhà rẻ ở xa" và "nhà gần nhưng đắt" luôn gây đau đầu.<br><br>
                    <b style="color:#111827;">Giải pháp từ AHP:</b> Bằng cách điều chỉnh thiết lập ưu tiên giữa <b>"Chi phí thuê"</b> và <b>"Khoảng cách đi lại"</b>, hệ thống sẽ tự động rà soát dữ liệu để tìm ra điểm giao thoa tốt nhất, giúp tối ưu cả tài chính lẫn thời gian.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with aud_col2:
        st.markdown("""
        <div class="audience-card">
            <img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=600&q=80" style="width:100%; height:220px; object-fit:cover;">
            <div class="audience-content">
                <div class="audience-title">Các Gia Đình Trẻ</div>
                <div class="audience-desc" style="text-align: justify; margin-top: 10px;">
                    <b style="color:#111827;">Bối cảnh thực tế:</b> Khi có con nhỏ, ưu tiên chọn nhà thay đổi hoàn toàn. Giá cả không còn là yếu tố độc tôn. Thay vào đó, môi trường sống an toàn, không gian rộng rãi và khoảng cách gần các tiện ích (trường học, bệnh viện) trở thành điều kiện tiên quyết.<br><br>
                    <b style="color:#111827;">Giải pháp từ AHP:</b> Hệ thống đóng vai trò như bộ lọc thông minh. Gia đình có thể thiết lập trọng số tuyệt đối cho tiêu chí <b>"An ninh khu vực"</b> và <b>"Diện tích sử dụng"</b>, tự động loại bỏ những căn hộ không phù hợp.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with aud_col3:
        st.markdown("""
        <div class="audience-card">
            <img src="https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=600&q=80" style="width:100%; height:220px; object-fit:cover;">
            <div class="audience-content">
                <div class="audience-title">Gia Đình Có Điều Kiện</div>
                <div class="audience-desc" style="text-align: justify; margin-top: 10px;">
                    <b style="color:#111827;">Bối cảnh thực tế:</b> Đối với tệp khách hàng có nền tảng tài chính vững chắc, chi phí không phải là rào cản. Điều họ thực sự tìm kiếm là sự nâng tầm phong cách sống, tính riêng tư tuyệt đối, và quỹ thời gian của họ vô cùng eo hẹp nên việc đi xem từng căn nhà là bất khả thi.<br><br>
                    <b style="color:#111827;">Giải pháp từ AHP:</b> Nền tảng DSS giúp cá nhân hóa trải nghiệm ở mức cao nhất. Bằng việc đẩy mạnh trọng số cho <b>"Tiện ích cao cấp"</b> và <b>"Sự riêng tư"</b>, thuật toán khoanh vùng chính xác các căn hộ hạng sang tương xứng với vị thế.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><hr style='border-top: 1px solid #E5E7EB;'><p style='text-align:center; color:#9CA3AF; font-size:14px;'>© 2026 DSS Rental Analytics - Nền Tảng Phân Tích Dữ Liệu Bất Động Sản</p>", unsafe_allow_html=True)

else:
    # --- GIAO DIỆN DASHBOARD (KHI ĐÃ ĐĂNG NHẬP) ---
    st.markdown("<h2 style='font-weight: 700; color: #111827;'>Dashboard Điều Hành</h2>", unsafe_allow_html=True)

    metric_c1, metric_c2, metric_c3 = st.columns(3)
    with metric_c1:
        st.markdown("""<div style='background: white; padding: 20px; border: 1px solid #E5E7EB; border-radius: 8px;'>
            <div style='color: #4B5563; font-size: 14px; font-weight: 600; margin-bottom: 8px;'>Tổng số dữ liệu BĐS</div>
            <div style='font-size: 32px; font-weight: 700; color: #111827;'>1,248</div>
        </div>""", unsafe_allow_html=True)
    with metric_c2:
        st.markdown("""<div style='background: white; padding: 20px; border: 1px solid #E5E7EB; border-radius: 8px;'>
            <div style='color: #4B5563; font-size: 14px; font-weight: 600; margin-bottom: 8px;'>Tài khoản người dùng</div>
            <div style='font-size: 32px; font-weight: 700; color: #111827;'>456</div>
        </div>""", unsafe_allow_html=True)
    with metric_c3:
        st.markdown("""<div style='background: white; padding: 20px; border: 1px solid #E5E7EB; border-radius: 8px;'>
            <div style='color: #4B5563; font-size: 14px; font-weight: 600; margin-bottom: 8px;'>Lượt gọi hàm AHP</div>
            <div style='font-size: 32px; font-weight: 700; color: #111827;'>156</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    dash_btn_col, _ = st.columns([1, 2])
    with dash_btn_col:
        if st.button("MỞ MODULE PHÂN TÍCH AHP", type="primary", use_container_width=True, key="dash_start_ahp"):
            st.switch_page("pages/3_AHP_Input.py")