import pandas as pd

class Cleaner:

    def data_loader(self, data_path):

        df = pd.read_excel(data_path)
        return df

    # Drops textual and irrelevant features
    def data_dropper(self, df):

        dropped_data = df.copy()
        to_drop = ['City name (CDP)',
                   'City location (CDP) [degrees]',
                   'Built-up area (PKU) [km2]',
                   'Other bounded (GEA+)',
                   'Energy per capita CO2 (WB) [tCO2-eq/capita/yr]',
                   'CO2 emissions per capita (PKU) [tCO2/capita]',
                   'City name',
                   'Country',
                   'Region',
                   'Unnamed: 0',
                   'Scope-1 GHG emissions units',
                   'City name (carbonn)',
                   'City name (PKU)',
                   'City name (GEA)',
                   'City name (UITP)',
                   'City name (WB)',
                   'Definition (CDP)',
                   'Definition (carbonn)',
                   'Definition (WB)',
                   'Study year (WB)',
                   'Reporting year (CDP)',
                   'Scope-1 source dataset',
                   'Year of emission',
                   'Emissions protocol',
                   'Gases included (CDP)',
                   'Methodology details (CDP)',
                   'Increase/Decrease from last year (CDP)',
                   'Reason for increase/decrease in emissions (CDP)',
                   'CDP2016 data edited (CDP)',
                   'Emissions Quality Flag (CDP)',
                   'Coordinate source (others)',
                   'Population year (WB)',
                   'Population year (others)',
                   'Population source (others)',
                   'Ancillary from GEA+',
                   'City area source year (others)',
                   'City area source (others)',
                   'Weather station ID (GEA+)',
                   'GDP year (CDP)',
                   'GDP source (CDP)',
                   'GDP-PPP source (others)',
                   'GDP-PPP year (others)',
                   'nGDP source (others)',
                   'nGDP year (others)',
                   'Household size year (GEA+)',
                   'Household source (GEA+)',
                   'Household size comment (GEA+)',
                   'Mean one-way travel time year (others)',
                   'Mean one-way travel time source (others)',
                   'Household size year (others)',
                   'Household size source (others)',
                   'Household size comment (others)',
                   'Urban area name (UEX)',
                   'Year from CIA (others)']
        return dropped_data.drop(to_drop, axis=1)

    if __name__ == "__main__":
        pass

#Load Main Data
test = Cleaner()
main_data = test.data_loader('Data/D_FINAL.xlsx')

#Drop Textual Features
dropped_data = test.data_dropper(main_data)
dropped_data.to_excel("Data/Dropped.xlsx")

#Merge Scope-1 and Scope-2 into Total Emissions
dropped_data['Scope-1 GHG emissions [tCO2 or tCO2-eq]'] = dropped_data['Scope-1 GHG emissions [tCO2 or tCO2-eq]'].fillna(0)
dropped_data['Scope-2 (CDP) [tCO2-eq]'] = dropped_data['Scope-2 (CDP) [tCO2-eq]'].fillna(0)
dropped_data['Total emissions (CDP) [tCO2-eq]'] = dropped_data['Total emissions (CDP) [tCO2-eq]'].fillna(dropped_data['Scope-1 GHG emissions [tCO2 or tCO2-eq]'] + dropped_data['Scope-2 (CDP) [tCO2-eq]'])
dropped_data.to_excel("Data/Merged.xlsx")

#Multiply Scope-1 and Scope-2 Fraction by Total Emissions
dropped_data['Scope fraction (CDP)'] = dropped_data['Scope fraction (CDP)'].fillna(1)
dropped_data['Total emissions (CDP) [tCO2-eq]'] = dropped_data['Total emissions (CDP) [tCO2-eq]'] * dropped_data['Scope fraction (CDP)']
dropped_data.to_excel("Data/Merged.xlsx")

#Drop Scope-1 and Scope-2 and Scope fraction (CDP) from Set
merged_data = dropped_data.drop(['Scope-1 GHG emissions [tCO2 or tCO2-eq]', 'Scope-2 (CDP) [tCO2-eq]', 'Scope fraction (CDP)'], axis=1)
merged_data.to_excel("Data/Merged.xlsx")

#Drop population (except "Population (others)")
to_drop = ['Population (WB)',
           'Population (UITP)',
           'Population (GEA)',
           'Urban population (PKU)',
           'Population year (carbonn)',
           'Population (carbonn)',
           'Population year (CDP)',
           'Population (CDP)',
           'Population 1950 (WB)',
           'Population 1990 (WB)',
           'Population 2010 (WB)',
           'Population growth rate 1950-2010 (WB) [people/60years]',
           'Population growth rate 1990-2010 (WB) [people/20years]']

