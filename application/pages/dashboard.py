import streamlit as st
import pandas as pd
import utils.database as database 

def create_page():
    conn = database.get_connection()
    users = pd.read_sql("SELECT * FROM user", conn)
    
    for index, user in users.iterrows():
        if user["email"] != st.session_state["email"]:
            continue
        
        st.write("Welcome " + user["username"] + ",")
        
        receive_notifications = st.checkbox(label = "Do you want to receive notifications?", value=not user["receive_notifications"])
        
        users.at[index, "receive_notifications"] = int(receive_notifications)
        users.to_sql("user", conn, if_exists="replace", index=False)
        
        return