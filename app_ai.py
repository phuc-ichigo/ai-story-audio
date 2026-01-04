import streamlit as st
import asyncio
import edge_tts
import os
import google.generativeai as genai

# --- CẤU HÌNH API KEY (ĐÃ THAY THẾ) ---
GEMINI_API_KEY = "AIzaSyAJTjyQ6U7mSJwmTncZN_YXAg9pUpsE3SA"

# Khởi tạo Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Cấu hình giao diện Streamlit
st.set_page_config(page_title="AI Story Master", page_icon="🎙️")
st.title("🎙️ Trạm Dịch & Sản Xuất Truyện AI")

# Tạo thư mục outputs nếu chạy local
if not os.path.exists("outputs"):
    os.makedirs("outputs")

# --- PHẦN 1: DỊCH THUẬT THÔNG MINH ---
st.header("1. Nhập văn bản & Dịch mượt")
raw_input = st.text_area("Dán tiếng Trung hoặc văn bản thô (Convert) vào đây:", height=200)

style = st.selectbox("Chọn văn phong muốn dịch:", 
                     ["Tiên hiệp / Kiếm hiệp", "Ngôn tình hiện đại", "Huyền ảo / Kỳ ảo", "Dịch thuật thông thường"])

if st.button("✨ Gemini - Dịch & Làm mượt"):
    if raw_input:
        with st.spinner("Gemini đang biên tập lại văn bản..."):
            try:
                # Prompt tối ưu cho việc dịch truyện
                prompt = f"""
                Bạn là một biên tập viên dịch truyện chuyên nghiệp. 
                Hãy dịch hoặc viết lại đoạn văn bản sau sang tiếng Việt mượt mà theo phong cách {style}.
                Yêu cầu:
                - Văn phong trôi chảy, hấp dẫn, không bị cứng nhắc như dịch máy.
                - Sử dụng từ ngữ phù hợp với bối cảnh truyện (ví dụ: dùng từ Hán Việt cho kiếm hiệp).
                - Giữ nguyên các tên riêng của nhân vật và địa danh.
                Văn bản cần xử lý:
                {raw_input}
                """
                response = model.generate_content(prompt)
                st.session_state['refined_text'] = response.text
                st.success("✅ Đã xử lý xong bản dịch!")
            except Exception as e:
                st.error(f"Lỗi khi gọi Gemini: {e}")
    else:
        st.warning("Vui lòng nhập nội dung cần dịch!")

st.divider()

# --- PHẦN 2: CHUYỂN ĐỔI AUDIO ---
st.header("2. Tạo Audio từ bản dịch")
# Nội dung từ Gemini sẽ tự động điền vào đây
final_text = st.text_area("Văn bản sau khi đã làm mượt (Có thể chỉnh sửa):", 
                          value=st.session_state.get('refined_text', ""), 
                          height=200)

voice = st.selectbox("Chọn giọng đọc:", ["vi-VN-HoaiNinhNeural (Nam)", "vi-VN-NamMinhNeural (Nữ)"])

if st.button("🚀 Phát Audio & Tải về"):
    if final_text:
        async def generate_audio():
            v = voice.split(" ")[0]
            communicate = edge_tts.Communicate(final_text, v)
            audio_data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            return audio_data

        with st.spinner("Đang chuyển đổi giọng nói..."):
            try:
                data = asyncio.run(generate_audio())
                st.audio(data, format='audio/mp3')
                st.download_button("📥 Tải file MP3 về máy", data, file_name="truyen_thanh_pham.mp3")
            except Exception as e:
                st.error(f"Lỗi khi tạo Audio: {e}")
    else:
        st.warning("Chưa có nội dung để đọc!")