import requests
import json
def get_hh_vacancies(search_text = "Data Engineer", area = 1, per_page = 5):
    url = "https://api.hh.ru/vacancies"  
    params = {
        "text": search_text,
        "area": area,
        "per_page": per_page
    }
    try:
        response = requests.get(url, params = params)
        print(f"Статус: {response.status_code}")
        return response.json() # Возвращаем реальные данные
    except:
        return None
# Текстовый вызов
if __name__ == "__main__":
    data = get_hh_vacancies()
    if data:
        print(f"Найдено вакансий: {data['found']}")
        # Анализируем структуру первой вакансии
        first_vacancy = data['items'][0]
        print("\n Структура данных вакансии")
        print(f"Зарплата: {first_vacancy.get('salary','не указана')}")
        print(f"Компания: {first_vacancy['employer']['name']}")
        print(f"Город: {first_vacancy['area']['name']}")
        print(f"Опыт: {first_vacancy['experience']['name']}")
        print(f"Навыки (требования): {first_vacancy['snippet']['requirement']}")
        print(f"Обязанности: {first_vacancy['snippet']['responsibility']}")
        
        # Сохраняем сырые данные для следующего шага
        with open('data/raw_vacancies.json', "w", encoding = 'utf-8') as f:
            json.dump(data, f, ensure_ascii = False, indent = 2)
        print("\n Сырые данные сохранены в data/raw_vacancies.json")
