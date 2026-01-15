import pandas as pd
import numpy as np

# Создаем синтетические данные для тестирования
np.random.seed(42)

# Генерируем 1000 записей
n_samples = 1000

data = {
    'MedInc': np.random.uniform(0.5, 15.0, n_samples),
    'HouseAge': np.random.randint(1, 52, n_samples),
    'AveRooms': np.random.uniform(0.8, 10.0, n_samples),
    'AveBedrms': np.random.uniform(0.5, 5.0, n_samples),
    'Population': np.random.randint(1, 3500, n_samples),
    'AveOccup': np.random.uniform(0.8, 10.0, n_samples),
    'Latitude': np.random.uniform(32.5, 42.0, n_samples),
    'Longitude': np.random.uniform(-124.3, -114.1, n_samples),
    'PRICE': np.random.uniform(50000, 500000, n_samples)
}

df = pd.DataFrame(data)
df.to_csv('data/housing.csv', index=False)

print(f"Dataset created: {len(df)} rows")
print(df.head())