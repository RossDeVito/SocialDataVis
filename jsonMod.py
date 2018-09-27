#jsonMod.py
import json
import pandas as pd

df_NTA = pd.read_excel("NTA_data.xlsx")
df_NTA = df_NTA[df_NTA['measure'] == 'Percent']
df_NTA[['NTA_code', 'NTA_name']] = df_NTA['nta'].str.split(' ', 1, expand=True)

df_NTA[df_NTA == '-'] = "No data"
df_NTA[df_NTA == 0] = "No data"
df_NTA[df_NTA.isnull()] = "No data"

df_NTA.loc[df_NTA['NTA_name'].str.contains('park-cemetery-etc-Manhattan'), 
	'Unemployment Rate'] = "No data"
df_NTA.loc[df_NTA['NTA_name'].str.contains('Airport'), 
	'GRAPI 35.0 percent or more'] = "No data"
df_NTA.loc[df_NTA['NTA_name'].str.contains('Rikers Island'), 
	'GRAPI 35.0 percent or more'] = "No data"
df_NTA.loc[df_NTA['NTA_name'].str.contains('park-cemetery-etc-Manhattan'), 
	'GRAPI 35.0 percent or more'] = "No data"
df_NTA.loc[df_NTA['NTA_name'].str.contains('park-cemetery-etc-Manhattan'), 
	'Vacant housing units'] = "No data"


gj = json.load(open('Neighborhood Tabulation Areas.geojson'))

for n in gj['features']:
	d = df_NTA[df_NTA['NTA_code'] == n['properties']['ntacode']].to_dict('list')
	n['properties']['unemployment_rate'] = d['Unemployment Rate'][0]
	n['properties']['GRAPI_35'] = d['GRAPI 35.0 percent or more'][0]
	n['properties']['less_that_10000'] = d['Households Less than $10,000'][0]
	n['properties']['food_stamps'] = d['Households With Food Stamp/SNAP bnfts in the past 12 mo'][0]
	n['properties']['cash_assistance'] = d['Households With cash public assistance income'][0]
	n['properties']['incomplete_plumbing'] = d['Lacking complete plumbing facilities'][0]
	n['properties']['bachelors_or_higher'] = d["Percent bachelor's degree or higher"][0]
	n['properties']['high_school_grad'] = d['Percent high school graduate or higher'][0]
	n['properties']['less_than_9th'] = d['Population 25 years and over  Less than 9th grade'][0]
	n['properties']['vacant_housing'] = d['Vacant housing units'][0]

json.dump(gj, open("NTA.geojson", 'w'))



