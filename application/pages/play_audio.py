from urllib import response
import streamlit as st
import requests

def create_page():
    # Gets the audio file from the URL
    audio_url = "http://95.217.2.100:8000/124489-9-0-12.wav"
    audio = requests.get(audio_url).content
    st.audio(audio)