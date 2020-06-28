#!/usr/bin/env python
# coding: utf-8

# Krishan Kumar Pandey

# # Project 2:Investigate a Dataset (TMDb Movie Data)

# In this project we are going to do general data analysis of data provided to us with the help of python libraries like numpy,pandas and matplotlib.

# # Table of Contents:

# 1.Introduction
# 
# 2.Data Wrangling
# 
# 3.Exploratory Data Analysis
# 
# 4.Conclusions

# # 1.Introduction

# ### About Dataset:

#  In this project I have chosen TMDb movie data set for data analysis process. It has the details of around 10000 movies.
#  I will analyse this data set on the basis of few questions.

# ### Questions:

# 1. Find the movie name which has highest runtime?
# 
# 2. How many movies have runtime less than 2hrs.(120 min) and greater than 2hrs ?
# 
# 3. Year of highest and lowest number of movie release?
# 
# 4. Get 5 directors with highest directed movies?
# 
# 5. What is maximum and minimum vote average?
# 
# 6. Name the movies with maximum and minimum vote average?
# 
# 7. Movies having vote average less than or equal to 5 and greater than 5?
# 
# 8. What is the vote average of most popular movie?
# 
# 9. Find the revenue of highest budget movie?
# 
# 10. Revenue of Most Popular movie?

# In[1]:


#first of all import the required libraries before going on the next phase of data analysis.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np


# # 2.Data Wrangling

# In this section i will load in the data, check for cleanliness, and then trim and clean  dataset for analysis.

# ### General Properties

# In[2]:


#loading data(CSV file) using pandas library 
df_tmdb=pd.read_csv("tmdb-movies.csv")


# In[3]:


#the sumerized information about dataset
df_tmdb.info()


# In[4]:


#First 3 rows of the dataset to take a glimpse of dataset.
df_tmdb.head(3)


# In[5]:


#last 3 rows of the dataset
df_tmdb.tail(3)


# In[6]:


#there are too many columns and some are hidden
#let's dig out each column.
df_tmdb.columns


# In[7]:


#the statistical summary of the data 
df_tmdb.describe()


# ### Data Cleaning(Removing Unwanted Data )

# First we will look at the missing values in the data set

# In[8]:


#to get the missing values in the columns.
df_tmdb.isna().sum()


# we can see that 'homepage ','tagline','overview','production_companies' has very large number of missing values.

# #### Steps To Delete Or Modify The dataset

# 1.Remove the unused columns and rows(if necessary) with missing values.
# 
# 2.Remove duplicate rows from the dataset.
# 
# 3.Change format if necessary.
# 
# 4.Treatment of outliers

# #### 1.Remove the unused columns  with missing values.

# Since few columns which are not usable in the data analysis process.columns are: imdb_id, keywords, homepage,tagline,overview and budget_adj,revenue_adj has huge number of 0 values so we can drop it. So these are the columns that are not involved in the analysis process.

# In[9]:


#removing the unused columns using drop() function.
df_tmdb.drop(['overview','imdb_id','homepage','tagline','budget_adj','revenue_adj','keywords','production_companies'],axis =1,inplace = True)


# In[10]:


#check rows and columns again
#we are left with 13 columns now.
df_tmdb.shape


# In[11]:


df_tmdb.head()


# #### 2. Remove duplicate rows from dataset

# In[12]:


#duplicated() function return the duplicate row as True and False
#To count the duplicate elements we use sum() function.
sum(df_tmdb.duplicated())


# In[13]:


# using drop_duplicates() function we can remove duplicate rows.
df_tmdb.drop_duplicates(inplace = True)


# #### 3. Change format if necessary

# Due to the string fromat of 'release_date' column. we will have to change the format.

# In[14]:


#changing the format or datatype of column.
df_tmdb['release_date'] = pd.to_datetime(df_tmdb['release_date'])


# In[15]:


#head to verify the apllied funcution.
df_tmdb['release_date'].head(2)


# #### 4.Getting rid of missing values in rows