merged_data.drop(to_drop, axis=1, inplace=True)
merged_data.to_excel("Data/Merged.xlsx")

#Drop city area (except "City area (others) [km2]")
to_drop = ['City area (CDP) [km2]',
           'City area (GEA) [km2]',
           'City area (WB) [km2]',]
merged_data.drop(to_drop, axis=1, inplace=True)
merged_data.to_excel("Data/Merged.xlsx")

#Drop statistical information about Scope-1 and 2 (too correlated with Total Emissions)
to_drop = ['S1 lower bound [tCO2] (CDP)',
           'S1 upper bound [tCO2] (CDP)',
           'S1 mean (CDP) [tCO2]',
           'TOT lower bound [tCO2] (CDP)',
           'TOT upper bound [tCO2] (CDP)',
           'TOT mean (CDP) [tCO2]']
merged_data.drop(to_drop, axis=1, inplace=True)
merged_data.to_excel("Data/Merged.xlsx")

#Drop PQF, AQF and HQF values as they are data quality checks and not good predictors
to_drop = ['AQF (CDP/GEA)',
           'AQF (CDP/WB)',
           'AQF (CDP/OTHERS)',
           'AQF (PKU/GEA)',
           'AQF (PKU/WB)',
           'AQF (PKU/OTHERS)',
           'PQF (CDP)',
           'PQF (carbonn)',
           'PQF (WB)',
           'PQF (WB2010)',
           'PQF (OTHERS)',
           'HQF (GEA+)',
           'HQF (OTHERS)']
merged_data.drop(to_drop, axis=1, inplace=True)
merged_data.to_excel("Data/Merged.xlsx")

#Merge population density and drop unmerged
merged_data['Population Density Merged (GEA/UITP/WB)'] = merged_data[['Population density (GEA) [people/km2]',
                                                                     'Population density (UITP) [people/km2]',
                                                                     'Population density (WB) [people/km2]']].mean(axis=1)
to_drop = ['Population density (GEA) [people/km2]',
           'Population density (UITP) [people/km2]',
           'Population density (WB) [people/km2]']
merged_data.drop(to_drop, axis=1, inplace=True)
merged_data.to_excel("Data/Merged.xlsx")

#Drop population/km
to_drop = ['Population/sqrt(area) (GEA) [people/km]', 'Population/sqrt(area) (WB) [people/km]']
merged_data.drop(to_drop, axis=1, inplace=True)
merged_data.to_excel("Data/Merged.xlsx")

#Merge BUAs 1990, 2000, 2014 and drop unmerged
merged_data['Low BUA Mean - 1990, 2000, 2014 (UEX) [km2]'] = merged_data[['Low BUA - 1990 (UEX) [km2]',
                                                                          'Low BUA - 2000 (UEX) [km2]',
                                                                          'Low BUA - 2014 (UEX) [km2]']].mean(axis=1)
merged_data['High BUA Mean - 1990, 2000, 2014 (UEX) [km2]'] = merged_data[['High BUA - 1990 (UEX) [km2]',
                                                                           'High BUA - 2000 (UEX) [km2]',
                                                                           'High BUA - 2014 (UEX) [km2]']].mean(axis=1)
to_drop = ['Low BUA - 1990 (UEX) [km2]',
           'Low BUA - 2000 (UEX) [km2]',
           'Low BUA - 2014 (UEX) [km2]',
           'High BUA - 1990 (UEX) [km2]',
           'High BUA - 2000 (UEX) [km2]',
           'High BUA - 2014 (UEX) [km2]']
merged_data.drop(to_drop, axis=1, inplace=True)
merged_data.to_excel("Data/Merged.xlsx")

#Merge BUA %s 1990, 2000, 2014 and drop unmerged
merged_data['Low BUA % - 1990, 2000, 2014 (UEX) [percent]'] = merged_data[['Low BUA % - 1990 (UEX) [percent]',
                                                                          'Low BUA % - 2000 (UEX) [percent]',
                                                                          'Low BUA % - 2014 (UEX) [percent]']].mean(axis=1)
merged_data['High BUA % - 1990, 2000, 2014 (UEX) [percent]'] = merged_data[['High BUA % - 1990 (UEX) [percent]',
                                                                           'High BUA % - 2000 (UEX) [percent]',
                                                                           'High BUA % - 2014 (UEX) [percent]']].mean(axis=1)
