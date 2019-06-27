#!/usr/bin/env python
# coding: utf-8

# # Tutorial 1

# ## Week 1

# ### 1) Import the cell cycle dataset excel spreadsheet (using Pandas). You may need to do some tidying of the data such as dropping rows with missing NaN values.

# In[3]:


# Importing necessary libraries and Cell-Cycle-Set.xlsx dataset
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df=pd.read_excel('Cell-Cycle-Set.xlsx')
df.head()


# In[4]:


# Exploring dataset characteristics
df.shape


# In[5]:


df.dtypes


# In[6]:


df.info()


# In[7]:


#Making each column of the dataset have the same number of rows (deleting not a number values and duplicates)

# Alternatively clean = df.dropna()
df.dropna(inplace=True)
df.head()


# In[8]:


# Checking dataset properties after having cleaned the original version

df.shape


# In[9]:


df.info()


# In[10]:


# Checking for duplicates

df.duplicated()


# ### 2) Perform exploratory analysis of the data, thus:
# 
# #### 1) Generate a histogram of one of the cell cycle stages of the RNA and protein distribution. Do you notice anything interesting with regards to the mean/variance of the distribution?

# $$\textbf{Answer}= $$ In all the RNA distributions cases the mean was equal to around 11 and the variance to around 2. Instead in the Protein cases the mean was equal to 25 (apart from the case of the S-stage m=22) and the variance around 10. Both the RNA and protein cases resemble a gaussian distribution. In all cases the Protein mean and variance is greater than in the RNA counterpart. (One RNA can produce multiple protein genes)

# In[11]:


# mean_RNA_G1 (blue) and mean_protein_G1 (orange) Histogram representation
x = df["mean_RNA_G1"]
plt.hist(x)
mean1 = np.mean(df["mean_RNA_G1"])
print("mean_RNA_G1 =", mean1)
variance1 = np.var(df["mean_RNA_G1"])
print("variance_RNA_G1 =", variance1)
x = df["mean_protein_G1"]
plt.hist(x)
plt.title('mean_RNA_G1 (blue) and mean_protein_G1 (orange)');
mean2 = np.mean(df["mean_protein_G1"])
print("mean_protein_G1= ", mean2)
variance2 = np.var(df["mean_protein_G1"])
print("variance_protein_G1=", variance2)


# In[12]:


# mean_RNA_S (blue) and mean_protein_S (orange) histogram representation
x2 = df["mean_RNA_S"]
plt.hist(x2)
mean3 = np.mean(df["mean_RNA_S"])
print("mean_RNA_S =", mean3)
variance3 = np.var(df["mean_RNA_S"])
print("variance_RNA_S =", variance3)
x2 = df["mean_protein_S"]
plt.hist(x2)
plt.title('mean_RNA_S (blue) and mean_protein_S (orange)');
mean4 = np.mean(df["mean_protein_S"])
print("mean_protein_S = ", mean4)
variance4 = np.var(df["mean_protein_S"])
print("variance_protein_S =", variance4)


# In[13]:


# mean_RNA_G2 (blue) and mean_protein_G2 (orange) histogram representation
x3 = df["mean_RNA_G2"]
plt.hist(x3)
mean5 = np.mean(df["mean_RNA_G2"])
print("mean_RNA_G2 =", mean5)
variance5 = np.var(df["mean_RNA_G2"])
print("variance_RNA_G2 =", variance5)
x3 = df["mean_protein_G2"]
plt.hist(x3)
plt.title('mean_RNA_G2 (blue) and mean_protein_G2 (orange)');
mean6 = np.mean(df["mean_protein_G2"])
print("mean_protein_G2 = ", mean6)
variance6 = np.var(df["mean_protein_G2"])
print("variance_protein_G2 =", variance6)


# #### 2) Look at the pairwise correlations between each of the RNA/protein columns (this can be achieved using the corr() function). Does the change in timestep have much effect on the relationship(s) between RNA and protein?

