import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

df = pd.read_csv('data.csv')

df['City_Class'] = df['ZIP Code'].apply(lambda x: 1 if str(x).startswith('48') else 0)

X = df[['Gini Index', 'Median Household Income', 'Vacancy Rates', 'More than 30 percent', 'City_Class']]
y = df['Median Home Value']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = LinearRegression()
model.fit(X_scaled, y)

y_pred_full = model.predict(X_scaled)

rmse = np.sqrt(mean_squared_error(y, y_pred_full))
r2 = r2_score(y, y_pred_full)

print(f"RMSE: {rmse:.2f}")
print(f"R²: {r2:.4f}")

percentage_diff = np.abs((y_pred_full - y) / y)
threshold_20_percentile = np.percentile(percentage_diff, 80)
top_20_error_indices = percentage_diff >= threshold_20_percentile

plt.figure(figsize=(10, 7))

plt.scatter(y[~top_20_error_indices], y_pred_full[~top_20_error_indices], alpha=0.7, color='purple', label='Bottom 80% errors')

plt.scatter(y[top_20_error_indices], y_pred_full[top_20_error_indices], color='orange', marker='x', s=100, label='Top 20% largest errors')

plt.plot([y.min(), y.max()], [y.min(), y.max()], 'g--', lw=2, label='Perfect Fit Line')

plt.ticklabel_format(style='plain', axis='both')
plt.xticks(rotation=45)
plt.yticks(rotation=45)
plt.xlabel('Actual Median Home Value', fontsize=12)
plt.ylabel('Predicted Median Home Value', fontsize=12)
plt.title('Actual vs. Predicted Median Home Values\n(Top 20% Errors Highlighted)', fontsize=14)
plt.legend()
plt.grid(True)
plt.show()
