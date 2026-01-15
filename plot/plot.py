import pandas as pd
import matplotlib.pyplot as plt
import time
import os

def update_plot():
    csv_file = '/app/logs/metric_log.csv'
    output_file = '/app/logs/error_distribution.png'
    
    while True:
        try:
            if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
                # Чтение данных
                df = pd.read_csv(csv_file)
                
                # Создание простого графика
                plt.figure(figsize=(10, 6))
                plt.hist(df['absolute_error'], bins=20, edgecolor='black', alpha=0.7)
                plt.xlabel('Absolute Error ($)')
                plt.ylabel('Frequency')
                plt.title(f'Distribution of Errors (Total: {len(df)} predictions)')
                
                # Сохраняем
                plt.tight_layout()
                plt.savefig(output_file, dpi=150)
                plt.close()
                
                print(f"Plot updated. Total records: {len(df)}")
            else:
                print("Waiting for data...")
                
        except Exception as e:
            print(f"Error updating plot: {e}")
        
        # Обновление каждые 10 секунд
        time.sleep(10)

if __name__ == "__main__":
    print("Plot service started. Updating visualization every 10 seconds...")
    update_plot()