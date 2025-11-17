import pandas as pd
import json
import re

def clean_text(text):
    "Очищает текст от HTML-тегов"
    if text is None:
        return ""
    return re.sub('<[^<]+?>', '', text)
    
def calculate_salary(salary_data):
    "Рассчитывает среднюю зарплату"
    if not salary_data:
        return None
    
    from_salary = salary_data.get('from')
    to_salary = salary_data.get('to')

    # Считаем среднее если есть оба значения
    if from_salary and to_salary:
        return (from_salary + to_salary) / 2
    elif from_salary:
        return from_salary
    elif to_salary:
        return to_salary
    else:
        return None

def clean_vacancy_data(raw_data):
    """
    Очищает и преобразует сырые данные о вакансиях
    """
    print("Обрабатываем все вакансии...")

    cleaned_data = []

    for vacancy in raw_data['items']:
        cleaned_vacancy = {
            'id': vacancy['id'],
            'name': vacancy['name'],
            'company': vacancy['employer']['name'],
            'city': vacancy['area']['name'],
            'salary': calculate_salary(vacancy.get('salary')),
            'skills': clean_text(vacancy['snippet']['requirement']),
            'url': vacancy['alternate_url']
        }
        cleaned_data.append(cleaned_vacancy)

    # Создаём DataFrame
    df = pd.DataFrame(cleaned_data)
    print(f"Создан Data Frame с {len(df)} вакансиями")

    return df

# Тестовый запуск
if __name__ == "__main__":
    # Загружаем сырые данные
    try:
        with open('data/raw_vacancies.json','r', encoding = 'utf-8') as f:
            raw_data = json.load(f)
        print("Файл с данными загружен")
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        raw_data = None

    if raw_data:
        result_df = clean_vacancy_data(raw_data)

        # Показываем результат
        print("\n Первые 3 вакансии:")
        print(result_df[['name', 'company', 'salary', 'city']].head(3))
