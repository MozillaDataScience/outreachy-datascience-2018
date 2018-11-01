#Issue number 2, reducing number of telementry attributes
import pandas as pd
import numpy as np
df = pd.read_csv('device_failure.csv', na_values=' ')
#selecting the attribute from dataset 
attributes = df.iloc[:,2:11]
target =df.iloc[:,11:12]
#One best way to reduce the number of features is applying Prinicipal componenet analysis, which reduce the number into prinicipal components
#So here we are going to apply PCA using SKLearn library
from sklearn.decomposition import PCA
from sklearn import preprocessing
#Before doing PCA we need to normalize our dataset
normalized_X = preprocessing.normalize(attributes)
#Now we are going to apply PCA, here we are choosing the number of PCA component equal to 5
pca = PCA(n_components=5)
principalComponents = pca.fit_transform(attributes)
pca.fit_transform(normalized_X)
#To show the variance in the data explained by our PCA components we are going to use 
pca.explained_variance_ratio_
#here we can see that our first PCA component can explain 94% of the variance in the dataset, which is a good sign. 
#Our top 5 PCA components can easily explain 99% variance in the dataset.
#So it clearly explains relations of our new features and our original dataset.

