import streamlit as st
import asyncio
import edge_tts
import os

# Cấu hình giao diện
st.set_page_config(page_title="AI Voice Cá Nhân", page_icon="🎙️")
st.title("🎙️ Trạm Sản Xuất Audio Cá Nhân")

# Tạo thư mục outputs để tránh lỗi nếu bạn chạy ở máy local
if not os.path.exists("outputs"):
    os.makedirs("outputs")

# Sidebar - Lịch sử (Chỉ hiện nếu có file)
st.sidebar.header("📜 Lịch sử tạo file")
files = [f for f in os.listdir("outputs") if f.endswith(".mp3")]
for f in files[-5:]: 
    st.sidebar.audio(f"outputs/{f}")

# Khu vực chính
text = st.text_area("Nhập kịch bản truyện của bạn:", height=250)
voice = st.selectbox("Chọn giọng đọc:", ["vi-VN-HoaiNinhNeural (Nam)", "vi-VN-NamMinhNeural (Nữ)"])

if st.button("🚀 Bắt đầu chuyển đổi"):
    if text:
        async def generate_audio_direct():
            v = voice.split(" ")[0]
            communicate = edge_tts.Communicate(text, v)
            audio_data = b""
            # Lấy dữ liệu âm thanh trực tiếp
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            return audio_data

        with st.spinner("Đang xử lý âm thanh..."):
            try:
                # Chạy và lấy dữ liệu byte audio
                data = asyncio.run(generate_audio_direct())
                
                if data:
                    # Phát trực tiếp trên trình duyệt (Sửa lỗi NoAudioReceived)
                    st.audio(data, format='audio/mp3')
                    
                    # Nút tải về cho người dùng
                    st.download_button(
                        label="📥 Tải file MP3 về máy",
                        data=data,
                        file_name="ai_audio.mp3",
                        mime="audio/mp3"
                    )
                    st.success("Đã tạo xong!")
                else:
                    st.error("Không nhận được dữ liệu từ máy chủ AI.")
            except Exception as e:
                st.error(f"Lỗi kết nối: {e}")
    else:
        st.warning("Bạn chưa nhập nội dung kìa!")