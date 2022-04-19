import sqlite3
import streamlit as st
import database as db
import pages.login

pages = {
    "Read from excel": pages.login.create_page,
}

choice = st.sidebar.radio("Choice your page: ", tuple(pages.keys()))

pages[choice]()

connection = db.create_connection()