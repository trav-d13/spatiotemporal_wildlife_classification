# Metadata Modelling

Please keep in mind the models are trained to form parent node classifiers within the cascading taxonomic structure. 

The metadata modelling process is accomplished through the below scripts:


### [Pipeline](../../src/models/meta/pipeline.md)
This file performs data cleaning, transformation, and structuring for use within the metadata models.

### [Model Training](../../src/models/meta/training.md)
This file performs all metadata classification model training. 
Specifically this file, performs metadata classification training at all taxonomic levels across all proposed models. 
This results in 5 complete cascading taxonomic classifiers that are compared at each taxonomic level to determine the most robust
metadata classifier. For the model comparison, please review `notebooks/meta_modelling/meta_data_model_comparison.ipynb`

### [Neural Network](../../src/models/meta/neural_network.md)
The neural network metadata model training and evaluation process. 
Hyperparameter tuning involves determining the optimal learning rate for the model due to the varying levels of abstraction
generated at different taxonomic levels. 

### [Random Forest](../../src/models/meta/random_forest.md)
The Random Forest metadata model training and evaluation process. 
Hyperparameter tuning involves determining the optimal tree depth for the estimators within the ensemble
method. 

### [XGBoost](../../src/models/meta/xgboost.md)
The XGBoost metadata model training and evaluation process. 
Hyperparameter tuning involves determining the optimal tree depth within the XGBoost model.

### [Decision Tree](../../src/models/meta/decision_tree.md)
The decision tree metadata model training and evaluation process.
Hyperparameter tuning involves determining the optimal decision tree depth for the model.

### [AdaBoost](../../src/models/meta/adaboost.md)
The AdaBoost metadata model training and evaluation process. 
Hyperparameter tuning involves determining the optimal number of estimators to be used within the ensemble model.

### [K-means Silhouette Score Automation](../../src/models/meta/sil_score.md)
The Silhouette score is a method of automating the selection of the number of centroids for a K-means clustering algorithms. 
This was used to determine the optimal number of centroids used to capture the geographic location distribution of at each parent node, to 
create a useful location encoding within the data. 