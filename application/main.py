import streamlit as st

import pages.login

pages = {
    "Read from excel": pages.login.create_page,
}

choice = st.sidebar.radio("Choice your page: ", tuple(pages.keys()))

pages[choice]()
