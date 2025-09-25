import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="YouTube Downloader", page_icon="📥")
st.title("📥 YouTube Video Downloader (1080p Max, No FFmpeg Required)")

# Folder for downloads
output_path = "downloads"
os.makedirs(output_path, exist_ok=True)

# Input URL
url = st.text_input("Enter YouTube video URL:")

# Button to start download
if st.button("Download Video"):
    if not url:
        st.warning("Please enter a YouTube video URL.")
    else:
        st.info("Downloading video... This may take a few moments.")

        # yt_dlp options
        options = {
            'format': 'best[height<=1080]+bestaudio/best',  # progressive download when possible
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
            'nocheckcertificate': True,
            'merge_output_format': 'mp4',  # only used if merging needed
            'http_headers': {
                'User-Agent': (
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/120.0.0.0 Safari/537.36'
                )
            }
        }

        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info_dict)

            st.success("✅ Download complete!")

            # Provide download button
            st.download_button(
                label="Download Video",
                data=open(filename, "rb"),
                file_name=os.path.basename(filename),
                mime="video/mp4"
            )

        except Exception as e:
            st.error(f"❌ Error: {e}\nThis usually happens if the video is age-restricted or blocked.")
