# 🤖 Job Matcher — система подбора кандидатов на основе семантического анализа

**Job Matcher** — это веб-приложение, использующее методы машинного обучения для автоматического сопоставления вакансий и резюме. Основная цель — упростить подбор подходящих IT-специалистов на основе смыслового анализа текста.

---

## 🚀 Возможности

- Добавление вакансий и резюме через web-интерфейс
- Алгоритм сравнения по смысловому сходству (semantic similarity)
- Ранжирование кандидатов по степени релевантности вакансии
- Использование ML-модели [`sergeyzh/LaBSE-ru-turbo`](https://huggingface.co/sergeyzh/LaBSE-ru-turbo) с дообучением
- Простая административная панель и REST API

---

## 🧠 Архитектура

- **Back-end**: Django, Django REST Framework  
- **Front-end**: HTML, CSS, JavaScript  
- **ML-модель**: `SentenceTransformer` с функцией потерь `MultipleNegativesRankingLoss`  
- **База данных**: SQLite

---

## 📊 Как работает

1. Вакансия и резюме преобразуются в эмбеддинги с помощью модели SentenceTransformer  
2. Вычисляется косинусное сходство между векторами  
3. Кандидаты ранжируются по степени соответствия и отображаются пользователю

---

## ⚙️ Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your-username/job-matcher.git
   cd job-matcher
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```


