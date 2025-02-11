import streamlit as st
from functions.hello import say_hello

st.title(f"Example streamlit app. {say_hello()}")
