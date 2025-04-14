#!/usr/bin/env python
# coding: utf-8

# In[242]:


import requests
from bs4 import BeautifulSoup
from datetime import date
from datetime import time
from datetime import datetime,timedelta,timezone
import pandas as pd
import re
import os
from urllib.parse import unquote
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


# In[243]:


try:
    df_check = pd.read_csv("C:/stock_news_article/tb_all_news.csv")
    df_check
except:
    pass


# In[244]:


df_check.columns = ['key_id', 'category', 'title', 'detail','url','date_time','sentiment']
df_check


# In[262]:


dic_df = {'key_id':[],'category':[],'title':[],'detail':[],'url':[],'date_time':[]}


# In[263]:


driver = webdriver.Chrome() 
driver.get('https://www.hoonvision.com/?s=PTT')


# In[264]:


news_posts = driver.find_elements(By.XPATH, '//main/section[3]/div/div[*]')
print(str(len(news_posts)))


# In[265]:


check_list = df_check["url"].tolist()


# In[266]:


count = 0
for n in range(1,len(news_posts)+1):
    try:
        print(n)
        news_ctg = driver.find_element(By.XPATH,f'//main/section[3]/div/div[{str(n)}]/div[2]/div[1]').text
        news_title = driver.find_element(By.XPATH,f'//main/section[3]/div/div[{str(n)}]/div[2]/h3').text
        news_url = driver.find_element(By.XPATH,f'//main/section[3]/div/div[{str(n)}]/div[2]/h3/a').get_attribute('href')
        news_date = driver.find_element(By.XPATH,f'//main/section[3]/div/div[{str(n)}]/div[2]/div[2]/time').get_attribute('datetime')
#         print(news_ctg,news_title,news_url,news_date)
        
        #get_detail
        response = requests.get(news_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_paragraph = soup.find('div','entry-content').find_all('p')
        news_detail = ''
        for dt in news_paragraph:
            news_detail = news_detail +"\n"+ dt.get_text()
       
        if unquote(news_url) not in check_list:
            dic_df['key_id'].append(str(datetime.today()).replace('-','').replace(' ','').replace(':','').replace('.','')[:17])
            dic_df['category'].append(news_ctg)
            dic_df['title'].append(news_title)
            dic_df['detail'].append(news_detail)
            dic_df['url'].append(unquote(news_url))
            dic_df['date_time'].append(news_date)
            count += 1
            if count > 10 :
                break
    except Exception as e:
        print(e)
        pass
driver.quit()


# In[267]:


df = pd.DataFrame(dic_df)
df


# In[233]:


def edit_datetime(date_str):
    #to Thailand time
    dt_local = datetime.fromisoformat(date_str)
    return dt_local.astimezone(timezone.utc)

def clean_text(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  
        u"\U0001F300-\U0001F5FF"  
        u"\U0001F680-\U0001F6FF" 
        u"\U0001F1E0-\U0001F1FF"  
        u"\U00002500-\U00002BEF"  
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  
        u"\u3030"
        "]+", flags=re.UNICODE)
    
    text = emoji_pattern.sub(r'', text)
    text = re.sub(r'\n', ' ', text)  # Replace newlines with spaces
    text = re.sub(r'\s+', ' ', text)  # Collapse multiple spaces
    return text.strip()
def new_key(df,key):
    result = []
    for i in df.index:
        k = str(i).zfill(4)
        t = df[key][i][2:-2]
        result.append(f'{t}{k}')
    df[key] = result
    return df


# In[234]:


df_clean = df.copy()


# In[235]:


df_clean = new_key(df_clean,'key_id')
df_clean['category']= df_clean['category'].apply(clean_text)
df_clean['title']= df_clean['title'].apply(clean_text)
df_clean['detail'] = df_clean['detail'].apply(clean_text)
df_clean['date_time'] = df_clean['date_time'].apply(edit_datetime)


# In[236]:


df_clean


# In[237]:


df_sentiment = df_clean.copy()


# In[238]:


def sentiment_analysis(text):
    def extract_sentiment(data):
        return {
            "score": float(data['sentiment']['score']),  
            "polarity": data['sentiment']['polarity']
        }

    url = "https://api.aiforthai.in.th/ssense"

    params = {'text':text}

    headers = {
        'Apikey': "" # api key from aiforthai here
        }

    response = requests.get(url, headers=headers, params=params)
    result = extract_sentiment(response.json())
    
    return result


# In[239]:


df_sentiment['sentiment'] = df_sentiment['title'].apply(sentiment_analysis)


# In[240]:


df_sentiment


# In[241]:


df_export = df_sentiment.copy()
time_export = datetime.today()
time_export = str(time_export).replace(':','_').replace('.','_')
df_export.to_csv(f'C:/stock_news_article/hoonvision_{time_export}.csv',index=False,encoding='UTF-8')
#for checking duplicate news (act like database)
df_export.to_csv(f'C:/stock_news_article/tb_all_news.csv',index=False,encoding='UTF-8', mode='a',header=False)
print('load success')

