import streamlit as st

def create_page():
    available_roles = [
        "Member",
        "Administrator"
    ]
    
    # Handle when the user submits the form.
    def submit():
        email = st.session_state["register_email"]
        password = st.session_state["register_password"]
        role = available_roles.index(st.session_state["register_role"]) + 1
        
        # TODO - Add the new user to the database.
        
        del st.session_state["register_email"]
        del st.session_state["register_password"]
        del st.session_state["register_role"]
    
    # Render the form.
    with st.form("register_form"):
        st.write("Register")
        
        st.text_input("Email", type="default", key="register_email")
        st.text_input("Password", type="password", key="register_password")
        st.selectbox("Role", available_roles, key="register_role")
        
        st.form_submit_button("Create user", on_click=submit)