import streamlit as st
import yt_dlp
import os

st.title("📥 YouTube Video Downloader (1080p Max)")
st.write("Enter a YouTube video link and download it with merged audio/video (single MP4).")

# Input URL
url = st.text_input("🎬 Enter YouTube URL:")

def get_available_qualities(url):
    """Fetch available video qualities from YouTube URL"""
    with yt_dlp.YoutubeDL({'noplaylist': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])
        # Get unique video qualities with video+audio available
        qualities = sorted(set(f"{f['height']}p" for f in formats if f.get('height') and f.get('acodec') != 'none'))
        return qualities, info

if url:
    try:
        qualities, info = get_available_qualities(url)

        if not qualities:
            st.error("❌ No downloadable video formats found.")
        else:
            # Dropdown to select quality
            selected_quality = st.selectbox("🎯 Select video quality:", qualities)

            if st.button("Download"):
                # Prepare output folder
                output_path = "downloads"
                os.makedirs(output_path, exist_ok=True)

                # yt-dlp options for selected quality (merging removed)
                options = {
                    'format': f"best[height={selected_quality.replace('p','')}]",
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'noplaylist': True,
                }

                with yt_dlp.YoutubeDL(options) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)

                st.success("✅ Download complete!")

                # Provide file download
                with open(filename, "rb") as file:
                    st.download_button(
                        label="⬇️ Download Video",
                        data=file,
                        file_name=os.path.basename(filename),
                        mime="video/mp4"
                    )

    except Exception as e:
        st.error(f"❌ Error: {e}")
