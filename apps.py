import streamlit as st
import plots
import preprocessor
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("whatsapp chat analyser")
uploaded_file = st.sidebar.file_uploader("choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    # st.dataframe(df)

    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0, "overall")

    selected_user = st.sidebar.selectbox("show user list", user_list)

    if st.sidebar.button("show Analysis"):
        st.title('Top Statistics')
        col1, col2, col3, col4 = st.columns(4)
        # number of words and messages and media and link sent
        num_message = plots.fetch_statstic(selected_user, df)
        total_words = plots.total_words(selected_user, df)
        total_media = plots.total_media(selected_user, df)
        total_link = plots.link(selected_user, df)

        with col1:
            st.header("Total message")
            st.title(num_message)

        with col2:
            st.header("Total Words")
            st.title(total_words)

        with col3:
            st.header("Media Shared")
            st.title(total_media)

        with col4:
            st.header("Link Shared")
            st.title(total_link)

        #Monthly Timeline
        timeline = plots.time_analysis(selected_user, df)
        st.title('Monthly Timeline')
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Timeline
        # st.title('Daily Timeline')
        # daily_timelines = plots.daily_timeline(selected_user, df)
        # fig, ax = plt.subplots()
        # ax.plot(daily_timelines['only_date'],daily_timelines['message'])
        # plt.xticks(rotation='vertical')
        # st.pyplot(fig)

        if selected_user == "overall":
            daily_timelines = plots.overall_daily_timeline(df)  # Use a copy to avoid modifying original DataFrame
        else:
            daily_timelines = plots.daily_timeline(selected_user, df)

        st.title('Daily Timeline')
        # daily_timelines = plots.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timelines['only_date'], daily_timelines['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)
        if selected_user == 'overall':
            busy_day = plots.overall_week_activity_map(df)
            busy_month = plots.overall_month_activity_map(df)
            user_heatmap = plots.overall_activity_heatmap(df)
        else:
            busy_day = plots.week_activity_map(selected_user, df)
            busy_month = plots.month_activity_map(selected_user, df)
            user_heatmap = plots.activity_heatmap(selected_user, df)

        with col1:
            st.header("Most busy day")
            # busy_day = plots.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            # busy_month = plots.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")

        # user_heatmap = plots.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap, vmin=0, vmax=1)
        st.pyplot(fig)

        #find user who do more chat

        if selected_user is 'overall':
            st.title('Most busy User')
            x, new_df = plots.busy_user(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        #create word cloud

        img = plots.create_cloud(selected_user, df)
        st.title("WordCloud")
        fig, ax = plt.subplots()
        ax = plt.imshow(img)
        st.pyplot(fig)

        #reoccurig words

        most_common = plots.most_used(selected_user, df)
        # st.dataframe(most_common)
        fig, ax = plt.subplots()
        ax.barh(most_common[0], most_common[1])
        # plt.xticks(rotation='vertical')
        st.title('Most common words')
        st.pyplot(fig)

        #emoji Analysis

        ndf = plots.emoji_analysis(selected_user, df)
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(ndf)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(ndf[1].head(), labels=ndf[0].head(), autopct="%0.2f")
            st.pyplot(fig)
#finished end by
