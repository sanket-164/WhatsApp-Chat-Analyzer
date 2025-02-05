import streamlit as st
import pandas as pd

def reset_session():
    st.session_state["messages"] = 0
    st.session_state["words"] = 0
    st.session_state["shared_media"] = 0
    st.session_state["shared_links"] = 0
    st.session_state["yearly_activity"] = pd.DataFrame()
    st.session_state["monthly_activity"] = pd.DataFrame()
    st.session_state["weekly_activity"] = pd.DataFrame()
    st.session_state["used_words"] = pd.DataFrame()
    st.session_state["used_emojis"] = pd.DataFrame()
    st.session_state["timeline"] = pd.DataFrame()

def delete_session():
    st.session_state.clear()
    st.experimental_rerun()