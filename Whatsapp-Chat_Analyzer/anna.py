import re
import pandas as pd

f= open('chatwmayank.txt','r',encoding='utf-8')

data= f.read()

#print(data)

pattern = r'\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{2}\s[ap]m'

messages = re.split(pattern, data) [1:]
messages

dates= re.findall(pattern, data)
dates

df= pd.DataFrame({'user_messages':messages, 'message_date': dates})
#convert message_data type
df['message_data'] = pd.to_datetime(df['message_date'], format= '%d/%m/%Y, %I:%M %p')

df.rename(columns={'message_date': 'date'}, inplace=True)

print(df.head())
