#!/usr/bin/env python
# coding: utf-8

# # Tutorial 2

# ## Week 3-5

# ### 1) Write a program to implement Needleman-Wunsch for proteins

# #### Importing blosum50 scoring matrix

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Importing blosum50 scoring matrix, adding column and row headers
header = ['A', 'R', 'N', 'D', 'C', 'Q','E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
df=pd.read_csv('blosum50.txt', delim_whitespace = True, names = header, index_col = False)
df.rename(index = dict(zip(range(len(header)),header)),inplace =True)
df.head(21)


# In[2]:


m = 11
n = 8

# Creating a table to run HEAGAWGHEE versus PAWHEAE
h = [' ', 'H', 'E', 'A', 'G', 'A', 'W','G', 'H', 'E', 'E']
header2 = [' ','P', 'A', 'W', 'H', 'E', 'A','E']
df1 = pd.DataFrame(data=[[np.zeros(3)]*m]*n)
df1.rename(index = dict(zip(range(len(header2)),header2)),inplace =True)
df1.rename(columns=dict(zip(range(len(h)),h)), inplace = True)

df1


# In[3]:


# Filling the Global Allignment Table (array in row-colum pair)
#Forward Pass

cost = -8 # Cost of insertion or delition

# Calculating price of substitution when arrows moves diagonally
def blos(r, c):
    cname = df1.columns[c]
    rname = df1.index[r]
    if r == 0 or c == 0:
        return np.nan # Handling nan error when filling first row/column
    else:
        return int(df[rname][cname]) + int(df1.iloc[r-1,c-1][0])

arrow =[]

# Loop to fill the table, deciding between if the upelement, leftelement or the diagelement gives us less loss.
for r in range(0,8):
    for c in range(0,11):
        upelement = int(df1.iloc[r-1,c][0]) + cost if r >= 1 else np.nan # Handling nan error when filling first row/column
        leftelement = int(df1.iloc[r,c-1][0]) + cost if c >= 1 else np.nan # Handling nan error when filling first row/column
        diagelement = blos(r, c)
        if r == 0 and c == 0:
            upelement = 0
        list1 = np.array([diagelement, upelement,leftelement])
        re = np.nanargmax(list1)
        # Storing the location of the selected max element to find arrow direction during the backward pass
        if list1[re] == diagelement:
            vec = [r-1,c-1]
            arrow.extend([r-1,c-1, r,c])
        elif list1[re] == upelement:
            vec = [r-1,c]
            arrow.extend([r-1,c, r,c])
        elif list1[re] == leftelement:
            vec = [r,c-1]
            arrow.extend([r,c-1, r,c])
        # Storing value, row and column coordinates in an array for each row-column pair in the table
        df1.iloc[r,c] = np.array([list1[re], vec[0], vec[1]])
    
df1


# In[4]:


# Filling the Global Allignment Table (integer in row-column pair)
#Forward Pass

cost = -8 # Cost of insertion or delition

# Calculating price of substitution when arrows moves diagonally
def blos(r, c):
    cname = df1.columns[c]
    rname = df1.index[r]
    if r == 0 or c == 0:
        return np.nan # Handling nan error when filling first row/column
    else:
        return int(df[rname][cname]) + int(df1.iloc[r-1,c-1])

arrow =[]

# Loop to fill the table, deciding between if the upelement, leftelement or the diagelement gives us less loss.
for r in range(0,8):
    for c in range(0,11):
        upelement = int(df1.iloc[r-1,c]) + cost if r >= 1 else np.nan # Handling nan error when filling first row/column
        leftelement = int(df1.iloc[r,c-1]) + cost if c >= 1 else np.nan # Handling nan error when filling first row/column
        diagelement = blos(r, c)
        if r == 0 and c == 0:
            upelement = 0
        list1 = np.array([diagelement, upelement,leftelement])
        # Storing the max integer in row-column pair to fill table
        re = np.nanargmax(list1)
        df1.iloc[r,c] = list1[re]
        # Storing the location of the selected max element and of the corrisponding added element
        # to find arrow direction during the backward pass
        if list1[re] == diagelement:
            arrow.extend([r-1,c-1, r,c])
        elif list1[re] == upelement:
            arrow.extend([r-1,c, r,c])
        elif list1[re] == leftelement:
            arrow.extend([r,c-1, r,c])
    
df1


# In[5]:


# Backward pass

# Making empty lists where to append the backward pass elements and the two strings
back = []
letter1 = []
letter2 = []

# Starting from the last column-row pair in the table
K = arrow[len(arrow)-1] # Storing it's column coordinate
M = arrow[len(arrow)-1-1] # Storing it's row coordinate
h1 = arrow[len(arrow)-1-2] # Storing the column coordinate where the arrow in the block element is pointing at
h2 = arrow[len(arrow)-1-3] # Storing the row coordinate where the arrow in the block element is pointing at
back.append(df1.iloc[r,c]) # Storing the element corrisponding to the M,K coordinates
letter1.append(df1.index[r]) # Storing the letter corrisponding to the M row to form the string
letter2.append(df1.columns[c]) # Storing the letter corrisponding to the K column to form the string

i = len(arrow) -5 # Looping throgh all the arrow array apart from all the initialization elements done in these lines above

while i > 0:
    if ((h1 <= arrow[i-2]) and (h2 <= arrow[i-3])): # If there are duplicates or coordinates that moves forwards
                                                    # in the arrow array, skip them
        i -=2
    elif ((arrow[i] == h1) and (arrow[i-1] == h2)): # If while going through the array we find the coordinates the element we  
                                                    # are in is pointing at, store its value in the back list and store the new 
                                                    # coorrdinates this new element is pointing at. Finally, find the 
                                                    # corrispondent row/column letter of the letter and store its value. If
                                                    # respect to the previous element the row number changes and the column not, 
                                                    # add - in the first string instead of the letter. If respect to the  
                                                    # previous element the column number changes and the row not, add - in   
                                                    # the second string instead of the letter. Otherwise add the letters to both
            K = arrow[i]
            M = arrow[i-1]
            h1 = arrow[i-2]
            h2 = arrow[i-3]
            back.append(df1.iloc[M,K])
            if i>5:                                # If we are too close to the end of the array, skip adding letters (letters
                                                   # are stored each time one iteration in advance)        
                if((K==h1) and (M!=h2)):
                    letter2.append('-')
                    letter1.append(df1.index[M])
                elif((K!=h1) and (M==h2)):
                    letter1.append('-')
                    letter2.append(df1.columns[K])
                else:
                    letter1.append(df1.index[M])
                    letter2.append(df1.columns[K])
            i -=4                                  # Once we store these 4 erray elements, we can skip them in the next loop
                                                   # iteration to avoid duplicates
    else:
        i -=1 # If no corrispondence if found go ahead to the next array element

back = np.asarray(back)
print(letter2[::-1]) # Reversing the string letter order
print(letter1[::-1]) # Reversing the string letter order
print(back)


# In[6]:


# Creating a table to Match the protein sequence SALPQPTTPVSSFTSGSMLGRTDTALTNTYSAL with PSPTMEAVTSVEASTASHPHSTSSYFATTYYHLY

m = 34
n = 35

# adding '' and , automatically to string
# import re
# st = 'S A L P Q P T T P V S S F T S G S M L G R T D T A L T N T Y S A L'
# print(re.findall(r"[\w']+", st))

# adding column and row headers
h = [' ', 'S', 'A', 'L', 'P', 'Q', 'P', 'T', 'T', 'P', 'V', 'S', 'S', 'F', 'T', 'S', 'G', 'S', 'M', 'L', 'G', 'R', 'T', 
         'D', 'T', 'A', 'L', 'T', 'N', 'T', 'Y', 'S', 'A', 'L']
header2 = [' ','P', 'S', 'P', 'T', 'M', 'E', 'A', 'V', 'T', 'S', 'V', 'E', 'A', 'S', 'T', 'A', 'S', 'H', 
           'P', 'H', 'S', 'T', 'S', 'S', 'Y', 'F', 'A', 'T', 'T', 'Y', 'Y', 'H', 'L', 'Y']
df2 = pd.DataFrame(data=[[np.zeros(1)]*m]*n)
df2.rename(index = dict(zip(range(len(header2)),header2)),inplace =True)
df2.rename(columns=dict(zip(range(len(h)),h)), inplace = True)

df2


# In[7]:


# Same as:
# Filling the Global Allignment Table (array in row-colum pair)
#Forward Pass

cost = -8

def blos(r, c):
    cname = df2.columns[c]
    rname = df2.index[r]
    if r == 0 or c == 0:
        return np.nan
    else:
        return int(df[rname][cname]) + int(df2.iloc[r-1,c-1][0])

arrow =[]

for r in range(0,35):
    for c in range(0,34):
        upelement = int(df2.iloc[r-1,c][0]) + cost if r >= 1 else np.nan
        leftelement = int(df2.iloc[r,c-1][0]) + cost if c >= 1 else np.nan
        diagelement = blos(r, c)
        if r == 0 and c == 0:
            upelement = 0
        list1 = np.array([diagelement, upelement,leftelement])
        re = np.nanargmax(list1)
        #df1.iloc[r,c] = list1[re]
        if list1[re] == diagelement:
            vec = [r-1,c-1]
            arrow.extend([r-1,c-1, r,c])
        elif list1[re] == upelement:
            vec = [r-1,c]
            arrow.extend([r-1,c, r,c])
        elif list1[re] == leftelement:
            vec = [r,c-1]
            arrow.extend([r,c-1, r,c])
        df2.iloc[r,c] = np.array([list1[re], vec[0], vec[1]])
    
df2


# In[8]:


arrow2 =[]
letter1 = []
letter2 = []

# Setting initial conditions, starting from the last element of the table
r =34
c =33
nextr = 34
nextc = 33
# Same as:
# Backward pass
if((c==nextc) and (r==nextr)):
    letter2.append('-')
    letter1.append(df2.index[r])
elif((c!=nextc) and (r==nextr)):
    letter1.append('-')
    letter2.append(df2.columns[c])
elif((c!=nextc) and (r!=nextr)):
    letter1.append(df2.index[r])
    letter2.append(df2.columns[c])

# Looping through the table to find the backward pass elements and their corrisponding strings
for r in range(34, 0,-1):
    for c in range(33,-1,-1):
        if r == nextr and c == nextc: # Similar implementation as in Backward pass, the main difference is that the arrow 
                                      # direction has been stored in an array direnctly in the row-column pair instead of
                                      # in a separate list
            arrow2.append(df2.iloc[r,c][0])
            nextr = df2.iloc[r,c][1]
            nextc = df2.iloc[r,c][2]
            if c == 33 and r==34:  # Handling starting condition
                letter2.append(df2.columns[c])
                letter1.append(df2.index[r-1])
            if c != 33 and r!=34:
                if(((c==nextc) and (r==nextr)) or (nextr==0 and nextc==0)):
                    letter2.append('-')
                    letter1.append(df2.index[r])
                elif((c!=nextc) and (r==nextr)):
                    letter1.append('-')
                    letter2.append(df2.columns[c])
                else:
                    letter1.append(df2.index[r])
                    letter2.append(df2.columns[c])
                    
arrow2.append(0)
arrow2 = np.asarray(arrow2)
print(letter2[::-1])
print(letter1[::-1])
print(arrow2)
# -SALPQPTTPVSSFTSGSMLGRTDTALTNTYSAL-
# PSPTMEAVTSVEA-STASHPHSTSSYFATTYYHLY


# ### 2) Modify your program to implement the Smith-Waterman algorithm

# #### Again run this on HEAGAWGHEE versus PAWHEAE

# In[9]:


m = 11
n = 8

# Creating a table to run HEAGAWGHEE versus PAWHEAE
h = [' ', 'H', 'E', 'A', 'G', 'A', 'W','G', 'H', 'E', 'E']
header2 = [' ','P', 'A', 'W', 'H', 'E', 'A','E']
df3 = pd.DataFrame(data=[[np.zeros(3)]*m]*n)
df3.rename(index = dict(zip(range(len(header2)),header2)),inplace =True)
df3.rename(columns=dict(zip(range(len(h)),h)), inplace = True)

# Filling the Global Allignment Table (array in row-colum pair)
#Forward Pass

cost = -8 # Cost of insertion or delition

# Calculating price of substitution when arrows moves diagonally
def blos(r, c):
    cname = df3.columns[c]
    rname = df3.index[r]
    if r == 0 or c == 0:
        return np.nan # Handling nan error when filling first row/column
    else:
        return int(df[rname][cname]) + int(df3.iloc[r-1,c-1][0])

arrow =[]
maxf = []

# Loop to fill the table, deciding between if the upelement, leftelement or the diagelement gives us less loss.
for r in range(0,8):
    for c in range(0,11):
        zero = 0
        upelement = int(df3.iloc[r-1,c][0]) + cost if r >= 1 else np.nan # Handling nan error when filling first row/column
        leftelement = int(df3.iloc[r,c-1][0]) + cost if c >= 1 else np.nan # Handling nan error when filling first row/column
        diagelement = blos(r, c)
        if r == 0 and c == 0:
            upelement = 0
        list1 = np.array([zero, diagelement, upelement,leftelement])
        re = np.nanargmax(list1)
        # Storing the location of the selected max element to find arrow direction during the backward pass
        if list1[re] == zero:   # Added condition of 0 with priority 1 between the options from which to take the max
            vec = [0,0]
            vec2 = [r,c]  # Added vec2 to find the index of the max element in the table
            arrow.extend([0,0, r,c])
        elif list1[re] == diagelement:
            vec = [r-1,c-1]
            vec2 = [r,c]
            arrow.extend([r-1,c-1, r,c])
        elif list1[re] == upelement:
            vec = [r-1,c]
            vec2 = [r,c]
            arrow.extend([r-1,c, r,c])
        elif list1[re] == leftelement:
            vec = [r,c-1]
            arrow.extend([r,c-1, r,c])
        # Storing value, row and column coordinates in an array for each row-column pair in the table
        df3.iloc[r,c] = np.array([list1[re], vec[0], vec[1]])
        maxf.append([list1[re],vec[0], vec[1], vec2[0], vec2[1]]) # Array for later finding the max value and location in the 
                                                                  # table
df3


# In[10]:


arrow2 =[]
letter1 = []
letter2 = []

print("Maximum element in matrix, it's coordinates in the table, coordinates of where the arrow is pointing from this position, index of max element in the array ="
      ,max([(v,i) for i,v in enumerate(maxf)]))

# Setting initial conditions, starting from the last element of the table
r =5
c =9
nextr = 4
nextc = 8
arrow2.append(df3.iloc[5,9][0])
# Same as:
# Backward pass
if((c==nextc) and (r==nextr)):
    letter2.append('-')
    letter1.append(df3.index[r])
elif((c!=nextc) and (r==nextr)):
    letter1.append('-')
    letter2.append(df3.columns[c])
elif((c!=nextc) and (r!=nextr)):
    letter1.append(df3.index[r])
    letter2.append(df3.columns[c])

# Looping through the table to find the backward pass elements and their corrisponding strings
for r in range(7, 1,-1):
    for c in range(10,-1,-1):
        if r == nextr and c == nextc: # Similar implementation as in Backward pass, the main difference is that the arrow 
                                      # direction has been stored in an array direnctly in the row-column pair instead of
                                      # in a separate list
            arrow2.append(df3.iloc[r,c][0])
            nextr = df3.iloc[r,c][1]
            nextc = df3.iloc[r,c][2]
            if c == 9 and r==5:  # Handling starting condition
                letter.append(df3.columns[c])
                letter1.append(df3.index[r-1])
            if c != 9 and r!=5:
                if(((c==nextc) and (r==nextr))):
                    letter2.append('-')
                    letter1.append(df3.index[r])
                elif((c!=nextc) and (r==nextr)):
                    letter1.append('-')
                    letter2.append(df3.columns[c])
                else:
                    letter1.append(df3.index[r])
                    letter2.append(df3.columns[c])
                    
arrow2.append(0)
arrow2 = np.asarray(arrow2)
print(letter2[::-1])
print(letter1[::-1])
print(arrow2)


# #### Find the best local match between:
# #### MQNSHSGVNQLGGVFVNGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRY and TDDECHSGVNQLGGVFVGGRPLPDSTRQKIVELAHSGARPCDISRI

# In[11]:


# Creating a table to Match the protein sequence SALPQPTTPVSSFTSGSMLGRTDTALTNTYSAL with PSPTMEAVTSVEASTASHPHSTSSYFATTYYHLY

m = 61
n = 47

# adding '' and , automatically to string
# import re
# st = 'T D D E C H S G V N Q L G G V F V G G R P L P D S T R Q K I V E L A H S G A R P C D I S R I'
# print(re.findall(r"[\w']+", st))

# adding column and row headers
h = [' ', 'M', 'Q', 'N', 'S', 'H', 'S', 'G', 'V', 'N', 'Q', 'L', 'G', 'G', 'V', 'F', 'V', 'N', 'G', 'R', 'P', 'L', 'P', 
     'D', 'S', 'T', 'R', 'Q', 'K', 'I', 'V', 'E', 'L', 'A', 'H', 'S', 'G', 'A', 'R', 'P', 'C', 'D', 'I', 'S', 'R', 'I', 
     'L', 'Q', 'V', 'S', 'N', 'G', 'C', 'V', 'S', 'K', 'I', 'L', 'G', 'R', 'Y']
header2 = [' ','T', 'D', 'D', 'E', 'C', 'H', 'S', 'G', 'V', 'N', 'Q', 'L', 'G', 'G', 'V', 'F', 'V', 'G', 'G', 'R', 'P', 
           'L', 'P', 'D', 'S', 'T', 'R', 'Q', 'K', 'I', 'V', 'E', 'L', 'A', 'H', 'S', 'G', 'A', 'R', 'P', 'C', 'D', 'I', 
           'S', 'R', 'I']
df4 = pd.DataFrame(data=[[np.zeros(1)]*m]*n)
df4.rename(index = dict(zip(range(len(header2)),header2)),inplace =True)
df4.rename(columns=dict(zip(range(len(h)),h)), inplace = True)

df4


# In[12]:


# Filling the Global Allignment Table (array in row-colum pair)
#Forward Pass

cost = -8 # Cost of insertion or delition

# Calculating price of substitution when arrows moves diagonally
def blos(r, c):
    cname = df4.columns[c]
    rname = df4.index[r]
    if r == 0 or c == 0:
        return np.nan # Handling nan error when filling first row/column
    else:
        return int(df[rname][cname]) + int(df4.iloc[r-1,c-1][0])

arrow =[]
maxf = []

# Loop to fill the table, deciding between if the upelement, leftelement or the diagelement gives us less loss.
for r in range(0,47):
    for c in range(0,61):
        zero = 0
        upelement = int(df4.iloc[r-1,c][0]) + cost if r >= 1 else np.nan # Handling nan error when filling first row/column
        leftelement = int(df4.iloc[r,c-1][0]) + cost if c >= 1 else np.nan # Handling nan error when filling first row/column
        diagelement = blos(r, c)
        if r == 0 and c == 0:
            upelement = 0
        list1 = np.array([zero, diagelement, upelement,leftelement])
        re = np.nanargmax(list1)
        # Storing the location of the selected max element to find arrow direction during the backward pass
        if list1[re] == zero:  # Added condition of 0 with priority 1 between the options from which to take the max
            vec = [0,0] # Added vec2 to find the index of the max element in the table
            vec2 = [r,c] 
            arrow.extend([0,0, r,c])
        elif list1[re] == diagelement:
            vec = [r-1,c-1]
            vec2 = [r,c]
            arrow.extend([r-1,c-1, r,c])
        elif list1[re] == upelement:
            vec = [r-1,c]
            vec2 = [r,c]
            arrow.extend([r-1,c, r,c])
        elif list1[re] == leftelement:
            vec = [r,c-1]
            arrow.extend([r,c-1, r,c])
        # Storing value, row and column coordinates in an array for each row-column pair in the table
        df4.iloc[r,c] = np.array([list1[re], vec[0], vec[1]])
        maxf.append([list1[re],vec[0], vec[1], vec2[0], vec2[1]]) # Array for later finding the max value and location in the 
                                                                  # table
    
df4


# In[13]:


arrow2 =[]
letter1 = []
letter2 = []

print("Maximum element in matrix, it's coordinates in the table, coordinates of where the arrow is pointing from this position, index of max element in the array ="
      ,max([(v,i) for i,v in enumerate(maxf)]))

# Setting initial conditions, starting from the last element of the table
r =46
c =45
nextr = 45
nextc = 44
#arrow2.append(df4.iloc[r,c][0])
# Same as:
# Backward pass
if((c==nextc) and (r==nextr)):
    letter2.append('-')
    letter1.append(df4.index[r])
elif((c!=nextc) and (r==nextr)):
    letter1.append('-')
    letter2.append(df4.columns[c])
elif((c!=nextc) and (r!=nextr)):
    letter1.append(df4.index[r])
    letter2.append(df4.columns[c])

# Looping through the table to find the backward pass elements and their corrisponding strings
for r in range(46, 0,-1):
    for c in range(60,4,-1): # Skipping the first 4 elements because we already analysed them before
        if r == nextr and c == nextc: # Similar implementation as in Backward pass, the main difference is that the arrow 
                                      # direction has been stored in an array direnctly in the row-column pair instead of
                                      # in a separate list
            arrow2.append(df4.iloc[r,c][0])
            nextr = df4.iloc[r,c][1]
            nextc = df4.iloc[r,c][2]
            if c == 45 and r==46:  # Handling starting condition
                letter.append(df4.columns[c])
                letter1.append(df4.index[r-1])
            if c != 45 and r!=46:
                if(((c==nextc) and (r==nextr))or (nextr==-1 and nextc==0)):
                    letter2.append('-')
                    letter1.append(df4.index[r])
                elif((c!=nextc) and (r==nextr)):
                    letter1.append('-')
                    letter2.append(df4.columns[c])
                else:
                    letter1.append(df4.index[r])
                    letter2.append(df4.columns[c])
                    
arrow2.append(0)
arrow2 = np.asarray(arrow2)
print(letter2[::-1])
print(letter1[::-1])
print(arrow2)
# HSGVNQLGGVFVNGRPLPDSTRQKIVELAHSGARPCDISRI
# HSGVNQLGGVFVGGRPLPDSTRQKIVELAHSGARPCDISRI


# ### 3) BLAST algorithm test

# In[11]:


#Pax6 protein for the mouse 

# MQNSHSGVNQLGGVFVNGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRY
# YETGSIRPRAIGGSKPRVATPEVVSKIAQYKRECPSIFAWEIRDRLLSEGVCTNDNIPSV
# SSINRVLRNLASEKQQMGADGMYDKLRMLNGQTGSWGTRPGWYPGTSVPGQPTQDGCQQQ
# EGGGENTNSISSNGEDSDEAQMRLQLKRKLQRNRTSFTQEQIEALEKEFERTHYPDVFAR
# ERLAAKIDLPEARIQVWFSNRRAKWRREEKLRNQRRQASNTPSHIPISSSFSTSVYQPIP
# QPTTPVSSFTSGSMLGRTDTALTNTYSALPPMPSFTMANNLPMQPPVPSQTSSYSCMLPT
# SPSVNGRSYDTYTPPHMQTHMNSQPMGTSGTTSTGLISPGVSVPVQVPGSEPDMSQYWPR
# LQ

# eyeless protein for the fruit fly

# NVIAMRNLPCLGTAGGSGLGGIAGKPSPTMEAVEASTASHPHSTSSYFATTYYHLTDDEC
# HSGVNQLGGVFVGGRPLPDSTRQKIVELAHSGARPCDISRI

# Comparison result: https://blast.ncbi.nlm.nih.gov/Blast.cgi 

df5=pd.read_csv('6P13GW4F114-Alignment-HitTable.csv')
df5.head()


# In[12]:


f = open('6P13GW4F114-Alignment.txt', 'r')
file_contents = f.read()
print (file_contents)
f.close()


# ### 4) HMM for detecting CG regions

# In[124]:


import random
import sys


def roll(sides, bias_list):
    assert len(bias_list) == sides
    number = random.uniform(0, sum(bias_list))
    current = 0
    for i, bias in enumerate(bias_list):
        current += bias
        if number <= current:
            return i + 1

prob1 = [0.2698, 0.3237, 0.2080, 0.1985]
#stayleave1 = [0.9998, 0.0002]
stayleave1 = [0.5, 0.5]
prob2 = [0.2459, 0.2079, 0.2478, 0.2984]
#stayleave2 = [0.9997, 0.0003]
stayleave2 = [0.5, 0.5]

initialstate = [0.5,0.5]

selectstate = roll(2, initialstate)
if selectstate == 1:
    print('Starting in state 1 \n')
    state1=1
    state2=0
else:
    print("Starting in state 2 \n")
    state1=0
    state2=1

numlist = []
letlist = []
hhmstate = []
numtolet = []
    
for i in range(0,150):
    if state1==1: 
        n = str(roll(4, prob1)-1)
        numlist.extend(['\033[91m', n,' '])
        #letlist.append('\033[91mAT')
        numtolet.append(n)
        hhmstate.append('\033[91mH')
        switchstate = roll(2, stayleave1)
        if switchstate == 1:
            state1=1
            state2=0
        else:
           # print("Switching to state 2 \n")
            state1=0
            state2=1
    if state2==1:
        n2 = str(roll(4, prob2)-1)
        numlist.extend(['\033[34m', n2, ' '])
        #letlist.append('\033[34mCG')
        numtolet.append(n2)
        hhmstate.append('\033[34mD')
        switchstate = roll(2, stayleave2)
        if switchstate == 1:
            state1=0
            state2=1
        else:
           # print("Switching to state 1 \n")
            state1=1
            state2=0
# print(len(prob1))

letemm = []
for l in range(0, len(numtolet)):
    letemm.append({'0' : 'A', '1' : 'T', '2' : 'C', '3' : 'G'}[numtolet[l]])
        
letemm = ''.join(letemm)
letlist = ''.join(letlist)
numlist = ''.join(numlist)
hhmstate = ''.join(hhmstate)
#numlist = int(''.join(str(i) for i in numlist))

print(letemm, '\n')
#print(letlist, '\n')
print(numlist, '\n')
print(hhmstate, '\n')


# ### 5) Viterbi Algorithm

# In[110]:


def viterbi(observations, transition, emission, priors):
    # A - initialise stuff
    n_samples = len(observations)
    n_states = transition.shape[0] # number of states
    c = np.zeros(n_samples) #scale factors (necessary to prevent underflow)
    viterbi = np.zeros((n_states, n_samples)) # initialise viterbi table
    psi = np.zeros((n_states,n_samples), dtype=int) # initialise the best path table
    best_path = np.zeros(n_samples); # this will be your output

    # B- appoint initial values for viterbi and best path tables
    viterbi[:,0] = priors.T.dot(emission[:,observations[0]])
    c[0] = 1.0 / np.sum(viterbi[:,0])
    viterbi[:,0] = c[0] * viterbi[:,0] # apply the scaling factor

    # C- Do the iterations for viterbi and psi for time>0 until T
    for t in range(1, n_samples): # loop through time
        for s in range (0, n_states): # loop through the states at (t-1)
            trans_p = viterbi[:,t-1] * transition[:,s]
            psi[s,t], viterbi[s,t] = max(enumerate(trans_p), key=lambda x: x[1])
            viterbi[s,t] = viterbi[s,t] * emission[s,observations[t]]

        c[t] = 1.0 / np.sum(viterbi[:,t]) # scaling factor
        viterbi[:,t] = c[t] * viterbi[:,t]

    # D - Back-tracking
    best_path[n_samples - 1] = viterbi[:,n_samples - 1].argmax() # last state
    for t in range(n_samples - 1, 0, -1): # states of (last-1)th to 0th time step
        #print(best_path[t], t)
        best_path[t - 1] = psi[int(best_path[t]), t]
    
    #print(viterbi)
    return best_path


# In[125]:


A = np.array([[0.5, 0.5], [0.5, 0.5]])
B = np.array([[0.2459, 0.2079, 0.2478, 0.2984], [0.2698, 0.3237, 0.2080, 0.1985]])
X = 'TTCAGAAGCACTCTGACGCGCTCACGGCAACCAAACAAGTGGTAAATAAATGATTCGTCGTCTCCCCTGGCCCCCATTCACAACAAGGTGGTGGACAGGCGACTATGCACCCCTATATGTAGCAGTTATGTCCCGCGGTACTTTCTGCAGTGGATCTAAAGCATTCGCTCTGTTCCACGCGAGCAGAAGAAA'
#X = open('tut2.txt').read().replace('\n', '')
states = []
for c in range(0, len(X)):
    states.append({'A': 0, 'T': 1, 'C': 2, 'G': 3}[X[c]])
        
states = np.array(states)
print(states)
Pi = np.array([0.5, 0.5])


# In[126]:


statenum = viterbi(states, A, B, Pi)
print(statenum)


# In[128]:


import sys
# from termcolor import colored
# print(colored('hello', 'red'), colored('world', 'green'))

letstate = []
for i in range(0,len(statenum)):
    if statenum[i] == 1:
        letstate.append('\033[91mH')
    elif statenum[i] == 0:
        letstate.append('\033[34mD')

letstate = ''.join(letstate)
print(letstate, '\n')
print(hhmstate, '\n')


# ### 6) Testing for the Phase Lambda

# In[129]:


A = np.array([[0.5, 0.5], [0.5, 0.5]])
B = np.array([[0.2459, 0.2079, 0.2478, 0.2984], [0.2698, 0.3237, 0.2080, 0.1985]])
X = open('tut2.txt').read().replace('\n', '')
states = []
for c in range(0, len(X)):
    states.append({'A': 0, 'T': 1, 'C': 2, 'G': 3}[X[c]])
        
states = np.array(states)
print(states)
Pi = np.array([0.5, 0.5])
statenum = viterbi(states, A, B, Pi)
print(statenum)
letstate = []
for i in range(0,len(statenum)):
    if statenum[i] == 1:
        letstate.append('\033[91mH')
    elif statenum[i] == 0:
        letstate.append('\033[34mD')

letstate = ''.join(letstate)
print(letstate)

