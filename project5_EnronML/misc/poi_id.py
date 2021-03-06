#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

from data_viz import dict_to_dataframe
from data_shape import engineered_features, outlier_cleaning, data_dict_info
from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.decomposition import PCA
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline

from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier

##################### Task 1: Select what features you'll use. #####################

### 'poi' must be 1st feature in list, comment out features to exclude from classifier
features_list = ["poi", 
				"salary",
				#"to_messages",
				#"deferral_payments",
				"total_payments",
				"exercised_stock_options",
				#"bonus",
				"restricted_stock",
				#"shared_receipt_with_poi",
				#"restricted_stock_deferred",
				#"total_stock_value",
				"expenses",
				#"loan_advances",
				#"from_messages",
				#"from_this_person_to_poi",
				"director_fees",
				"deferred_income",
				#"long_term_incentive",
				#"from_poi_to_this_person",
				# Engineered Features:
				"from_poi_to_this_person_fraction",
				"from_this_person_to_poi_fraction",
				#"poi_email_interaction",
				"poi_email_reciept_interaction"]
				#"adj_compensation"]

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)


##################### Task 2: Remove outliers #####################

### send data_dict to data_shape.py for cleaning
outlier_cleaning(data_dict)

##################### Task 3: Create new feature(s) #####################

### sends data to data_shape.py to add new features
engineered_features(data_dict)

### prints out useful info about the data set
#data_dict_info(data_dict) 

### creates a PANDAS df to visualize data
#dict_to_dataframe(data_dict)

### useful to stop program so I can print/graph without 
### running classifiers/make pickles.
#sys.exit()


### store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True, remove_NaN = True)
labels, features = targetFeatureSplit(data)



##################### Task 4: Try a varity of classifiers #####################

### DT out of box
# test_pipeline_dt = Pipeline([	
# 			('select', SelectKBest(k=3)),
# 			('dt', DecisionTreeClassifier()),
# 			])
# clf = test_pipeline_dt



### GussianNB out of box
# test_pipeline_gnb = Pipeline([	
# 			('select', SelectKBest(k=3)),
# 			('gnb', GaussianNB())
# 			])
# clf = test_pipeline_gnb



### AdaBoost out of box
# test_pipeline_adaboost = Pipeline([	
# 			('select', SelectKBest(k=3)),
# 			('adaboost', AdaBoostClassifier())
# 			])
# clf = test_pipeline_adaboost



### Linear SVC out of box
# test_pipeline_Lsvc = Pipeline([	
# 			('select', SelectKBest(k=3)),
# 			('Lsvc', svm.LinearSVC())
# 			])
# clf = test_pipeline_Lsvc



### Random Forest out of box
# test_pipeline_rf = Pipeline([	
# 			('select', SelectKBest(k=3)),
# 			('rf', RandomForestClassifier(n_estimators=10))
# 			])
# clf = test_pipeline_rf


##################### Task 5: Tune your classifier #####################


### Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html


################### -- Decision Tree [start] -- ###################

### testing out a DT classifier without any pipeline/GridSearch, also determining
### important features and printing them out
# clf = DecisionTreeClassifier()
# clf.fit(features, labels)
# tree_scores = zip(features_list[1:],clf.feature_importances_)
# sorted_dict = sorted(tree_scores, key=lambda feature: feature[1], reverse = True)
# for item in sorted_dict:
#  	print item[0], item[1]

'''
we might not want to pass pipeline as clf to tester with a selectKbest in there.
Perhaps we should perform select K best on the data set prior and then print the
get_scores and then set that list = to features_list.? and take selectKbest out 
pipeline?
https://discussions.udacity.com/t/selectkbest-pca-and-pipelines/22986/6
'''
### pipeline that will transform data and then fit it for a classifier. 
decision_tree_pipeline = Pipeline([	
			#('select', SelectKBest(score_func=f_classif)),
			#('scaler', MinMaxScaler()),
			#('select', SelectKBest(k=6)),
			#('scaler', MinMaxScaler()),
			#('scaler', StandardScaler()),
			('pca', PCA()),
			#('dt', DecisionTreeClassifier()),
			('dt', DecisionTreeClassifier(max_depth=10, min_samples_split=10, min_samples_leaf=3))
			])

### 2 param_dict, one for testing GridSearch with no params
param_dict = {}
#param_dict = {'pca__n_components' : [1,2,3,8,9,10]}
#param_dict = {'dt__max_depth' : [2,3,4,5,6,7,8,9,10,11,12]}
# 			  #'dt__min_samples_split' : [2, 4, 8],
# 			  #'dt__min_samples_leaf' : []}

clf = GridSearchCV(decision_tree_pipeline, param_dict)


################### -- Decision Tree [end] -- ###################



##################### Task 6: Dump your classifier #####################

dump_classifier_and_data(clf, my_dataset, features_list)












