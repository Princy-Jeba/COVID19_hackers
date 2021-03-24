import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv

root_dir='E:\\Hackathon\\'


cases_df = pd.read_csv (r'https://api.covid19india.org/csv/latest/state_wise.csv')

cases_df = cases_df.loc[1:36, ['State', 'Recovered','Deaths','Active']]
print (cases_df)

vaccine_df = pd.read_csv(r'http://api.covid19india.org/csv/latest/vaccine_doses_statewise.csv')
vaccine_df = vaccine_df.iloc[0:36,list(range(1)) + [-1]] #first column has state names and last column latest no of doses administered
print (vaccine_df)


data = pd.merge(cases_df,vaccine_df,sort = True)
# print (data)
keep_col = ['STATE','Recovered','Deaths','Active','Population_vaccinated']
data.columns = keep_col

data.to_csv(root_dir+'DATA_INPUT1.csv',index=False)
data_input1=pd.read_csv(root_dir+'DATA_INPUT1.csv')
data_input2=pd.read_csv(root_dir+'DATA_INPUT.csv')

#Find the percentage of statewise non vaccinated people from the population:
Non_vaccinated =data_input2['Projected_population_2020'] -data_input1['Population_vaccinated'] 
Percentage_Nonvaccinated = (Non_vaccinated).div(sum(Non_vaccinated))
percent_Nonvaccinated_ratio=Percentage_Nonvaccinated.div(sum(Percentage_Nonvaccinated))


###No of people per bed in each states:

Number_people_per_bed=data_input2['Projected_population_2020'].div(data_input2['Number_of_hospital_bed_Public_and_private'])
Frno_of_pplperbed=(Number_people_per_bed).div(max(Number_people_per_bed))
fr_ratio=(Frno_of_pplperbed).fillna(0)
normalise_Frno_of_pplperbed=(Frno_of_pplperbed).div(sum(fr_ratio))


# Find the number of uncured people
fr_uncured =(data_input1['Active']+data_input1['Deaths']).div(data_input1['Active']+data_input1['Recovered']+data_input1['Deaths'])
normalise_fr_uncured=(fr_uncured).div(sum(fr_uncured))

##looking at HDI:
fr_hdi =(data_input2['HDI']).div(sum(data_input2['HDI']))

data_input1['Priority_Index']=((percent_Nonvaccinated_ratio+normalise_Frno_of_pplperbed+normalise_fr_uncured+fr_hdi)/4.0)*100.0
data_input1= data_input1.fillna(0)

data_input1=data_input1.drop(['Recovered','Deaths','Active','Population_vaccinated'], axis = 1)
data_input1.to_csv(root_dir+'priorityindex1.csv',index=None)



###Pie chart showing the critical states need to vaccinated :
df = pd.read_csv(root_dir+'priorityindex1.csv')
df = df.sort_values(by=['STATE'])
df['Priority_Index'] = df['Priority_Index'].round(1)
# Creating dataset
state1 = df['STATE'].values[:]
state = ['A & N', 'AP', 'Arunachal', 'Assam',
        'Bihar', 'Chandigarh', 'Chhattisgarh',
        'UT Dadra', 'Delhi', 'Goa', 'Gujarat',
        'Haryana', 'HP', 'J & K', 'Jharkhand',
        'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'MP',
        'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland',
        'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim',
        'TN', 'Telangana', 'Tripura', 'UP',
        'Uttarakhand', 'WB']

data = df['Priority_Index'].values[:]

# Creating explode data
explode = (0.1, 0.0, 0.2, 0.3, 0.0, 0.0, 0.1, 0.0, 0.2, 0.3, 0.0, 0.0,
            0.1, 0.0, 0.2, 0.3, 0.0, 0.0, 0.1, 0.0, 0.2, 0.3, 0.0, 0.0,
            0.1, 0.0, 0.2, 0.3, 0.0, 0.0, 0.1, 0.0, 0.2, 0.3, 0.0, 0.0)

# Creating color parameters
colors = ( "orange", "cyan", "brown","grey", "indigo", "beige", 
          "magenta","green", "yellow","blue", "violet", "purple",
          "black", "pink", "white","darkorange", "cyan", "brown",
          "slategrey", "darkorchid", "burlywood","darkmagenta","darkgreen", "tan",
          "maroon", "darkviolet", "mediumpurple","tomato", "plum", "wheat",
          "grey", "navy", "bisque","goldenrod", "aqua", "salmon")
# Wedge properties
wp = { 'linewidth' : 1, 'edgecolor' : "black" }

# Creating autocpt arguments
def func(pct, allvalues):
 	absolute = int(pct / 100.*np.sum(allvalues))
 	return "{:.1f}%".format(pct, absolute)

# Creating plot
fig, ax = plt.subplots(figsize =(10, 8))
#wedges, texts, autotexts = ax.pie(data,,
#								explode = explode,
#								labels = state,
#								shadow = True,
#								colors = colors,
#								startangle = 90,
#								wedgeprops = wp,
#								textprops = dict(color ="red"))
wedges, texts, autotexts = ax.pie(data, autopct = lambda pct: func(pct, data),
								explode = explode,
								labels = state,
								shadow = True,
								colors = colors,
								startangle = 90,
								wedgeprops = wp,
								textprops = dict(color ="black"))

# Adding legend
ax.legend(wedges, state1,
		title ="State",
		loc ="center left",
		bbox_to_anchor =(1, 0, 0.5, 1))

plt.setp(autotexts, size = 8, weight ="bold")
ax.set_title("Prioritizing Vaccination for States of India",fontdict=None, loc='center', pad=None)

# show plot
plt.savefig(root_dir+'Piechart_covid.png')
plt.show()



