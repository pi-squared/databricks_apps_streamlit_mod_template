import streamlit as st

st.header("Form")
st.write("A minimal page with a form that submits as one batch.")

with st.form("demo_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120, value=18)
    submitted = st.form_submit_button("Submit")

if submitted:
    st.success(f"Hello, {name or 'stranger'}! You are {age} years old.")
