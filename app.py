import streamlit as st
import yt_dlp
import os

st.title("📥 YouTube Video Downloader (1080p Max)")
st.write("Enter a YouTube video link and download it directly in MP4 format.")

# Input URL
url = st.text_input("🎬 Enter YouTube URL:")

def get_available_qualities(url):
    """Fetch available video+audio qualities from YouTube URL"""
    ydl_opts = {
        'noplaylist': True,
        'quiet': True,
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
        },
        'geo_bypass': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])

        # Only keep formats with both video and audio
        qualities = sorted(
            set(f"{f['height']}p" for f in formats if f.get('height') and f.get('vcodec') != 'none' and f.get('acodec') != 'none')
        )
        return qualities, info

if url:
    try:
        qualities, info = get_available_qualities(url)

        if not qualities:
            st.error("❌ No downloadable video formats with both video and audio found.")
        else:
            # Dropdown to select quality
            selected_quality = st.selectbox("🎯 Select video quality:", qualities)

            if st.button("Download"):
                # Prepare output folder
                output_path = "downloads"
                os.makedirs(output_path, exist_ok=True)

                # yt-dlp options for selected quality
                options = {
                    'format': f"best[height={selected_quality.replace('p','')}]",
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'noplaylist': True,
                    'quiet': True,
                    'merge_output_format': None,  # No merging
                    'headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                      '(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
                    },
                    'geo_bypass': True
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
