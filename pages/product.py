import streamlit as st

st.header("About")
st.write("A minimal page with a two-column layout.")

left, right = st.columns(2)

with left:
    st.subheader("Left column")
    st.write("Anything you put under `with left:` renders here.")

with right:
    st.subheader("Right column")
    st.write("Anything you put under `with right:` renders here.")
