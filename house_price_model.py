# libraries import
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import joblib


# data load
df = pd.read_csv("House Price Prediction Dataset.csv")


# understand the data
print(df.head(7))
print(df.columns)
print(df.shape)


# unwanted column remove
df = df.drop(["Id"], axis=1)

print("After removing unwanted column:")
print(df)


# feature creation using mean


df["House_Age"] = 2026 - df["YearBuilt"]

print("After Feature Creation:")
print(df)


# missing values check
print("Missing Values:")
print(df.isnull().sum())


# check the duplicate value
print("Duplicates:")
print(df.duplicated().sum())


# filling missing values with mean
df["Area"] = df["Area"].fillna(df["Area"].mean())

df["Bedrooms"] = df["Bedrooms"].fillna(
    df["Bedrooms"].mean()
)

df["Bathrooms"] = df["Bathrooms"].fillna(
    df["Bathrooms"].mean()
)

df["Floors"] = df["Floors"].fillna(
    df["Floors"].mean()
)

df["YearBuilt"] = df["YearBuilt"].fillna(
    df["YearBuilt"].mean()
)

df["Price"] = df["Price"].fillna(
    df["Price"].mean()
)


# filling missing values with mode
df["Location"] = df["Location"].fillna(
    df["Location"].mode()[0]
)

df["Condition"] = df["Condition"].fillna(
    df["Condition"].mode()[0]
)

df["Garage"] = df["Garage"].fillna(
    df["Garage"].mode()[0]
)


print("After filling missing values:")
print(df.isnull().sum())


# finding the total duplicate
print("Duplicates:")
print(df.duplicated().sum())


# remove duplicate values
df = df.drop_duplicates()

print("Duplicates after removal:")
print(df.duplicated().sum())


# label encoding
le_location = LabelEncoder()
le_condition = LabelEncoder()
le_garage = LabelEncoder()


df["Location"] = le_location.fit_transform(
    df["Location"]
)

df["Condition"] = le_condition.fit_transform(
    df["Condition"]
)

df["Garage"] = le_garage.fit_transform(
    df["Garage"]
)


print("After Label Encoding:")
print(df.head(10))


# EDA
print(df.tail(10))
print(df.shape)
print(df.columns)
print(df.dtypes)
print(df.info())


print(df["Location"].unique())
print(df["Location"].nunique())
print(df["Location"].value_counts())

print(df.describe())


# histogram
plt.hist(df["Price"])

plt.xlabel("House Price")
plt.ylabel("Number of Houses")
plt.title("House Price Distribution")

plt.show()


# matplotlib.pyplot bar chart
bedroom_count = (
    df["Bedrooms"]
    .value_counts()
    .sort_index()
)

plt.bar(
    bedroom_count.index,
    bedroom_count.values
)

plt.xlabel("Number of Bedrooms")
plt.ylabel("Number of Houses")
plt.title("Number of Houses by Bedrooms")

plt.show()


# seaborn bar chart
sns.barplot(
    x=df["Bedrooms"],
    y=df["Price"]
)

plt.xlabel("Bedrooms")
plt.ylabel("House Price")
plt.title("Bedrooms vs House Price")

plt.show()


# seaborn scatter plot
sns.scatterplot(
    x=df["Area"],
    y=df["Price"]
)

plt.xlabel("Area")
plt.ylabel("House Price")
plt.title("Area vs House Price")

plt.show()


# correlation
correlation = df.corr()

print("Correlation with Price:")
print(
    correlation["Price"]
    .sort_values(ascending=False)
)


# correlation heatmap
plt.figure(figsize=(10, 6))

sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm"
)

plt.title("Correlation Heatmap")

plt.show()


# feature selection
X = df.drop("Price", axis=1)

y = df["Price"]

print("Features:")
print(X.columns)

print("Target:")
print(y.name)


# feature importance
rf_feature = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

rf_feature.fit(X, y)


feature_importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": rf_feature.feature_importances_
})


feature_importance = feature_importance.sort_values(
    by="Importance",
    ascending=False
)


print("Feature Importance:")
print(feature_importance)


# feature importance graph
plt.figure(figsize=(10, 6))

sns.barplot(
    x="Importance",
    y="Feature",
    data=feature_importance
)

plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("Feature Importance for House Price")

plt.show()


# train test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


print("Training Data:")
print(X_train.shape)

print("Testing Data:")
print(X_test.shape)


# random forest regression
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)


model.fit(
    X_train,
    y_train
)


print("Model Training Completed!")


# prediction
y_pred = model.predict(X_test)


print("Predicted Values:")
print(y_pred[:10])


# model evaluation
mae = mean_absolute_error(
    y_test,
    y_pred
)


rmse = np.sqrt(
    mean_squared_error(
        y_test,
        y_pred
    )
)


r2 = r2_score(
    y_test,
    y_pred
)


print("Model Performance:")

print("MAE:", mae)

print("RMSE:", rmse)

print("R2 Score:", r2)


# actual vs predicted
comparison = pd.DataFrame({
    "Actual Price": y_test.values,
    "Predicted Price": y_pred
})


print("Actual vs Predicted:")
print(comparison.head(10))


# actual vs predicted graph
plt.figure(figsize=(8, 6))

plt.scatter(
    y_test,
    y_pred
)

plt.xlabel("Actual Price")
plt.ylabel("Predicted Price")
plt.title("Actual Price vs Predicted Price")

plt.show()


# save model
joblib.dump(
    model,
    "house_price_model.pkl"
)


# save encoders
joblib.dump(
    le_location,
    "location_encoder.pkl"
)

joblib.dump(
    le_condition,
    "condition_encoder.pkl"
)

joblib.dump(
    le_garage,
    "garage_encoder.pkl"
)


print("Model and Encoders saved successfully!")