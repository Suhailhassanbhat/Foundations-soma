#!/usr/bin/env python
# coding: utf-8

# # Using APIs/Data Structures
# Using the Dark Sky Forecast API at https://developer.forecast.io/, generate a sentence that describes the weather that day.
# 
# Right now it is TEMPERATURE degrees out and SUMMARY. Today will be TEMP_FEELING with a high of HIGH_TEMP and a low of LOW_TEMP. RAIN_WARNING.
# 
# TEMPERATURE is the current temperature
# 
# SUMMARY is what it currently looks like (partly cloudy, etc - it's "summary" in the dictionary). Lowercase, please.
# 
# TEMP_FEELING is whether it will be hot, warm, cold, or moderate. You will probably use HIGH_TEMP and your own thoughts and feelings to determine this.
# 
# HIGH_TEMP is the high temperature for the day.
# LOW_TEMP is the low temperature for the day.
# 
# RAIN_WARNING is something like "bring your umbrella!" if it is going to rain at some point during the day.
# You can take a look at the documentation, but "current" contains the current conditions and the first element of "daily" is for the current day. But you knew that, right?!
# 
# Feel free to steal your old code! I bet that trying to read it will make you depressed and teaches you the value of naming variables.
# 
# Once you've accomplished that part, use Mailgun to send yourself an email every morning at 8AM telling you the sentence. The subject line of the email should be something like "8AM Weather forecast: January 1, 1970."
# 
# Dates are obtained by doing something like this, using http://strftime.org/ as a reference:
# 
# import datetime
# right_now = datetime.datetime.now()
# date_string = right_now.strftime("%Y-%M")
# 
# BONUS: List the forecasted temperatures as the day goes on.
# 
# BONUS: Set the timezone on your server so emails go out at the right time.

# In[1]:


import requests
import pandas as pd


# In[2]:


from dotenv import load_dotenv
load_dotenv('/Users/suhailbhat/Desktop/foundations/Foundations-soma/env')
import os

get_ipython().system('touch .env')


# In[3]:


DARKSKY_API_KEY = os.getenv('DARKSKY_API_KEY')


# In[4]:


import os

os.getenv('DARKSKY_API_KEY')


# In[5]:


response =requests.get(f'https://api.darksky.net/forecast/{DARKSKY_API_KEY}/40,-73')
data = response.json()
data


# In[6]:


TEMPERATURE = data['currently']['temperature']
SUMMARY = data['currently']['summary'].lower()
TEMP_FEELING = data['currently']['apparentTemperature']
HIGH_TEMP = data['daily']['data'][0]['temperatureHigh']
LOW_TEMP = data['daily']['data'][0]['temperatureLow']
RAIN_WARNING = data['daily']['data'][0]['summary'].lower()

if "rain" in "RAIN_WARNING":
    RAIN_WARNING = "Likely to rain today"
else:
    RAIN_WARNING = "Unlikely to rain today."


# In[7]:


weather_update = f'Right now it is {TEMPERATURE} degrees out and {SUMMARY}. Today will be {TEMP_FEELING} with a high of {HIGH_TEMP} and a low of {LOW_TEMP}. {RAIN_WARNING}'


# In[8]:


import datetime
right_now = datetime.datetime.now()
date_string = right_now.strftime("%Y-%M")


# In[9]:


import datetime

date = datetime.datetime.utcfromtimestamp(data['daily']['data'][0]["time"])
# my_time = datetime.datetime.utcfromtimestamp(data['daily']['data'][0]["time"] + 3600 * 4) 
my_time = data['daily']['data'][0]["time"] + 3600 * 4
my_time
date


# In[10]:


response = requests.get(f'https://api.darksky.net/forecast/{DARKSKY_API_KEY}/40,-73,{my_time}')
data2 = response.json()
data2


# In[11]:


hour_list = []

for hour in data2['hourly']['data'][4:21]:
    hour_dic = {}
    
    hour_dic["time"] = datetime.datetime.utcfromtimestamp(hour["time"]).strftime("%H:%M")
    hour_dic["Temperature"] = hour['temperature']
    hour_dic["summary"] = hour["summary"]
    
    
    hour_list.append(hour_dic)
    
    


# In[12]:


df = pd.DataFrame(hour_list)
hourly_weather = df[["time", "Temperature", "summary"]]
hourly_weather.to_csv("hourly_weather.csv", index = False)


# In[13]:


weather_update = f'Right now it is {TEMPERATURE} degrees out and {SUMMARY}. Today will be {TEMP_FEELING} with a high of {HIGH_TEMP} and a low of {LOW_TEMP}. {RAIN_WARNING}'
weather_update


# In[14]:


f'8 AM Weather forecast: {date.strftime("%B")} {date.day}, {date.year}'


# In[15]:


print(weather_update)
print(hourly_weather)


# In[ ]:




