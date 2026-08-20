import streamlit as st
from groq import Groq
import tempfile
import os
import re 
st.title ("Extract Text from Audio or Video")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
st.subheader("Upload your audio or video file")
uploaded = st.file_uploader("Upload your file", type=["mp3", "wav", "mp4", "avi"])
def transcribe_audio_file(path):
    with open(path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=(os.path.basename(path), f),
            response_format="text"
        )
    return transcript
if uploaded:
    if uploaded.size / 1024**2 > 25:
        st.error("File size exceeds 25MB limit. Please upload a smaller file.")
    elif st.button("Extract Text", key="file_btn"):
        with st.spinner("Extracting text from audio/video..."):
            ext = os.path.splitext(uploaded.name)[-1].lower()
            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
                tmp_file.write(uploaded.read())
                path = tmp_file.name
            try:
                transcript = transcribe_audio_file(path)
            finally:
                os.unlink(path)
        if not transcript or len(transcript.strip()) < 5:
            st.error("Could not extract text from the audio/video.")
        else:
            st.subheader("The Extracted Text:")
            st.write(transcript)
            st.download_button("Download Transcript", transcript, file_name="transcript.txt")
st.markdown("---")
st.subheader("Upload your YouTube video link")
youtube_link = st.text_input("Enter YouTube video link", placeholder="https://www.youtube.com/watch?v=...")