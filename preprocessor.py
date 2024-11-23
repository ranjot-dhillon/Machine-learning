import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s\-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'usermessage': messages, 'message_date': dates})
    df['date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M - ')
    df = df.drop('message_date', axis=1)
    users = []
    messeges = []
    for i in df['usermessage']:
        entry = re.split('([\w\W]+?):\s', i)
        if entry[1:]:
            users.append(entry[1])
            messeges.append(entry[2])
        else:
            users.append('group notification')
            messeges.append(entry[0])
    df['user'] = users
    df['message'] = messeges
    df.drop(columns=['usermessage'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['day_name'] = df['date'].dt.day_name()

    period = []
    for hour in df[['day', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df