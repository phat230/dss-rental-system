import streamlit as st

# --- 1. THIẾT LẬP CẤU HÌNH TRANG ---
st.set_page_config(page_title="Hệ Thống Thẩm Định Thuê Trọ", layout="wide", initial_sidebar_state="expanded")

# --- 2. CSS TÙY CHỈNH (ENTERPRISE LONG-FORM NO-ICON) ---
st.markdown("""
    <style>
    /* Tổng thể */
    .main { background-color: #f8fafc; font-family: 'Inter', 'Segoe UI', sans-serif; }
    h1, h2, h3, h4 { color: #0f172a !important; font-weight: 800 !important; letter-spacing: -0.02em; }
    p { color: #475569; line-height: 1.7; font-size: 1.05rem; }
    
    .block-container { max-width: 1280px; padding-top: 3rem !important; padding-bottom: 0rem !important; }
    
    .text-highlight { color: #3b82f6; font-weight: 800; }
    
    /* Box Thống kê (Stat Box) */
    .stat-box {
        background-color: #1e293b; color: white; padding: 3.5rem 2rem; border-radius: 12px;
        text-align: center; margin: 2rem 0 4rem 0; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
    }
    .stat-number { font-size: 4rem; font-weight: 900; color: #60a5fa; margin-bottom: 0.5rem; line-height: 1; }
    .stat-text { font-size: 1.15rem; color: #cbd5e1; max-width: 800px; margin: 0 auto; line-height: 1.6; }

    /* Thẻ Vấn Đề (Problem Cards) */
    .problem-card {
        background-color: #ffffff; border-radius: 12px; overflow: hidden;
        border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease; height: 100%;
    }
    .problem-card:hover { transform: translateY(-5px); box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); }
    .img-container { width: 100%; height: 200px; overflow: hidden; }
    .img-container img { width: 100%; height: 100%; object-fit: cover; }
    .card-content { padding: 1.5rem; }
    .card-title { font-weight: 700; color: #0f172a; font-size: 1.15rem; margin-bottom: 0.5rem; }
    .card-desc { font-size: 0.95rem; color: #64748b; line-height: 1.5; }
    
    /* Khối Chi Phí Chìm (Sunk Cost) */
    .sunk-cost-section {
        background-color: #fef2f2; border: 1px solid #fecaca; padding: 3rem; border-radius: 12px; margin: 4rem 0;
    }
    .sunk-cost-title { color: #991b1b; font-size: 1.8rem; font-weight: 800; margin-bottom: 1.5rem; text-align: center;}
    .sunk-cost-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; margin-top: 2rem; }
    .sunk-item { border-top: 3px solid #dc2626; padding-top: 1rem; }
    .sunk-item-title { font-weight: 700; color: #7f1d1d; font-size: 1.1rem; margin-bottom: 0.5rem; }
    
    /* Khối Iceberg (Tảng băng chìm) */
    .iceberg-section {
        background-color: #ffffff; padding: 4rem; border-radius: 12px; border: 1px solid #e2e8f0;
        margin: 4rem 0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
    }
    .iceberg-visible { border-left: 4px solid #3b82f6; padding-left: 1.5rem; margin-bottom: 2rem; }
    .iceberg-hidden { border-left: 4px solid #ef4444; padding-left: 1.5rem; }

    /* Bảng So Sánh (Comparison Table) */
    .compare-section { margin: 4rem 0; }
    .compare-table { width: 100%; border-collapse: collapse; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; }
    .compare-table th { background-color: #0f172a; color: #ffffff; padding: 1.2rem; text-align: left; font-size: 1.05rem; }
    .compare-table td { padding: 1.2rem; border-bottom: 1px solid #e2e8f0; color: #475569; font-size: 0.95rem; line-height: 1.6; }
    .compare-table tr:last-child td { border-bottom: none; }
    .compare-table td:first-child { font-weight: 700; color: #0f172a; width: 25%; background-color: #f8fafc; border-right: 1px solid #e2e8f0;}
    .compare-table td:nth-child(2) { width: 37.5%; border-right: 1px dashed #cbd5e1; }
    .compare-table td:nth-child(3) { width: 37.5%; background-color: #f0fdf4; color: #166534; font-weight: 500;}

    /* Khối Tính Năng (Features) */
    .feature-box {
        background-color: #ffffff; padding: 2.5rem 2rem; border-radius: 12px; border: 1px solid #e2e8f0;
        text-align: left; height: 100%; box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        border-top: 4px solid #0f172a;
    }
    .feature-box h4 { font-size: 1.15rem; margin-bottom: 1rem; color: #0f172a; text-transform: uppercase; letter-spacing: 0.5px;}
    .feature-box p { font-size: 0.95rem; color: #64748b; margin: 0;}

    /* Khối Đối tượng (Audience) */
    .audience-section { background-color: #f1f5f9; padding: 4rem 2rem; border-radius: 12px; margin: 4rem 0; }
    .audience-card { border-left: 4px solid #3b82f6; padding-left: 1.5rem; margin-bottom: 1.5rem; }
    .audience-title { color: #0f172a; font-weight: 800; font-size: 1.1rem; text-transform: uppercase; margin-bottom: 0.5rem; letter-spacing: 0.5px;}

    /* Khối Step */
    .step-box { 
        background-color: #ffffff; padding: 1.5rem; border-radius: 8px; 
        border-left: 4px solid #1e293b; margin-bottom: 1.2rem;
        border-top: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0;
    }
    .step-num { font-weight: 800; color: #0f172a; font-size: 0.95rem; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 0.5px;}
    
    /* Khối CTA Premium */
    .cta-premium-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 3rem 2.5rem; border-radius: 12px; box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.4);
        display: flex; flex-direction: column; justify-content: center; height: calc(100% - 1.5rem); border: 1px solid #334155;
    }
    .cta-premium-card h4 { color: #ffffff !important; font-size: 1.4rem; font-weight: 800; margin-bottom: 15px; line-height: 1.4;}
    .cta-premium-card p { color: #94a3b8; font-size: 1rem; line-height: 1.6; margin-bottom: 2.5rem; }
    .cta-premium-btn {
        background-color: #3b82f6; color: #ffffff !important; padding: 1.1rem 1.5rem; border-radius: 6px;
        font-weight: 700; font-size: 1rem; text-align: center; text-decoration: none !important;
        transition: all 0.3s ease; display: block; letter-spacing: 0.5px;
    }
    .cta-premium-btn:hover { background-color: #2563eb; transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.4); }
    
    /* Footer */
    .footer { text-align: center; padding: 3rem 0; margin-top: 5rem; border-top: 1px solid #e2e8f0; color: #94a3b8; font-size: 0.9rem; }
    </style>
""", unsafe_allow_html=True)