to_drop = ['Low BUA % - 1990 (UEX) [percent]',
           'Low BUA % - 2000 (UEX) [percent]',
           'Low BUA % - 2014 (UEX) [percent]',
           'High BUA % - 1990 (UEX) [percent]',
           'High BUA % - 2000 (UEX) [percent]',
           'High BUA % - 2014 (UEX) [percent]']
merged_data.drop(to_drop, axis=1, inplace=True)
merged_data.to_excel("Data/Merged.xlsx")

#Merge BUA population densities 1990, 2000, 2014 and drop unmerged
merged_data['Low BUA population density Mean - 1990, 2000, 2014 (UEX) [people/km2]'] = \
    merged_data[['Low BUA population density - 1990 (UEX) [people/km2]',
                 'Low BUA population density - 2000 (UEX) [people/km2]',
                 'Low BUA population density - 2014 (UEX) [people/km2]']].mean(axis=1)
merged_data['High BUA population density Mean - 1990, 2000, 2014 (UEX) [people/km2]'] = \
    merged_data[['High BUA population density - 1990 (UEX) [people/km2]',
      'High BUA population density - 2000 (UEX) [people/km2]',
      'High BUA population density - 2014 (UEX) [people/km2]']].mean(axis=1)

to_drop = ['Low BUA population density - 1990 (UEX) [people/km2]',
           'Low BUA population density - 2000 (UEX) [people/km2]',
           'Low BUA population density - 2014 (UEX) [people/km2]',
           'High BUA population density - 1990 (UEX) [people/km2]',
           'High BUA population density - 2000 (UEX) [people/km2]',
           'High BUA population density - 2014 (UEX) [people/km2]']
merged_data.drop(to_drop, axis=1, inplace=True)
merged_data.to_excel("Data/Merged.xlsx")

#Drop IESE predictors
to_drop = ['Environment (IESE) [dimensionless]',
                   'Governance (IESE) [dimensionless]',
                   'Human capital (IESE) [dimensionless]',
                   'International impact (IESE) [dimensionless]',
                   'Mobility and transportation (IESE) [dimensionless]',
                   'Public management (IESE) [dimensionless]',
                   'Social cohesion (IESE) [dimensionless]',
                   'Technology (IESE) [dimensionless]',
                   'Urban planning (IESE) [dimensionless]',
                   'CIMI (IESE) [dimensionless]',
                   'CIMI ranking (IESE) [dimensionless]',
                   'CIMI performance (IESE) [dimensionless]',
           'Economy (IESE) [dimensionless]']
merged_data.drop(to_drop, axis=1, inplace=True)
merged_data.to_excel("Data/Merged.xlsx")

#Drop Tom-Tom predictors
to_drop = ['Congestion rank (TomTom) [dimensionless]',
           'Congestion level (TomTom) [× 100 percent]',
           'Congestion change (TomTom) [× 100 percent]',
           'Evening peak (TomTom) [percent]',
           'Morning peak (TomTom) [percent]']
merged_data.drop(to_drop, axis=1, inplace=True)
merged_data.to_excel("Data/Merged.xlsx")

#Drop INRIX
to_drop = ['Congestion rank (INRIX) [dimensionless]',
           'Peak hours spent in congestion (INRIX) [hours]',
           'INRIX congestion index (INRIX) [dimensionless]',
           'Average congestion rate (INRIX) [percent]']
merged_data.drop(to_drop, axis=1, inplace=True)
merged_data.to_excel("Data/Merged.xlsx")

#Drop all GDPs besides nGDP
to_drop = ['GDP (CDP) [multiple units]',
           'Income per capita (PKU) [RMB/capita]',
           'GDP unit (CDP)',
           'GDP (carbonn) [multiple units]',
           'nGDP (carbonn) [multiple units]',
           'GDP unit (carbonn)',
           'GDP year (carbonn)',
           'GDP (PKU) [10000 RMB]',
           'GDP-PPP (others) [$BN]',
           'GDP-PPP/capita (others) [USD/capita]',
           'nGDP/capita (others) [USD/capita]',
           'GDP-PPP/capita (GEA) [USD/year]',
           'GDP-PPP/capita (UITP) [USD/year]',
           'GDP-PPP/capita (WB) [USD/year]']
merged_data.drop(to_drop, axis=1, inplace=True)
merged_data.to_excel("Data/Merged.xlsx")

#Check correlations
#corr_matrix = merged_data.corr()
#print(corr_matrix['Total emissions (CDP) [tCO2-eq]'].sort_values(ascending=False))
#print(merged_data)