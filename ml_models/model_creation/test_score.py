"""Сравнение вакансии с кандидатами с помощью SentenceTransformer."""

from sentence_transformers import SentenceTransformer, util

# Инициализация модели
model = SentenceTransformer('models/fine_tuned_model')

# Описание вакансии
job_posting: str = (
    "Вакансия: Project Manager в продуктовую IT-компанию, специализирующуюся на разработке "
    "финансовых веб-приложений. Обязанности: ведение нескольких Scrum-команд, контроль сроков и бюджета, "
    "управление бэклогом, проведение ежедневных стендапов, взаимодействие с продакт-менеджерами и архитекторами. "
    "Требования: опыт в управлении IT-проектами от 4 лет, обязательное знание Jira, Confluence, опыт работы с API, "
    "REST/GraphQL, английский уровень не ниже C1, умение писать техническую документацию и работать с TDD/CI/CD."
)

# Список кандидатов
candidates = [
    # 10 лет
    "Project Manager с опытом 10 лет. Управлял IT-проектами в сфере разработки веб-приложений. Использую Scrum, Jira, Confluence, пишу документацию, работаю с REST API. Руководил командами до 12 человек. Английский — C1.",

    # 7 лет
    "Project Manager с 7-летним опытом. Работал с Agile-подходом, вел несколько проектных команд. Использую Jira, Confluence, REST API, пишу документацию. Английский — C1.",

    # 5 лет
    "Project Manager. Опыт работы — 5 лет. Руководил Scrum-командами, работал с Jira, Confluence, документацией, API-интеграциями. Английский — C1.",

    # 3 года
    "Project Manager с 3-летним опытом. Управлял командой из 5 человек, писал user stories, использую Jira, Confluence, API, веду проектную документацию. Английский — C1.",

    # 1 год
    "Работаю Project Manager 1 год. Участвую в Scrum-ритуалах, использую Jira и Confluence, немного писал документацию, взаимодействовал с API. Английский — C1."
]

expected_scores = [5, 4, 3, 2, 1]  # ожидание по убыванию стажа

# Вычисление схожести между вакансией и каждым кандидатом
similarities: list[float] = []

for candidate in candidates:
    emb_job, emb_candidate = model.encode([job_posting, candidate])
    score = util.cos_sim(emb_job, emb_candidate).item()
    similarity_percent = round(score * 100, 2)
    similarities.append(similarity_percent)

# Вывод результатов
print("Ожидаемое ранжирование (ручное):", expected_scores)
print("Результаты модели (совпадение в %):")
for i, score in enumerate(similarities, start=1):
    print(f"Кандидат {i}: {score}% совпадения")
