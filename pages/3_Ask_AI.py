import streamlit as st
import session_states
import copy

def updated_context():
    obj=copy.deepcopy(st.session_state.role.context[0])
    obj['parts'][0]['text'] = obj['parts'][0]['text'].replace('#length#',str(st.session_state.responselength))+ " At the end of your response, you can ask whether the user wants to chat about the response in more detail but dont try to be repititive. If yes, then try to be more effective and go deep in solving the query."
    return obj

def llm_function(query):
    text_response = ""
    obj=updated_context()
    print(obj)
    print(st.session_state.role.chat.history)
    st.session_state.role.chat.history[0] = obj
    response: GenerateContentResponse = st.session_state.role.chat.send_message(query,stream=True)
    st.session_state.messages[st.session_state.role.name].append(
        {
            "role":"user",
            "content": query
        }
    )
    st.session_state.messages[st.session_state.role.name].append(
                {
                    "role":"assistant",
                    "content":text_response
                }
            )
    placeholder=st.empty()
    try:
        for chunk in response:
            text_response+=chunk.text
            with placeholder.container():
                with st.chat_message("assistant"):
                    st.markdown(text_response)
            st.session_state.messages[st.session_state.role.name][-1]['content']=text_response
    except Exception as e:
        st.error("Something went wrong! Please try again!")
    finally:
        del obj
def main():
    st.title(f"{st.session_state.role.name}s' assistant")
    for message in st.session_state.messages[st.session_state.role.name]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    query = st.chat_input(st.session_state.role.chatplaceholder)

    if query:
        with st.chat_message("user"):
            st.markdown(query)

        llm_function(query)

if __name__=="__main__":
    try:
        session_states.main()
        main()
    except Exception as e:
        #st.error("Something went wrong, can you help me get back up?")
        st.error(e)
