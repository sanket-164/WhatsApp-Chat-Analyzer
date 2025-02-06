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

def preprocess(data, date_format):
    pattern_2 = r"\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2}\s*-\s"

    try:

        data = "\n".join([convert_format1_to_format2(log) for log in data.split('\n')])

        messages = re.split(pattern_2, data)[1:]
        dates = re.findall(pattern_2, data)

        df = pd.DataFrame({'user_message': messages, 'message_date': dates})
        
        # '%m/%d/%y, %H:%M - '
        
        df['message_date'] = pd.to_datetime(df['message_date'], format=date_format)
        
        df.rename(columns={'message_date' : 'date'}, inplace = True)

        users = []
        messages = []

        for message in df['user_message']:
            entry = re.split('(.*?):\s', message)
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

        return df
    except Exception as e:
        return e