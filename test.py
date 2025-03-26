import time
import streamlit as st
import pandas as pd
from widgets.work_flow import workflow_widget

st.set_page_config(layout="wide")

file_path = "lm_guide_parsed.csv"

height = 600
def get_container(height):
    container = st.container(height=height)
    return container

def init_session_state():
    if "current_chat" not in st.session_state:
        st.session_state.current_chat = []
    if "selected_chat" not in st.session_state:
        st.session_state.selected_chat = None
    if "history_titles" not in st.session_state:
        st.session_state.history_titles = []
    if "show_input" not in st.session_state:
        st.session_state.show_input = False

init_session_state()

st.sidebar.title("Chat History")
if st.sidebar.button("➕ New Chat"):
    new_chat_id = str(int(time.time()))
    new_chat_name = f"Chat {new_chat_id}"
    st.session_state.history_titles.append((new_chat_id, new_chat_name))
    st.session_state.selected_chat = new_chat_id
    st.session_state.current_chat = []
    st.session_state.show_input = True
    st.rerun()

history = st.session_state.history_titles
for chat_id, chat_name in history:
    col1, col2 = st.sidebar.columns([0.8, 0.2])
    with col1:
        if st.button(chat_name, key=str(chat_id)):
            st.session_state.selected_chat = chat_id
            st.rerun()
    with col2:
        if st.button("🗑️", key=f"delete_{chat_id}"):
            st.session_state.history_titles = [h for h in history if h[0] != chat_id]
            if st.session_state.selected_chat == chat_id:
                st.session_state.selected_chat = None
                st.session_state.current_chat = []
                st.session_state.show_input = False
            st.rerun()
    
st.sidebar.write("### Rename Chat")
chat_options = {name: cid for cid, name in history}
selected_rename_chat = st.sidebar.selectbox("Select Chat", options=chat_options.keys(), key="rename_select")
new_chat_name = st.sidebar.text_input("New Chat Name", value=selected_rename_chat)
if st.sidebar.button("Rename"):
    if new_chat_name and new_chat_name != selected_rename_chat:
        st.session_state.history_titles = [(cid, new_chat_name) if cid == chat_options[selected_rename_chat] else (cid, name) for cid, name in history]
        st.rerun()

exchanges, preview = st.columns([1,2])
container = st.container(border=True)

if not st.session_state.selected_chat:
    st.title("Start a new Chat", anchor=False)
    st.write("No chat history available. Start a New Chat")
else:
    with exchanges:
        with get_container(820):
            selected_chat_name = next((name for cid, name in history if cid == st.session_state.selected_chat), "Chat")
            st.subheader(selected_chat_name, anchor=False, divider="gray")
            
            exchanges = st.session_state.current_chat
            message_box = get_container(height)
            
            if exchanges:
                with message_box:
                    for exchange in exchanges:
                        with st.chat_message("user"):
                            st.write(exchange["request"])
                        with st.chat_message("assistant"):
                            st.write(exchange["response"])
            
            if st.session_state.show_input:
                if prompt := st.chat_input("Type a message..."):
                    st.session_state.current_chat.append({"request": prompt, "response": prompt})
                    st.rerun()

    with preview:
        with get_container(800):
            st.subheader("Preview", anchor=False, divider="gray")
            workflow_widget()
            st.divider() 
            df = pd.read_csv(file_path)
            st.data_editor(df)



# --- STYLES ---
st.markdown('''
<style>
.st-emotion-cache-jh76sn {
    width: 100%;
    justify-content: start;
    border: hidden;
}
@media (min-width: calc(736px + 8rem)) {
    .st-emotion-cache-t1wise {
        padding-left: 5rem;
        padding-right: 5rem;
        position: relative;
    }
}

.chat-container {
    border: 2px solid #4CAF50;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 20px;
    background-color: #f9f9f9;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
}

# .st-emotion-cache-bm2z3a {
#     overflow: hidden;
# }

.st-emotion-cache-s1namz {
    border: 1px solid rgba(250, 250, 250, 0.2);
    border-radius: 0.5rem;
    padding: calc(-1px + 1rem);
    height: 650px;
    overflow: auto;
}
</style>
''', unsafe_allow_html=True)