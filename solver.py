from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

def stats(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]

    words = []
    for message in df['message']:
        words.extend(message.split())

    num_messages = df.shape[0]

    num_media_msg=df[df['message']=='<Media omitted>\n'].shape[0]

    return num_messages, len(words),num_media_msg


def most_chatty_users(df):
    x = df['user'].value_counts().head().reset_index()
    x.rename(columns={'index': 'User', 'user': 'Message Count'}, inplace=True)
    df=round(((df['user'].value_counts()) / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'Name', 'user': 'percent'})
    return x,df

def createt_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    f = open('stop_hinkonkalishhhh.txt', 'r', encoding='utf-8')
    stop_words = f.read()

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stopwords(message):
        y =[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    temp['message']=temp['message'].apply(remove_stopwords)



    Wc=WordCloud(height=500,width=500,min_font_size=10,background_color='white')
    df_wc=Wc.generate(temp['message'].str.cat(sep=' '))
    return df_wc

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]

    total = df.groupby(['Year', 'Month_name', 'Month'])['message'].count().reset_index()
    time = []
    for i in range(len(total)):
        time.append(total['Month_name'][i] + '-' + str(total['Year'][i]))
    total['Time'] = time
    total=total.sort_values(by=['Year', 'Month'])
    return total


def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    daily=df.groupby('Date')['message'].count().reset_index()
    return daily

def day_activity(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    day_df=df['Day_name'].value_counts().reset_index()
    day_df.rename(columns={'index': 'Day', 'Day_name': 'Count'}, inplace=True)
    return day_df

def monthly_activity(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    monthly_df=df['Month_name'].value_counts().reset_index()
    monthly_df.rename(columns={'index': 'Month', 'Month_name': 'Count'}, inplace=True)
    return monthly_df


def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='Day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap

