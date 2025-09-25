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
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])
        for f in formats:
            # Filter for video-only formats that have a height specified
            if f.get('vcodec') != 'none' and f.get('acodec') == 'none' and f.get('height'):
                qualities.add(f"{f['height']}p")
    
    # Return a sorted list of unique qualities, highest first
    return sorted(list(qualities), key=lambda q: int(q.replace('p', '')), reverse=True)

# --- Streamlit App UI ---
url = st.text_input("🎬 Enter YouTube URL:")

if url:
    try:
        with st.spinner("Fetching available qualities..."):
            qualities = get_video_qualities(url)

        if not qualities:
            st.warning("⚠️ No video-only formats found. Using best available single file.")
            qualities = ["best"] 
        
        st.info("ℹ️ Higher qualities (1080p+) have no sound and will be merged with the best audio.")
        selected_quality = st.selectbox("🎯 Select video quality:", qualities)

        if st.button("Download Video"):
            with st.spinner("Downloading and merging... this may take a moment."):
                output_path = "downloads"
                os.makedirs(output_path, exist_ok=True)
                
                height = selected_quality.replace('p', '') if selected_quality != 'best' else 'best'
                
                format_string = f'bestvideo[height={height}]+bestaudio/best' if height != 'best' else 'best'

                options = {
                    'format': format_string,
                    'outtmpl': os.path.join(output_path, '%(title)s - %(height)sp.%(ext)s'),
                    'noplaylist': True,
                    'merge_output_format': 'mp4',
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

                with open(downloaded_file_path, "rb") as file:
                    st.download_button(
                        label="⬇️ Click to Download Video",
                        data=file,
                        file_name=os.path.basename(downloaded_file_path),
                        mime="video/mp4"
                    )
    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
