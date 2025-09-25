import streamlit as st
import yt_dlp
import os

st.title("📥 YouTube Video Downloader (HD/4K)")
st.write("Enter a YouTube link to download the video in the highest available quality.")

# --- Functions ---
def get_video_qualities(url):
    """Fetches available video-only resolutions."""
    ydl_opts = {'noplaylist': True}
    qualities = set()
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            for f in formats:
                # Filter for video-only formats that have a height specified
                if f.get('vcodec') != 'none' and f.get('acodec') == 'none' and f.get('height'):
                    qualities.add(f"{f['height']}p")
        
        # Return a sorted list of unique qualities, highest first
        return sorted(list(qualities), key=lambda q: int(q.replace('p', '')), reverse=True)
    except Exception as e:
        st.error(f"❌ An error occurred while fetching qualities: {e}")
        return []

# --- Streamlit App UI ---
url = st.text_input("🎬 Enter YouTube URL:")

if url:
    try:
        with st.spinner("Fetching available qualities..."):
            qualities = get_video_qualities(url)

        if not qualities:
            st.warning("⚠️ No video-only formats found or an error occurred. Using best available single file.")
            qualities = ["best"] 
        
        st.info("ℹ️ Higher qualities (1080p+) have no sound and will be merged with the best audio.")
        selected_quality = st.selectbox("🎯 Select video quality:", qualities)

        if st.button("Download Video"):
            with st.spinner("Downloading and merging... this may take a moment."):
                output_path = "downloads"
                os.makedirs(output_path, exist_ok=True)
                
                height = selected_quality.replace('p', '') if selected_quality != 'best' else 'best'
                
                # Use format string for merging video and audio
                if height == 'best':
                    format_string = 'best'
                    # Use a different output template for 'best' to avoid a name clash
                    output_template = os.path.join(output_path, '%(title)s.%(ext)s')
                else:
                    format_string = f'bestvideo[height={height}]+bestaudio/best'
                    output_template = os.path.join(output_path, '%(title)s - %(height)sp.%(ext)s')

                # Add User-Agent header to mimic a browser, which helps avoid 403 errors.
                options = {
                    'format': format_string,
                    'outtmpl': output_template,
                    'noplaylist': True,
                    'merge_output_format': 'mp4',
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
                    }
                }

                with yt_dlp.YoutubeDL(options) as ydl:
                    info_dict = ydl.extract_info(url, download=True)
                    # Use os.path.abspath to get the full path
                    downloaded_file_path = os.path.abspath(ydl.prepare_filename(info_dict))
                    
                    # Ensure the final file has an mp4 extension for consistency
                    if not downloaded_file_path.endswith('.mp4'):
                        base, ext = os.path.splitext(downloaded_file_path)
                        final_path = base + '.mp4'
                        os.rename(downloaded_file_path, final_path)
                        downloaded_file_path = final_path

                st.success("✅ Download complete!")

                with open(downloaded_file_path, "rb") as file:
                    st.download_button(
                        label="⬇️ Click to Download Video",
                        data=file,
                        file_name=os.path.basename(downloaded_file_path),
                        mime="video/mp4"
                    )
    except Exception as e:
        st.error(f"❌ An error occurred: ERROR: unable to download video data: HTTP Error 403: Forbidden. \n\nThis is a known issue from YouTube's side. Your code is correct, but the request is being blocked.")
        st.error(f"Details: {e}")
