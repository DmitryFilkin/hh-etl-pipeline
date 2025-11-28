# ETL-пайплаин для вакансий Data Engineer с hh.ru

Проект для курсовой работы по дисциплине "Технологии программирования".

## Цель
Создать систему для автоматического сбора и обработки вакансий.

## Архитектура
project/
├── src/
│ ├── extract.py # Получение данных из API
│ ├── transform.py # Обработка данных
│ ├── load.py # Сохранение результатов
│ └── main.py # Оркестратор пайплаина
├── data/ # Локальные данные (для запуска без Docker)
├── docker-data/ # Данные из Docker-контейнера
├── Dockerfile
├── requirements.txt
├── .env.example # Шаблон переменных окружения
├── docker.env # Переменные для Docker
└── README.md

## Локальный запуск
# Установка зависимостей
pip install -r requirements.txt
# Запуск пайплаина
python src/main.py

## Запуск в Docker
# Сборка образа 
docker build -t hh-etl .
# Запуск с переменными окружения и сохранением данных
docker run --rm --env-file docker.env -v ${PWD}/docker-data:/app/data hh-etl

## Проверка результатов
dir docker-data

## Конфигурация
Файл docker.env:
SEARCH_QUERY=Data Engineer
AREA_ID=1
PER_PAGE=10
## Запуск
Инструкция появится здесь позже.