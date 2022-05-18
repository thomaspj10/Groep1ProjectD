import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
    
__cookies = None

def initialize_cookes():
    global __cookies
    __cookies = EncryptedCookieManager(
        prefix="prefix",
        password="password",
    )
    if not __cookies.ready():
        st.stop()
    
def get_cookies() -> EncryptedCookieManager:
    return __cookies