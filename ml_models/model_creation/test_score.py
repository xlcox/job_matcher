# -*- coding: utf-8 -*-

"""Сравнение вакансии с кандидатами с помощью SentenceTransformer."""

from scipy.stats import spearmanr
from sentence_transformers import SentenceTransformer, util

# Инициализация модели
model = SentenceTransformer(
    'D:\\Dev\\job_matcher\\ml_models\\fine_tuned_model')

# Описание вакансии
job_posting: str = (
    "Вакансия: Project Manager в продуктовую IT-компанию, специализирующуюся на разработке "
    "финансовых веб-приложений. Обязанности: ведение нескольких Scrum-команд, контроль сроков и бюджета, "
    "управление бэклогом, проведение ежедневных стендапов, взаимодействие с продакт-менеджерами и архитекторами. "
    "Требования: опыт в управлении IT-проектами от 4 лет, обязательное знание Jira, Confluence, опыт работы с API, "
    "REST/GraphQL, английский уровень не ниже C1, умение писать техническую документацию и работать с TDD/CI/CD."
)

# Группы кандидатов с id
candidate_groups = {
    "ГРУППА 1: Реалистичные описания «размытые»": {
        "candidates": [
            {"id": 1,
             "text": "Работаю менеджером проектов в IT-сфере. Очень люблю работать с людьми, считаю, что коммуникация — это ключ к успеху. Использую Jira, но чаще решаю всё через личные договорённости. Последний проект — запуск приложения для микрофинансовой компании. Участвую в стендапах. Английский хороший, но предпочитаю русскоязычные команды."},
            {"id": 2,
             "text": "Я проактивный, инициативный и ответственный. Люблю Agile, потому что он гибкий. В команде всегда стараюсь быть лидером. У меня за плечами более 10 проектов, но я не люблю писать отчёты. Уровень английского нормальный. Программированием не занимаюсь, но разбираюсь в людях. Уверенный пользователь ПК."},
            {"id": 3,
             "text": "Project Manager с техническим образованием. До этого занимался разработкой игр, а ещё увлекаюсь психологией и плаванием. Писал статьи на Хабр, люблю читать документацию. Jira знаю, но считаю её переоценённой. Работал в одной команде с DevOps, но не вникал в детали. Английский — B2."},
            {"id": 4,
             "text": "В проектах давно. В основном работал с командой из 5 человек, делали портал для госуслуг. Я больше по организационке. Вроде как Product Manager был, но формально — Project. Всё было на русском. С английским не особо. Jira была, но в Excel было удобнее."},
            {"id": 5,
             "text": "Я Project Manager, но также иногда беру на себя функции аналитика. Могу и в QA при необходимости. Работаю в стартапе, где всё делаем сами. Пишу в Notion, делаю wireframe'ы. Вроде как API у нас есть, но я не лезу туда. С английским работаю, но редко. Иногда веду команду, иногда просто координирую."}
        ],
        "expected_scores": [3, 5, 1, 2, 4]
        # Ранжирование по id, слева - самый подходящий кандидат.
    },
    "ГРУППА 2: Смешанные кандидаты (разная релевантность)": {
        "candidates": [
            {"id": 6,
             "text": "Садовод с 10-летним опытом. Занимаюсь выращиванием цветов и овощей, управляю небольшим хозяйством. IT навыков нет, технической документацией не владею."},
            # Не подходящий кандидат
            {"id": 7,
             "text": "DevOps-инженер с 5-летним опытом. Автоматизация CI/CD, работа с Jenkins, Kubernetes, Docker, опыт настройки инфраструктуры для веб-приложений."},
            # Кандидат из другой IT сферы
            {"id": 8,
             "text": "Project Manager с 6-летним опытом, специализация на финансовых IT-проектах. Владею Jira, Confluence, опыт работы с REST API, English — C1, веду несколько Scrum-команд."},
            # Подходящий кандидат
            {"id": 9,
             "text": "Project Manager с опытом в маркетинговых IT-проектах. Знаком с Agile, Kanban, активно использую Jira и Confluence, опыт работы с документацией. Английский — B2."},
            # PM с другими навыками
            {"id": 10,
             "text": "Business Analyst с опытом 4 года. Проводил сбор требований, работал с документацией, участвовал в планировании проектов. Опыт работы с Jira, Confluence. Английский — B2."}
            # Кандидат на выбор
        ],
        "expected_scores": [8, 9, 10, 7, 6]
        # Ранжирование по id, слева - самый подходящий кандидат.
    },
    "ГРУППА 3: Реалистичные + нерелевантные кандидаты": {
        "candidates": [
            # Из группы 1
            {"id": 1,
             "text": "Работаю менеджером проектов в IT-сфере. Очень люблю работать с людьми, считаю, что коммуникация — это ключ к успеху. Использую Jira, но чаще решаю всё через личные договорённости. Последний проект — запуск приложения для микрофинансовой компании. Участвую в стендапах. Английский хороший, но предпочитаю русскоязычные команды."},
            {"id": 2,
             "text": "Я проактивный, инициативный и ответственный. Люблю Agile, потому что он гибкий. В команде всегда стараюсь быть лидером. У меня за плечами более 10 проектов, но я не люблю писать отчёты. Уровень английского нормальный. Программированием не занимаюсь, но разбираюсь в людях. Уверенный пользователь ПК."},
            {"id": 3,
             "text": "Project Manager с техническим образованием. До этого занимался разработкой игр, а ещё увлекаюсь психологией и плаванием. Писал статьи на Хабр, люблю читать документацию. Jira знаю, но считаю её переоценённой. Работал в одной команде с DevOps, но не вникал в детали. Английский — B2."},
            {"id": 4,
             "text": "В проектах давно. В основном работал с командой из 5 человек, делали портал для госуслуг. Я больше по организационке. Вроде как Product Manager был, но формально — Project. Всё было на русском. С английским не особо. Jira была, но в Excel было удобнее."},
            {"id": 5,
             "text": "Я Project Manager, но также иногда беру на себя функции аналитика. Могу и в QA при необходимости. Работаю в стартапе, где всё делаем сами. Пишу в Notion, делаю wireframe'ы. Вроде как API у нас есть, но я не лезу туда. С английским работаю, но редко. Иногда веду команду, иногда просто координирую."},
            # Новые нерелевантные кандидаты
            {"id": 11,
             "text": "Водитель такси, 5 лет стажа. Вожу в основном в городе, хорошо знаю маршруты."},
            {"id": 12,
             "text": "Повар с 8-летним опытом, специализация на итальянской кухне."},
            {"id": 13,
             "text": "Продажник. Опыт работы с CRM, ведение клиентской базы, выполнение планов продаж."},
        ],
        "expected_relevant": [1, 2, 3, 4, 5],
        "expected_scores": [3, 5, 1, 2, 4]
    }

}