# --- 3. HERO SECTION (GIỚI THIỆU TỔNG QUAN) ---
col_text, col_img = st.columns([1.2, 1], gap="large")

with col_text:
    st.markdown("<h1 style='font-size: 3.2rem; margin-bottom: 1.2rem; line-height: 1.15;'>TÌM KHÔNG GIAN SỐNG <br><span class='text-highlight'>BẰNG DỮ LIỆU TOÁN HỌC</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.15rem; margin-bottom: 2rem;'>Việc lựa chọn một căn hộ hay phòng trọ không đơn thuần là nhìn vào giá cả. Đó là sự đánh đổi phức tạp giữa hàng loạt tiêu chí: Khoảng cách đi làm, mức độ an ninh, chi phí sinh hoạt và sự tự do cá nhân.</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.05rem; font-weight: 600; color: #0f172a; border-left: 4px solid #3b82f6; padding-left: 15px;'>Ứng dụng hệ thống phân tích đa tiêu chí AHP để tìm ra phương án tối ưu nhất, hoàn toàn tự động và khách quan.</p>", unsafe_allow_html=True)

with col_img:
    st.image("https://images.unsplash.com/photo-1560518883-ce09059eeffa?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", use_container_width=True)

# --- 4. SỰ THẬT CẢNH TỈNH (THE HOOK) ---
st.markdown("""
    <div class="stat-box">
        <div class="stat-number">70%</div>
        <div class="stat-text">Người đi thuê nhà thừa nhận họ cảm thấy hối hận hoặc muốn chuyển đi chỉ sau 3 tháng đầu tiên vì những rắc rối không lường trước được trong quá trình khảo sát cảm tính.</div>
    </div>
""", unsafe_allow_html=True)