# since cast, director,genre are important columns and have missing values we should remove the coresponding rows

# In[16]:


#use dropna function to remove the missing vlaues
df_tmdb=df_tmdb.dropna()


# In[17]:


#again recheck the missing values to varify.
df_tmdb.isna().sum()


# #### 4.Treatment of Outliers

# Since the columns 'revenue','runtime' and 'budget' has outliers we need to treat them with mean, median, mode or if necessary delete the data

# In[18]:


#plotting boxplot for revenue to see the frequency of outliers
plt.figure(figsize=(15,5))
sns.boxplot(
    data=df_tmdb['revenue'],
    color='red')
plt.ylabel('revenue in million dollors')
plt.xlabel('label')
plt.title('To find Outliers')
plt.show()


# with boxplot we can analyse that there is significant number of outliers and droping all of them will reduce our scope of analysis. therfore we will try to sort this problem with statistical models

# In[19]:


#calculating outlier i.e 0 in revenue column
df_tmdb[df_tmdb['revenue']==0].count()['id']


# In[20]:


#replace function is used to make 0 to NAN value and further dealing with nan values will be easy
df_tmdb=df_tmdb.replace(0,np.NaN)


# In[21]:


#fill all the value of nan with mean()
df_tmdb.fillna(df_tmdb.mean())


# So we are done with all the introduction and data wrangling process the next step is Exploratory Data Analysis(EDA).In this section we will try to analyse our clean data with few questions.

# # 3.Exploratory Data Analysis

# ### Research Question 1:Find the movie name which has highest runtime?

# In[58]:


#using function to DRY:Do not repeat 
def max_function(column_name):
    return df_tmdb[column_name].max()


# In[59]:


#using function for 'runtime'
max_function('runtime')


# In[23]:


#now find out the movie name  coresposnding to maximum runtime value
df_tmdb[df_tmdb['runtime']==max_runtime]['original_title']


# ### Research Question 2: How many movies have runtime less than 2hrs.(120 min) and greater than 2hrs ?

# In[84]:


#greater_function is used to calculate greater values while comparing with other data
def greater_function(column_name,value):
    return df_tmdb[df_tmdb[column_name]>value].count()['id']


# In[85]:


#apply on rruntime column
greater_function('runtime',120)


# In[86]:


#lessfunction is used to calculate lesser or equal to given values while comparing with other data
def less_function(column_name,value):
    return df_tmdb[df_tmdb[column_name]<=value].count()['id']


# In[87]:


#applied on runtime column
less_function('runtime',120)


# In[88]:


#visualizing and comparing the length of the movie using bar graph
fig = plt.figure()
ax = fig.add_axes([0,0,0.5,1])
length = ['less_than120', 'g_than120']
counts = [less_function('runtime',120),greater_function('runtime',120)]
ax.bar(length,counts)
plt.title('Different Runtime Comparisions')
plt.xlabel('Runtime')
plt.ylabel('Total movies')
plt.show()


# we can observe that the movies having less than or equal to 120 min is the standard movie runtime

# ### Research Question 3: Year of highest and lowest number of movie release?

# In[27]:


#Groupby fucntion is used to get yearwise movie release
highest=df_tmdb.groupby('release_year').count()['id']
print(highest.head())


# In[71]:


#visualizing the comparision
highest.plot(xticks = np.arange(1960,2016,4))
sns.set(rc={'figure.figsize':(10,5)})
plt.title("Year Vs No. of Movies",fontsize = 14)
plt.xlabel('year of release',fontsize = 13)
plt.ylabel('Number Of Movies',fontsize = 15)
sns.set_style("whitegrid")


# In[72]:


#analysis of release year using histogram
df_tmdb['release_year'].hist()
plt.show()


# Year 1961 has 31(lowest) and 2014 has 700(highest) numbers of movie released.
# 
# The trend shows that the release of movies every year is inceasing.

# ### Research Question 4: Get 5 directors with highest directed movies?

# In[29]:


