

import numpy as np
import pandas as pd
# Plotting Packages
import matplotlib.pyplot as plt
# Custom functions to help project
from ResourceCode import *


# TASK 1.1: read in country values (from CountryValues.csv) into country dataframe
country_df = pd.read_csv('CountryValues.csv',index_col=0)
country_df = country_df.transpose()

# TASK 1.2: read in unit values (from UnitValues.csv) into unit_df dataframe,
unit_df = pd.read_csv('UnitValues.csv',index_col=0)

# and conve to a 1D series (variable name: units) for easily accessing
#units = unit_df["Unit"]
#units = unit_df.set_index('Name')
units = unit_df["Unit"]

def print_df(df_in, units):
    print(df_in.transpose().merge(units,left_index=True, right_index=True))
#print_df(country_df, units)

# TASK 1.3: set up (empty, to be filled in) model dataframe called model_df
# # - it should have one index column ("Name") and two rows called "CountryA" and "CountryB"
#model_df = pd.DataFrame(data, columns=['Name'], index =['CountryA','CountryB'])
model_df = pd.DataFrame()
model_df["Name"] = ['CountryA', 'CountryB']
model_df.set_index("Name", inplace = True)
#print(model_df)
#print_df(model_df, units)
# check to see that things have loaded: print the population of CountryB:
# - this should print: "Population of Country B: 110000000 people"
#print("Population of Country B:", country_df["Population"]["CountryB"], units["Population"])


# TASK 1.4: Print out (formatted nicely with units) the amount of
# water flowing into the region for Country B
# (hint: stored in the "Water Into Region" value of the country_df dataframe)
#print("Water Into Country B's Region: ", country_df["Water Into Region"]["CountryB"], units["Water Into Region"])

# TASK 2.1: calculate and add the Total Energy Demand for the countries to the model (model_df)
# - Total Energy Demand is equal to the Population times the Energy Demand Coefficient

total_demand = (country_df["Energy Demand Coefficient"]) * (country_df["Population"])
model_df["Total Energy Demand"] = total_demand.values


# TASK 3.1: create new field in model_df called "Percent Energy from Renewable" and
# set the percent energy from renewable for CountryA (to 15%) and CountryB (to 25%)

model_df["Percent Energy from Renewable"] = ['15' , '25']

# calculate and print the energy breakdown (calcEnergyBreakdown is defined in ResourceCode.py)

model_df = calcEnergyBreakdown(country_df, model_df)

#print('** This is the model after completing TASK 3.2:')
#print_df(model_df,units)

# calculate and print the energy costs (calcEnergyCosts is defined in ResourceCode.py)
model_df = calcEnergyCosts(country_df, model_df)
#print('** This is the model after completing TASK 3.3:')
#print_df(model_df, units)

# calculate and print the fossil fuel emissions (calcFossilFuelEmissions is defined in ResourceCode.py)
model_df = calcFossilFuelEmissions(model_df)
#print('** This is the model after completing TASK 3.4:')
#print_df(model_df, units)

# calculate and print the water required for energy (calcWaterRequriredEnergy is defined in ResourceCode.py)
model_df = calcWaterRequiredEnergy(country_df, model_df)
#print('** This is the model after completing TASK 3.5:')
#print_df(model_df, units)

# use the modelEnergy function in TASK 4 to model energy:
model_df = modelEnergy(country_df, model_df)
#print('** This is the model after completing TASK 4:')
#print_df(model_df, units)
# TASK 5: use modelEnergy to check various simulations of the model
# - vary input paraemters
# - check output model values to see if they match the given ones


# calculate and print the WSI for Energy via calcWSI function (defined in ResourceCode)
# - (e.g. ratio water use to make energy to water available)
# This code is to test the results of TASK 6:

WSI_energy_countryB = calcWSI(model_df["Water Required for Energy"]["CountryB"], country_df["Water Into Region"]["CountryB"])
#print('WSI for Energy in country B is:')
#print(WSI_energy_countryB)

# TASKS 7.1, 7.2, and 7.3:
# - TASK 7.1: implement code to vary renewable percentages and keep track of
#   percent value, total cost, emissions about, and WSI for Energy values for later evaluation
percent_renewable = [0,25,50,75,100]

countryB_df = pd.DataFrame(columns = ['%', 'Total Energy Cost', 'Emission from Fossil Fuel','WSI for Energy'])
countryB_df['%'] = range(0, 101)

arr_totalE = []
arr_emission = []
arr_WSI = []
for i in range(0, 101):
    model_df['Percent Energy from Renewable']['CountryB'] = i
    model_df = modelEnergy(country_df, model_df)
    #countryB_df[i]['Total Energy Cost']= model_df['Cost Energy Total']['CountryB']
    total_energy =  model_df['Cost Energy Total']['CountryB']
    emiss = model_df['Emissions from Fossil Fuel']['CountryB']
    wsi= calcWSI(model_df["Water Required for Energy"]["CountryB"], country_df["Water Into Region"]["CountryB"])
    arr_totalE.append(total_energy)
    arr_emission.append(emiss)
    arr_WSI.append(wsi)

countryB_df['Total Energy Cost'] =  arr_totalE
countryB_df['Emission from Fossil Fuel'] =  arr_emission
countryB_df['WSI for Energy'] =  arr_WSI
  
    #countryB_df[i]['Emission from fossil fuel']=model_df['Emissions from Fossil Fuel']['CountryB']
    #countryB_df[i]['WSI for energy']= calcWSI(model_df["Water Required for Energy"]["CountryB"], country_df["Water Into Region"]["CountryB"])
    
#print(countryB_df)
# - TASK 7.2: use that code to optimize for budget (find minimum budget) and print
#   out associated values
print( "The minimum budget is", countryB_df['Total Energy Cost'].min(), "the associated emissions amount is",  countryB_df['Emission from Fossil Fuel'][25], "and the WSI energy is", countryB_df['WSI for Energy'][25])
# - TASK 7.3: then optimize the budget for certain SDGs: find the minimum budget needed in order to achieve certain Sustainable Development Goals (levels of emissions and WSI ratios)
print( "The minimum budget needed in order to achieve certain Sustainable Development Goals is", countryB_df['Total Energy Cost'][64], "the associated emissions amount is",  countryB_df['Emission from Fossil Fuel'][64], "and the WSI energy is", countryB_df['WSI for Energy'][64])

# TASK 8.1: Generate Visualizations
# - As the amount of renewable energy increases, visualize the effect
#   on Budget, Fossil Fuel Emissions, and the WSI for Energy values.

#BUDGET GRAPH
plt.figure()
plt.plot(countryB_df['%'].values, arr_totalE)
plt.xticks(np.arange(0, 101, 5))
plt.title('Budget vs % Renewable Energy')
plt.xlabel('Percentage of Renewable Energy (%)')
plt.ylabel('Total Budget ($)')
plt.savefig("Budget.png")


#EMISSION GRAPH
plt.figure()
plt.plot(countryB_df['%'].values, arr_emission)
plt.xticks(np.arange(0, 101, 5))
plt.title('Fossil Fuel Emissions vs % Renewable Energy')
plt.xlabel('Percentage of Renewable Energy (%)')
plt.ylabel('Total Emissions (matric tons)')
plt.savefig("Emission.png")

#WSI GRAPH
plt.figure()
plt.plot(countryB_df['%'].values, arr_WSI)
plt.xticks(np.arange(0, 101, 5))
plt.title('WSI vs % Renewable Energy')
plt.xlabel('Percentage of Renewable Energy (%)')
plt.ylabel('Total WSI for Energy values')
plt.savefig("WSI.png")