# --- 5. CÁC THÁCH THỨC THỰC TẾ (PROBLEM CARDS) ---
st.markdown("<h2 style='text-align: center; margin-bottom: 1rem; font-size: 2.2rem;'>NGUYÊN NHÂN CỦA NHỮNG QUYẾT ĐỊNH SAI LẦM</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-bottom: 3rem; max-width: 800px; margin-left: auto; margin-right: auto;'>Đứng trước quá nhiều lựa chọn, bộ não con người dễ bị quá tải thông tin. Chúng ta thường bị đánh lừa bởi bề ngoài mà quên đi các yếu tố cốt lõi mang tính quyết định.</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
        <div class="problem-card">
            <div class="img-container">
                <img src="https://images.unsplash.com/photo-1554224155-6726b3ff858f?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" alt="Budget">
            </div>
            <div class="card-content">
                <div class="card-title">Cạm Bẫy Giá Rẻ</div>
                <div class="card-desc">Một căn phòng giá rẻ bất ngờ thường đi kèm với phí dịch vụ cao, điện nước bị tính giá kinh doanh, hoặc nằm ở khu vực thường xuyên ngập lụt.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="problem-card">
            <div class="img-container">
                <img src="https://images.unsplash.com/photo-1524661135-423995f22d0b?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" alt="Location">
            </div>
            <div class="card-content">
                <div class="card-title">Ảo Tưởng Khoảng Cách</div>
                <div class="card-desc">"Chỉ 15 phút đến trung tâm" trên bản đồ có thể biến thành 45 phút kẹt xe khói bụi vào giờ cao điểm, bòn rút năng lượng làm việc mỗi ngày.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="problem-card">
            <div class="img-container">
                <img src="https://images.unsplash.com/photo-1558002038-1055907df827?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" alt="Security">
            </div>
            <div class="card-content">
                <div class="card-title">Bỏ Qua Yếu Tố Chìm</div>
                <div class="card-desc">Chủ nhà khó tính, hàng xóm ồn ào, bãi xe chật chội hay an ninh kém là những thứ bạn hiếm khi nhận ra ngay trong lần đầu đi xem phòng.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- 6. PHÂN TÍCH CHI PHÍ CHÌM (SUNK COSTS) - NỘI DUNG MỚI ---
st.markdown("""
    <div class="sunk-cost-section">
        <div class="sunk-cost-title">CÁI GIÁ PHẢI TRẢ KHI CHỌN SAI PHƯƠNG ÁN</div>
        <p style="text-align: center; color: #7f1d1d; margin-bottom: 2rem;">Một quyết định vội vàng không chỉ ảnh hưởng đến trải nghiệm sống mà còn gây ra những thiệt hại nặng nề về mặt tài chính và thời gian.</p>
        <div class="sunk-cost-grid">
            <div class="sunk-item">
                <div class="sunk-item-title">Mất Trắng Tiền Cọc</div>
                <p style="font-size: 0.95rem; color: #991b1b; margin: 0;">Chuyển đi trước thời hạn hợp đồng đồng nghĩa với việc bạn sẽ mất hoàn toàn 1 đến 2 tháng tiền cọc nhà ban đầu.</p>
            </div>
            <div class="sunk-item">
                <div class="sunk-item-title">Chi Phí Vận Chuyển</div>
                <p style="font-size: 0.95rem; color: #991b1b; margin: 0;">Thuê xe tải, đóng gói đồ đạc, hư hỏng tài sản trong quá trình chuyển trọ liên tục tiêu tốn một khoản ngân sách không hề nhỏ.</p>
            </div>
            <div class="sunk-item">
                <div class="sunk-item-title">Khủng Hoảng Thời Gian</div>
                <p style="font-size: 0.95rem; color: #991b1b; margin: 0;">Bạn sẽ phải lặp lại vòng lặp mệt mỏi: Lên mạng tìm phòng, gọi điện, sắp xếp thời gian đi xem nhà vào những ngày cuối tuần quý giá.</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 7. NGUYÊN LÝ TẢNG BĂNG CHÌM (THE ICEBERG CONCEPT) ---
st.markdown("<div class='iceberg-section'>", unsafe_allow_html=True)
col_ice_text, col_ice_img = st.columns([1, 1], gap="large")

with col_ice_text:
    st.markdown("<h3 style='font-size: 1.8rem; margin-bottom: 1.5rem; color: #0f172a;'>NGUYÊN LÝ TẢNG BĂNG CHÌM KHI THUÊ NHÀ</h3>", unsafe_allow_html=True)
    st.markdown("<p style='margin-bottom: 2rem;'>Hầu hết mọi người chỉ so sánh các phương án dựa trên <b>Phần bề nổi</b>, dẫn đến sự thiếu toàn diện trong khâu phân tích.</p>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class='iceberg-visible'>
            <h4 style='color: #3b82f6; font-size: 1.1rem; margin-bottom: 5px; text-transform: uppercase;'>Bề Nổi Dễ Thấy (20%)</h4>
            <p style='font-size: 0.95rem; margin: 0; color: #475569;'>Giá thuê hàng tháng, biểu giá điện nước, diện tích sàn thực tế, và danh sách nội thất cơ bản đi kèm.</p>
        </div>
        <div class='iceberg-hidden'>
            <h4 style='color: #ef4444; font-size: 1.1rem; margin-bottom: 5px; text-transform: uppercase;'>Bề Chìm Cốt Lõi (80%)</h4>
            <p style='font-size: 0.95rem; margin: 0; color: #475569;'>Chi phí cơ hội của thời gian kẹt xe, tổn hao sức khỏe do môi trường ô nhiễm tiếng ồn, rủi ro mất cắp tài sản và sự ràng buộc về giờ giấc sinh hoạt.</p>
        </div>
    """, unsafe_allow_html=True)

with col_ice_img:
    st.image("https://images.unsplash.com/photo-1559128010-7c1ad6e1b6a5?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- 8. BẢNG SO SÁNH PHƯƠNG PHÁP (COMPARISON TABLE) ---
st.markdown("<h2 style='text-align: center; margin-bottom: 1rem; font-size: 2.2rem;'>TẠI SAO CẦN MỘT HỆ THỐNG PHÂN TÍCH?</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-bottom: 3rem; max-width: 800px; margin-left: auto; margin-right: auto;'>Bảng đối chiếu sự khác biệt cốt lõi giữa việc tự quyết định dựa trên cảm giác và việc áp dụng mô hình toán học AHP.</p>", unsafe_allow_html=True)

st.markdown("""
<div class="compare-section">
<table class="compare-table">
<thead>
<tr>
<th>Tiêu chí đánh giá</th>
<th>Phương pháp truyền thống (Cảm tính)</th>
<th>Hệ thống AHP Analytics (Dữ liệu)</th>
</tr>
</thead>
<tbody>
<tr>
<td>Cơ sở ra quyết định</td>
<td>Dựa vào ấn tượng ban đầu, trí nhớ ngắn hạn hoặc đánh giá chủ quan bằng mắt thường.</td>
<td>Sử dụng ma trận so sánh cặp kết hợp thuật toán phân cấp để lượng hóa mọi ưu khuyết điểm.</td>
</tr>
<tr>
<td>Xử lý mâu thuẫn</td>
<td>Thường xuyên bỏ qua các điểm mâu thuẫn do não bộ không thể xử lý cùng lúc nhiều biến số.</td>
<td>Tích hợp chỉ số Consistency Ratio (CR) để tự động cảnh báo và ép buộc tư duy logic.</td>
</tr>
<tr>
<td>Đánh giá trọng số</td>
<td>Đồng nhất mọi tiêu chí (Giá cả) dẫn đến việc cộng điểm sai lệch.</td>
<td>Cho phép phân bổ trọng số ưu tiên chính xác theo tỷ lệ phần trăm (Tùy biến).</td>
</tr>
<tr>
<td>Kết quả đầu ra</td>
<td>Một quyết định mang tính "hên xui", tiềm ẩn rủi ro phải thay đổi trong tương lai.</td>
<td>Bảng xếp hạng minh bạch với tỷ lệ phù hợp chính xác đến từng số thập phân.</td>
</tr>
</tbody>
</table>
</div>
""", unsafe_allow_html=True)

# --- 9. GIẢI PHÁP TỪ CHUYÊN GIA (AHP FEATURES) ---
st.markdown("<div style='margin-top: 5rem;'></div>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; margin-bottom: 1rem; font-size: 2.2rem;'>GIẢI PHÁP TỪ CHUYÊN GIA: <span class='text-highlight'>AHP ANALYTICS</span></h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-bottom: 3rem; max-width: 800px; margin-left: auto; margin-right: auto;'>Quy trình phân tích phân cấp (Analytic Hierarchy Process) là thuật toán ra quyết định được cấu trúc hóa, nay được tùy biến để giải quyết bài toán của chính bạn.</p>", unsafe_allow_html=True)

col_f1, col_f2, col_f3 = st.columns(3, gap="large")
with col_f1:
    st.markdown("""
        <div class='feature-box'>
            <h4>I. Phân Bổ Trọng Số Tùy Chỉnh</h4>
            <p>Mỗi cá nhân có một thước đo giá trị riêng. Hệ thống cho phép bạn tự thiết lập sự ưu tiên tương đối: Đối với bạn, Vị trí quan trọng gấp mấy lần so với Tiện ích đi kèm?</p>
        </div>
    """, unsafe_allow_html=True)
with col_f2:
    st.markdown("""
        <div class='feature-box'>
            <h4>II. Kiểm Định Tính Nhất Quán</h4>
            <p>Thuật toán tích hợp bộ lọc Consistency Ratio (CR). Hệ thống sẽ tự động đối chiếu chéo các câu trả lời và từ chối những lập luận mang tính chất mâu thuẫn, phi logic.</p>
        </div>
    """, unsafe_allow_html=True)
with col_f3:
    st.markdown("""
        <div class='feature-box'>
            <h4>III. Xếp Hạng Kết Quả Tự Động</h4>
            <p>Loại bỏ các bảng tính Excel thủ công dễ sai sót. Sau khi hoàn tất đối chiếu, hệ thống sử dụng phép nhân ma trận đa hướng để xuất ra tỷ lệ phần trăm ưu việt cho từng phương án.</p>
        </div>
    """, unsafe_allow_html=True)

# --- 10. ĐỐI TƯỢNG SỬ DỤNG (PERSONAS) ---
st.markdown("""
    <div class='audience-section'>
        <h2 style='text-align: center; margin-bottom: 3rem; font-size: 2rem;'>HỆ THỐNG NÀY ĐƯỢC THIẾT KẾ CHO AI?</h2>
        <div style='display: flex; flex-wrap: wrap; justify-content: space-between; gap: 2rem;'>
            <div style='flex: 1; min-width: 250px;'>
                <div class='audience-card'>
                    <div class='audience-title'>Nhóm Sinh Viên & Người Trẻ</div>
                    <p style='font-size: 0.95rem; color: #475569; margin-top: 5px;'>Tập trung phân tích sự cân bằng giữa ngân sách eo hẹp và khoảng cách di chuyển đến trường học. Ưu tiên sự linh hoạt và chi phí sinh hoạt thấp.</p>
                </div>
            </div>
            <div style='flex: 1; min-width: 250px;'>
                <div class='audience-card'>
                    <div class='audience-title'>Nhóm Chuyên Gia & Khối Văn Phòng</div>
                    <p style='font-size: 0.95rem; color: #475569; margin-top: 5px;'>Tập trung phân tích các phương án tối ưu hóa thời gian di chuyển, yêu cầu bãi đỗ xe an toàn và không gian cách âm tốt để phục hồi năng lượng.</p>
                </div>
            </div>
            <div style='flex: 1; min-width: 250px;'>
                <div class='audience-card'>
                    <div class='audience-title'>Nhóm Gia Đình Trẻ</div>
                    <p style='font-size: 0.95rem; color: #475569; margin-top: 5px;'>Đưa các yếu tố về An ninh khu vực, diện tích sử dụng rộng rãi và chất lượng môi trường xung quanh lên làm trọng số quyết định cao nhất.</p>
                </div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 11. CÂU HỎI THƯỜNG GẶP (FAQ SECTION) ---
st.markdown("<h2 style='text-align: center; margin-bottom: 2rem; font-size: 2.2rem;'>GIẢI ĐÁP CƠ CHẾ VẬN HÀNH</h2>", unsafe_allow_html=True)

faq_col1, faq_col2, faq_col3 = st.columns([1, 4, 1])
with faq_col2:
    with st.expander("Sự khác biệt giữa việc dùng AHP và chấm điểm thủ công?"):
        st.write("Chấm điểm thủ công thường dẫn đến việc gán điểm đồng đều một cách cảm tính. Thuật toán AHP bắt buộc bạn phải sử dụng ma trận so sánh từng cặp (Pairwise Comparison). Quá trình này ép buộc người dùng phải định lượng hóa mức độ ưu tiên giữa biến A và biến B một cách cực kỳ khắt khe, từ đó loại bỏ tối đa sự thiên vị.")
    
    with st.expander("Số lượng phương án tối ưu nên đưa vào hệ thống?"):
        st.write("Dựa trên giới hạn nhận thức của não bộ trong việc so sánh chéo, hệ thống khuyến nghị bạn chỉ nên nhập từ 3 đến tối đa 5 phương án đã qua chọn lọc sơ bộ. Vượt quá con số này, ma trận sẽ mở rộng theo cấp số nhân, làm tăng độ phức tạp và dễ gây ra sai số logic.")
        
    with st.expander("Chỉ số Nhất quán (Consistency Ratio - CR) cảnh báo điều gì?"):
        st.write("CR là thước đo tính logic trong suy luận của bạn. Ví dụ: Nếu bạn khẳng định A quan trọng hơn B, và B quan trọng hơn C, nhưng lại đánh giá C quan trọng hơn A, hệ thống sẽ phát hiện vòng lặp mâu thuẫn này. Nếu chỉ số CR > 0.1, hệ thống sẽ từ chối kết quả và yêu cầu điều chỉnh lại ma trận.")

st.markdown("<hr style='border-top: 1px solid #e2e8f0; margin: 4rem 0;'>", unsafe_allow_html=True)

# --- 12. LỘ TRÌNH VÀ ĐIỀU HƯỚNG CUỐI CÙNG ---
st.markdown("<h2 style='text-align: center; margin-bottom: 3rem; font-size: 2.2rem;'>KHỞI TẠO TIẾN TRÌNH PHÂN TÍCH</h2>", unsafe_allow_html=True)
col_sol_text, col_sol_action = st.columns([1.5, 1], gap="large")

with col_sol_text:
    st.markdown("""
        <div class='step-box'>
            <div class='step-num'>BƯỚC 1: THIẾT LẬP MA TRẬN TIÊU CHÍ</div>
            <div style='color: #475569; font-size: 0.95rem;'>Chấm điểm mức độ tương quan giữa Giá thuê, Vị trí, Diện tích, An ninh, Tiện ích và Tự do sinh hoạt.</div>
        </div>
        <div class='step-box'>
            <div class='step-num'>BƯỚC 2: KIỂM ĐỊNH NĂNG LỰC PHƯƠNG ÁN</div>
            <div style='color: #475569; font-size: 0.95rem;'>Nhập danh sách các bất động sản mục tiêu và tiến hành so sánh đối chiếu trên từng hệ quy chiếu riêng biệt.</div>
        </div>
        <div class='step-box'>
            <div class='step-num'>BƯỚC 3: KẾT XUẤT BÁO CÁO TỔNG HỢP</div>
            <div style='color: #475569; font-size: 0.95rem;'>Hệ thống tổng hợp cấu trúc dữ liệu, xử lý thuật toán và kết xuất chính xác phương án đầu tư tối ưu nhất.</div>
        </div>
    """, unsafe_allow_html=True)

with col_sol_action:
    # Khối CTA Premium dẫn link hoàn toàn không có icon
    st.markdown("""
        <div class="cta-premium-card">
            <h4>Xác định giá trị thực</h4>
            <p>Hệ thống dữ liệu số đã sẵn sàng. Hãy bắt đầu quá trình lượng hóa các lựa chọn của bạn để đưa ra một quyết định an toàn và chính xác.</p>
            <a href="AHP_Input" target="_self" class="cta-premium-btn">BẮT ĐẦU THIẾT LẬP AHP</a>
        </div>
    """, unsafe_allow_html=True)

# --- 13. FOOTER ---
st.markdown("""
    <div class="footer">
        <div style="font-weight: 700; color: #64748b;">HỆ THỐNG PHÂN TÍCH ĐA TIÊU CHÍ © 2024</div>
        <div style="margin-top: 8px; color: #94a3b8;">Cốt lõi vận hành dựa trên nền tảng thuật toán Analytic Hierarchy Process.</div>
        <div style="margin-top: 4px; color: #94a3b8;">Nghiêm ngặt, khách quan và hoàn toàn minh bạch bằng dữ liệu số.</div>
    </div>
""", unsafe_allow_html=True)