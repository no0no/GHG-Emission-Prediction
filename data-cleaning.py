# coding=utf-8
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pd.options.display.max_rows = 500
pd.options.display.max_columns = 500
pd.options.display.width = 500

EMISSION_PATH = os.path.join("datasets")

def load_emission_data(emission_path=EMISSION_PATH):
	csv_path = os.path.join(emission_path, "final-emission.csv")
	return pd.read_csv(csv_path, encoding="ISO-8859-1")

emission = load_emission_data()
emission.drop(
	columns=[
		"Unnamed: 0",
		"City name (CDP)",
		"City name (carbonn)",
		"City name (PKU)",
		"City name (GEA)",
		"City name (UITP)",
		"City name (WB)",
		"Definition (CDP)",
		"Definition (carbonn)",
		"Definition (WB)",
		"Study year (WB)",
		"Emissions protocol",
		"Gases included (CDP)",
		"Methodology details (CDP)",
		"Increase/Decrease from last year (CDP)",
		"Reason for increase/decrease in emissions (CDP)",
		"CDP2016 data edited (CDP)",
		"Coordinate source (others)",
		"Region",
		"Population source (others)",
		"Ancillary from GEA+",
		"City area source year (others)",
		"City area source (others)",
		"Weather station ID (GEA+)",
		"GDP source (CDP)",
		"GDP-PPP source (others)",
		"nGDP source (others)",
		"GDP year (carbonn)",
		"Household source (GEA+)",
		"Household size comment (GEA+)",
		"Urbanization ratio (GEA+) [percent]",
		"Water bounded (GEA+)",
		"Other bounded (GEA+)",
		"Mean one-way travel time source (others)",
		"Household size source (others)",
		"Household size comment (others)",
		"Congestion change (TomTom) [× 100 percent]",
		"Urban area name (UEX)",
		"Year from CIA (others)",
		"AQF (CDP/GEA)",
		"AQF (CDP/WB)",
		"AQF (CDP/OTHERS)",
		"AQF (PKU/GEA)",
		"AQF (PKU/WB)",
		"AQF (PKU/OTHERS)",
		"PQF (CDP)",
		"PQF (carbonn)",
		"PQF (WB)",
		"PQF (WB2010)",
		"PQF (OTHERS)",
		"HQF (GEA+)",
		"HQF (OTHERS)",
		"Scope-1 source dataset",
		"Population 1950 (WB)",
		"Population 1990 (WB)",
		"Population 2010 (WB)",
		"Population growth rate 1950-2010 (WB) [people/60years]",
		"Population growth rate 1990-2010 (WB) [people/20years]",
		"GDP year (CDP)",
		"nGDP year (others)",
		"GDP-PPP year (others)",
		"Energy per capita CO2 (WB) [tCO2-eq/capita/yr]",
		"Center of commerce index (GEA+) [dimensionless]",
		"Household size year (GEA+)",
		"Diesel price (GEA+) [USD/liter]",
		"Gasoline price (GEA+) [USD/liter]",
		"Household size year (others)",
		"Governance (IESE) [dimensionless]",
		"International impact (IESE) [dimensionless]",
		"Public management (IESE) [dimensionless]",
		"Social cohesion (IESE) [dimensionless]",
		"CIMI (IESE) [dimensionless]",
		"CIMI ranking (IESE) [dimensionless]",
		"CIMI performance (IESE) [dimensionless]",
		"Congestion rank (INRIX) [dimensionless]",
		"Peak hours spent in congestion (INRIX) [hours]",
		"INRIX congestion index (INRIX) [dimensionless]",
		"Average congestion rate (INRIX) [percent]",
		"Congestion rank (TomTom) [dimensionless]",
		"Congestion level (TomTom) [× 100 percent]",
		"Congestion change (TomTom) [× 100 percent]",
		"Morning peak (TomTom) [percent]",
		"Evening peak (TomTom) [percent]",
		"Economy (IESE) [dimensionless]",
		"Environment (IESE) [dimensionless]",
		"Human capital (IESE) [dimensionless]",
		"Mobility and transportation (IESE) [dimensionless]",
		"Technology (IESE) [dimensionless]",
		"Urban planning (IESE) [dimensionless]",
		"Urban population (PKU)",
		"Scope-1 GHG emissions [tCO2 or tCO2-eq]",
		"Scope-1 GHG emissions units",
		"Scope-2 (CDP) [tCO2-eq]",
		"S1 lower bound [tCO2] (CDP)",
		"S1 upper bound [tCO2] (CDP)",
		"S1 mean (CDP) [tCO2]",
		"TOT lower bound [tCO2] (CDP)",
		"TOT upper bound [tCO2] (CDP)",
		"TOT mean (CDP) [tCO2]",
		"Scope fraction (CDP)",
		"CDD 23C (GEA+) [degrees C × days]",
		"HDD 15.5C (GEA+) [degrees C × days]",
		"HDD 15.5C (clim) [degrees C × days]",
		"CDD 23C (clim) [degrees C × days]",
		"Emissions Quality Flag (CDP)"
	],
	axis=1,
	inplace=True
)

