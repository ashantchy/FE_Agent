import streamlit as st

# Hardcoded credentials
VALID_USERNAME = "user123"
VALID_PASSWORD = "password123"

def login():
    
    with st.container(border=True):
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        with col3:
            st.subheader("Login", anchor=False)
        
        form_col1, form_col2, form_col3 = st.columns([0.2, 1, 0.2], border=False)
        with form_col2:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            st.markdown("")

            if st.button("Login", use_container_width=True, type="secondary"):
                if username == VALID_USERNAME and password == VALID_PASSWORD:
                    
                    st.success("Login successful!")
                else:
                    st.error("Incorrect username or password.")



login()
