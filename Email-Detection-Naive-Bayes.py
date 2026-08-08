# Email Spam Detection using Naive Bayes

# Import Libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load Dataset
df = pd.read_csv("spam.csv", encoding="latin-1")

# Keep only required columns
df = df[['v1', 'v2']]

# Rename columns
df.columns = ['Label', 'Email']

print("First 5 Records : \n")
print(df.head())

print("\nDataset Shape : ", df.shape)

# Convert Labels
# spam -> 1
# ham -> 0
df['Label'] = df['Label'].map({
    'ham':0,
    'spam':1
})

# Features and Target
X = df['Email']
y = df['Label']

# Convert Text into Numbers
vectorizer = CountVectorizer(stop_words='english')
X = vectorizer.fit_transform(X)

# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# Train Model
model = MultinomialNB()
model.fit(X_train, y_train)

import joblib
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model Saved Successfully!")

# Prediction
y_pred = model.predict(X_test)

# Evaluation
print("\nAccuracy : ", accuracy_score(y_test, y_pred))

print("\nClassification Report : \n")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix : \n")
print(confusion_matrix(y_test, y_pred))

# User Input
print("\n--------------------------------")

message = input("Enter an Email Message : \n")
message_vector = vectorizer.transform([message])
prediction = model.predict(message_vector)
probability = model.predict_proba(message_vector)

print("\nPrediction Probability : ")
print("Not Spam : ", round(probability[0][0]*100,2), "%")
print("Spam : ", round(probability[0][1]*100,2), "%")

if prediction[0] == 1:
    print("\nResult : SPAM EMAIL")
else:
    print("\nResult : NOT SPAM")