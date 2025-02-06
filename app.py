import streamlit as st

import utils.preprocess as preprocess
from utils.constants import LOGO_IMAGE_PATH, TRAFFIC_FILE_PATH, APP_NAME, TOP_NAV_HEADERS
from utils.update_data import read_traffic, update_traffic

from ui.guidelines import guidelines_page
from ui.navigation import top_navbar
from ui.analysis.top_users import basic_page
from ui.analysis.activity import activity_page
from ui.analysis.timeline import timeline_page
from ui.feedback import feedback_page

st.set_page_config(
    page_title=APP_NAME,
    page_icon=LOGO_IMAGE_PATH,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None,
)

st.sidebar.title(APP_NAME)

# Read file
traffic = read_traffic(TRAFFIC_FILE_PATH)

if "new_user" not in st.session_state:
    st.session_state["new_user"] = True
    traffic["Visits"] = traffic["Visits"] + 1
    update_traffic(TRAFFIC_FILE_PATH, traffic)


uploaded_file = st.sidebar.file_uploader("Choose a txt chat file", type=['txt'], accept_multiple_files=False)

if uploaded_file is not None:
    try:
        if "chat_file" not in st.session_state or st.session_state["chat_file"] != uploaded_file.name:
            st.cache_data.clear()
            st.session_state['chat_file'] = uploaded_file.name
            traffic["Chats Analyzed"] = traffic["Chats Analyzed"] + 1
            update_traffic(TRAFFIC_FILE_PATH, traffic)
            st.cache_data.clear()
        
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = preprocess.preprocess(data)

        user_list = df['user'].unique().tolist()
        if 'group_notification' in user_list:
            user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0, "All")

        selected_user = st.sidebar.selectbox("Select User", user_list)
        
        st.sidebar.header(f"{traffic["Visits"]} Visited")
        st.sidebar.header(f"{traffic["Chats Analyzed"]} Chat Analyzed")

        top_navbar()

        if st.session_state["current_page"] == TOP_NAV_HEADERS[0]:
                basic_page(user_list, df)
        elif st.session_state["current_page"] == TOP_NAV_HEADERS[1]:
                activity_page(selected_user, df)
        elif st.session_state["current_page"] == TOP_NAV_HEADERS[2]:
                timeline_page(selected_user, df)
        elif st.session_state["current_page"] == TOP_NAV_HEADERS[3]:
                feedback_page()
    except Exception as e:
         st.error(f"Error: {e}")
else:
     guidelines_page()
     
st.sidebar.text("Got an Error!?\nContact me at sanketsadadiya53@gmail.com")