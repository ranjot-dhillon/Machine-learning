#total meaagaes sent by user
def fetch_statstic(selected_user, df):
    if selected_user == 'overall':
        return df.shape[0]
    else:
        return df[df['user'] == selected_user].shape[0]


# total words sent by user
def total_words(selected_user, df):
    if selected_user == 'overall':
        word = []
        for i in df['message']:
            word.extend(i.split(' '))
        return len(word)
    else:
        new_df = df[df['user'] == selected_user]
        word = []
        for i in new_df['message']:
            word.extend(i.split(' '))
        return len(word)


# Total media sent by user

def total_media(selected_user, df):
    new_df = df[df['message'] == '<Media omitted>\n']
    if selected_user == 'overall':
        return new_df.shape[0]

    else:
        return new_df[new_df['user'] == selected_user].shape[0]


# Number of links

from urlextract import URLExtract

extract = URLExtract()


def link(selected_user, df):
    if selected_user == 'overall':
        link = []
        for msg in df['message']:
            link.extend(extract.find_urls(msg))
        return len(link)

    else:
        new_df = df[df['user'] == selected_user]
        link = []
        for msg in new_df['message']:
            link.extend(extract.find_urls(msg))
        return len(link)


# Most busy user

def busy_user(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'user': 'name', 'count': 'percentage'})
    return x, df


import pandas as pd

# create wordcloud

from wordcloud import WordCloud


def create_cloud(selected_user, df):
    file = open('stop_hinglish.txt', 'r')
    stop_word = file.read()
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    tem = df[df['user'] != 'group notification']
    tem = tem[tem['message'] != '<Media omitted>\n']

    def remove_stops_words(message):
        y = []
        for word in message.split():
            if word not in stop_word:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    tem['message'] = tem['message'].apply(remove_stops_words)
    df_wc = wc.generate(tem["message"].str.cat(sep=" "))
    return df_wc


from collections import Counter


# import pandas as pd


def most_used(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    tem = df[df['user'] != 'group notification']
    tem = tem[tem['message'] != '<Media omitted>\n']
    file = open('stop_hinglish.txt', 'r')
    stop_word = file.read()

    words = []
    for msg in tem['message']:
        for word in msg.split():
            if word not in stop_word:
                words.append(word)
    common_df = pd.DataFrame(Counter(words).most_common(20))
    return common_df


import emoji


def emoji_analysis(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    emojis = []
    for msg in df['message']:
        emojis.extend([c for c in msg if emoji.is_emoji(c)])

    ndf = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return ndf


# Time Analysis
def time_analysis(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline


# def daily_timeline(selected_user, df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
#
#     daily_timelines = df.groupby('only_date').count()['message'].reset_index()
#
#     return daily_timelines


# Week Activity

def week_activity_map(selected_user, df):
    df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()


def overall_week_activity_map(df):
    return df['day_name'].value_counts()


def overall_month_activity_map(df):
    return df['month'].value_counts()


def month_activity_map(selected_user, df):
    df = df[df['user'] == selected_user]
    return df['month'].value_counts()


def overall_activity_heatmap(df):
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap


def activity_heatmap(selected_user, df):
    df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap


def daily_timeline(selected_user, df):
    df = df[df['user'] == selected_user]
    daily_timelines = df.groupby('only_date').count()['message'].reset_index()

    return daily_timelines


def overall_daily_timeline(df):
    daily_timelines = df.groupby('only_date').count()['message'].reset_index()

    return daily_timelines
