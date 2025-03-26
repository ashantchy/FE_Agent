import time
import streamlit as st
import requests
import pandas as pd
from widgets.work_flow import workflow_widget

API_BASE_URL = "http://192.168.20.114:8012/v1/interactions"
node_id = "ashant"

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

def get_node(node_id=node_id):
    response = requests.get(f"{API_BASE_URL}/nodes/{node_id}")
    if response.status_code == 200:
        return response.json()
    return {}

def fetch_chat_history(node_id: str):
    node = get_node(node_id)
    chat_ids = node.get("chat_ids", [])
    history = []
    for chat_id in chat_ids:
        response = requests.get(f"{API_BASE_URL}/chats/{chat_id}")
        if response.status_code == 200:
            chat = response.json()
            history.append((chat["id"], chat["name"]))
    return history


def fetch_chat_messages(chat_id):
    response = requests.get(f"{API_BASE_URL}/exchanges/filter/{chat_id}")
    if response.status_code == 200:
        exchanges = response.json()
        # Sort by created_at (assumes format allows lexicographical sorting)
        exchanges_sorted = sorted(exchanges, key=lambda x: x.get("created_at", ""))
        return exchanges_sorted
    return []

def create_new_chat():
    payload = {
        "name": f"Chat {int(time.time())}",
        "node_id": node_id
    }
    response = requests.post(f"{API_BASE_URL}/chats", json=payload)

    if response.status_code == 201:
        chat_data = response.json()
        st.session_state.history_titles.append((chat_data["id"], chat_data["name"]))
        st.session_state.selected_chat = chat_data["id"]
        st.session_state.show_input = True

def send_message(chat_id, role, content):
    # Sends a message to the chat and then refetches the exchanges.
    requests.post(f"{API_BASE_URL}/chats/{chat_id}/messages", json={"role": role, "content": content})
    st.session_state.current_chat = fetch_chat_messages(chat_id)

def save_exchange(chat_id, user_request, assistant_response):
    # Saves the exchange (request and response) to the /exchanges endpoint.
    payload = {
        "node_id": node_id,
        "chat_id": chat_id,
        "request": user_request,
        "response": assistant_response,
        "type": "UNKNOWN"
    }
    requests.post(f"{API_BASE_URL}/exchanges", json=payload)

def delete_chat(chat_id):
    requests.delete(f"{API_BASE_URL}/chats/{chat_id}")
    if st.session_state.selected_chat == chat_id:
        st.session_state.selected_chat = None
        st.session_state.current_chat = []
        st.session_state.show_input = False

def load_chat(chat_id):
    st.session_state.current_chat = fetch_chat_messages(chat_id)
    st.session_state.selected_chat = chat_id
    st.session_state.show_input = True

def update_chat_name(chat_id, new_name):
    payload = {"name": new_name}
    response = requests.put(f"{API_BASE_URL}/chats/{chat_id}", json=payload)
    
    if response.status_code == 200:
        st.session_state.history_titles = fetch_chat_history(node_id)  # Refresh history
        st.rerun()

init_session_state()

# Sidebar for chat history
st.sidebar.title("Chat History")
if st.sidebar.button("➕ New Chat"):
    create_new_chat()
    st.rerun()

history = fetch_chat_history(node_id=node_id)
for chat_id, chat_name in history:
    col1, col2 = st.sidebar.columns([0.8, 0.2])
    with col1:
        if st.button(chat_name, key=str(chat_id)):
            load_chat(chat_id)
            st.rerun()
    with col2:
        if st.button("🗑️", key=f"delete_{chat_id}"):
            delete_chat(chat_id)
            st.rerun()


            
st.sidebar.write("### Rename Chat")
# Dropdown to select a chat to rename
chat_options = {name: cid for cid, name in history}  # Create a mapping for easy lookup
selected_rename_chat = st.sidebar.selectbox("Select Chat", options=chat_options.keys(), key="rename_select")

# Text input for the new name
new_chat_name = st.sidebar.text_input("New Chat Name", value=selected_rename_chat)

# Rename button
if st.sidebar.button("Rename"):
    if new_chat_name and new_chat_name != selected_rename_chat:
        update_chat_name(chat_options[selected_rename_chat], new_chat_name)  # Update using chat ID

exchanges, preview = st.columns([1,2])
container = st.container(border=True)

if not st.session_state.selected_chat:
    st.title("Start a new Chat", anchor=False)
    st.write("No chat history available. Start a New Chat")
else:
    
    with exchanges:
        with get_container(820):
            st.markdown('''<style>.st-emotion-cache-jh76sn { width: 100%; justify-content: start; border: hidden; }</style>''', unsafe_allow_html=True)
            selected_chat_name = next((name for cid, name in history if cid == st.session_state.selected_chat), "Chat")
            st.subheader(selected_chat_name, anchor=False, divider="gray")

            # --- EXCHANGE MESSAGES ---
            exchanges = st.session_state.current_chat
            message_box = get_container(height)
            parse1, parse2, parse3 = st.columns([1,1,1])
            with parse1:
                parse_html = st.checkbox("Parse HTML")
            with parse2:
                parse_pdf = st.checkbox("Parse PDF")
        
            if not exchanges:
                pass
            else:
                # Ensure the message_box container is initialized
                
                with message_box:
                    # Loop through each exchange, displaying the user prompt and assistant response
                    for exchange in exchanges:
                        with st.chat_message("user"):
                            st.write(exchange["request"])
                        with st.chat_message("assistant"):
                            st.write_stream(exchange["response"])

            # --- INPUT AREA (user message and assistant response) ---
            if st.session_state.show_input:
                if prompt := st.chat_input("Type a message..."):
                    # Send user's message and display it immediately
                    send_message(st.session_state.selected_chat, "user", prompt)

                    # Display the message inside the message_box container
                    
                    
                    with message_box:
                        with st.chat_message("user"):
                            st.write(prompt)

                    # Generate assistant's response (here, simply echoing the prompt)
                    response = f"{prompt}"
                    send_message(st.session_state.selected_chat, "assistant", response)

                    # Display the assistant's response inside the message_box container
                    with message_box:
                        with st.chat_message("assistant"):
                            st.write(response)

                    # Save the exchange (user request and assistant response) to the /exchanges endpoint
                    save_exchange(st.session_state.selected_chat, prompt, response)

                    # Refetch and update the conversation dynamically
                    st.session_state.current_chat = fetch_chat_messages(st.session_state.selected_chat)
                    
    with preview:
        with get_container(800):
            st.markdown('''<style>.st-emotion-cache-jh76sn { width: 100%; justify-content: start; border: hidden; }</style>''', unsafe_allow_html=True)
            st.subheader("Preview", anchor=False, divider="gray")
            
            # --- CREATING CARDS ---
            workflow_widget()

            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path)

            if df.empty:
                st.write("Your data will be visualized here.")
            else:
                # Display the DataFrame using st.data_editor
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
</style>
''', unsafe_allow_html=True)