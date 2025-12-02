import streamlit as st
from pytube import YouTube
from urllib.error import HTTPError
import os
import traceback

st.title("📥 YouTube Video Downloader (1080p Max)")
st.write("Enter a YouTube video link and download it directly in MP4 format.")

# Input URL
url = st.text_input("🎬 Enter YouTube URL:")

def get_available_qualities(url: str):
    """
    Fetch available progressive (video+audio) streams for the given URL.
    Raises a clear error if YouTube/pytube fails.
    """
    try:
        yt = YouTube(url)
        # Filter streams with both video and audio
        streams = yt.streams.filter(progressive=True, file_extension='mp4')
        qualities = sorted(
            {stream.resolution for stream in streams if stream.resolution},
            reverse=True
        )
        return qualities, streams

    except HTTPError as e:
        # YouTube / network-side issue
        raise RuntimeError(
            "YouTube returned an HTTP error (e.g., 400 Bad Request). "
            "This often happens when pytube is out of date or YouTube is blocking the server."
        ) from e
    except Exception as e:
        # Any other pytube-related error
        raise RuntimeError(f"Failed to fetch video info: {e}") from e


if url:
    try:
        # Try to fetch qualities once URL is entered
        qualities, streams = get_available_qualities(url)

        if not qualities:
            st.error("❌ No downloadable video formats found (no progressive MP4 streams).")
        else:
            # Dropdown to select quality
            selected_quality = st.selectbox("🎯 Select video quality:", qualities)

            if st.button("Download"):
                output_path = "downloads"
                os.makedirs(output_path, exist_ok=True)

                # Get the stream for selected quality
                stream = streams.filter(res=selected_quality).first()
                if not stream:
                    st.error("❌ Selected quality not available.")
                else:
                    filename = stream.download(output_path=output_path)
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
        # Show a friendly error in the app + full traceback for debugging
        st.error(f"❌ Error: {e}")
        st.code(traceback.format_exc())
