import streamlit as st

import plots
import preprocessor
st.sidebar.title("whatsapp chat analyser")
uploaded_file=st.sidebar.file_uploader("choose a file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    st.dataframe(df)

    #fetch unique users
    user_list=df['user'].unique().tolist()
    user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0,"overall")

    selected_user=st.sidebar.selectbox("show user list",user_list)

    if st.sidebar.button("show Analysis"):
        col1,col2,col3,col4=st.columns(4)
        # number of words and messages and media and link sent
        num_message=plots.fetch_statstic(selected_user,df)
        total_words=plots.total_words(selected_user,df)
        total_media=plots.total_media(selected_user,df)
        total_link=plots.link(selected_user,df)

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