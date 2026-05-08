import streamlit as st


def render() -> None:
    name = st.text_input("Your name", value="world")
    st.write(f"Hello, {name}!")
