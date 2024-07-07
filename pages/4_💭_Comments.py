import streamlit as st
import sqlite3
from auth import get_comments,add_comment
import session_states
from datetime import datetime

def cssDo():
    st.markdown("""
<style>
    .custom-message {
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        transition: background-color 0.5s ease; /* Smooth transition for background color */
    }

    .custom-info {
        background-color: #2196F3; /* Blue */
        color: black;
    }

    @keyframes brighten {
        0% { background-color: inherit; }
        50% { background-color: #fff3cd; } /* Bright yellowish color */
        100% { background-color: inherit; }
    }

    .animate-brighten {
        animation: brighten 4s infinite alternate;
    }

    .comment-container {
                    border: 1px solid #ddd;
                    padding: 15px;
                    border-radius: 10px;
                    margin-bottom: 15px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    transition: all 0.3s ease;
                }
                .comment-container:hover {
                    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
                }
                .comment-username {
                    font-weight: bold;
                    font-size: 1.1em;
                    color: #333;
                }
                .comment-timestamp {
                    color: #999;
                    font-size: 0.9em;
                }
                .comment-text {
                    margin-top: 10px;
                    font-size: 1em;
                    color: #555;
                }
                .load-more-btn {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    transition: background-color 0.3s ease;
                }
                .load-more-btn:hover {
                    background-color: #45a049;
                }
</style>
""", unsafe_allow_html=True)


def main():
    st.title("Your words matter :)")
    st.markdown('<p class="custom-message custom-info animate-brighten">We Value Your Feedback! 🌟 Share your thoughts and help us improve!</p>', unsafe_allow_html=True)
    username = st.session_state['username']
    col1, col2 = st.columns([5,1])
    with col1:
        comment = st.text_input("Comment now...",placeholder="Comment now...",label_visibility='collapsed')
    with col2:
        sbt_btn=st.button("Submit",key='sbt_btn')
    if sbt_btn:
        if username and comment:
            add_comment(username, comment)
            st.success("Comment added successfully!")
            st.session_state.comments=[(username,datetime.now().strftime('%Y-%m-%d %H:%M:%S'),comment)]+st.session_state.comments
        else:
            st.error("Please enter both a username and a comment")

    comment_container = st.container()

    def load_more_comments():
        st.session_state.offset += 10
        new_comments = get_comments(st.session_state.offset, 10)
        st.session_state.comments.extend(new_comments)
        return st.session_state.comments

    with comment_container:
        st.markdown(
            """
            <style>
                .comment-container {
                    border: 1px solid #ddd;
                    padding: 15px;
                    border-radius: 10px;
                    margin-bottom: 15px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    transition: all 0.3s ease;
                }
                .comment-container:hover {
                    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
                }
                .comment-username {
                    font-weight: bold;
                    font-size: 1.1em;
                    color: #333;
                }
                .comment-timestamp {
                    color: #999;
                    font-size: 0.9em;
                }
                .comment-text {
                    margin-top: 10px;
                    font-size: 1em;
                    color: #555;
                }
                .load-more-btn {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    transition: background-color 0.3s ease;
                }
                .load-more-btn:hover {
                    background-color: #45a049;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

        for username, created_at, comment in st.session_state.comments:
            st.markdown(
                f"""
                <div class='comment-container'>
                    <div class='comment-username'>{username}</div>
                    <div class='comment-timestamp'>{created_at}</div>
                    <div class='comment-text'>{comment}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if st.button("Load more comments"):
            load_more_comments()
            st.rerun()

if __name__ == "__main__":
    try:
        session_states.main()
        cssDo()
        main()
    except Exception as e:
        print(f"Exception in comments: {e}")
        st.error("Something went wrong, can you help me get back up?")
