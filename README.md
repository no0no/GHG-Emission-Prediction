# GHG-Emission-Prediction

## Introduction
In this repository, we present a machine learning approach to prediciting the emissions of city's greenhouse gases (also known as GHG). We analyze a list of socio-economic variables of each city such as population size, hours spent in traffic, gross domestic product, energy consumption, etc, and find the correlation between those variables and the amount of GHG emissions each city generates.

<img src="https://i.imgur.com/jTkUqqS.png" alt="City Map">
<img src="https://i.imgur.com/pkKrQFl.png" alt="Heat Map">
<img src="https://i.imgur.com/lG7fUEC.png" alt="Outliers - After">
<img src="https://i.imgur.com/KhB9xpB.png" alt="Outliers - Before">
<img src="https://i.imgur.com/sB2VEJ6.png" alt="Population Chart">
<img src="https://i.imgur.com/UnT0WdK.png" alt="City Area Chart">
<img src="https://i.imgur.com/DcPaLaG.png" alt="GDP Chart">

## Dataset Description
The dataset contains information of 343 cities and 179 socio-economic attributes of each city (343 × 179). The GHG emissions information in the dataset is taken from 3 main sources, namely, 187 cities are from Carbon Disclosure Project (CDP), 73 cities are from the Bonn Center for Local Climate Action and Reporting, and 83 cities (all in China) are from the database of Peking University (PKU). Other socio-economic attributes are also obtained from other sources that include TomTom (a navigation technology company), Instituto de Estudios Superiores de la Empresa (IESE), and the Center for International Earth Science Information Network (CIESIN). 

## Data Cleaning Process


## Data Preparation Process
For data preperation we used an open-source machine learning library in Python called `scikit-learn`. This library provides a simple and clean interface for performing machine learning tasks in just a few lines of code. We used `SimpleImputer` and `RobustScaler` to impute missing values and noramalize the data. We also took time to remove outliers in the dataset. Outliers were defined as any values that exceeded 1.5 times the standard deviation.

## Proposed Models
Our proposed models will include consist of a support-vector machine (SVR), a linear regressor, and an ensemble method called "bagging". We also conducted feature selection as our feature space is 299 × 32. We used sckit-learn's `SelectKBest` class and `f_regression()` function to select the top `k` features. After processing we recieved a `k` value of 3. Meaning that we have reduced our feature space to 299 × 3. The three features that were selected are population, high built-up area mean for the years 1990, 2000, 2014 and the low built-up area mean for the years 1990, 2000, 2014.

## Results
These three features tell us that the most important predictors for city emissions are it's built-up area and population. This is consistent wit the fact that concrete production alone accounts for 7% of total global emissions[1].

## References
[1] 
