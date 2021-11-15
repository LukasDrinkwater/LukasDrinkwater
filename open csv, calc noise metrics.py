import sys
import numpy as np
import pandas as pd
from datetime import datetime
import timeit

start = timeit.default_timer()



# read .txt file output from AS60, skips reading 14 rows of data
# converts file to csv
# change to .csv\.txt file you want to calc
data = pd.read_csv('Term_Report_Auto_3302_Lp.csv', delimiter=',', skiprows=14)
##data.to_csv('testtocsv.csv',encoding='utf-8') 


# change date and time format
data['Start'] = pd.to_datetime(data['Start'], format='%Y/%m/%d %H:%M')


# assigns true next to rows where the time is between 23:00 and 06:59
# change dates to start and stop dates - dont change time
dataMod = data['Start'].between('24/07/2019 23:00', '25/07/2019 06:59', inclusive = True)
# change true and false to 1 and 0
dataMod = dataMod.astype(int)


# adds new column for splitting the time 
dataSplit = data
dataSplit['Night'] = dataMod

# adds new column to add antilog values to
dataAnti = data
dataAnti['anti'] = dataSplit['LAeq']

# loops through 'anti' column, does calc, creates new column,
# updates values
for x in dataAnti['anti']:
    #does antilog calc
    dataAnti['antilog'] = 10**(dataAnti['anti']/10)
# deletes 'anti' column no longer needed
dataAnti = dataAnti.drop(columns='anti')

print dataAnti


# splits dataframe to only contain rows with 1
dayMod = dataAnti
day = dataAnti['Night']==0
dayMod = dayMod[day]
##Laeq = round(dayMod['Laeq'].mean(),1)
# does some calcs
# Laeq uses the antilog column created earlier
Laeq = dayMod['antilog'].mean()
Laeq = 10*np.log10(Laeq)
Laeq = round(Laeq,1)
Lmax = dayMod['LAFmax']
Lmax = round(max(Lmax),1)
L10 = round(dayMod['L10'].mean(),1)
L90 = round(dayMod['L90'].mean(),1)


# splits dataframe to only contain rows with 0
nightMod = dataAnti
night = dataAnti['Night']==1
nightMod = nightMod[night]
#does some calcs
Laeq_night = nightMod['antilog'].mean()
Laeq_night = 10*np.log10(Laeq_night)
Laeq_night = round(Laeq_night,1)
Lmax_night = nightMod['LAFmax']
Lmax_night = round(max(Lmax_night),1)
L10_night = round(nightMod['L10'].mean(),1)
L90_night = round(nightMod['L90'].mean(),1)




#prints the results
Night_Values = [Laeq_night, Lmax_night, L10_night, L90_night]
Day_Values = [Laeq, Lmax, L10, L90]
print 'Day values:\n', Day_Values
print 'Night values:\n', Night_Values


##data.close()

stop  = timeit.default_timer()

print('Time: ',stop - start)

