import streamlit as st
from pytube import YouTube
from urllib.error import HTTPError, URLError
import os

st.title("📥 YouTube Video Downloader (1080p Max)")
st.write("Enter a YouTube video link and download it directly in MP4 format.")

# Input URL
url = st.text_input("🎬 Enter YouTube URL:")


def get_available_qualities(url: str):
    """Fetch available progressive (video+audio) streams for the given URL."""
    yt = YouTube(url)

    # progressive=True → includes both video and audio
    streams = yt.streams.filter(progressive=True, file_extension="mp4")

    qualities = sorted(
        {stream.resolution for stream in streams if stream.resolution},
        reverse=True,
    )
    return qualities, streams


if url:
    # Simple validation (not perfect, but helps avoid obvious bad input)
    if not ("youtube.com" in url or "youtu.be" in url):
        st.error("❌ Please enter a valid YouTube video URL.")
    else:
        try:
            qualities, streams = get_available_qualities(url)

            if not qualities:
                st.error(
                    "❌ No downloadable MP4 (video+audio) formats found for this video."
                )
            else:
                selected_quality = st.selectbox("🎯 Select video quality:", qualities)

                if st.button("Download"):
                    output_path = "downloads"
                    os.makedirs(output_path, exist_ok=True)

                    stream = streams.filter(res=selected_quality).first()

                    if not stream:
                        st.error("❌ Selected quality not available.")
                    else:
                        filename = stream.download(output_path=output_path)
                        st.success("✅ Download complete!")

                        with open(filename, "rb") as file:
                            st.download_button(
                                label="⬇️ Download Video",
                                data=file,
                                file_name=os.path.basename(filename),
                                mime="video/mp4",
                            )

        except HTTPError as e:
            # This is what you're seeing: HTTP Error 400 from YouTube
            st.error(
                "❌ YouTube rejected the request from this server (HTTP error). "
                "This often happens on hosted platforms like Streamlit Cloud and "
                "is not something you can fully fix in code.\n\n"
                "👉 Try running this app **locally on your own PC** instead."
            )
        except URLError as e:
            st.error(
                "❌ Network error while trying to reach YouTube. "
                "The hosting environment may be blocking outbound requests."
            )
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")
