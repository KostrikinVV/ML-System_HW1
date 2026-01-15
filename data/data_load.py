import pandas as pd
from sklearn.datasets import fetch_california_housing
import numpy as np

# Используем California Housing вместо Boston (более современный)
data = fetch_california_housing()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['PRICE'] = data.target * 100000  # Преобразуем в доллары

# Сохраняем
df.to_csv('housing.csv', index=False)
print(f"Dataset saved with {len(df)} rows")
print(f"Features: {data.feature_names}")
print(f"Target range: ${df['PRICE'].min():,.0f} - ${df['PRICE'].max():,.0f}")