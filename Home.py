import streamlit as st
import session_states
from auth import create_user
from api import validatePayment
from urllib.parse import unquote

def homer():
    st.title("📱 Appalyser") 
    if('username' in st.query_params and st.session_state.username!=st.query_params['username']):
        st.success(f"Your payment has been received, {st.query_params['username']}")
        if validatePayment(st.query_params['token']) and create_user(unquote(st.query_params['username']), unquote(st.query_params['password']),unquote(st.query_params['email']), paid=1):
            st.success("User signed up successfully")
            st.switch_page("Home.py")
        else:
            st.error("Shutup you hacker")
    st.write(f"Hi {st.session_state.username},")
    st.markdown(f"""
    ## Welcome to the App Analyser Platform! 🛠️

    ### Analyze, Read Reviews and Solve Problems with AI about {st.session_state.role.home[0]}!

    **Our platform provides you with in-depth analysis, personalized suggestions, and comprehensive reviews for a wide range of applications. Whether you're looking for productivity tools, entertainment apps, or educational resources, we've got you covered.**

    ### How to Use:
    1. **Choose your role:** Select your role from the sidebar provided. This will primarily decide how the AI should behave.
    2. **Search for an App:** Use the navigation to visit playground and type an app name you want to analyze. """+'<a href="/Playground" target="_self">Visit Playground Now</a>'+f"""
    3. **Read Reviews:** Read expert and user reviews to get a holistic view of the app.
    4. **Summarise reviews with AI:** Click the button next to each app review to uncover issues and see AI-generated solutions from a {st.session_state.role.name.lower()}'s perspective
    5. **Chat with AI:** When the summarisation is complete, a chat button should appear. You can further discuss about the AI response by clicking on it. {st.session_state.role.home[1]}
    6. **View Analysis:** Access detailed reports and metrics about similar app's performances.

    ### Features:
    - **Interactive AI:** Personalised summarisation and solutions based on whether you are a developer/consumer
    - **App Analysis:** Get detailed insights into app performance, user engagement, and more.
    - **Comprehensive Reviews:** Read reviews from real users to help you make informed decisions.
    - **Summarise with AI:** Summarize reviews using AI to uncover issues and see AI solutions on just the click of a button. Summarization will happen based on your role (Developer/Consumer)
    - **Store results in sheet:** Store reviews and metadata of the apps in a google sheet

    ### Start Exploring Now!
    Use the sidebar to navigate through different sections. Begin by searching for an app!

    ### Contact Us:
    If you have any questions or feedback, feel free to visit the """+'<a href="/Comments" target="_self">Comment Section</a>'+""" now or reach out to us at [email](mailto:sandipt335@gmail.com).

    ---
    **Happy Exploring!**

    **Created with love by Sandip | Thanks Thomas for the inspiration** 
    """,unsafe_allow_html=True)
if __name__ == '__main__':
    try:
        session_states.main()
        homer()
    except Exception as e:
        st.error("Something went wrong. Please report this problem in the comments section")
