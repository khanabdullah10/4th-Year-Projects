import streamlit as st
import preprocessing,Action_methods
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    #Converting bytes data into string data
    data = bytes_data.decode("utf-8")
    df = preprocessing.preprocess(data)

    st.title("#DataFrame")
    st.dataframe(df)

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Select the User",user_list)

    if st.sidebar.button("Show analysis"):
        total_messages,total_words,num_media,num_links= Action_methods.fetch_stats(selected_user,df)

        #Stats area
        st.title("#TopStatistic")
        col1,col2,col3,col4 =  st.columns(4)
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
            st.header("links shared")
            st.title(num_links)

            # monthly timeline
            st.title("Monthly Timeline")
            timeline = Action_methods.monthly_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'], color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)




    #Most Active user
    if selected_user == 'Overall':
        st.title("Active user")
        x,new_df= Action_methods.fetch_most_busy_user(df)
        fig,ax = plt.subplots()

        col1,col2  = st.columns(2)
        with col1:
            ax.bar(x.index, x.values,color = 'red')
            #plt.xticks(rotation = 'Vertical')
            st.pyplot(fig)
        with col2:
            st.title("w.r.t %")
            st.dataframe(new_df)

    #wordcloud
    st.title('#Wordcloud')
    df_wc = Action_methods.create_wordcloud(selected_user,df)
    fig,ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

    #Most Common Words
    st.title('#MostCommonWords')
    most_common_df = Action_methods.most_common_words(selected_user, df)
    fig, ax = plt.subplots()
    ax.bar(most_common_df[0],most_common_df[1])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    #Emoji analysis
    emoji_df = Action_methods.emoji_helper(selected_user,df)
    st.title("#EmojiAnlysis")
    col1,col2  = st.columns(2)

    with col1:
        st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1],labels = emoji_df[0])
            st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = Action_methods.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = Action_methods.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = Action_methods.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)









