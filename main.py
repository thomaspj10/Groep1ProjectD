import streamlit as st
import pages.download_event
import utils.cookies as cookies

st.set_page_config(
    page_title="Chengeta Dashboard",
    page_icon=":deer:",
    initial_sidebar_state="expanded",
    layout="wide"
)

hide_streamlit_style = """
                <style>
                .css-18e3th9 {padding-top: 0rem;}
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

cookies.initialize_cookes()

if "event" in st.experimental_get_query_params():
    pages.download_event.create_download()
    
else:
    import components.sidebar
    components.sidebar.create_page()