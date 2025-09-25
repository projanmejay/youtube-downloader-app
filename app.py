import streamlit as st
import yt_dlp
import os

def download_and_merge_video_audio(url, output_path='.'):
    ffmpeg_path = r'C:\Users\hp\Downloads\ffmpeg-2025-07-10-git-82aeee3c19-full_build\ffmpeg-2025-07-10-git-82aeee3c19-full_build\bin'

    options = {
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': False,
        'merge_output_format': 'mp4',
        'ffmpeg_location': ffmpeg_path
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).replace(".webm", ".mp4").replace(".mkv", ".mp4")
        return filename
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return None

# ---------------- Streamlit UI ----------------
st.title("📥 YouTube Video Downloader (1080p max)")
st.write("Download and merge YouTube videos with audio using yt-dlp + ffmpeg")

url = st.text_input("Enter YouTube video URL:")

if st.button("Download"):
    if url:
        st.info("Downloading... please wait ⏳")
        filepath = download_and_merge_video_audio(url)
        if filepath and os.path.exists(filepath):
            st.success("✅ Download complete!")
            with open(filepath, "rb") as f:
                st.download_button(
                    label="⬇️ Download File",
                    data=f,
                    file_name=os.path.basename(filepath),
                    mime="video/mp4"
                )
    else:
        st.warning("⚠️ Please enter a valid URL.")
