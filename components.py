import streamlit as st
from auth import create_user,authenticate_user,check_duplicate
from utils import set_page
from api import mainApi
import re

# Sign-in page
def sign_in_page():
    st.title("Sign In")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    col1,col2,col_gp=st.columns([1,1,5])
    g=False
    with col1:
        if st.button("Sign In"):
            t=authenticate_user(username, password)
            if t:
                st.switch_page('Home.py')
            else:
                g=True
    with col2:
        if st.button("Sign Up"):
            set_page('Sign Up')
    if g:
        st.error("Invalid username or password")
# Sign-up page
def sign_up_page():
    st.title("Sign Up")
    
    col1, col_gap, col2 = st.columns([1,0.2, 1])

    with col1:
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type='password')
        new_email=st.text_input("Your email...")
        next_btn=st.button('Next')
        signin_btn=st.button('Sign In')
        g=False
        if next_btn and new_username and new_password and new_email:
            t=check_duplicate(new_username)
            if not t:
                url=mainApi(new_username,new_password,new_email)
                st.write(f'<meta http-equiv="refresh" content="0;url={url}">', unsafe_allow_html=True)
            else:
                g=True
        if g:
            st.error("Username already exists. Choose any other like deeznutz...")
        if signin_btn:
            set_page('Sign In')

    with col2:

        benefits_html = """
        <div style="
            border: 2px solid #4CAF50;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.1);
            font-family: Arial, sans-serif;
            color: #333;
            ">
            <h2 style="text-align: center; color: #2e7d32; margin-top: 0;">Benefits of Signing Up</h2>
            <ul style="padding-left: 20px; list-style-type: none;">
                <li style="padding: 10px 0; font-size: 18px; display: flex; align-items: center;">
                    <span style="background-color: #4CAF50; color: white; padding: 5px 10px; border-radius: 5px; margin-right: 10px;">✔</span>
                    $20 affordable price
                </li>
                <li style="padding: 10px 0; font-size: 18px; display: flex; align-items: center;">
                    <span style="background-color: #4CAF50; color: white; padding: 5px 10px; border-radius: 5px; margin-right: 10px;">✔</span>
                    Unlimited usage
                </li>
                <li style="padding: 10px 0; font-size: 18px; display: flex; align-items: center;">
                    <span style="background-color: #4CAF50; color: white; padding: 5px 10px; border-radius: 5px; margin-right: 10px;">✔</span>
                    Priority user support
                </li>
            </ul>
        </div>
        """
        st.markdown(benefits_html, unsafe_allow_html=True)
