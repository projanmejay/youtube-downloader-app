import streamlit as st
import yt_dlp
import os

# Set a title and description for the app
st.title("📥 YouTube Video Downloader")
st.write("Enter a YouTube link to download the video in the best available quality (1080p max).")

# Input field for the YouTube URL
url = st.text_input("🎬 Enter YouTube URL:")

# Create a variable to hold the FFmpeg path. Note: This path is specific to your local machine.
# For a production app, you would need to have FFmpeg installed on the server and ensure it's in the PATH.
ffmpeg_path = r'C:\Users\hp\Downloads\ffmpeg-2025-07-10-git-82aeee3c19-full_build\ffmpeg-2025-07-10-git-82aeee3c19-full_build\bin'

if url:
    if st.button("Download Video"):
        try:
            with st.spinner("Downloading and merging... this may take a moment."):
                # The 'downloads' folder will be created in the directory where the app is run
                output_path = "downloads"
                os.makedirs(output_path, exist_ok=True)
                
                # Set up the yt-dlp options, including your FFmpeg path
                options = {
                    'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'noplaylist': True,
                    'quiet': False,
                    'merge_output_format': 'mp4',
                    'ffmpeg_location': ffmpeg_path,
                    'postprocessors': [{
                        'key': 'FFmpegMetadata',
                        'add_metadata': True,
                    }],
                    # Add a User-Agent header to mimic a browser, which helps avoid 403 errors
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
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
            st.write(f"File saved to: `{downloaded_file_path}`")
            
            # Create a download button for the user
            with open(downloaded_file_path, "rb") as file:
                st.download_button(
                    label="⬇️ Click to Download Video",
                    data=file,
                    file_name=os.path.basename(downloaded_file_path),
                    mime="video/mp4"
                )

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
            st.warning("Please ensure FFmpeg is correctly installed and its path is set.")
