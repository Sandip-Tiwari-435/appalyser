import streamlit as st
from customPilot import appStoreScraper,gsheetCacher
import session_states
import types
from genAi import model
from gsheetUploader import create_google_sheet
from auth import update_user
from utils import addFromPlayground
import copy

def update_context():
    obj=copy.deepcopy(st.session_state.role.context)
    newContext=st.session_state.role.context[0]['parts'][0]['text'].replace('#length#',str(st.session_state.responselength))+ " At the end of your response, you can ask whether the user wants to chat about this in case of any doubts and remind them the button to chat with you is at the top beside the button which generated your response."
    obj[0]['parts'][0]['text']=newContext
    return obj

def cacheSummarize(dfs,noOfReviews):
    with st.spinner("Summarizing reviews with AI..."):
        obj=update_context()
        new_context = obj + [{"role":"user","parts":[{"text":str(dfs["df"]["review"].tolist())[:30000]}]}]
        response=model.generate_content(new_context,stream=True)
        for chunk in response:
            yield chunk.text
        st.session_state.summaries[st.session_state.role.name][(dfs['name'],noOfReviews)]=response.text
    del obj


def summarize_reviews(dfs,noOfReviews):
    if (dfs['name'],noOfReviews) in st.session_state.summaries[st.session_state.role.name]:
        return st.session_state.summaries[st.session_state.role.name][(dfs['name'],noOfReviews)]
    if(st.session_state.summaryFree<0):
        st.error("You have exceeded free usage quota. Sign in to continue....")
        return
    st.session_state.summaryFree-=1
    update_user(st.session_state['username'])
    return cacheSummarize(dfs,noOfReviews)    

def cacheList(name,noOfReviews):
    if(st.session_state.searchFree<0):
        st.error("You have exceeded free usage quota. Sign in to continue....")
        return []
    libo = appStoreScraper(name,int(noOfReviews))
    return libo

def actuate(name,noOfReviews):
    if (name,noOfReviews) in st.session_state.review:
        return st.session_state.review[(name,noOfReviews)]
    else:
        if st.session_state['user_authenticated']:
            update_user(st.session_state['username'])
        return cacheList(name,noOfReviews)

def playground():
    st.markdown(f"""<div style='display:flex;margin:auto;'>
        <h1>App Store App Analyser</h1>
        <div style='margin:auto;'>
            <p style='color: grey; margin:auto;font-size:10px;'>Search Uses left: {st.session_state.searchFree}</p>
            <p style='color: grey; margin:auto;font-size:10px;'>Summary Uses left: {st.session_state.summaryFree}</p>
        </div>
    </div>""",unsafe_allow_html=True)
    st.subheader('Search, analyse and solve app problems with AI')
    col1, col2, col3 = st.columns(3)

    with col1:
        name = st.text_input("Enter an app name:",placeholder="Enter an app name",
            label_visibility='collapsed')
    with col2:
        noOfReviews = st.text_input("How many reviews?",placeholder="How many reviews?",
                label_visibility='collapsed')
    with col3:
        go_btn=st.button("Go")
    st.session_state.csv = st.checkbox("I want the results stored in a Google Sheet")
    lino=[]
    st.session_state.spreadsheet_id=''

    if not (name and noOfReviews.isdigit()):
        st.error("Please enter a name and reviewCount to see the results.")
        return

    d=actuate(name,noOfReviews)
    if st.session_state.csv:
        if isinstance(d, types.GeneratorType):
            st.session_state.spreadsheet_id=create_google_sheet()
            st.success(f"Here you go: https://docs.google.com/spreadsheets/d/{st.session_state.spreadsheet_id}")
        elif d[0]=='':
            st.session_state.spreadsheet_id=create_google_sheet()
            st.success(f"We are on it: https://docs.google.com/spreadsheets/d/{st.session_state.spreadsheet_id}")
            st.session_state.usingAppStoreScraper=False
            st.session_state.review[(name,noOfReviews)][0]=st.session_state.spreadsheet_id
            gsheetCacher(int(noOfReviews),st.session_state.myDict,d[1])
        else:
            st.success(f"Here you go: https://docs.google.com/spreadsheets/d/{d[0]}")
            d=d[1]
    if not isinstance(d, types.GeneratorType) and isinstance(d[1],list):
        d=d[1]

    for i,dfs in enumerate(d):
        col1, col2, col3 = st.columns([3,1, 1])
        try:
            with col1:
                st.subheader(dfs["name"])
            with col3:
                button_clicked=st.button("Summarize the reviews with AI", key=dfs["name"])
            if (dfs['name'],noOfReviews) in st.session_state.summaries[st.session_state.role.name]:
                with col2:
                    chat_btn=st.button("Chat with AI regarding this", key="chat"+dfs["name"])
            if button_clicked:
                p=summarize_reviews(dfs,noOfReviews)
                with st.expander("Summary", expanded=True):
                    st.write(p)
                st.rerun()
            if (dfs['name'],noOfReviews) in st.session_state.summaries[st.session_state.role.name]:
                st.success("Summarization completed")
                with st.expander("Summary", expanded=True):
                    st.session_state.summaries[st.session_state.role.name][(dfs['name'],noOfReviews)]
            if (dfs['name'],noOfReviews) in st.session_state.summaries[st.session_state.role.name] and chat_btn:
                req=f"Summarize reviews for {dfs['name']}"
                res=st.session_state.summaries[st.session_state.role.name][(dfs['name'],noOfReviews)]
                obj=[{
                    "role": "user",
                    "parts": [{ "text": req}],
                },{
                    "role": "model",
                    "parts": [{ "text": res}],
                },]
                addFromPlayground(req,res,obj)
                st.switch_page('pages/3_Ask_AI.py')

            st.dataframe(dfs["df"])
            lino.append(dfs)
        except Exception as e:
            print(f"Exception in playground {e}")
            st.error("Something went wrong...")
    if len(lino)!=0 and name and noOfReviews and (name,noOfReviews) not in st.session_state.review:
        st.session_state.searchFree-=1
        st.session_state.review[(name,noOfReviews)]=[st.session_state.spreadsheet_id,lino]
        st.rerun()

if __name__=='__main__':
    session_states.main()
    playground()
