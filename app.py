import streamlit as st
import yt_dlp
import os

st.title("📥 YouTube Video Downloader (1080p Max)")
st.write("Enter a YouTube video link and download it with merged audio/video (single MP4).")

url = st.text_input("🎬 Enter YouTube URL:")

if url:
    if st.button("Download"):
        try:
            # Save in a temporary folder
            output_path = "downloads"
            os.makedirs(output_path, exist_ok=True)

            options = {
                'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'merge_output_format': 'mp4',   # ensures single combined MP4
            }

            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info).replace(".webm", ".mp4")

            st.success("✅ Download complete! Your video is ready.")

            # Provide a single file download
            with open(filename, "rb") as file:
                st.download_button(
                    label="⬇️ Download Video",
                    data=file,
                    file_name=os.path.basename(filename),
                    mime="video/mp4"
                )

        except Exception as e:
            st.error(f"❌ Error: {e}")
