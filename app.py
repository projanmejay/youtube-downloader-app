import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="YouTube Downloader", page_icon="📥")

st.title("📥 YouTube Video Downloader (1080p Max)")

# Input URL
url = st.text_input("Enter YouTube video URL:")

# Output folder inside app
output_path = "downloads"
os.makedirs(output_path, exist_ok=True)

if st.button("Download Video"):
    if not url:
        st.warning("Please enter a YouTube video URL.")
    else:
        st.info("Downloading and merging video...")
        options = {
            'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
            'merge_output_format': 'mp4',
        }

        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info_dict)
            st.success("✅ Download and merge complete.")
            # Provide download link
            st.download_button(
                label="Download Video",
                data=open(filename, "rb"),
                file_name=os.path.basename(filename),
                mime="video/mp4"
            )
        except Exception as e:
            st.error(f"❌ Error: {e}")
