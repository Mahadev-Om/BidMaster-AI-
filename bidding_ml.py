
import joblib
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

# Load model
model = joblib.load('bidding_model.pkl')

# Load and preprocess data
df = pd.read_csv('cleaned_dataset_new_3.csv', low_memory=False)
numeric_features = df.select_dtypes(include=['int64', 'float64']).columns
categorical_features = df.select_dtypes(include=['object']).columns

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean'))
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

df_processed = preprocessor.fit_transform(df)

# Function to get the best bid
def get_best_bid():
    features = df_processed[0].reshape(1, -1)
    best_bid_value = model.predict(features)[0]
    best_bid_supplier = df.iloc[0]['supplierLegalName']
    return best_bid_value, best_bid_supplier
