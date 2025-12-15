import os
from datetime import datetime

import pandas as pd
import yaml


def load_config():
    "Загружает конфигурацию из config.yaml"
    try:
        with open("config.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {"OUTPUT_DIR": "data"}


def save_to_csv(dataframe, output_dir=None):
    "Сохраняет DataFrame в CSV файл"

    print("Модуль load запущен!")

    config = load_config()
    output_dir = output_dir or config.get("OUTPUT_DIR", "data")

    # Создаём папку, если её нет
    os.makedirs(output_dir, exist_ok=True)

    # Создаём имя файла с датой и временем
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"vacancies_{current_time}.csv"
    filepath = os.path.join(output_dir, filename)

    try:
        # Сохраняем DataFrame в CSV
        dataframe.to_csv(filepath, index=False, encoding="utf-8")
        print(f"Данные сохранены в: {filepath}")
        return filepath
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")
        return None


# Тестовый запуск
if __name__ == "__main__":
    # Создаём тестовый DataFrame
    test_data = pd.DataFrame(
        {
            "name": ["Data Engineer", "ML Engineer"],
            "company": ["Yandex", "VK"],
            "salary": [150000, 180000],
        }
    )

    result_path = save_to_csv(test_data)
    if result_path:
        print(f"Тест пройден! Файл: {result_path}")
    else:
        print("Тест не пройден")