# $$\textbf{Answer}= $$ The change in timestep does not cause any overall effect. If there is any change, in the grand scheme of things they cancel out. The correlation value considering two times the same element is equal to 1 (table main diagonal, the elements are the same therefore correlation is maximum). Correlations between RNA and RNA values during different cell sphases gives values close to 1 (very high correlation). Correlations between protein and protein values during different cell sphases gives values close to 1 (very high correlation). Correlations between RNA and protein values (or protein and RNA) during different or same cell sphases gives values close to 0.5 (low correlation). 
# 
# Correlation between mean_RNA_G1 and mean_protein_G1 = 0.522657733063862
# <br>
# Correlation between mean_RNA_S and mean_protein_S = 0.5361902686743043
# <br>
# Correlation between mean_RNA_G2 and mean_protein_G2 = 0.5325650185250103
# <br>
# <br>
# There are two different ways to calculate correlation = Springer and Pearson (the difference between the two is that one assumes the data can be fitted with a linear model)
# 
# We can use the same model generated at on one stage to make prediction on the other stages (there is now nmuch change in correlation between the different stages)

# In[14]:


# Looking at the table, increasing the time-steps does not cause substantial changes in correlation
df.corr()


# In[15]:


# Calculating 
# 1) Correlation between mean_RNA_G1 and mean_protein_G1
# 2) Correlation between mean_RNA_S and mean_protein_S
# 3) Correlation between mean_RNA_G2 and mean_protein_G2

print("Correlation between mean_RNA_G1 and mean_protein_G1 =", df["mean_RNA_G1"].corr(df["mean_protein_G1"]))
print("Correlation between mean_RNA_G1 and mean_protein_G1 considering just the first 50 elements=", 
      (df["mean_RNA_G1"].loc[0:50]).corr(df["mean_protein_G1"].loc[0:50]))
print("Correlation between mean_RNA_G1 and mean_protein_G1 considering just the first 100-200 index elements=", 
      (df["mean_RNA_G1"].loc[100:200]).corr(df["mean_protein_G1"].loc[100:200]))
print("Correlation between mean_RNA_G1 and mean_protein_G1 considering just the first 250-350 index elements=", 
      (df["mean_RNA_G1"].loc[250:350]).corr(df["mean_protein_G1"].loc[250:350]))

print("\n")

print("Correlation between mean_RNA_S and mean_protein_S =", df["mean_RNA_S"].corr(df["mean_protein_S"]))
print("Correlation between mean_RNA_S and mean_protein_S considering just the first 50 elements=", 
      (df["mean_RNA_S"].loc[0:50]).corr(df["mean_protein_S"].loc[0:50]))
print("Correlation between mean_RNA_S and mean_protein_S considering just the first 100-200 index elements=", 
      (df["mean_RNA_S"].loc[100:200]).corr(df["mean_protein_S"].loc[100:200]))
print("Correlation between mean_RNA_S and mean_protein_S considering just the first 250-350 index elements=", 
      (df["mean_RNA_S"].loc[250:350]).corr(df["mean_protein_S"].loc[250:350]))

print("\n")

print("Correlation between mean_RNA_G2 and mean_protein_G2 =", df["mean_RNA_G2"].corr(df["mean_protein_G2"]))
print("Correlation between mean_RNA_G2 and mean_protein_G2 considering just the first 50 elements=", 
      (df["mean_RNA_G2"].loc[0:50]).corr(df["mean_protein_G2"].loc[0:50]))
print("Correlation between mean_RNA_G2 and mean_protein_G2 considering just the first 100-200 index elements=", 
      (df["mean_RNA_G2"].loc[100:200]).corr(df["mean_protein_G2"].loc[100:200]))
print("Correlation between mean_RNA_G2 and mean_protein_G2 considering just the first 250-350 index elements=", 
      (df["mean_RNA_G2"].loc[250:350]).corr(df["mean_protein_G2"].loc[250:350]))


# #### 3) Generate a scatterplot of the RNA versus protein for each cell cycle stage. Fit a linear model to the data, can we infer protein concentration from RNA concentration?

# $$\textbf{Answer}= $$ In all the considered cases (G1,S and G2 phases), when trying to fit a linear model to the data we don't get very good results. That because, as seen in the previous section, there is a low correlation between RNA and proteins values (around 0.5). 
# <br>
# <br>
# When trying to fit a straight line to the data, we can only get good results if the data variables are all strongly correlated each other (either positively or negatively). If there is a low variables correlation, then there will be some outlier values in the data that can't be captured using a straight line.
# <br>
# <br>
# That's quite interesting to observe, especially considering that historically, RNA concentration was used to infer protein concentration. The outlier values (the values that are further away from the straight line), are particularly important in determining cell phases characteristics.

