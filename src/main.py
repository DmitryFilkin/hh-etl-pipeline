import os

from extract import get_hh_vacancies
from load import save_to_csv
from transform import clean_vacancy_data


def run_etl_pipeline():
    "Запускает полный ETL-пайплаин"

    print("=" * 50)
    print("Запуск ETL-пайплаина")
    print("=" * 50)

    # Читаем настройки из переменных окружения
    search_query = os.getenv("SEARCH_QUERY", "Data Engineer")
    area_id = int(os.getenv("AREA_ID", "1"))
    per_page = int(os.getenv("PER_PAGE", "10"))

    print(
        f"Настройки: поиск = '{search_query}', "
        f"регион = {area_id}, вакансий = {per_page}"
    )
    # 1. Extract
    print("\n Этап 1: Получение данных из HH API...")
    raw_data = get_hh_vacancies(
        search_text=search_query, area=area_id, per_page=per_page
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
    result_path = save_to_csv(cleaned_data)
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
