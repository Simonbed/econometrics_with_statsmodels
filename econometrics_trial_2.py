import sqlite3
import json # Our Data comes out in JSON format from the API
import re#We might use it this time
from pandas import datetime
from pandas import Series
import statsmodels.stats.api as sms
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd
import statsmodels.stats.diagnostic as ssd
#from matplotlib import pyplot
## still importing things
import matplotlib.pyplot as plt

import numpy as np

conn = sqlite3.connect('econometrics_trial.sqlite')
cur = conn.cursor()


##===========THIS (   *   ) WILL SELECT ALL THE VARIABLES FROM THE DATABASE===========================

cur = conn.cursor()
cur.execute('SELECT * FROM Economics')
rows = cur.fetchall()

##============BUT THIS IS EQUIVALENT BUT WE DIDN'T TAKE THE DATES BECAUSE WE WILL USE THE PERIODS (T)
#Take the data from the database that we will plot for now.
cur.execute('''SELECT Economics.id, Economics.CPICANADARTE, Economics.employment_rate, Economics.CPIUSRTE
                FROM Economics
                Order By Economics.id''')
rows = cur.fetchall()

t = list()
CPI_C = list()
TX_EMPL = list()
CPI_US = list()

for row in rows:
    t.append(row[0])
    CPI_C.append(row[1])
    TX_EMPL.append(row[2])
    CPI_US.append(row[3])



#We close the connection to data and we commit changes
conn.commit()
cur.close()


#LETS DO SOME PLOTTING OF THE DATA TO MAKE SURE WE HAVE THE ONE WE BELIEVE WE DO
#... oh and also because we are analysing
# 1) CPI CANADA LINE GRAPH
plt.plot(t, CPI_C, c='red')     ##Modify graph visual: 1) PLOT = LINE 2) SCATTER = dots / SIZE OF POINT (default = 20) s=, COLOR c=, SHAPE marker:
plt.title('CPI Monthly CANADA 1995-01-01 to 2018-01-01')
plt.xlabel('1995-01 to 2018-01')
plt.ylabel('CPI Cad')
#plt.show()

# 2 ) CPI USA LINE GRAPH
plt.plot(t, CPI_US, c='red')     ##Modify graph visual: 1) PLOT = LINE 2) SCATTER = dots / SIZE OF POINT (default = 20) s=, COLOR c=, SHAPE marker:
plt.title('CPI Monthly USA 1995-01-01 to 2018-01-01')
plt.xlabel('1995-01 to 2018-01')
plt.ylabel('CPI US')
#plt.show()

# 3 ) EMPLOYMENT RATE CANADA
plt.plot(t, TX_EMPL, c='red')     ##Modify graph visual: 1) PLOT = LINE 2) SCATTER = dots / SIZE OF POINT (default = 20) s=, COLOR c=, SHAPE marker:
plt.title('EMPLOYMENT RATE CANADA 1995-01-01 to 2018-01-01')
plt.xlabel('1995-01 to 2018-01')
plt.ylabel('TX DEmploi Canadien')
#plt.show()


# 5 ) Now that we have the new variavble, we can do some regressions. Lets do the basic model


df = pd.read_sql_query("SELECT Economics.id, Economics.CPIUSRTE, Economics.CPICANADARTE, Economics.employment_rate FROM Economics;", conn)

x = df[['CPICANADARTE', 'CPIUSRTE']]
y = df['employment_rate']
#THis is the intercept (constant) ---- This is what you always do when you use statsmodels, it doesn't add the constant for you -
#On another note, scipy does it for you but doesnt print out the results lovely like this or like R or STATA
x = sm.add_constant(x)

model = sm.OLS(y, x).fit()
print(model.resid)
print(model.summary())

#We can see that we get skewness, kurtosis, JB, Durbin Watson Tests with (SUMMARY)

# IN THIS MODEL, We notice jarque bera (JB).

#HERE I WANTED TO GET THE JB HISTOGRAM --Let's add it if i find it. The JB Stat is shown in Summary, but I like the histogram view I had in Stata/eviews
print('Jarque Bera Test Statistics : ')
name_jb = ['Jarque-Bera', 'Chi^2 two-tail prob.', 'Skew', 'Kurtosis']
test_jb = sms.jarque_bera(model.resid)
print(name_jb[0], ' ', test_jb[0], ' ', name_jb[1], ' ', test_jb[1], ' ', name_jb[2], ' ', test_jb[2], ' ', name_jb[3], ' ', test_jb[3],)
print('     ')
# Lets try some more test_result  --- TEST FOR HETEROSCEDASTICITY "WHITE's test"
print('WHITE TEST')
white_t = ssd.het_white(model.resid, model.model.exog, retres=False)
print(white_t[1])
stat_1 = white_t[1]
print('Whites test for hetero using lm test: ', stat_1, 'Whites test for hetero using F-Stat :', white_t[3])
print( ' ')

#Next test :ARCH For heteroscedasticity
print('ARCH TEST')
arch = ssd.het_arch(model.resid, maxlag=2, autolag=None, store=False, regresults=False, ddof=0)
print('LM test stat:',  arch[0], 'LM P value:', arch[1], 'F test stat:', arch[2], 'F P value', arch[3])
print(' ')

#Next test : RESET
print('Ramsey RESET test')