TOP_K = 5


def print_results(group_name, similarities_sorted, group_data):
    print("\n" + "=" * 80)
    print(group_name)
    print("=" * 80)

    # Вывод результатов модели
    print("Результаты модели (совпадение в %):")
    for candidate_id, score in similarities_sorted:
        print(f"Кандидат {candidate_id}: {score}% совпадения")

    # Вывод эталонного ранжирования (если есть)
    if "expected_scores" in group_data:
        print("\nОжидаемое ранжирование по id (от наиболее подходящего):",
              group_data["expected_scores"])
    elif "expected_relevant" in group_data:
        print("\nСписок релевантных кандидатов:",
              group_data["expected_relevant"])

    # Precision@1 (по умолчанию — на первом месте)
    precision_at_1 = 0.0
    if "expected_scores" in group_data:
        first_candidate_id = similarities_sorted[0][0]
        if first_candidate_id in group_data["expected_scores"]:
            precision_at_1 = 1.0

    # Recall@5
    recall_at_5 = 0.0
    if "expected_relevant" in group_data:
        top_k_ids = [cid for cid, _ in similarities_sorted[:TOP_K]]
        relevant_ids = set(group_data["expected_relevant"])
        relevant_in_top_k = sum(1 for cid in top_k_ids if cid in relevant_ids)
        recall_at_5 = relevant_in_top_k / len(relevant_ids)

    # Spearman’s rho (учитываются все кандидаты)
    spearman_score = None
    if "expected_scores" in group_data:
        # Ожидаемое ранжирование: id -> rank
        expected_ranks = {cid: rank for rank, cid in
                          enumerate(group_data["expected_scores"], start=1)}
        # Предсказанное ранжирование: id -> rank
        predicted_ranks = {cid: rank for rank, (cid, _) in
                           enumerate(similarities_sorted, start=1)}
        # Для всех кандидатов в предсказании создаем ранги:
        all_ids = [cid for cid, _ in similarities_sorted]
        # Заполняем эталонные ранги для всех кандидатов: если нет в эталоне — ставим rank = len(expected_scores) + 1
        default_rank = len(expected_ranks) + 1
        y_true = [expected_ranks.get(cid, default_rank) for cid in all_ids]
        y_pred = [predicted_ranks[cid] for cid in all_ids]
        if len(y_true) >= 2:
            spearman_score, _ = spearmanr(y_true, y_pred)

    # Вывод метрик
    print("\nМетрики:")
    if "expected_relevant" in group_data:
        print(f"Recall@5: {recall_at_5:.2f}")
    if spearman_score is not None:
        print(f"Precision@1: {precision_at_1:.2f}")
        print(f"Spearman's rho: {spearman_score:.2f}")


# Основной цикл
for group_name, group_data in candidate_groups.items():
    candidates = group_data["candidates"]
    similarities = []

    for candidate in candidates:
        emb_job, emb_candidate = model.encode([job_posting, candidate["text"]])
        score = util.cos_sim(emb_job, emb_candidate).item()
        similarity_percent = round(score * 100, 2)
        similarities.append((candidate["id"], similarity_percent))

    similarities_sorted = sorted(similarities, key=lambda x: x[1],
                                 reverse=True)

    print_results(group_name, similarities_sorted, group_data)
