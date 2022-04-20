from urllib import response
import streamlit as st

def create_audio(url):
    # Creates an audio player with the given url to the .wav file
    st.audio(url)