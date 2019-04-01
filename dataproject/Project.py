#Import the neccesary packages
import numpy as np
import pandas as pd
import pydst
import matplotlib.pyplot as plt

Dst = pydst.Dst(lang='en')
Dst.get_data(table_id='INDKP101')
Vars = Dst.get_variables(table_id='INDKP101')
Everything = Dst.get_data(table_id = 'INDKP101', variables={'OMRÅDE':['000','01','02','03','04','05','06','07','08','09','10','11'], 'KOEN':['M','K'], 'TID':['*'], 'ENHED':['116'], 'INDKOMSTTYPE':['100']}).rename(columns={'OMRÅDE':'Municipality'})

#Changing the index to Municipality:
New_index = Everything.set_index('Municipality')

#Picking out the neccesary variables:
Sortet = New_index[['TID','KOEN','INDHOLD']].rename(columns={'KOEN':'Gender', 'TID':'Year', 'INDHOLD':'Disposal income'})

#Making a table for each gender:
Men = Sortet[Sortet['Gender']=='Men'].sort_values(['Municipality','Year']).rename(columns={'Disposal income':'Disposal income men'})
Women = Sortet[Sortet['Gender']=='Women'].sort_values(['Municipality', 'Year']).rename(columns={'Disposal income':'Disposal income women'})

#We don't want year to appear twice when we concat:
Women_without_year = Women[['Gender', 'Disposal income women']]

#Concatenate the two tables:
Concatenated_table = pd.concat([Men, Women_without_year], axis=1)

#Removing the gender nicer look:
Final_table = Concatenated_table[['Year','Disposal income men','Disposal income women']]
Final_table

#Creates a function with provides the difference between the genders in %:
def f(x):
    """Gives the procentual difference between the genders"""
    return (x['Disposal income men']/x['Disposal income women']-1)*100
Final_table['Difference in %']=Final_table.apply(f, axis=1)

#Example on finding the numbers for All Denmark:
Whole_country = Final_table.loc['All Denmark']
print(Whole_country)

#We can show this in a graph like this:
def Difference(Region):
    plt.plot(Region['Year'],Region['Difference in %'])
    plt.xlabel('Year')
    plt.ylabel('Difference in %')
    plt.title('Difference in disposal income for all Denmark')
    plt.grid(True)
    return plt.show()
Difference(Whole_country)

#Makes all the provinces to variables for later use:
All_Denmark = Final_table.loc['All Denmark']
Province_Bornholm = Final_table.loc['Province Bornholm']
Province_CityOfCopenhagen = Final_table.loc['Province Byen København']
Province_Fyn = Final_table.loc['Province Fyn']
Province_GreaterCopenhagen = Final_table.loc['Province Københavns omegn']
Province_NorthernJylland = Final_table.loc['Province Nordjylland']
Province_NorthernSjælland = Final_table.loc['Province Nordsjælland']
Province_SouthJylland = Final_table.loc['Province Sydjylland']
Province_West_and_SouthSjælland = Final_table.loc['Province Vest- og Sydsjælland']
Province_WestJylland = Final_table.loc['Province Vestjylland']
Province_EastJylland = Final_table.loc['Province Østjylland']
Province_EastSjælland = Final_table.loc['Province Østsjælland']


def standard_for_all(Municipality):
    plt.subplot(2,1,1)
    s = np.random.normal(Municipality['Disposal income men'].mean(), Municipality['Disposal income men'].std(), 10000)
    count, bins, ignored = plt.hist(s, 30, density=True)
    plt.plot(bins, 1/(Municipality['Disposal income men'].std() *np.sqrt(2*np.pi)) * np.exp(-(bins-Municipality['Disposal income men'].mean())**2 / (2 * Municipality['Disposal income men'].std()**2)), linewidth = 2, label=Municipality['Disposal income men'].std())
    plt.title('Men')
    plt.xlabel('Disposal income')
    plt.legend(bbox_to_anchor=(1.05,1),loc = 5, borderaxespad=0)
    plt.subplot(2,1,2)
    s = np.random.normal(Municipality['Disposal income women'].mean(), Municipality['Disposal income women'].std(), 10000)
    count, bins, ignored = plt.hist(s, 30, density=True)
    plt.plot(bins, 1/(Municipality['Disposal income women'].std() *np.sqrt(2*np.pi)) * np.exp(-(bins-Municipality['Disposal income women'].mean())**2 / (2 * Municipality['Disposal income women'].std()**2)), linewidth = 2, label=Municipality['Disposal income women'].std())
    plt.title('Women')
    plt.xlabel('Disposal income')
    plt.legend(bbox_to_anchor=(1.05,1),loc = 5, borderaxespad=0)
    plt.subplots_adjust(top=2, bottom=0, left=0, right=1, hspace=0.2)
       
    return plt.show
standard_for_all(Province_Bornholm)