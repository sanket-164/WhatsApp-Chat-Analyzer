import streamlit as st
import preprocess
import matplotlib.pyplot as plt
from constants import TRAFFIC_FILE_PATH, APP_NAME, TOP_NAV_HEADERS, DATETIME_FORMATS, DATETIME_FORMATS_PREPROCESS
from navigation import top_navbar

from guidelines import guidelines_page

from analysis.top_users import basic_page
from analysis.activity import activity_page
from analysis.timeline import timeline_page

from feedback import feedback_page

st.set_page_config(
    page_title=APP_NAME,
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None,
)

st.sidebar.title(APP_NAME)

traffic = {}

# Function to read and parse the file
def read_file(file_path):
    data = {}
    try:
        with open(file_path, "r") as file:
            for line in file:
                key, value = line.strip().split(": ")
                data[key] = int(value)
    except FileNotFoundError:
        # Initialize the file if not found
        data = {"Visits": 0, "Chats Analyzed": 0}
        write_file(file_path, data)
    return data

# Function to write updated data back to the file
def write_file(file_path, data):
    with open(file_path, "w") as file:
        for key, value in data.items():
            file.write(f"{key}: {value}\n")

# Read file
traffic = read_file(TRAFFIC_FILE_PATH)

if "new_user" not in st.session_state:
    st.session_state["new_user"] = True
    traffic["Visits"] = traffic["Visits"] + 1
    write_file(TRAFFIC_FILE_PATH, traffic)


uploaded_file = st.sidebar.file_uploader("Choose a txt chat file", type=['txt'], accept_multiple_files=False)

if uploaded_file is not None:
    try:
        selected_format = st.sidebar.selectbox(label="Date Format of your chat", placeholder="Date Time Format", options=DATETIME_FORMATS)

        if selected_format is not None and selected_format != DATETIME_FORMATS[0]:
            bytes_data = uploaded_file.getvalue()
            data = bytes_data.decode("utf-8")
            df = preprocess.preprocess(data, DATETIME_FORMATS_PREPROCESS[DATETIME_FORMATS.index(selected_format)])

            if "chat_file" not in st.session_state or st.session_state["chat_file"] != uploaded_file.name:
                st.session_state['chat_file'] = uploaded_file.name
                traffic["Chats Analyzed"] = traffic["Chats Analyzed"] + 1
                write_file(TRAFFIC_FILE_PATH, traffic)

            user_list = df['user'].unique().tolist()
            if 'group_notification' in user_list: 
                user_list.remove('group_notification')
            user_list.sort()
            user_list.insert(0, "All")

            selected_user = st.sidebar.selectbox("Select User", user_list)
            
            st.sidebar.header(f"{traffic["Visits"]} Visited")
            st.sidebar.header(f"{traffic["Chats Analyzed"]} Chat Analyzed")
            st.sidebar.text("Got an Error!?\nContact me at sanketsadadiya53@gmail.com")

            top_navbar()

            if st.session_state["current_page"] == TOP_NAV_HEADERS[0]:
                    basic_page(user_list, df)
            elif st.session_state["current_page"] == TOP_NAV_HEADERS[1]:
                    activity_page(selected_user, df)
            elif st.session_state["current_page"] == TOP_NAV_HEADERS[2]:
                    timeline_page(selected_user, df)
            elif st.session_state["current_page"] == TOP_NAV_HEADERS[3]:
                    feedback_page()
        else:
             st.title("Select Date Format of you chat from Sidebar")
    except Exception as e:
         st.error(f"Error: {e}")
else:
     guidelines_page()