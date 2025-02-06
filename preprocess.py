import streamlit as st
import re
import pandas as pd
from datetime import datetime

def convert_format1_to_format2(text):
    format1_pattern = r"(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2})\s*([APMapm]{2}) - (.*?): (.*)"

    match = re.match(format1_pattern, text)
    if match:
        date_part, time_part, am_pm, user, message = match.groups()

        # Convert 12-hour format to 24-hour format
        time_str = f"{time_part} {am_pm}"
        time_24h = datetime.strptime(time_str, "%I:%M %p").strftime("%H:%M")

        # Reconstruct in Format 2
        return f"{date_part}, {time_24h} - {user}: {message}"
    
    return text  # If already Format 2, return as is

@st.cache_data
def preprocess(data):
    pattern_2 = r"\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2}\s*-\s"

    date_patterns = [
        ("%d/%m/%y, %H:%M - ", r"\d{1,2}/\d{1,2}/\d{2},\s*\d{1,2}:\d{1,2}\s*-\s"),
        ("%m/%d/%y, %H:%M - ", r"\d{1,2}/\d{1,2}/\d{2},\s*\d{1,2}:\d{1,2}\s*-\s"),
        ("%d/%m/%Y, %H:%M - ", r"\d{1,2}/\d{1,2}/\d{4},\s*\d{1,2}:\d{1,2}\s*-\s"),
        ("%m/%d/%Y, %H:%M - ", r"\d{1,2}/\d{1,2}/\d{4},\s*\d{1,2}:\d{1,2}\s*-\s"),
        # ("%y/%m/%d, %H:%M - ", r"\d{2}/\d{2}/\d{2},\s*\d{1,2}:\d{2}\s*-\s"),
        # ("%y/%d/%m, %H:%M - ", r"\d{2}/\d{2}/\d{2},\s*\d{1,2}:\d{2}\s*-\s"),
        # ("%Y/%d/%m, %H:%M - ", r"\d{4}/\d{2}/\d{2},\s*\d{1,2}:\d{2}\s*-\s"),
        # ("%Y/%m/%d, %H:%M - ", r"\d{4}/\d{2}/\d{2},\s*\d{1,2}:\d{2}\s*-\s"),
    ]

    try:        
        data = "\n".join([convert_format1_to_format2(log) for log in data.split('\n')])
        messages = re.split(pattern_2, data)[1:]
        dates = re.findall(pattern_2, data)

        df = pd.DataFrame({'user_message': messages, 'message_date': dates})
        print("Preprocessed called")

        for fmt, pattern in date_patterns:
            date_part = None, None
            for date_string in dates:
                match = re.search(pattern, date_string)
                if match:
                    date_part = match.group()
                    try:
                        datetime.strptime(date_part, fmt)
                    except ValueError:
                        date_part = None
                        break
                else:
                    date_part = None
                    break
            
            if date_part:
                print(f"New Detected format: {fmt}")
                df['message_date'] = pd.to_datetime(df['message_date'], format=fmt)
                break
        
        df.rename(columns={'message_date' : 'date'}, inplace = True)

        users = []
        messages = []

        for message in df['user_message']:
            entry = re.split(r'(.*?):\s', message)
            if entry[1:]:
                users.append(entry[1])
                messages.append(entry[2])
            else:
                users.append('group_notification')
                messages.append(entry[0])

        df['user'] = users
        df['message'] =  messages
        df.drop(columns=['user_message'], inplace=True)

        df['year'] = df['date'].dt.year
        df['month_num'] = df['date'].dt.month
        df['month'] = df['date'].dt.month_name()
        df['day'] = df['date'].dt.day
        df['day_name'] = df['date'].dt.day_name()
        df['hour'] = df['date'].dt.hour
        df['minute'] = df['date'].dt.minute

        st.session_state['preprocessed_data'] = df

        return df
    except Exception as e:
        return e