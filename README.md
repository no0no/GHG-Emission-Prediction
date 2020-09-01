# GHG-Emission-Prediction

## Introduction
Predicts Green House Gas Emissions(GHG) of cities around the world using a dataset of 343 cities

<img src="https://i.imgur.com/jTkUqqS.png" alt="City Map">
<img src="https://i.imgur.com/pkKrQFl.png" alt="Heat Map">
<img src="https://i.imgur.com/lG7fUEC.png" alt="Outliers - After">
<img src="https://i.imgur.com/KhB9xpB.png" alt="Outliers - Before">
<img src="https://i.imgur.com/sB2VEJ6.png" alt="Population Chart">
<img src="https://i.imgur.com/UnT0WdK.png" alt="City Area Chart">
<img src="https://i.imgur.com/DcPaLaG.png" alt="GDP Chart">

## Dataset Description

## Data Cleaning Process

## Data Preparation Process
For data preperation we used an open-source machine learning library in Python called scikit-learn. This library provides a simple and clean interface for performing machine learning tasks in just a few lines of code. We used SimpleImputer and RobustScaler to impute missing values and noramalize the data. We also took time to remove outliers in the dataset. Outliers were defined as any values that exceeded 1.5 times the standard deviation.
## Proposed Models
Our proposed models will include consist of a support-vector machine (SVR), a linear regressor, and an ensemble method called "bagging". We also conducted feature selection as our feature space is 299 × 32. We used sckit-learn's SelectKBest class and f_regression() function to select the top k features. After processing we recieved a k value of 3. Meaning that we have reduced our feature space to 299 × 3. The three features that were selected are population, high built-up area mean for the years 1990, 2000, 2014 and the low built-up area mean for the years 1990, 2000, 2014.
## Results
These three features tell us that the most important predictors for city emissions are it's built-up area and population. This is consistent wit the fact that concrete production alone accounts for 7% of total global emissions[1].
## References
[1] 
