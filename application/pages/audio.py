from urllib import response
import streamlit as st
import requests

def create_page(url):
    # Gets the audio file from the URL
    audio = requests.get(url).content

    # Creates an audio player 
    st.audio(audio)