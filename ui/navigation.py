import streamlit as st
from streamlit_option_menu import option_menu

from utils.constants import TOP_NAV_HEADERS, TOP_NAV_ICONS

def top_navbar():
    if "current_page"  not in st.session_state:
        st.session_state["current_page"] = TOP_NAV_HEADERS[0]
        
    st.session_state["current_page"] = option_menu(
        menu_title="Chat Analysis",
        options=TOP_NAV_HEADERS,
        icons=TOP_NAV_ICONS,
        default_index=TOP_NAV_HEADERS.index(st.session_state["current_page"]),
        orientation="horizontal",
        menu_icon="chat",
        key="navbar",
    )
