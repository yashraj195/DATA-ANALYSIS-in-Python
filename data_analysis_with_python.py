"""
**Data Analysis in Python**

**Data Exploration**
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv('streaming_service_data.csv', parse_dates=['join_date','last_active_date'])
df.describe()

df.head()

df.tail()

"""**Data Cleaning**"""

from datetime import datetime

df['last_active_date'].fillna(datetime.today(), inplace = True)

df['churn_flag'] = df['churn_flag'].astype(bool)

df['user_tenure'] = (pd.to_datetime(df['last_active_date']) - pd.to_datetime(df['join_date'])).dt.days

df.info()

"""**Data Visualization**"""

plt.figure(figsize = (8,5))
sns.countplot(x='subscription_type', data=df)
plt.title('Distribution of Subscription Types')
plt.show()

plt.figure(figsize = (8,5))
sns.histplot(df['total_watch_time'], bins = 20, kde = True)
plt.title('Distribution of Total Watch Time')
plt.show()

plt.figure(figsize = (8,5))
sns.boxplot(x = 'subscription_type', y ='total_watch_time', data = df)
plt.title('Total Watch Time by Substcription Type')
plt.show()

"""**Data Analysis - My favorite part **

1. What is the churn rate by subscrption type?
"""

churn_by_subscription = df.groupby('subscription_type')['churn_flag'].mean()
print(churn_by_subscription)

"""2. What is the average age of users by subscription type?"""

avg_age= df.groupby('subscription_type')['age'].mean()
print(avg_age)

"""3. How does user engagement vary by the number of devices used?"""

engagement_by_devices = df.groupby('num_devices')['total_watch_time'].mean()
print(engagement_by_devices)

"""4. Which favorite genre is most popular among users?"""

df['favorite_genre'].value_counts()

"""5. Calculate the retention rate for users who joined in different months?"""

df['join_month'] = pd.to_datetime(df['join_date']).dt.to_period('M')
cohort_data = df.groupby(['join_month','churn_flag']).size().unstack(fill_value=0)
cohort_data['retention_rate']= cohort_data[(False)] / (cohort_data[(False)] + cohort_data[(True)])
print(cohort_data[['retention_rate']])

"""6. Calculate the average user tenure for users who have been active for less than 6 months?"""

import datetime
new_users = df[df['join_date'] > (pd.Timestamp(datetime.date.today()) - datetime.timedelta(days=180))]
avg_tenure = new_users['user_tenure'].mean()
print(avg_tenure)

"""7. Can we identify the most popular subscription type among users who have churned?"""

churned_users = df[df['churn_flag'] == 1]
popular_subscription = churned_users['subscription_type'].value_counts().index[0]
print(popular_subscription)

"""-----------------------------------------------------------------------------------------------------End---------------------------------------------------------------------------------------------------"""