# Fill in missing reporting year values using median
reporting_year_median = emission["Reporting year (CDP)"].median()
emission["Reporting year (CDP)"].fillna(reporting_year_median, inplace=True)

# Fill in missing city coordinates
for i in range(0, len(emission["City name"])):
	if pd.isnull(emission.loc[i, "City location (CDP) [degrees]"]):
		lat = emission.loc[i, "Latitude (others) [degrees]"].astype(str)
		long = emission.loc[i, "Longitude (others) [" \
									  "degrees]"].astype(str)
		lat_long = "(" + lat + ", " + long + ")"
		emission.at[i, "City location (CDP) [degrees]"] = lat_long

# No longer need Latitude and Longitude columns
emission.drop(
	columns=[
		"Latitude (others) [degrees]",
		"Longitude (others) [degrees]"
	],
	axis=1,
	inplace=True
)

# Fill in missing city population
for i in range(0, len(emission["City name"])):
	if pd.isnull(emission.loc[i, "Population (CDP)"]):
		if pd.isnull(emission.loc[i, "Population (carbonn)"]):
			if pd.isnull(emission.loc[i, "Population (GEA)"]):
				emission.at[i, "Population (CDP)"] = \
					emission.loc[i, "Population (others)"]
			else:
				emission.at[i, "Population (CDP)"] = \
					emission.loc[i, "Population (GEA)"]
		else:
			emission.at[i, "Population (CDP)"] = emission.loc[
				i, "Population (carbonn)"]

emission.drop(
	columns=[
		"Population (carbonn)",
		"Population (GEA)",
		"Population (UITP)",
		"Population (WB)",
		"Population (others)"
	],
	axis=1,
	inplace=True
)

# Fill in Population year (CDP)
for i in range(0, len(emission["City name"])):
	if pd.isnull(emission.loc[i, "Population year (CDP)"]):
		if pd.isnull(emission.loc[i, "Population year (carbonn)"]):
			if pd.isnull(emission.loc[i, "Population year (WB)"]):
				emission.at[i, "Population year (CDP)"] = \
					emission.loc[i, "Population year (others)"]
			else:
				emission.at[i, "Population year (CDP)"] = \
					emission.loc[i, "Population year (WB)"]
		else:
			emission.at[i, "Population year (CDP)"] = \
				emission.loc[i, "Population year (carbonn)"]

emission.drop(
	columns=[
		"Population year (carbonn)",
		"Population year (WB)",
		"Population year (others)"
	],
	axis=1,
	inplace=True
)

# Fill in missing city area
for i in range(0, len(emission["City name"])):
	if pd.isnull(emission.loc[i, "City area (CDP) [km2]"]):
		if pd.isnull(emission.loc[i, "City area (GEA) [km2]"]):
			if pd.isnull(emission.loc[i, "City area (WB) [km2]"]):
				emission.at[i, "City area (CDP) [km2]"] = emission.loc[
					i, "City area (others) [km2]"]
			else:
				emission.at[i, "City area (CDP) [km2]"] = emission.loc[
					i, "City area (WB) [km2]"]
		else:
			emission.at[i, "City area (CDP) [km2]"] = emission.loc[i,
														"City area (GEA) [km2]"]

emission.drop(
	columns=[
		"City area (GEA) [km2]",
		"City area (WB) [km2]",
		"City area (others) [km2]"
	],
	axis=1,
	inplace=True
)

# Add Population density column
for i in range(0, len(emission["City name"])):
	if not (pd.isnull(emission.loc[i, "Population (CDP)"]) and
			pd.isnull(emission.loc[i, "City area (CDP) [km2]"])):
		emission.at[i, "Population density [people/km2]"] = \
			emission.loc[i, "Population (CDP)"] \
			/ emission.loc[i, "City area (CDP) [km2]"]

emission.drop(
	columns=[
		"Population density (GEA) [people/km2]",
		"Population density (UITP) [people/km2]",
		"Population density (WB) [people/km2]",
		"Population/sqrt(area) (GEA) [people/km]",
		"Population/sqrt(area) (WB) [people/km]"
	],
	axis=1,
	inplace=True
)

# Fill in Household size
for i in range(0, len(emission["City name"])):
	if pd.isnull(emission.loc[i, "Household size (GEA+) [people/household]"]):
		emission.at[i, "Household size (GEA+) [people/household]"] = \
			emission.loc[i, "Household size (others) [people/household]"]

emission.drop(columns=["Household size (others) ["
								  "people/household]"], axis=1, inplace=True)

# Fill in GDP (USD)
# 2016 Avg. closing price: 1USD = 6.65RMB, 10000RMB = 1503.76USD
# Source - www.macrotrends.net

