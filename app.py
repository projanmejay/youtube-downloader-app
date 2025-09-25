import streamlit as st
import yt_dlp
import os

def download_and_merge_video_audio(url, resolution="1080", output_path="."):
    # yt-dlp format string based on chosen resolution
    format_str = f"bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]"

    options = {
        'format': format_str,
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': False,
        'merge_output_format': 'mp4'
        # no ffmpeg_location needed if ffmpeg is in PATH
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            # normalize extension to mp4
            filename = filename.replace(".webm", ".mp4").replace(".mkv", ".mp4")
        return filename
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return None


# ---------------- Streamlit UI ----------------
st.title("📥 YouTube Video Downloader")
st.write("Download and merge YouTube videos with audio using yt-dlp + ffmpeg")

url = st.text_input("Enter YouTube video URL:")

resolution = st.selectbox(
    "Choose maximum resolution:",
    ["360", "480", "720", "1080"],
    index=3
)

if st.button("Download"):
    if url:
        st.info("Downloading... please wait ⏳")
        filepath = download_and_merge_video_audio(url, resolution)
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
