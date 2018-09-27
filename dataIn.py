#dataIn.py
import pandas as pd
import numpy as np
import random

# pd.set_option('display.height', 1000)
# pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 1000)

df_NTA = pd.read_excel("NTA_data.xlsx")
df_NTA = df_NTA[df_NTA['measure'] == 'Percent']
df_NTA[['NTA_code', 'NTA_name']] = df_NTA['nta'].str.split(' ', 1, expand=True)

df_HSD = pd.read_excel("2017_DOE_HSD.xlsx")

df_SQR = pd.read_excel("201617SQR_data.xlsx", 0)
df_SQR1 = pd.read_excel("201617SQR_data.xlsx", 1)
df_SQR2 = pd.read_excel("201617SQR_data.xlsx", 2)

df_SQR = df_SQR.join(df_SQR1.set_index('DBN'), on='DBN', rsuffix='_1')
df_SQR = df_SQR.join(df_SQR2.set_index('DBN'), on='DBN', rsuffix='_2')

df_sch = df_SQR.join(df_HSD.set_index('dbn'), how = 'inner',  on='DBN')

p=df_sch[df_sch['NTA'].str.contains("park", na=False)]

df_sch['NTA_lower'] = df_sch['NTA'].str.lower().str.strip()
df_NTA['NTA_name_lower'] = df_NTA['NTA_name'].str.lower().str.strip()

df_sch.loc[df_sch['NTA_lower'] == 'hudson yards-chelsea-flatiron-union square', 
	'NTA_lower'] = 'hudson yards-chelsea-flat iron-union square'

df_sch.loc[df_sch['NTA_lower'] == 'sheepshead bay-gerritsen beach-manhattan beach', 
	'NTA_lower'] = 'sheepshead bay-gerritsen bch-manhattan bch'

df_sch.loc[df_sch['NTA_lower'] == 'breezy point-belle harbor-rockaway park-broad channel', 
	'NTA_lower'] = 'breezy pnt-belle harbor-rockaway pk-broad channel'

df_sch = df_sch.join(df_NTA.set_index('NTA_name_lower'), 
										how='left', on='NTA_lower')

df_sch['girls'] = np.where(df_sch['girls']==1, True, False)
df_sch['boys'] = np.where(df_sch['boys']==1, True, False)
df_sch['pbat'] = np.where(df_sch['pbat']==1, True, False)
df_sch['international'] = np.where(df_sch['international']==1, True, False)
df_sch['specialized'] = np.where(df_sch['specialized']==1, True, False)
df_sch['transfer'] = np.where(df_sch['transfer']==1, True, False)
df_sch['ptech'] = np.where(df_sch['ptech']==1, True, False)
df_sch['earlycollege'] = np.where(df_sch['earlycollege']==1, True, False)
df_sch['geoeligibility_b'] = np.where(df_sch['geoeligibility'].notnull(), True, False)

df_sch['community_school'] = np.where(
	df_sch['addtl_info1'].str.contains("Community School"), True, False)

df_sch['uniforms'] = np.where(
	df_sch['addtl_info1'].str.contains("Uniform"), True, False)

g=df_sch.groupby(['girls','boys','pbat','international','specialized',
	'transfer','ptech','earlycollege','community_school']
	).size().reset_index().rename(columns={0:'count'})

gnc=df_sch.groupby(['girls','boys','pbat','international','specialized',
	'transfer','ptech','earlycollege']
	).size().reset_index().rename(columns={0:'count'})

df_sch['type'] = "No Type"

df_sch.loc[df_sch['community_school'], 'type'] = "Community"

df_sch.loc[df_sch['earlycollege'], 'type'] = "Early College"

df_sch.loc[df_sch['ptech'],'type'] = "P-TECH"

df_sch.loc[df_sch['specialized'], 'type'] = "Specialized"

df_sch.loc[df_sch['international'], 'type'] = "School for New Arrivals"

df_sch.loc[df_sch['pbat'], 'type'] = "Performance Assessment"

df_sch.loc[df_sch['pbat'] & df_sch['international'], 'type'] = "International Performance Assessment"

df_sch.loc[df_sch['boys'], 'type'] = "Male Only"

df_sch.loc[df_sch['girls'], 'type'] = "Female Only"


tc=df_sch.groupby(['type']
	).size().reset_index().rename(columns={0:'count'})

tl=df_sch.groupby(['Latitude', 'Longitude']
	).size().reset_index().rename(columns={0:'count'})
tl = tl[tl["count"] > 1]

need_jitter = np.array(tl[['Latitude','Longitude']]);

for i, row in df_sch.iterrows():
	if [row.Latitude, row.Latitude] in need_jitter:
		df_sch.loc[i,"Latitude"] = row["Latitude"] + random.triangular(-.0025,.0025,0)
		df_sch.loc[i,"Longitude"] = row["Longitude"] + random.triangular(-.0025,.0025,0)

tc=df_sch.groupby(['type']
	).size().reset_index().rename(columns={0:'count'})

tl=df_sch.groupby(['Latitude', 'Longitude']
	).size().reset_index().rename(columns={0:'count'})
tl = tl[tl["count"] > 1]

df_sch.fillna("No data", inplace=True)

df_sch["Metric Value - % College Ready SAT Math"] = df_sch[
	"Metric Value - % College Ready SAT Math"]*100

df_sch["Metric Value - % College Ready SAT Reading and Writing"] = df_sch[
	"Metric Value - % College Ready SAT Reading and Writing"]*100

df_sch["Metric Value - % Passing an Industry-Recognized Technical Assessment"] = df_sch[
	"Metric Value - % Passing an Industry-Recognized Technical Assessment"]*100

df_sch["Percent English Language Learners"] = df_sch[
	"Percent English Language Learners"]*100

df_sch["Percent Overage/ Undercredited"] = df_sch[
	"Percent Overage/ Undercredited"]*100

df_sch["pct_stu_safe"] = df_sch[
	"pct_stu_safe"]*100

df_sch["Percent Students with Disabilities"] = df_sch[
	"Percent Students with Disabilities"]*100

df_sch["Percent in Temp Housing"] = df_sch[
	"Percent in Temp Housing"]*100

df_sch["Percent of teachers with 3 or more years of experience"] = df_sch[
	"Percent of teachers with 3 or more years of experience"]*100

df_sch.to_csv("schools.csv", index=False)