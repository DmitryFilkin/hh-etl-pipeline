import os
import sys

import yaml

# Добавляем папку src в путь для импортов
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Импорты из src с отключением проверки E402
from src.extract import get_hh_vacancies  # noqa: E402
from src.load import save_to_csv  # noqa: E402
from src.transform import clean_vacancy_data  # noqa: E402


def load_config():
    "Загружает конфигурацию из config.yaml"
    try:
        with open("config.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        # Возвращаем значения по умолчанию если файл не найден
        return {
            "SEARCH_QUERY": "Data Engineer",
            "AREA_ID": 1,
            "PER_PAGE": 10,
            "OUTPUT_DIR": "data",
        }


def run_etl_pipeline():
    "Запускает полный ETL-пайплаин"

    print("=" * 50)
    print("Запуск ETL-пайплаина")
    print("=" * 50)

    # Загружаем конфигурацию
    config = load_config()

    print(
        f"Настройки: поиск = '{config['SEARCH_QUERY']}', "
        f"регион = {config['AREA_ID']}, вакансий = {config['PER_PAGE']}"
    )
    # 1. Extract
    print("\n Этап 1: Получение данных из HH API...")
    raw_data = get_hh_vacancies(
        search_text=config["SEARCH_QUERY"],
        area=config["AREA_ID"],
        per_page=config["PER_PAGE"],
    )

    if not raw_data:
        print("Не удалось получить данные")
        return False

    print(f"Получено {len(raw_data['items'])} вакансий")

    # 2. Transform
    print("\n Этап 2: Обработка данных...")
    cleaned_data = clean_vacancy_data(raw_data)

    if cleaned_data.empty:
        print("Не удалось обработать данные")
        return False
    print(f"Данные обновлены: {len(cleaned_data)} записей")

    # 3. Load
    print("\n Этап 3: Сохранение результатов...")
    result_path = save_to_csv(cleaned_data, output_dir=config["OUTPUT_DIR"])
    if not result_path:
        print("Не удалось сохранить данные")
        return False

    # Статистика
    print("\n Статистика:")
    print(f"• Обработано вакансий: {len(cleaned_data)}")
    print(f"• Вакансий с зарплатой: {cleaned_data['salary'].notna().sum()}")
    print(f"• Уникальных компаний: {cleaned_data['company'].nunique()}")
    print(f"• Файл с результатами: {result_path}")
    print("ETL-пайплаин успешно завершён!")

    return True


if __name__ == "__main__":
    run_etl_pipeline()