#using groupby fucntion to count the total number of movies directed by each director
#using sort_values fucntion to sort in descending order
director_name=df_tmdb.groupby('director')['id'].count().sort_values(ascending=False).iloc[:5]


# In[30]:


#getting top 5 directors with directed movies
print(director_name)


# ### Research Question 5: What  is maximum and minimum vote average?

# In[60]:


#max_funtion is used to calculate the maximum of vote average
print("maximum vote average:",max_function('vote_average'))


# In[61]:


#a min_func function is made to calculate the minimum value
def min_function(column_name):
    return df_tmdb[column_name].min()


# In[62]:


print("minimum vote average:",min_function('vote_average'))


# ### Research Question 6: Name the movies with maximum and minimum vote average?

# In[74]:


#movie having maximum vote average
df_tmdb[df_tmdb['vote_average']==max_function('vote_average')]['original_title']


# In[75]:


#movies with minimum vote average
df_tmdb[df_tmdb['vote_average']==min_function('vote_average')]['original_title']


# There are two movies which have same minimum rating(1.5)

# ### Research Question 7:Movies having vote average less than or equal to 5 and greater than 5?

# In[91]:


#Movies vote average greater than 5
print("Number of Movies with rating greater than 5:",greater_function('vote_average',5))


# In[92]:


#Movies vote average less than or equal to 5
print("Number of Movies with rating less than or equal to 5:",less_function('vote_average',5))


# In[93]:


#visualizing the rating less than or equal to 5 and greater than 5
fig = plt.figure()
ax = fig.add_axes([0,0,0.5,1])
Number = ['less_than5', 'g_than5']
counts = [less_function('vote_average',5),greater_function('vote_average',5)]
ax.bar(Number,counts)
plt.title('rating and counts')
plt.xlabel('Rating')
plt.ylabel('Total movies')
plt.show()


# Movies with rating greater than 5 has frequency higher than movies rating less than or equal to 5. It shows that directors are well aware of delivering quality content among the audience

# ### Research Question 8: What is the vote average of most popular movie?

# In[63]:


#get the vote average of popular movie
df_tmdb[df_tmdb['popularity']==max_function('popularity')]['vote_average']


# In[64]:


#visualizing the data using scatter plot
x = df_tmdb['vote_average']
y = df_tmdb['popularity']

plt.scatter(x, y)
plt.xlabel("Vote Average")
plt.ylabel("Popularity")
plt.title("Vote_Average vs popularity")
plt.show()


# Movies having rating greater than 5 seems to be very popular

# ### Research Question 9: Find the revenue of highest budget movie?

# In[66]:


#getting revenue of highest budget movie
df_tmdb[df_tmdb['budget']==max_function('budget')]['revenue']


# ### Research Question 10: Revenue of Most Popular movie?

# In[68]:


#get revenue of most popular movie
df_tmdb[df_tmdb['popularity']==max_function('popularity')]['revenue']


# # 4.Conclusions

# 1. The movie 'The Story of Film: An Odyssey' has runtime 900 min.This is because many parts are counted together.

# 2. Movie length less than or equal to 2hrs is the ideal length for production.

# 3. Year 1961 has 31(lowest) and 2014 has 700(highest) numbers of movie released. This is because of evolution in technologies and public demand has raised the production of more movies year to year 

# 4. According to dataset Woody Allen has directed maximum movies (45) so far.

# 5. The Story of Film: An Odyssey has the maximum vote average (9.2) whereas Transmorphers and  Manos: The Hands of Fate has the lowest rating(1.5). It shows that people are interested in quality content.

# 6. Most popular movie has the rating 6.5 and revenue earned is 1513528810($).

# 7. Movie with highest budget had earned (11087569)($).

# #### Limitations

#  1.This study has limitations of dealing with NaN values.It affects the process of data analysis.
#  NAN values limit our scope of exploration when they are in significant amount.
#  Sometimes deleting all these makes our data monotonous.
#  
#  2.The data given to us was sufficient but columns containing outliers made the analysis less interesting. 
#  
#  This is how i conclude my General Data analysis of Movie data set!

# In[ ]:




