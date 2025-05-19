import requests
import json

# Профессии в сфере IT (ID из URL)
professional_roles = [
    156, 160, 10, 12, 150, 25, 165, 34, 36, 73, 155, 96,
    164, 104, 157, 107, 112, 113, 148, 114, 116, 121, 124,
    125, 126
]


def get_vacancies(text="project manager", per_page=50):
    url = "https://api.hh.ru/vacancies"

    # Собираем параметры
    params = {
        "text": text,
        "area": 2,  # Санкт-Петербург
        "per_page": per_page,
        "page": 0,
        "search_field": ["name", "company_name", "description"],
        "enable_snippets": False
    }

    # Добавляем каждую роль как отдельный параметр
    for role_id in professional_roles:
        params.setdefault("professional_role", []).append(role_id)

    # Выполняем запрос на список вакансий
    response = requests.get(url, params=params)
    response.raise_for_status()
    items = response.json()["items"]

    result = []
    for i, vacancy in enumerate(items[:per_page], start=1):
        # Получаем полное описание каждой вакансии
        detail_response = requests.get(
            f"https://api.hh.ru/vacancies/{vacancy['id']}")
        detail_response.raise_for_status()
        detail_data = detail_response.json()

        result.append({
            "id": i,
            "name": detail_data.get("name", ""),
            "description": detail_data.get("description", "").replace("\n",
                                                                      " "),
            "conditions": detail_data.get("conditions", "") or ""
        })

    return result


# Получаем вакансии и сохраняем
vacancies = get_vacancies()
with open("vacancies.json", "w", encoding="utf-8") as f:
    json.dump(vacancies, f, ensure_ascii=False, indent=4)

print("Вакансии сохранены в 'vacancies.json'")
import re

# Загружаем исходный файл
with open("vacancies.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Ключевые слова для определения подходящих вакансий
pm_keywords = [
    "project manager", "руководитель проекта", "менеджер проекта",
    "project-management", "pm", "руководство проектом", "project-manager"
]


def is_pm_vacancy(vac):
    name = vac.get("name", "").lower()
    description = vac.get("description", "").lower()
    return any(kw in name or kw in description for kw in pm_keywords)


def clean_description(desc):
    # Удаление HTML-тегов и упоминаний компаний
    text = re.sub(r'<[^>]+>', '', desc)  # remove HTML tags
    text = re.sub(r'Компания [^.,\n]+', '', text)  # remove "Компания XXX"
    text = re.sub(r'О компании:?[^.,\n]+', '', text, flags=re.IGNORECASE)
    return text.strip()


# Фильтрация и очистка вакансий
filtered = []
for i, vac in enumerate(data, 1):
    if is_pm_vacancy(vac):
        filtered.append({
            "id": i,
            "name": vac.get("name", ""),
            "description": clean_description(vac.get("description", "")),
            "conditions": vac.get("conditions", "")
        })

# Сохраняем результат
output_path = "cleaned_pm_vacancies.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(filtered, f, ensure_ascii=False, indent=4)
