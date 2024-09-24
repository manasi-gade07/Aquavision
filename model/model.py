import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
import joblib

# Load the CSV file
data = pd.read_csv('data/modnim.csv')

# Replace '-' with NaN for missing values
data.replace('-', np.nan, inplace=True)

# Melt the DataFrame to reshape it for modeling
data_melted = data.melt(id_vars=["Year"], var_name="Month", value_name="GWL")

# Convert month names to numerical format (Jan=1, Feb=2, etc.)
data_melted['Month'] = pd.to_datetime(data_melted['Month'], format='%b', errors='coerce').dt.month

# Drop rows with missing GWL values
data_melted.dropna(subset=['GWL'], inplace=True)

# Ensure GWL is a float
data_melted['GWL'] = pd.to_numeric(data_melted['GWL'], errors='coerce')

# Drop rows where the month is NaN
data_melted.dropna(subset=['Month'], inplace=True)

# Split into input (X) and output (y)
X = data_melted[['Year', 'Month']]
y = data_melted['GWL']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the RandomForestRegressor model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict the groundwater levels for the test set
y_pred = model.predict(X_test)

# Evaluate the model performance
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print(f"Root Mean Squared Error (RMSE): {rmse}")

# Save the trained model
joblib.dump(model, 'model/model.pkl')

# Function to predict groundwater levels based on input year and month
def predict_gwl(year, month):
    month_num = pd.to_datetime(month, format='%b').month
    input_data = pd.DataFrame({'Year': [year], 'Month': [month_num]})
    prediction = model.predict(input_data)[0]
    return prediction
