import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#school data
df1 = pd.read_csv("2010_-_2011_School_Progress_Report.csv")

df1 = (df1[df1['2010-2011 OVERALL GRADE'].notnull() 
	& df1['PROGRESS REPORT TYPE'].str.contains('HS',case=False,na=False)])
df1 = df1[df1['PROGRESS REPORT TYPE'] == 'HS']
df1 = df1.drop_duplicates()
df1 = df1.reset_index(drop=True)

df2 = pd.read_excel("2018_DOE.xlsx")

# ['dbn',
#  'school_name',
#  'boro',
#  'overview_paragraph',
#  'neighborhood',
#  'phone_number',
#  'school_email',
#  'website',
#  'grades2018',
#  'total_students',
#  'start_time',
#  'end_time',
#  'addtl_info1',
#  'graduation_rate',
#  'attendance_rate',
#  'pct_stu_enough_variety',
#  'college_career_rate',
#  'pct_stu_safe',
#  'girls',
#  'boys',
#  'pbat',
#  'international',
#  'specialized',
#  'transfer',
#  'ptech',
#  'earlycollege',
#  'geoeligibility',
#  'school_accessibility_description',
#  'primary_address_line_1',
#  'city',
#  'Postcode',
#  'state_code',
#  'Borough',
#  'Latitude',
#  'Longitude',
#  'Community Board',
#  'Council District',
#  'Census Tract',
#  'BIN',
#  'BBL',
#  'NTA']

df3 = pd.read_excel("Median Household Income.xlsx")
df3 = df3.drop_duplicates(subset='tract_num')

dfa = pd.merge(df1, df2, how='inner', left_on='DBN', right_on='dbn')

df = pd.merge(dfa, df3, how='left', 
	left_on='Census Tract', 
	right_on='tract_num')

# N = 100
# dfa['Census Tract'] = np.round(dfa['Census Tract']*N).astype(int) 
# df3['tract_num'] = np.round(df3['tract_num']*N).astype(int) 

# df = pd.merge(dfa, df3, how='inner', 
# 	left_on='Census Tract', 
# 	right_on='tract_num')

# df['Census Tract'] = df['Census Tract']/N 

plt.plot()
sns.regplot(x='PEER INDEX*',
	y='attendance_rate', 
 	data=df,
 	fit_reg=False,
 	ci=None)
plt.show()

plt.plot()
sns.regplot(x='pct_stu_safe',
	y='college_career_rate', 
 	data=df,
 	fit_reg=False,
 	ci=None)
plt.show()

plt.plot()
sns.regplot(x='pct_stu_safe',
	y='graduation_rate', 
 	data=df,
 	fit_reg=False,
 	ci=None)
plt.show()