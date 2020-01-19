# Filtering of Aerial Light Detection and Ranging Data using Support Vector Classification
## Ross Winans
## ICS635 Final Project: May 7, 2018

## Objectives
This study will explore the ability of soft-margin support vector classification (SVC) to filter aerial LiDAR data. Soft-margin SVC has been chosen because it is a large margin classifier, which should help a relatively small number of training points generalize to a larger data set while avoiding overfitting.
## Study data
The study data for this project is taken from the 2013 National Oceanic and Atmospheric Administration’s Topographic LiDAR for Oahu, Hawai’i. This data set was collected at a sampling density of 2 points per square meter, 10cm RMSE vertical accuracy, and pre-labeled as ground or object with 98% or higher classification accuracy.  
## Study Area
A neighborhood in the town of Haleiwa was chosen for this study (Figure 1). This area was chosen due to its relatively flat terrain and mixed land cover (residential, agricultural, and forest cover). The study area is 2,250 km2 and is comprised of 4.49 million sample points. A centrally located, representative location was chosen for the training data. The training data is 1/36th of the full data set, representing 62.5 km2, consisting of 132,217 total samples. The remaining study area (2,187.5 km2, 4.36 million points) will be used to test the performance of the classification.

![Haleiwa Map](/images/ics635_haleiwa.png)

## Methods
1. A through literature review of traditional aerial LiDAR filtering algorithms have identified features that are useful for filtering of aerial LiDAR. These features were calculated for each point. Below is a list of all features used for classification:
    * Z- the elevation of the point above local mean sea level
    * HAGL- the vertical distance between the point and its lowest neighbor within 1m
    * STD_1m- the standard deviation of all neighbors’ elevation within 1m
    * STD_10m- the standard deviation of all neighbors’ elevation within 10m
    * RET_NUM- the return number of the point
    * NUM_RET- the total number of returns for the point
2. A grid search with 3-fold cross validation is run for the following kernels: linear, radial basis function (RBF), polynomial (poly), and sigmoid. Each kernel’s primary hyperparameters (C and gamma) are optimized based on the results of the grid search.
3. The highest performing kernel on the 3-fold cross validation will be fit to the training data set using the tuned parameters. Next the trained model will be used to predict the labels of the 35 test data sets. The performance will be reported in terms of accuracy (the percent of samples that are correctly labeled).
4. A qualitative assessment will be performed to determine the cause of misclassifications and examine the ability of SVC to filter aerial LiDAR.
## Results
### Grid Search with 3-fold cross validation
The results of the grid search with 3-fold cross validation produced surprising results. Each kernel was able to achieve perfect accuracy when properly tuned (Figures 2-5). Initially I had a fear of overfitting of the data, however SVC by its nature is designed to avoid overfitting. Also, changing the value of the regularization parameter, C, had little effect on the results. This leads me to believe that overfitting is not occurring.  LinearSVC was selected for the remainder of the experiment since it produces strong results with higher computational efficiency.