# In[16]:


# Making a scatter plot of mean_RNA_G1 vs mean_protein_G1 and then finding the best fit line to describe the data
plt.figure(figsize=(8,6))
plt.scatter(df["mean_RNA_G1"], df["mean_protein_G1"], color='r', linestyle='dashed', marker='3',alpha = 0.6)
plt.title('mean_RNA_G1 vs mean_protein_G1')
plt.xlabel('mean_RNA_G1')
plt.ylabel('mean_protein_G1')
# Fit a line to the data
plt.plot(np.unique(df["mean_RNA_G1"]), np.poly1d(np.polyfit(df["mean_RNA_G1"], 
                                                            df["mean_protein_G1"], 1))(np.unique(df["mean_RNA_G1"])))
plt.show()


# In[17]:


# Making a scatter plot of mean_RNA_S vs mean_protein_S and then finding the best fit line to describe the data
plt.figure(figsize=(8,6))
plt.scatter(df["mean_RNA_S"], df["mean_protein_S"], color='r', linestyle='dashed', marker='3',alpha = 0.6)
plt.title('mean_RNA_S vs mean_protein_S')
plt.xlabel('mean_RNA_S')
plt.ylabel('mean_protein_S')
# Fit a line to the data
plt.plot(np.unique(df["mean_RNA_S"]), np.poly1d(np.polyfit(df["mean_RNA_S"], 
                                                            df["mean_protein_S"], 1))(np.unique(df["mean_RNA_S"])))
plt.show()


# In[18]:


# Making a scatter plot of mean_RNA_G2 vs mean_protein_G2 and then finding the best fit line to describe the data
plt.figure(figsize=(8,6))
plt.scatter(df["mean_RNA_G2"], df["mean_protein_G2"], color='r', linestyle='dashed', marker='3',alpha = 0.6)
plt.title('mean_RNA_G2 vs mean_protein_G2')
plt.xlabel('mean_RNA_G2')
plt.ylabel('mean_protein_G2')
# Fit a line to the data
plt.plot(np.unique(df["mean_RNA_G2"]), np.poly1d(np.polyfit(df["mean_RNA_G2"], 
                                                            df["mean_protein_G2"], 1))(np.unique(df["mean_RNA_G2"])))
plt.show()


# In[19]:


# Alternative way to fit a line to the data
from numpy.polynomial.polynomial import polyfit

# Sample data
x = df["mean_RNA_G2"]
y = df["mean_protein_G2"]

# Fit with polyfit
b, m = polyfit(x, y, 1)

plt.figure(figsize=(8,6))
plt.plot(x, y, '.')
plt.plot(x, b + m * x, '-')
plt.xlabel('mean_RNA_G2')
plt.ylabel('mean_protein_G2')
plt.show()


# # Week 2

# ## 1) Find all genes that contain 'cell cycle' in their GOBP term and plot them as a scatterplot (with different colour) overlaid across all genes for each cell cycle phase. Is there a stronger/weaker correlation?

# $$\textbf{Answer}= $$ When superimposing mean_RNA_G1 vs mean_protein_G1 with the elements of mean_RNA_G1 and mean_protein_G1 containing 'cell cycle' in their GOBP term it can be noticed quite a strong positive correlation between the considered features. The same can be obesrved when considering mean_RNA_S vs mean_protein_S and mean_RNA_G2 vs mean_protein_G2. 
# <br>
# <br>
# The elements of mean_RNA_G1 and mean_protein_G1 containing 'cell cycle' in their GOBP represents quite well the overall trend of the data contained by mean_RNA_G1 vs mean_protein_G1. (Same for mean_RNA_S vs mean_protein_S and mean_RNA_G2 vs mean_protein_G2).
# <br>
# <br>
# Although, that doesn't enable us to describe the elements of mean_RNA_G1 and mean_protein_G1 containing 'cell cycle' in their GOBP using a straight line (the data is too sparse, too many outliers) (Same for mean_RNA_S vs mean_protein_S and mean_RNA_G2 vs mean_protein_G2).
# <br>
# <br>
# When comparing the different cell stages (G1,S,G2), it can be noticed that the distance between each of the point is almost the same in all the cases, there is just a scaling factor that varies when comparing the different cell phases.

