import streamlit as st
import preprocessing, Action_methods
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    # Converting bytes data into string data
    data = bytes_data.decode("utf-8")
    df = preprocessing.preprocess(data)

    st.title("#DataFrame")
    st.dataframe(df)

    # build user list safely
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Select the User", user_list)

    if st.sidebar.button("Show analysis"):
        total_messages, total_words, num_media, num_links = Action_methods.fetch_stats(selected_user, df)

        # Stats area
        st.title("#Top Statistic")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(total_messages)
        with col2:
            st.header("Total Words")
            st.title(total_words)
        with col3:
            st.header("Media shared")
            st.title(num_media)
        with col4:
            st.header("Links shared")
            st.title(num_links)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = Action_methods.monthly_timeline(selected_user, df)
        if timeline is None or timeline.shape[0] == 0:
            st.write("No data for timeline.")
        else:
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'])
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)

    # Most Active user (only for Overall)
    if selected_user == 'Overall':
        st.title("Active user")
        x, new_df = Action_methods.fetch_most_busy_user(df)
        fig, ax = plt.subplots()
        col1, col2 = st.columns(2)
        with col1:
            ax.bar(x.index, x.values)
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)
        with col2:
            st.title("w.r.t %")
            st.dataframe(new_df)

    # Wordcloud
    st.title('#Wordcloud')
    try:
        df_wc = Action_methods.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
    except Exception as e:
        st.write("Could not create wordcloud:", e)

    # Most Common Words
    st.title('#MostCommonWords')
    most_common_df = Action_methods.most_common_words(selected_user, df)
    if most_common_df is None or most_common_df.shape[0] == 0:
        st.write("No words to display.")
    else:
        # robust access to first and second columns
        if 'word' in most_common_df.columns and 'count' in most_common_df.columns:
            labels = most_common_df['word']
            counts = most_common_df['count']
        else:
            labels = most_common_df.iloc[:, 0].astype(str)
            counts = most_common_df.iloc[:, 1].astype(int)

        fig, ax = plt.subplots()
        ax.bar(labels, counts)
        plt.xticks(rotation='vertical')
        plt.tight_layout()
        st.pyplot(fig)

    # Emoji analysis
    emoji_df = Action_methods.emoji_helper(selected_user, df)
    st.title("#EmojiAnalysis")
    col1, col2 = st.columns(2)
    with col1:
        if emoji_df is None or emoji_df.shape[0] == 0:
            st.write("No emojis found.")
        else:
            st.dataframe(emoji_df)

    with col2:
        if emoji_df is None or emoji_df.shape[0] == 0:
            st.write("No emoji chart to show.")
        else:
            # robust column handling: support both ['emoji','count'] or unnamed numeric columns
            if 'count' in emoji_df.columns and 'emoji' in emoji_df.columns:
                sizes = emoji_df['count']
                labels = emoji_df['emoji']
            else:
                # fallback to first two columns (whatever their names are)
                sizes = emoji_df.iloc[:, 1]
                labels = emoji_df.iloc[:, 0]

            # If there are too many emoji labels, you might want to limit them (optional)
            if len(sizes) > 30:
                sizes = sizes.iloc[:30]
                labels = labels.iloc[:30]

            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            plt.tight_layout()
            st.pyplot(fig)

    # Activity Map
    st.title('Activity Map')
    col1, col2 = st.columns(2)

    with col1:
        st.header("Most busy day")
        busy_day = Action_methods.week_activity_map(selected_user, df)
        if busy_day is None or busy_day.shape[0] == 0:
            st.write("No data.")
        else:
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)

    with col2:
        st.header("Most busy month")
        busy_month = Action_methods.month_activity_map(selected_user, df)
        if busy_month is None or busy_month.shape[0] == 0:
            st.write("No data.")
        else:
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values)
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)

    st.title("Weekly Activity Map")
    user_heatmap = Action_methods.activity_heatmap(selected_user, df)
    if user_heatmap is None or user_heatmap.shape[0] == 0:
        st.write("No heatmap data.")
    else:
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.heatmap(user_heatmap, ax=ax)
        plt.tight_layout()
        st.pyplot(fig)
