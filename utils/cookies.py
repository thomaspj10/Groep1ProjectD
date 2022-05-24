import streamlit as st
from streamlit_cookies_manager import CookieManager
    
__cookies = None

def initialize_cookes():
    global __cookies
    __cookies = CookieManager()
    if not __cookies.ready():
        st.stop()
    
def get_cookies() -> CookieManager:
    return __cookies