# In[20]:


# Finding all genes that contain 'cell cycle' in their GOBP term
cellcgobp = df[df.GOBP.str.contains('cell cycle')]
print("Number of genes containging 'cell cycle' in their GOBP term =", len(cellcgobp))
cellcgobp.GOBP.head()


# In[21]:


# Superimposing mean_RNA_G1 vs mean_protein_G1 with the elements of mean_RNA_G1 and mean_protein_G1 containing 'cell cycle'
# in their GOBP term
plt.figure(figsize=(8,6))
plt.scatter(df['mean_RNA_G1'], df['mean_protein_G1'], color='b', linestyle='dashed', marker='3',alpha = 0.6)
plt.scatter(cellcgobp.mean_RNA_G1, cellcgobp.mean_protein_G1, color='g', linestyle='dashed', marker='3',alpha = 1)
plt.xlabel('mean_RNA_G1')
plt.ylabel('mean_protein_G1')


# In[22]:


# Superimposing mean_RNA_S vs mean_protein_S with the elements of mean_RNA_S and mean_protein_S containing 'cell cycle'
# in their GOBP term
plt.figure(figsize=(8,6))
plt.scatter(df['mean_RNA_S'], df['mean_protein_S'], color='b', linestyle='dashed', marker='3',alpha = 0.6)
plt.scatter(cellcgobp.mean_RNA_S, cellcgobp.mean_protein_S, color='g', linestyle='dashed', marker='3',alpha = 1)
plt.xlabel('mean_RNA_S')
plt.ylabel('mean_protein_S')


# In[23]:


# Superimposing mean_RNA_G2 vs mean_protein_G2 with the elements of mean_RNA_G2 and mean_protein_G2 containing 'cell cycle'
# in their GOBP term
plt.figure(figsize=(8,6))
plt.scatter(df['mean_RNA_G2'], df['mean_protein_G2'], color='b', linestyle='dashed', marker='3',alpha = 0.6)
plt.scatter(cellcgobp.mean_RNA_G2, cellcgobp.mean_protein_G2, color='g', linestyle='dashed', marker='3',alpha = 1)
plt.xlabel('mean_RNA_G2')
plt.ylabel('mean_protein_G2')


# In[24]:


print("Correlation between mean_RNA_G1 and mean_protein_G1 =", df["mean_RNA_G1"].corr(df["mean_protein_G1"]))
print("Correlation between mean_RNA_S and mean_protein_S =", df["mean_RNA_S"].corr(df["mean_protein_S"]))
print("Correlation between mean_RNA_G2 and mean_protein_G2 =", df["mean_RNA_G2"].corr(df["mean_protein_G2"]))

print("Correlation between mean_RNA_G1 and mean_protein_G1 containing 'cell cycle' in their GOBP term =", 
      cellcgobp.mean_RNA_G1.corr(cellcgobp.mean_protein_G1))
print("Correlation between mean_RNA_S and mean_protein_S containing 'cell cycle' in their GOBP term =", 
      cellcgobp.mean_RNA_S.corr(cellcgobp.mean_protein_S))
print("Correlation between mean_RNA_G2 and mean_protein_G2 containing 'cell cycle' in their GOBP term =", 
      cellcgobp.mean_RNA_G2.corr(cellcgobp.mean_protein_G2))


# ## 2) Repeat task 1 by finding genes that contain 'ribosome' in their GOCC term.

# $$\textbf{Answer}= $$ When superimposing mean_RNA_G1 vs mean_protein_G1 with the elements of mean_RNA_G1 and mean_protein_G1 containing 'ribosome' in their GOCC term it can be noticed that there are just 19 corrisponding cells. Because of this, there are not enough features to fully understand if there is a strong corraltion. The same can be obesrved when considering mean_RNA_S vs mean_protein_S and mean_RNA_G2 vs mean_protein_G2. 
# <br>
# <br>
# When comparing the different cell stages (G1,S,G2), it can be noticed that the distance between each of the point is almost the same in all the cases, there is just a scaling factor that varies when comparing the different cell phases.
# <br>
# <br>
# That doesn't enable us to describe the elements of mean_RNA_G1 and mean_protein_G1 containing 'ribosome' in their GOCC using a straight line (the data is too sparse, and there are not enough data-points) (Same for mean_RNA_S vs mean_protein_S and mean_RNA_G2 vs mean_protein_G2).

