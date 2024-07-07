import streamlit as st
from components import sign_in_page,sign_up_page
import session_states

if __name__=='__main__':
    try:
        session_states.main()
        if st.session_state['current_page']!='Sign Up':
            sign_in_page()
        else:
            sign_up_page()
    except Exception as e:
        print(f"Exception in sign in: {e}")
        st.error("Something went wrong. Please report this in the comments section")
