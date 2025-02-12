import streamlit as st
from functions.hello import say_hello

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title(f"Example streamlit app. {say_hello()}")
