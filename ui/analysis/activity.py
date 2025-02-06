import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import emoji

def activity_page(selected_user, df):
    # Busy users
    if selected_user == "All":
        st.title("Active users")
        x, most_users = active_users(df)
        
        col1, col2 = st.columns(2)

        with col1:
            fig, axes = plt.subplots()
            axes.bar(x.index, x.values)
            plt.ylabel("Messages")
            plt.xlabel("User")
            st.pyplot(fig)

        with col2:
            st.dataframe(most_users, use_container_width=True)

    # Acitivity map
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Yearly Activity")
        actve_year = year_activity_map(selected_user, df)
        fig, axes = plt.subplots()
        axes.bar(actve_year.index, actve_year.values)
        plt.xticks(rotation='vertical')
        plt.xlabel("Year")
        plt.ylabel("Messages")
        st.pyplot(fig)

    with col2:
        st.header("Monthly Activity")
        active_month = month_activity_map(selected_user, df)
        fig, axes = plt.subplots()
        axes.bar(active_month.index, active_month.values)
        plt.xticks(rotation='vertical')
        plt.xlabel("Month")
        plt.ylabel("Messages")
        st.pyplot(fig)

    with col3:
        st.header("Week Day Activity")
        active_day = week_activity_map(selected_user, df)
        fig, axes = plt.subplots()
        axes.bar(active_day.index, active_day.values)
        plt.xticks(rotation='vertical')
        plt.xlabel("Day")
        plt.ylabel("Messages")
        st.pyplot(fig)


    # Word analysis
    st.title("Words")
    common_words_df = used_words(selected_user, df)

    col1, col2 = st.columns([0.5, 0.5])

    with col1:
        st.dataframe(common_words_df, use_container_width=True)
        st.text("NOTE: Hover on table you will have a search icon on the top use it to search for your favourite words")
    with col2:
        fig, axes = plt.subplots()
        axes.barh(common_words_df.head(10)['Word'], common_words_df.head(10)['Count'])
        axes.set_title("Top 10 words")
        st.pyplot(fig)

    # Emoji analysis
    st.title("Emojis")
    emoji_df = used_emojis(selected_user, df)

    col1, col2 = st.columns([0.5, 0.5])

    with col1:
        st.dataframe(emoji_df, use_container_width=True)
        st.text("NOTE: Hover on table you will have a search icon on the top use it to search for your favourite emojis")
    with col2:
        fig, axes = plt.subplots()
        axes.barh(emoji_df.head(10)['Emoji'], emoji_df.head(10)['Count'])
        axes.set_title("Top 10 Emojis")
        st.pyplot(fig)

def active_users(df):
    x = df['user'].value_counts().head()
    new_df = round((df['user'].value_counts()/df.shape[0]) * 100, 2).reset_index().rename(columns={'user' : 'name', 'count': 'percentage'})
    return x, new_df

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

def used_words(selected_user, df):
    if selected_user != 'All':
        df = df[df['user'] == selected_user]

    f = open('utils/stop_hinglish.txt', 'r')
    stop_words = f.read()

    temp = df[df['user'] != 'group_notifications']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                if not emoji.is_emoji(word):
                    words.append(word)

    common_words_df = pd.DataFrame(Counter(words).most_common())

    return common_words_df.rename(columns={0: 'Word', 1: 'Count'})

def used_emojis(selected_user, df):
    if selected_user != 'All':
        df = df[df['user'] == selected_user]

    emojis = []

    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df =  pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df.rename(columns={0: 'Emoji', 1: 'Count'})
