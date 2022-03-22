import streamlit as st
import pandas as pd
import requests
import sqlite3

def read_data_from_excel():
    data = pd.read_excel("mockdata.xlsx")
    st.write(data)
    
def load_data_from_api():
    response = requests.get("https://api.weatherapi.com/v1/current.json?key=db80636dea1c46a384d171903221103&q=Papendrecht")
    data = response.json()
    
    st.write(data)
    
def load_data_from_database():
    data = pd.read_excel("mockdata.xlsx")
    st.write(data)
    
    conn = sqlite3.connect("db.sqlite")
    data.to_sql("table_name", conn, if_exists="replace", index=False)
    
    new_data = pd.read_sql("SELECT * FROM table_name", conn)
    st.write(new_data)