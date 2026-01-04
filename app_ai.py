import streamlit as st
import asyncio
import edge_tts
import pandas as pd
from datetime import datetime
import os

# Cấu hình giao diện
st.set_page_config(page_title="AI Voice Cá Nhân", page_icon="🎙️")
st.title("🎙️ Trạm Sản Xuất Audio Cá Nhân")

# Tạo thư mục lưu trữ nếu chưa có
if not os.path.exists("outputs"):
    os.makedirs("outputs")

# Sidebar - Lịch sử tạo file
st.sidebar.header("📜 Lịch sử tạo file")
files = os.listdir("outputs")
for f in files[-5:]: # Hiện 5 file gần nhất
    st.sidebar.audio(f"outputs/{f}")

# Khu vực chính
text = st.text_area("Nhập kịch bản truyện của bạn:", height=250)
voice = st.selectbox("Chọn giọng đọc:", ["vi-VN-HoaiNinhNeural (Nam)", "vi-VN-NamMinhNeural (Nữ)"])

if st.button("🚀 Bắt đầu chuyển đổi"):
    if text:
        # Đặt tên file đơn giản để kiểm tra
        filename = f"outputs/test_audio.mp3"
        
        async def generate():
            v = voice.split(" ")[0]
            # Thêm rate và volume để ổn định đường truyền
            communicate = edge_tts.Communicate(text, v, rate="+0%", volume="+0%")
            await communicate.save(filename)
        
        with st.spinner("Đang " + ("ông Ninh" if "HoaiNinh" in voice else "bà Minh") + " đọc truyện..."):
            asyncio.run(generate())
            st.audio(filename)
            st.success(f"Đã tạo xong file tại: {filename}")
    else:
        st.warning("Bạn chưa nhập nội dung kìa!")