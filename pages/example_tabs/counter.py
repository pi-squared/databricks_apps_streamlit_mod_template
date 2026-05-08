import streamlit as st


def render() -> None:
    st.session_state.setdefault("count", 0)
    if st.button("Increment"):
        st.session_state.count += 1
    st.write(f"Count: {st.session_state.count}")