# In[25]:


# Finding all genes that contain 'ribosome' in their GOBP term
ribgocc = df[df.GOCC.str.contains('ribosome')]
print("Number of genes containging 'ribosome' in their GOCC term =", len(ribgocc))
ribgocc.GOCC.head()


# In[26]:


# Superimposing mean_RNA_G1 vs mean_protein_G1 with the elements of mean_RNA_G1 and mean_protein_G1 containing 'ribosome'
# in their GOCC term
plt.figure(figsize=(8,6))
plt.scatter(df['mean_RNA_G1'], df['mean_protein_G1'], color='y', linestyle='dashed', marker='3',alpha = 0.6)
plt.scatter(ribgocc.mean_RNA_G1, ribgocc.mean_protein_G1, color='b', linestyle='dashed', marker='3',alpha = 1)
plt.xlabel('mean_RNA_G1')
plt.ylabel('mean_protein_G1')


# In[27]:


# Superimposing mean_RNA_S vs mean_protein_S with the elements of mean_RNA_S and mean_protein_S containing 'ribosome'
# in their GOCC term
plt.figure(figsize=(8,6))
plt.scatter(df['mean_RNA_S'], df['mean_protein_S'], color='y', linestyle='dashed', marker='3',alpha = 0.6)
plt.scatter(ribgocc.mean_RNA_S, ribgocc.mean_protein_S, color='b', linestyle='dashed', marker='3',alpha = 1)
plt.xlabel('mean_RNA_S')
plt.ylabel('mean_protein_S')


# In[28]:


# Superimposing mean_RNA_G2 vs mean_protein_G2 with the elements of mean_RNA_G2 and mean_protein_G2 containing 'ribosome'
# in their GOCC term
plt.figure(figsize=(8,6))
plt.scatter(df['mean_RNA_G2'], df['mean_protein_G2'], color='y', linestyle='dashed', marker='3',alpha = 0.6)
plt.scatter(ribgocc.mean_RNA_G2, ribgocc.mean_protein_G2, color='b', linestyle='dashed', marker='3',alpha = 1)
plt.xlabel('mean_RNA_G2')
plt.ylabel('mean_protein_G2')


# In[29]:


print("Correlation between mean_RNA_G1 and mean_protein_G1 =", df["mean_RNA_G1"].corr(df["mean_protein_G1"]))
print("Correlation between mean_RNA_S and mean_protein_S =", df["mean_RNA_S"].corr(df["mean_protein_S"]))
print("Correlation between mean_RNA_G2 and mean_protein_G2 =", df["mean_RNA_G2"].corr(df["mean_protein_G2"]))

print("Correlation between mean_RNA_G1 and mean_protein_G1 containing 'ribosome' in their GOCC term =", 
      ribgocc.mean_RNA_G1.corr(ribgocc.mean_protein_G1))
print("Correlation between mean_RNA_S and mean_protein_S containing 'ribosome' in their GOCC term =", 
      ribgocc.mean_RNA_S.corr(ribgocc.mean_protein_S))
print("Correlation between mean_RNA_G2 and mean_protein_G2 containing 'ribosome' in their GOCC term =", 
      ribgocc.mean_RNA_G2.corr(ribgocc.mean_protein_G2))


# ## 3) Count the number of occurrences of every GOBP term across all genes, what are some of the difficulties that arise when using these terms?

# $$\textbf{Answer}= $$ It might have been better to have used a readme file or a legend attached to this dataset (Cell-Cycle-Set.xlsx) in order to make clear the meaning and the implications of all the terms used. This would in fact make easier for the public to make use of this data-set and would avoid the use of repetitive words across all the description terms.

# In[30]:


print(df.GOBP.str.split(';',expand=True).stack().value_counts())


# ## 4) Calculate the change in mRNA/protein level across the cell cycle by taking the difference at each stage (G1-S, S-G2, G2-G1), and standardize the differences by mean-centering and variance scaling. Repeat tasks 1 and 2 by plotting the changes in levels with GOBP/GOCC labelling. What do we notice about changes in the cell cycle? Is there any apparent clustering of GO terms?

