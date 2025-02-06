import streamlit as st
import matplotlib.pyplot as plt

def timeline_page(selected_user, df):
    # Timeline analysis
    all_timeline = timeline(selected_user, df)
    st.title("Timeline")

    fig, axes = plt.subplots()
    axes.plot(all_timeline['time'], all_timeline['message'])
    plt.xticks(rotation='vertical')
    plt.ylabel("Messages")
    plt.xlabel("Month/Year")
    st.pyplot(fig)

    col1, col2 = st.columns(2)
    selected_year = ""
    selected_month = ""

    with col1:
        st.header("Year")
        
        selected_year = st.selectbox("Select Year", df['year'].unique().tolist())
        year_timeline = yearly_timeline(selected_user, selected_year, df)
        
        fig, axes = plt.subplots()
        axes.plot(year_timeline['time'], year_timeline['message'])
        plt.ylabel("Messages")
        plt.xlabel("Month")
        st.pyplot(fig)

    with col2:
        st.header("Month")
        
        selected_month = st.selectbox("Select Month", df[df['year'] == selected_year]['month'].unique().tolist())
        month_timeline = monthly_timeline(selected_user, selected_year, selected_month, df)

        fig, axes = plt.subplots()
        axes.plot(month_timeline['time'], month_timeline['message'])
        plt.xticks(rotation='vertical')
        plt.ylabel("Messages")
        plt.xlabel("Date")
        st.pyplot(fig)

    # from_year = st.selectbox("Select Year", df['year'].unique().tolist())
    # from_month = st.selectbox("Select Year", df['month'].unique().tolist())
    # to_year = st.selectbox("Select Year", df['year'].unique().tolist())
    # to_month = st.selectbox("Select Year", df['month'].unique().tolist())
    

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