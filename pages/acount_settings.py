import streamlit as st
import pandas as pd
import utils.database as database 
import utils.cookies as cookies

def create_page():
    conn = database.get_connection()
    users = pd.read_sql("SELECT * FROM user", conn)
    filtered_users = users[users["email"] == cookies.get_cookies()["email"]]
    
    user = filtered_users.iloc[0]

    receive_notifications = st.checkbox(label = "Do you want to receive notifications?", value=user["receive_notifications"])

    for index, _user in users.iterrows():
        if user["email"] == _user["email"]:
            users.at[index, "receive_notifications"] = int(receive_notifications)
    
    users.to_sql("user", conn, if_exists="replace", index=False)