# $$\textbf{Answer}= $$ Now all the graphs are centred around 0. 
# <br>
# <br>
# When superimposing mean_RNA_g1s vs mean_protein_g1s with the elements of mean_RNA_g1s and mean_protein_g1s containing 'cell cycle' in their GOBP term and 'ribosome' in their GOCC term we can see: 
# <br>
# 1) mean_RNA_g1s and mean_protein_g1s form a clear clouster centered around 0 (in blue)
# <br>
# 2) the elements of mean_RNA_g1s and mean_protein_g1s containing 'cell cycle' in their GOBP term form another clouster (in green) centered at X=0 and Y=3.
# <br>
# 3) the elements of mean_RNA_g1s and mean_protein_g1s containing 'ribosome' in their GOCC term form another clouseter (in yellow) centred at X=0 and Y=2.6/2.7.
# <br>
# <br>
# When superimposing mean_RNA_sg2 vs mean_protein_sg2 with the elements of mean_RNA_sg2 and mean_protein_sg2 containing 'cell cycle' in their GOBP term and 'ribosome' in their GOCC term we can see: 
# <br>
# 1) mean_RNA_sg2 and mean_protein_sg2 form a clear clouster centered around 0 (in blue) (the blue clouster has some big outliers values)
# <br>
# 2) the elements of mean_RNA_sg2 and mean_protein_sg2 containing 'cell cycle' in their GOBP term form another clouster (in green) centered at X=0 and Y=-3.
# <br>
# 3) the elements of mean_RNA_sg2 and mean_protein_sg2 containing 'ribosome' in their GOCC term form another clouseter (in yellow) centred at X=0 and Y=-2.6/2.7. (the yellow clouser is more compact than the green one)
# <br>
# <br>
# When superimposing mean_RNA_g2g1 vs mean_protein_g2g1 with the elements of mean_RNA_g2g1 and mean_protein_g2g1 containing 'cell cycle' in their GOBP term and 'ribosome' in their GOCC term we can see: 
# <br>
# 1) mean_RNA_g2g1 and mean_protein_g2g1 form a clear clouster centered around 0 (in blue)
# <br>
# 2) the elements of mean_RNA_g2g1 and mean_protein_g2g1 containing 'cell cycle' in their GOBP term form another clouster (in green) centered at X=0 and Y=0 (smaller dimensions than the blue clouster).
# <br>
# 3) the elements of mean_RNA_g2g1 and mean_protein_g2g1 containing 'ribosome' in their GOCC term form another clouseter (in yellow) centred at X=0 and Y=0 (smaller dimensions than the blue clouster and more compact than the green clouster).
# <br>
# <br>
# During each different cell cycle the blue clouster position remains unaltered but the green and yellow clousters change alsways their position

# In[31]:


# Calculating the change in mRNA/protein level across the cell cycle by taking the difference at each stage (G1-S,S-G2,G2-G1), 
# and standardizing the differences by mean-centering and veriance scaling

from sklearn import preprocessing

df['mean_RNA_g1s'] = (df.mean_RNA_G1 - df.mean_RNA_S)
df['mean_RNA_sg2'] = (df.mean_RNA_S - df.mean_RNA_G2)
df['mean_RNA_g2g1'] = (df.mean_RNA_G2 - df.mean_RNA_G1)
df['mean_protein_g1s'] = (df.mean_protein_G1 - df.mean_protein_S)
df['mean_protein_sg2'] = (df.mean_protein_S - df.mean_protein_G1)
df['mean_protein_g2g1'] = (df.mean_protein_G2 - df.mean_protein_G1)

print("Dataset mean before standardizing and normalizing the data")
print(df.mean())
print("\nDataset variance before standardizing and normalizing the data")
print(df.std())

