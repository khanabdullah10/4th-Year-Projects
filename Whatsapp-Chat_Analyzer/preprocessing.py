import re
import pandas as pd
def preprocess(data):
    # this regular expression indicatee
    pattern = r'\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{2}\s[ap]m'

    # seperating the messages format(ie. user and its conceptual messages) into a list
    messages = re.split(pattern, data)[1:]
    # extracting the dates
    dates = re.findall(pattern, data)

    # creating data frame of two seperate columns
    df = pd.DataFrame({'messages_date': dates, 'user_messages': messages})

    # converting date fromat type
    df['messages_date'] = pd.to_datetime(df['messages_date'], format='%d/%m/%Y, %I:%M %p')
    df.rename(columns={'messages_date': 'date'}, inplace=True)

    # seperating  user and thier messages
    users = []
    messages = []
    for message in df['user_messages']:
        entry = re.split(r'([^:]+):\s', message)
        #entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])
    # creating new column
    df['user'] = users
    df['message'] = messages
    # deleting the previous column that  has user and messages in one column
    df.drop(columns=['user_messages'], inplace=True)

    # Extracting the year form the 'date' column by using dt.year attribute and placing it into a seperate column name 'year'
   # df['year'] = df['date'].dt.year
    #df['month'] = df['date'].dt.month_name()
   # df['day'] = df['date'].dt.day
    #df['hour'] = df['date'].dt.hour
    #df['minute'] = df['date'].dt.minute

    #return df
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df




