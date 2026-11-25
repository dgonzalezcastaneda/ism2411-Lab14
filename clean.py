#Question 1- Filling missing values feels most ambiguos to me because it can be done in many ways. For example, we can fill missing values with the mean, median, or mode of the column, or we can use more advanced techniques like interpolation or predictive modeling. The choice of method depends on the nature of the data and the specific context of the analysis.
#question 2- I reviewd my comments to make sure they explain why each cleaning decision was made.
#question 3- The most surpricing thing was the quantity sold of 9999, which demonstrates why inspecting descriptive statistics is important. 

#Exercise 1

import pandas as pd

df=pd.read_csv('data/messy_sales.csv')
df.info()
print(df.isnull().sum())
print(df.isnull().mean() * 100)

# Data quality observations:
# 1. Customer ID has 362 missing values (7.54%).
# 2. Region has 111 missing values (2.31%).
# 3. Quantity Sold has 94 missing values (1.96%).


# Exercise 2 

df.columns = df.columns.str.lower().str.replace(' ', '_')

print(df.columns.tolist())

# Exercise 3 

print("Shape before cleaning:", df.shape)

# Fill missing numeric values with the column mean
# to preserve rows with otherwise useful information.

for col in ['unit_price', 'quantity_sold']:
    if pd.api.types.is_numeric_dtype(df[col]):
        df[col] = df[col].fillna(df[col].mean())

# Drop rows missing essential identifiers because
# these orders cannot be reliably identified.

df = df.dropna(subset=['order_id', 'order_date'])

print("Shape after cleaning:", df.shape)

print(df.isnull().sum())

# Exercise 4 

df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
print("Invalid dates:", df['order_date'].isna().sum())
df['unit_price'] = df['unit_price'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(float)
df['quantity_sold'] = df['quantity_sold'].astype(int)
df['revenue'] = (df['unit_price'] * df['quantity_sold']).round(2)

print(df.dtypes)

# Exercise 5 

print("Duplicate rows:", df.duplicated().sum())

df = df.drop_duplicates()

print("Shape after removing duplicates:", df.shape)

# Exercise 6 

print(df.describe())

# Negative revenue represents customer returns.
# These values should be kept because they are real
# transactions where money was returned to customers.

# A quantity sold of 9999 is a placeholder or data
# entry error and does not represent a real order.
# Keeping it would artificially inflate total revenue.

df = df[df['quantity_sold'] != 9999]
print("Shape after removing incorrect quantities:", df.shape)

print(df.describe())

# Exercise 7

df.to_csv('data/clean_sales.csv', index=False)
clean_df = pd.read_csv('data/clean_sales.csv')
clean_df.info()


clean_df = pd.read_csv('data/clean_sales.csv',
                       parse_dates=['order_date'])

clean_df.info()