mean_RNA_G1 = preprocessing.scale(df["mean_RNA_G1"])
mean_RNA_S = preprocessing.scale(df["mean_RNA_S"])
mean_RNA_G2 = preprocessing.scale(df["mean_RNA_G2"])
mean_protein_G1 = preprocessing.scale(df["mean_protein_G1"])
mean_protein_S = preprocessing.scale(df["mean_protein_S"])
mean_protein_G2 = preprocessing.scale(df["mean_protein_G2"])
mean_RNA_g1s = preprocessing.scale(df["mean_RNA_g1s"])
mean_RNA_sg2 = preprocessing.scale(df["mean_RNA_sg2"])
mean_RNA_g2g1 = preprocessing.scale(df["mean_RNA_g2g1"])
mean_protein_g1s = preprocessing.scale(df["mean_protein_g1s"])
mean_protein_sg2 = preprocessing.scale(df["mean_protein_sg2"])
mean_protein_g2g1 = preprocessing.scale(df["mean_protein_g2g1"])

print("\nSome exaples of Dataset after having been standardized and normalized:")
print("1) mean_protein_G2\n",mean_protein_G2.mean())
print("",mean_protein_G2.std())
print("2) mean_RNA_G1\n",mean_RNA_G1.mean())
print("",mean_RNA_G1.std())
print("3) mean_protein_g1s\n",mean_protein_g1s.mean())
print("",mean_protein_g1s.std())

# Alternative way to standardise and normilize data
# from sklearn.preprocessing import StandardScaler
# ss = StandardScaler()
# scaled = ss.fit_transform(df[["mean_RNA_G1","mean_RNA_S","mean_RNA_G2","mean_protein_G1","mean_protein_S",
#                                     "mean_protein_G2","mean_RNA_g1s","mean_RNA_sg2","mean_RNA_g2g1","mean_protein_g1s",
#                                    "mean_protein_sg2", "mean_protein_g2g1"]])
# print(scaled.mean(),scaled.std())


# In[32]:


# Superimposing mean_RNA_g1s vs mean_protein_g1s with the elements of mean_RNA_g1s and mean_protein_g1s containing 'cell cycle'
# in their GOBP term and 'ribosome' in their GOCC term
plt.figure(figsize=(8,6))

cellcgobp = df[df.GOBP.str.contains('cell cycle')]
ribgocc = df[df.GOCC.str.contains('ribosome')]

plt.scatter(mean_RNA_g1s, mean_protein_g1s, color='b', linestyle='dashed', marker='3',alpha = 0.6, label='mRNA/protein level')
plt.scatter(cellcgobp.mean_RNA_g1s, cellcgobp.mean_protein_g1s, color='g', linestyle='dashed', marker='3',alpha = 1, 
            label='GOBP')
plt.scatter(ribgocc.mean_RNA_g1s, ribgocc.mean_protein_g1s, color='y', linestyle='dashed', marker='3',alpha = 1, 
            label='GOCC')
plt.xlabel('mean_RNA_g1s')
plt.ylabel('mean_protein_g1s')
plt.legend(loc="best")


# In[33]:


# Superimposing mean_RNA_sg2 vs mean_protein_sg2 with the elements of mean_RNA_sg2 and mean_protein_sg2 containing 'cell cycle'
# in their GOBP term and 'ribosome' in their GOCC term
plt.figure(figsize=(8,6))

cellcgobp = df[df.GOBP.str.contains('cell cycle')]
ribgocc = df[df.GOCC.str.contains('ribosome')]

plt.scatter(mean_RNA_sg2, mean_protein_sg2, color='b', linestyle='dashed', marker='3',alpha = 0.6, label='mRNA/protein level')
plt.scatter(cellcgobp.mean_RNA_sg2, cellcgobp.mean_protein_sg2, color='g', linestyle='dashed', marker='3',alpha = 1, 
           label='GOBP')
plt.scatter(ribgocc.mean_RNA_sg2, ribgocc.mean_protein_sg2, color='y', linestyle='dashed', marker='3',alpha = 1, 
           label='GOCC')
plt.xlabel('mean_RNA_sg2')
plt.ylabel('mean_protein_sg2')
plt.legend(loc="lower right")


# In[34]:


# Superimposing mean_RNA_g2g1 vs mean_protein_g2g1 with the elements of mean_RNA_g2g1 and mean_protein_g2g1 containing 
# 'cell cycle' in their GOBP term and 'ribosome' in their GOCC term
plt.figure(figsize=(8,6))

cellcgobp = df[df.GOBP.str.contains('cell cycle')]
ribgocc = df[df.GOCC.str.contains('ribosome')]

