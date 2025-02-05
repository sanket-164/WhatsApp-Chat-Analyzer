import streamlit as st
from urlextract import URLExtract
import pandas as pd
import matplotlib.pyplot as plt

def basic_page(user_list, df):
    stats = []

    for user in user_list:
        user_stats = fetch_user_stats(user, df)
        stats.append([user, user_stats['num_messages'], user_stats['num_words'], user_stats['num_medias'], user_stats['num_links']])
        # st.header(f"{user_stats['num_messages']} Messages, {user_stats['num_words']} Words {user_stats['num_medias']} Shared Media, {user_stats['num_links']} Shared Links")

    stats_df = pd.DataFrame(stats, columns=["User", "Messages", "Words", "Media", "Links"])
    st.dataframe(stats_df, use_container_width=True)

    user_stats = stats_df.drop(stats_df[stats_df['User'] == 'All'].index)
    top_x = st.slider("Select Top X User", 1, len(user_list), len(user_list))

    for feature in user_stats.columns:
        if feature == 'User':
            continue
        
        col1, col2 = st.columns(2)
        
        top_user = user_stats.sort_values(by=feature, ascending=False).head(top_x)
        users = top_user['User']
        feature_count = top_user[feature]
        
        with col1:
            fig, axes = plt.subplots()
            axes.bar(users, feature_count)
            axes.set_title(f"Top {top_x} Users by {feature}")
            plt.ylabel(feature)
            st.pyplot(fig)

        with col2:
            fig, axes = plt.subplots()
            axes.pie(feature_count, labels=top_user['User'], autopct='%1.1f%%')
            axes.set_title(f"Top {top_x} Users by {feature}")
            st.pyplot(fig)


def fetch_stats(df):
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

    return {'num_messages': num_messagse, 'num_words': len(words), 'num_medias': num_media, 'num_links': len(links)}

def fetch_user_stats(selected_user, df):
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
    
    return {'num_messages': num_messagse, 'num_words': len(words), 'num_medias': num_media, 'num_links': len(links)}
