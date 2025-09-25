import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="YouTube Downloader", page_icon="📥")
st.title("📥 YouTube Video Downloader (1080p Max)")

# Output folder
output_path = "downloads"
os.makedirs(output_path, exist_ok=True)

# YouTube URL input
url = st.text_input("Enter YouTube video URL:")

# Optional cookies for age-restricted videos
cookie_file = st.file_uploader("Optional: Upload cookies.txt (for age-restricted videos)", type=["txt"])

if st.button("Download Video"):
    if not url:
        st.warning("Please enter a YouTube video URL.")
    else:
        st.info("Downloading and merging video... This may take a few moments.")
        
        options = {
            'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
            'merge_output_format': 'mp4',
            'nocheckcertificate': True,
            'http_headers': {
                'User-Agent': (
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/120.0.0.0 Safari/537.36'
                )
            },
        }

        # Save cookies if uploaded
        if cookie_file:
            cookie_path = os.path.join(output_path, "cookies.txt")
            with open(cookie_path, "wb") as f:
                f.write(cookie_file.getbuffer())
            options['cookiefile'] = cookie_path

        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info_dict)
            
            st.success("✅ Download and merge complete!")

            # Download button
            st.download_button(
                label="Download Video",
                data=open(filename, "rb"),
                file_name=os.path.basename(filename),
                mime="video/mp4"
            )

        except yt_dlp.utils.DownloadError as e:
            st.error(f"❌ Download error (403 Forbidden likely): {e}\n\n"
                     "Try uploading cookies.txt from your logged-in YouTube account.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
