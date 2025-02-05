from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(selected_user, df):
    if selected_user != 'All':
        df = df[df['user'] == selected_user]

    # Fetch number of messages
    num_messagse = df.shape[0]

    # Fetch number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # Fetch number of media messages
    num_media = df[df['message'] == '<Media omitted>\n'].shape[0]

    # Fetch number of links
    extractor = URLExtract()
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messagse, len(words), num_media, len(links)

def active_users(df):
    x = df['user'].value_counts().head()
    new_df = round((df['user'].value_counts()/df.shape[0]) * 100, 2).reset_index().rename(columns={'user' : 'name', 'count': 'percentage'})
    return x, new_df

def used_words(selected_user, df):
    if selected_user != 'All':
        df = df[df['user'] == selected_user]

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    temp = df[df['user'] != 'group_notifications']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    common_words_df = pd.DataFrame(Counter(words).most_common(20))

    return common_words_df

def used_emojis(selected_user, df):
    if selected_user != 'All':
        df = df[df['user'] == selected_user]

    emojis = []

    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df =  pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def timeline(selected_user, df):
    if selected_user != 'All':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(f"{timeline['month_num'][i]}/{timeline['year'][i]}")

    timeline['time'] = time

    return timeline

def yearly_timeline(selected_user, selected_year, df):
    if selected_user != 'All':
        df = df[df['user'] == selected_user]
    
    df = df[df['year'] == selected_year]

    timeline = df.groupby(['month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(f"{timeline['month_num'][i]}")

    timeline['time'] = time

    return timeline

def monthly_timeline(selected_user, selected_year, selected_month, df):
    if selected_user != 'All':
        df = df[df['user'] == selected_user]

    df = df[df['year'] == selected_year]
    df = df[df['month'] == selected_month]

    timeline = df.groupby(['day']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(f"{timeline['day'][i]}")

    timeline['time'] = time

    return timeline

def year_activity_map(selected_user, df):
    if selected_user != 'All':
        df = df[df['user'] == selected_user]

    return df['year'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'All':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def week_activity_map(selected_user, df):
    if selected_user != 'All':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()