for i in range(0, len(emission["City name"])):
	if pd.isnull(emission.loc[i, "GDP (PKU) [10000 RMB]"]):
		if pd.isnull(emission.loc[i, "GDP-PPP (others) [$BN]"]):
			if not pd.isnull(emission.loc[i, "nGDP (others) [$BN]"]):
				emission.at[i, "GDP (USD)"] = \
					emission.loc[i, "nGDP (others) [$BN]"] * 1000000000
		else:
			emission.at[i, "GDP (USD)"] = \
				emission.loc[i, "GDP-PPP (others) [$BN]"] * 1000000000
	else:
		emission.at[i, "GDP (USD)"] = \
			emission.loc[i, "GDP (PKU) [10000 RMB]"] * 1503.76

def currency_conversion(label, index, rate):
	if label == "CDP":
		for i in index:
			emission.at[i, "GDP (USD)"] = \
				emission.loc[i, "GDP (CDP) [multiple units]"] * rate
	elif label == "carbonn":
		for i in index:
			emission.at[i, "GDP (USD)"] = \
				emission.loc[i, "GDP (carbonn) [multiple units]"] * rate

# Source: https://www.irs.gov/individuals/international-taxpayers/yearly-average-currency-exchange-rates
# US currency
currency_conversion("CDP", [15, 33, 101, 124, 205, 222, 236, 297, 329], 1)
currency_conversion("carbonn", [5, 51, 85, 163, 169, 192, 253, 298], 1)

# 1GBP = 1.35USD -- Great British Pounds
currency_conversion("CDP", [37], 1.35)

# 1EUR = 1.11USD -- Euros
currency_conversion("CDP", [88, 117, 160], 1.11)
currency_conversion("carbonn", [301], 1.11)

# 1NZD = 0.70USD -- New Zealand Dollars
currency_conversion("CDP", [311], 0.70)

# 1AUD = 0.74USD -- Australian Dollars
currency_conversion("CDP", [54], 0.74)

# 1JOD = 1.4114USD -- Jordanian Dinars
currency_conversion("CDP", [10], 1.4114)

# 1USD = 13302.2IRD -- Indonesian Rupiahs
currency_conversion("CDP", [39], 1/13302.2)

# 1USD = 3.632BRL -- Brazilian Reals
currency_conversion("CDP", [103, 214], 1/3.632)

# 1USD = 7.000DKK -- Danish Krones
currency_conversion("CDP", [98, 123], 1/7.000)

# 1USD = 1.379CAD -- Canadian Dollars
currency_conversion("CDP", [176, 314], 1/1.379)

# 1USD = 3.146TRY -- Turkish Liras
currency_conversion("CDP", [150], 1/3.416)

# 1USD = 126.256ISK -- Icelandic Kronas
currency_conversion("CDP", [241], 1/126.256)

# 1USD = 69.956INR -- Indian Rupees
currency_conversion("carbonn", [105], 1/69.956)

# 1USD = 36.778THD -- Thai Bahts
currency_conversion("carbonn", [113, 153, 220, 299], 1/36.778)

# 1USD = 15.319ZAR -- South African Rands
currency_conversion("carbonn", [203, 339], 1/15.319)

# 1USD = 113.138JPY -- Japanese Yens
currency_conversion("carbonn", [157], 1/113.138)

# 1USD = 8.910SEK -- Swedish Krona
currency_conversion("carbonn", [303, 308, 341], 1/8.910)

# 1USD = 14.7015NAD -- Namibian Dollars
currency_conversion("carbonn", [313], 1/14.7015)

emission.drop(
	columns=[
		"GDP (CDP) [multiple units]",
		"GDP unit (CDP)",
		"GDP (carbonn) [multiple units]",
		"nGDP (carbonn) [multiple units]",
		"GDP unit (carbonn)",
		"GDP (PKU) [10000 RMB]",
		"GDP-PPP (others) [$BN]",
		"nGDP (others) [$BN]",
		"GDP-PPP/capita (others) [USD/capita]",
		"nGDP/capita (others) [USD/capita]",
		"GDP-PPP/capita (GEA) [USD/year]",
		"GDP-PPP/capita (UITP) [USD/year]",
		"GDP-PPP/capita (WB) [USD/year]"
	],
	axis=1,
	inplace=True
)

# Simple fill-ins of Total emissions
for i in range(len(emission["City name"])):
	if pd.isnull(emission.loc[i, "Total emissions (CDP) [tCO2-eq]"]):
		emission.at[i, "Total emissions (CDP) [tCO2-eq]"] = \
			emission.loc[i, "CO2 emissions per capita (PKU) [tCO2/capita]"] \
			* emission.loc[i, "Population (CDP)"]

#print(emission.info())
corr_matrix = emission.corr()
print(corr_matrix["Total emissions (CDP) [tCO2-eq]"].sort_values(
		ascending=False))
#print(emission[["City name", "GDP (USD)"]])
#emission.to_csv("datasets/results/emissions.csv", encoding="ISO-8859-1")
