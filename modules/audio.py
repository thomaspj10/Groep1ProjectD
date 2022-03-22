import streamlit as st

def create_audio_element():
    with open("audio.mp3", "rb") as audio_file:
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/ogg")