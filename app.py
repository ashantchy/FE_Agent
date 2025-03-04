import os
import streamlit as st
import pandas as pd
from agent import agent, CATEGORY_HIERARCHY, answer_chat, ValidationResponse
import random
import toml
 
# Theme configuration
 
 
# Save theme config
 
 
# Custom CSS for React-like styling
css = '''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
 
    :root {
        --primary-color: #03346E;
        --background-color: ##121413;
        --card-background: #504B38;
        --text-color: ##f7faf8;
        --accent-color: #504B38;
        --shadow: 0 4px 6px rgba(0,0,0,0.1);
        --hover-shadow: 0 6px 12px rgba(0,0,0,0.15);
        --transition: all 0.3s ease;
        --text-background: #1976D2;
    }
 
    .stApp {
        font-family: 'Inter', sans-serif;
        background-color: var(--background-color);
        color: var(--text-color);
    }
    .st-emotion-cache-mtjnbi {
    width: 100%;
    max-width: 100%;
    }
    .main-container {
        display: flex;
        gap: 8em;
        padding: 0rem;
        justify-content: space-between;
        width:100vw;
    }
 
    .chat-column, .preview-column {
        background-color: var(--card-background);
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: var(--shadow);
        transition: var(--transition);
    }
 
    .chat-column:hover, .preview-column:hover {
        box-shadow: var(--hover-shadow);
    }
 
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: var(--primary-color);
    }
 
    .chat-message {
        margin-bottom: 1rem;
        padding: 0.75rem 1rem;
        border-radius: 20px;
        max-width: 80%;
        animation: fadeIn 0.3s ease-in-out;
    }
 
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
 
    .user-message {
        background-color: var(--text-background);
        color: white;
        align-self: flex-end;
        margin-left: auto;
    }
 
    .assistant-message {
        background-color: #E9ECEF;
        color:black;
        align-self: flex-start;
    }
 
    .custom-button {
        background-color: var(--primary-color);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: var(--transition);
        cursor: pointer;
    }
 
    .custom-button:hover {
        background-color: #3A7BC8;
        transform: translateY(-2px);
    }
    /* Adding borders around columns */
    .stColumn {
        border: 2px solid #3C3D37;  /* Border color */
        border-radius: 10px;         /* Rounded corners */
        padding: 1rem;
    }
   
    .category-item {
        cursor: pointer;
        padding: 0.5rem;
        border-radius: 5px;
        transition: var(--transition);
    }
 
    .category-item:hover {
        background-color: #E9ECEF;
    }
 
    .chat-input {
        display: flex;
        gap: 1rem;
        margin-top: 1rem;
    }
 
    .chat-input input {
        flex-grow: 1;
        padding: 0.5rem;
        border: 1px solid #ccc;
        border-radius: 5px;
    }
 
    @media (max-width: 768px) {
        .main-container {
            flex-direction: column;
        }
       
        .chat-message {
            max-width: 100%;
        }
    }
    
    /* Streamlit Modified CSS */
    .st-emotion-cache-fvdmmq{
        height: 100% !important;
    }
    .st-emotion-cache-mtjnbi {
        width: 100%;
        padding: 2rem 1rem 2rem;
    }
</style>
'''
 
st.markdown(css, unsafe_allow_html=True)
with st.sidebar:
    st.subheader("hehe")
    st.button("New Chat")
 
# Define max chat history length
MAX_CHAT_HISTORY = 100
CONTAINER_HEIGHT = 10*60
 
if "messages" not in st.session_state:
    st.session_state.messages = []
 
if "show_preview" not in st.session_state:
    st.session_state.show_preview = False
 
def file_handler(key, *args, **kwargs):
    file = st.file_uploader(label="Upload File", key=key)
 
    if file:
        file_path = f"uploaded_files/{file.name}"
        os.makedirs("uploaded_files", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
 
        st.image(file_path, caption="Detected Tables", use_container_width=True)
 
widget_mp = {
    "file-upload": lambda key="file-uploader": file_handler(key),
}
 
def preview(container):
    with container:
 
        st.header("Preview", divider="gray", anchor=False)
 
        if st.session_state.show_preview:
            for category, subcategories in CATEGORY_HIERARCHY.items():
                with st.expander(category):
                    if isinstance(subcategories, list):
                        for subcategory in subcategories:
                            st.markdown(f'<div class="category-item">{subcategory}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="category-item">{subcategories}</div>', unsafe_allow_html=True)
        else:
            st.info("No preview available. Send a message to see the category hierarchy.")
       
        st.markdown('</div>', unsafe_allow_html=True)
 
def display_chat(parent):
    with parent:
        for role, resp in st.session_state.messages[-MAX_CHAT_HISTORY:]:
            message_class = "user-message" if role == "user" else "assistant-message"
            st.markdown(f'<div class="chat-message {message_class}">{resp}</div>', unsafe_allow_html=True)
 
def answer(user_input: str):
    st.session_state.messages.append(("user", user_input))
 
    if user_input.casefold() == "show input":
        st.session_state.messages.append(
            (
                "assistant-tool",
                (widget_mp.get("file-upload"), str(random.randint(10000, 99999))),
            )
        )
    else:
        try:
            response = answer_chat(user_input)
 
            if isinstance(response, ValidationResponse):
                assistant_reply = response.message
                st.session_state.show_preview = not response.valid
                st.session_state.messages.append(("assistant", assistant_reply))
            else:
                assistant_reply = "No valid response object found."
                st.session_state.messages.append(("assistant", assistant_reply))
 
        except Exception as e:
            st.session_state.messages.append(("assistant", f"Error: {str(e)}"))
 
def chat(container):
    with container:
        st.header("Chat History", divider="gray", anchor=False)
 
        chat_container = st.container(height=CONTAINER_HEIGHT)
        display_chat(chat_container)
 
        user_input = st.chat_input("Enter your message:")
        if user_input:
 
            with chat_container:
                try:
                    answer(user_input)
                except Exception as e:
                    print(e)
                st.session_state.messages = st.session_state.messages[ -MAX_CHAT_HISTORY: ]
 
                st.rerun()
 
        st.markdown('</div>', unsafe_allow_html=True)
 
def main():
    # Page Heading
   
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
   
    with col1:
        chat(st.container())
   
    with col2:
        preview(st.container())
   
    st.markdown('</div>', unsafe_allow_html=True)
 
 
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.markdown(
           
            f'<p>Oops! Something went wrong. Please try refreshing the page or contact support if the issue persists.</p>'
            f'<p>Error details: {str(e)}</p>'
            '</div>',
            unsafe_allow_html=True
        )
 
 
 