plt.scatter(mean_RNA_g2g1, mean_protein_g2g1, color='b', linestyle='dashed', marker='3',alpha = 0.6,label='mRNA/protein level')
plt.scatter(cellcgobp.mean_RNA_g2g1, cellcgobp.mean_protein_g2g1, color='g', linestyle='dashed', marker='3',alpha = 1, 
           label='GOBP')
plt.scatter(ribgocc.mean_RNA_g2g1, ribgocc.mean_protein_g2g1, color='y', linestyle='dashed', marker='3',alpha = 1, 
           label='GOCC')
plt.xlabel('mean_RNA_g2g1')
plt.ylabel('mean_protein_g2g1')
plt.legend(loc="lower right")


# ## EXTRA: Finding clustering/correlations by using other terms in GOBP, GOMF or GOCC

# In[35]:


# Superimposing mean_RNA_g1s vs mean_protein_g1s with the elements of mean_RNA_g1s and mean_protein_g1s containing 
# 'binding' in their GOMF term and 'cellular metabolic process' in their GOBP term
plt.figure(figsize=(8,6))

bindgomf = df[df.GOMF.str.contains('binding')]
cmpgobp = df[df.GOBP.str.contains('cellular metabolic process')]
print("Number of genes containging 'binding' in their GOMF term =", len(bindgomf))
print(bindgomf.GOCC.head())
print("\n")
print("Number of genes containging 'cellular metabolic process' in their GOMF term =", len(cmpgobp))
print(cmpgobp.GOBP.head())

plt.scatter(mean_RNA_g1s, mean_protein_g1s, color='b', linestyle='dashed', marker='3',alpha = 0.6,label='mRNA/protein level')
plt.scatter(bindgomf.mean_RNA_g1s, bindgomf.mean_protein_g1s, color='g', linestyle='dashed', marker='3',alpha = 1, 
           label='GOMF')
plt.scatter(cmpgobp.mean_RNA_g1s, cmpgobp.mean_protein_g1s, color='y', linestyle='dashed', marker='3',alpha = 1, 
           label='GOBP')
plt.xlabel('mean_RNA_g2g1')
plt.ylabel('mean_protein_g2g1')
plt.legend(loc="lower right")


# In[36]:


# Superimposing mean_RNA_sg2 vs mean_protein_sg2 with the elements of mean_RNA_sg2 and mean_protein_sg2 containing 
# 'binding' in their GOMF term and 'cellular metabolic process' in their GOBP term
plt.figure(figsize=(8,6))

plt.scatter(mean_RNA_sg2, mean_protein_sg2, color='b', linestyle='dashed', marker='3',alpha = 0.6,label='mRNA/protein level')
plt.scatter(bindgomf.mean_RNA_sg2, bindgomf.mean_protein_sg2, color='g', linestyle='dashed', marker='3',alpha = 1, 
           label='GOMF')
plt.scatter(cmpgobp.mean_RNA_sg2, cmpgobp.mean_protein_sg2, color='y', linestyle='dashed', marker='3',alpha = 1, 
           label='GOBP')
plt.xlabel('mean_RNA_g2g1')
plt.ylabel('mean_protein_g2g1')
plt.legend(loc="lower right")


# In[38]:


# Superimposing mean_RNA_g2g1 vs mean_protein_g2g1 with the elements of mean_RNA_g2g1 and mean_protein_g2g1 containing 
# 'binding' in their GOMF term and 'cellular metabolic process' in their GOBP term
plt.figure(figsize=(8,6))

plt.scatter(mean_RNA_g2g1, mean_protein_g2g1, color='b', linestyle='dashed', marker='3',alpha = 0.6,label='mRNA/protein level')
plt.scatter(bindgomf.mean_RNA_g2g1, bindgomf.mean_protein_g2g1, color='g', linestyle='dashed', marker='3',alpha = 1, 
           label='GOMF')
plt.scatter(cmpgobp.mean_RNA_g2g1, cmpgobp.mean_protein_g2g1, color='y', linestyle='dashed', marker='3',alpha = 1, 
           label='GOBP')
plt.xlabel('mean_RNA_g2g1')
plt.ylabel('mean_protein_g2g1')
plt.legend(loc="lower right")

