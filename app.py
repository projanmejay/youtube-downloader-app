import streamlit as st
import yt_dlp
import os

# Set a title and description for the app
st.set_page_config(page_title="YouTube Video Downloader", layout="centered")
st.title("📥 YouTube Video Downloader")
st.write("Enter a YouTube link to download the video in the best available quality (1080p max).")
st.write("This app uses `yt-dlp` and `ffmpeg` to download and merge video and audio streams.")

# Input field for the YouTube URL
url = st.text_input("🎬 Enter YouTube URL:")

if url:
    if st.button("Download Video"):
        try:
            with st.spinner("Downloading and merging... this may take a moment."):
                # The 'downloads' folder will be created in the temporary directory of the hosted app
                output_path = "downloads"
                os.makedirs(output_path, exist_ok=True)
                
                # Set up the yt-dlp options
                options = {
                    'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'noplaylist': True,
                    'quiet': False,
                    'merge_output_format': 'mp4',
                    'postprocessors': [{
                        'key': 'FFmpegMetadata',
                        'add_metadata': True,
                    }],
                    # Add a User-Agent header to mimic a browser and avoid 403 errors
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
                    },
                    # Add this line to specify a different player client and avoid 403 errors
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['web_embedded', 'web', 'android', 'ios']
                        }
                    }
                }

                with yt_dlp.YoutubeDL(options) as ydl:
                    info_dict = ydl.extract_info(url, download=True)
                    downloaded_file_path = ydl.prepare_filename(info_dict)
                    
                    # Ensure the final file has an mp4 extension for consistency
                    if not downloaded_file_path.endswith('.mp4'):
                        base, ext = os.path.splitext(downloaded_file_path)
                        final_path = base + '.mp4'
                        os.rename(downloaded_file_path, final_path)
                        downloaded_file_path = final_path

            st.success("✅ Download complete!")
            st.write(f"File saved on the server as: `{os.path.basename(downloaded_file_path)}`")
            
            # Create a download button for the user to download the file from the server
            with open(downloaded_file_path, "rb") as file:
                st.download_button(
                    label="⬇️ Click to Download Video",
                    data=file,
                    file_name=os.path.basename(downloaded_file_path),
                    mime="video/mp4"
                )

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
            st.warning("Please ensure the URL is valid.")
