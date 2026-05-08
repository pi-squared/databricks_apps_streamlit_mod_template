import streamlit as st

st.header("Example page")
st.write("Hello, world!")

tab_a, tab_b = st.tabs(["Greeting", "Counter"])

with tab_a:
    from pages.example_tabs.greeting import render as render_greeting
    render_greeting()

with tab_b:
    from pages.example_tabs.counter import render as render_counter
    render_counter()
