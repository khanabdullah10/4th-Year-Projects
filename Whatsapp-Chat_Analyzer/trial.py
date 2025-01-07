import re
import pandas as pd
def preprocess(data):
    f = open('WhatsApp Chat with 🧛🏻‍♀️🖤.txt', 'r', encoding='utf-8')
    data = f.read()

    # pattern = '\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{2}\s[ap]m'
    pattern = r'\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{2}\s[ap]m'
    messages = re.split(pattern, data)[1:]
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
        # entry = re.split('([\w\W]+?):\s', message)
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
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    return df







