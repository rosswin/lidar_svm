# Filtering of Aerial Light Detection and Ranging Data using Support Vector Classification
## W. Ross Winans | ICS635 Final Project | May 7, 2018

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

![gridsearch_linearkernel](/images/ics635_fig2.png)


![grid_search_poly_kernel](/images/ics635_fig3.png)


![grid_search_rbf_kernel](/images/ics635_fig4.png)


![grid_search_sigmoid_kernel](/images/ics635_fig5.png)

## Test Results
The results of a LinearSVC yielded an average accuracy of 0.59 across all 35 testing data sets. The standard deviation of accuracies was 0.39, with a low accuracy of 0.013, and a high accuracy of 0.99. The average accuracy is well below the current industry best. However, 40% of the test data sets’ accuracy exceeded 0.90. These results are well above the current industry best results. See the histogram showing the frequency of accuracy values (Figure 6). Due to the wide range of accuracy values, the bins were determined using Natural Jenks, a data clustering algorithm designed to minimize the variance within classes, while maximizing the variance between classes.

![test_accuracy_histogram](/images/ics635_accuracies_histogram.png)

A qualitative assessment of the data showed that there is a strong spatial correlation between accuracy and proximity to the training data. The map below plots the accuracy of each test data set on the surface of the earth (Figure 7). Visual examination shows that the test data sets that are adjacent or near to the training data tend to perform very well. Another unsurprising trend is that data sets with similar land cover to the training data (single family residential) tend to perform much better than other land covers. This is best exemplified by the two high performing tiles at the top-center of the study area, which perform well despite their distance from the study area. This is most likely because they contain similar land cover to the training data.

![results_mapped](/images/ics635_haleiwa_map_results.png)

## Conclusion
This preliminary study has identified two interesting findings. First, LinearSVC performance was equally high as the other more complex kernels, such as RBF. This dramatically reduces model run times. SVC was assumed to be a poorly suited algorithm for classification of aerial LiDAR due to the incredibly large sample sizes. However, the ability to apply LinearSVC dramatically reduces model training times and makes data sets in the millions very manageable on high-end workstations. Second, a LinearSVC can be trained on a small subset of labeled data and applied to the surrounding area with accuracies that exceed the current state of the art. However, this ability to generalize to new areas is heavily constrained by the terrain and land cover characteristics. 
A Recursive Feature Elimination (RFE) feature selection algorithm was run to identify the features that drove the model results, and the SVC classifiers were found to be highly dependent on the Z (elevation) value of the point. This is most likely the leading cause of SVCs’ inability to generalize to new terrain. The algorithm has learned that objects only occur above a certain elevation, and when the terrain slopes uphill all points become classified as objects. Essentially, our model is overfit to flat residential neighborhoods that occur at approximately 10 meters above local mean sea level. Future directions of research should focus on better feature selection and training on more diverse terrains and land covers.

