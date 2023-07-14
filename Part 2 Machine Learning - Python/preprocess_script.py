import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder


# load data
df = pd.read_csv('Loan_Train.csv')
df.drop(['Loan_ID'], axis=1, inplace =True)

# fill Nan value with mean
df.LoanAmount=df.LoanAmount.fillna(df.LoanAmount.mean())
df.Credit_History=df.Credit_History.fillna(df.Credit_History.mean())
df.Loan_Amount_Term=df.Loan_Amount_Term.fillna(df.Loan_Amount_Term.mean())
df['Gender'].fillna(df['Gender'].value_counts().idxmax(), inplace=True)
df['Married'].fillna(df['Married'].value_counts().idxmax(), inplace=True)
df.Dependents.fillna(df.Dependents.value_counts().idxmax(), inplace=True)

# encode categorical label to numeric
df['Education']=LabelEncoder().fit_transform(df['Education'])
df['Dependents']=LabelEncoder().fit_transform(df['Dependents'])
df['Self_Employed']=LabelEncoder().fit_transform(df['Self_Employed'])
df['Gender']=LabelEncoder().fit_transform(df['Gender'])
df['Married']=LabelEncoder().fit_transform(df['Married'])
df['Property_Area']=LabelEncoder().fit_transform(df['Property_Area'])
df.Loan_Status.replace('N',0,inplace=True)
df.Loan_Status.replace('Y',1,inplace=True)

# copy to df2 to choose feature and keep original df untouched
df2=df
x=df2[['Dependents','Education','Self_Employed','ApplicantIncome','LoanAmount','Credit_History']]
y=df2[['Loan_Status']]

# split train, test
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.25,random_state=50)

# train DecisionTree model with specified parameters
from sklearn.tree import DecisionTreeClassifier 
model=DecisionTreeClassifier(max_depth=3,min_samples_leaf = 35)
model.fit(x_train,y_train)
y_pred = model.predict(x_test)

# evaluate DecisionTree model
from sklearn.metrics import accuracy_score as ac, f1_score, classification_report
from sklearn.model_selection import cross_val_score
print("DecisionTree Accuracy:", ac(y_test,y_pred)*100)
sco =(cross_val_score(model,x,y,cv=5))
print("DecisionTree CV Average Accuracy:", np.mean(sco)*100)
print("F1 Score: ",f1_score(y_test,y_pred))
print("Classification report", classification_report(y_test, y_pred))




# this is it for KNN

from sklearn import datasets, neighbors

# scale x
from sklearn.preprocessing import StandardScaler
ss = StandardScaler()
x_tf = ss.fit_transform(x)

x_tf_train,x_tf_test,y_train,y_test=train_test_split(x_tf,y.values.ravel(),test_size=0.25,random_state=50)


# fit KNN model trying with different n_neighbors to find best performer
scoreListknn = []
for i in range(1,21):
    KNclassifier = neighbors.KNeighborsClassifier(n_neighbors = i)
    KNclassifier.fit(x_tf_train, y_train)
    scoreListknn.append(KNclassifier.score(x_tf_test, y_test))
    
y_predknn = KNclassifier.predict(x_tf_test)

# evaluate KNN model
print("KNN Accuracy:", ac(y_test,y_predknn)*100)
sco_knn =(cross_val_score(KNclassifier,x_tf,y.values.ravel(),cv=5))
print("KNN Cross Validated Average Accuracy:", np.mean(sco_knn)*100)
print("F1 Score: ",f1_score(y_test,y_predknn))
print("Classification report", classification_report(y_test, y_predknn))