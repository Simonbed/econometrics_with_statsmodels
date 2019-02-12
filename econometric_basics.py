
import sqlite3
import io
import csv

#Creating the Database
conn = sqlite3.connect('econometrics_trial.sqlite')
cur = conn.cursor()
cur.execute('''DROP TABLE IF EXISTS Economics''')

#create tables for our database
cur.execute('''CREATE TABLE IF NOT EXISTS Economics
    (id INTEGER PRIMARY KEY,  CPICANADARTE FLOAT, DATE_LIST TEXT, employment_rate FLOAT, CPIUSRTE FLOAT)''')

gdplist = list()
gnplist = list()
empllist = list()

#From every csv file we downloaded and put in the directory, we extract the data and put it in lists
with open('CPICADRTE.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        #print(row[0]) 
        #print(row)
        if row[0] == "DATE":
            continue
        else:
            gdplist.append(row)

with open('CPIUSRTE.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        if row[0] == "DATE":
            continue
        else:
            gnplist.append(row)

with open('employmentratecanada.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        print(row)
        if row[0] == "DATE":
            continue
        else:
            empllist.append(row)


count = 0
TX_EMPL = list()


for row in empllist:
    TX_EMPL.append(row[1])
count = 0
TX_EMPL_INC = list()

for object in TX_EMPL :
    if count == 0 :
        temp = 0
    else:
        count_moins_un = count - 1
        temp = ( float(TX_EMPL[count]) - float(TX_EMPL[(count_moins_un)]) ) / float(TX_EMPL[(count_moins_un)])


    TX_EMPL_INC.append(temp)
    count = count + 1


count = 0
for row in gnplist :
    try:
        gdp = gdplist[count]
    except:
        gdp = 'null', 'NULL'
    try:
        gnp = gnplist[count]
    except:
        gnp = 'null', 'NULL'
    try:


        empl = TX_EMPL_INC[count]
    except:
        empl = 'null', 'NULL'

    cur.execute('''INSERT INTO Economics (CPICANADARTE, DATE_LIST, CPIUSRTE, employment_rate) VALUES (?,?,?,?)''', (gdp[1], gdp[0], gnp[1], empl,))
    count = count + 1


conn.commit()
cur.close()
