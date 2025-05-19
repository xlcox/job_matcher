"""Модуль для загрузки и обновления данных резюме и вакансий."""

import csv, html, json, re
from pathlib import Path
from typing import Any, Dict, List, Set

ground_truth: Dict[int, Set[int]] = {}


def clean_text(text: str) -> str:
    """
    Очищает входной текст от HTML-тегов, HTML-энтити и лишних пробелов.

    :param text: Исходный текст (возможно, с HTML).
    :return: Очищенный текст.
    """
    if text is None:
        return ""
    text_no_html = re.sub(r"<[^>]*>", " ", text)
    text_unescaped = html.unescape(text_no_html)
    text_normalized = re.sub(r"\s+", " ", text_unescaped)
    return text_normalized.strip()


def load_resumes(csv_path: str) -> List[Dict[str, Any]]:
    """
    Загружает резюме из CSV-файла. Каждое резюме представлено как словарь с полями 'id' и 'text'.

    :param csv_path: Путь к CSV-файлу.
    :return: Список резюме.
    """
    resumes = []
    path = Path(csv_path)
    if not path.exists():
        return resumes

    with open(path, mode='r', encoding='utf-8') as file:
        sample_line = file.readline()
        has_header = any(char.isalpha() for char in sample_line)
        file.seek(0)

        if has_header:
            reader = csv.DictReader(file)
            for row in reader:
                if not row:
                    continue
                resume_id = row.get('id') or row.get('resume_id') or row.get('ID') or row.get('ResumeID')
                try:
                    resume_id = int(resume_id)
                except Exception:
                    pass

                raw_text = row.get('text')
                if not raw_text:
                    fields_to_combine = [k for k in row if k.lower() not in ('id', 'resume_id')]
                    raw_text = " ".join(str(row[k]) for k in fields_to_combine if row[k])

                resumes.append({
                    "id": resume_id,
                    "text": raw_text or ""
                })
        else:
            reader = csv.reader(file)
            for row in reader:
                if not row or len(row) < 2:
                    continue
                resume_id, raw_text = row[0], row[1]
                if len(row) > 2:
                    raw_text += " " + " ".join(row[2:])
                try:
                    resume_id = int(resume_id)
                except Exception:
                    pass
                resumes.append({
                    "id": resume_id,
                    "text": raw_text or ""
                })

    return resumes


def load_vacancies(json_path: str) -> List[Dict[str, Any]]:
    """
    Загружает вакансии из JSON-файла.

    :param json_path: Путь к JSON-файлу.
    :return: Список вакансий.
    """
    vacancies = []
    path = Path(json_path)
    if not path.exists():
        return vacancies

    with open(path, mode='r', encoding='utf-8') as file:
        data = json.load(file)

        if isinstance(data, dict):
            vacancies_list = data.get('vacancies') or data.get('items') or [data]
        else:
            vacancies_list = data

        for vacancy in vacancies_list:
            if not isinstance(vacancy, dict):
                continue

            vacancy_id = vacancy.get('id')
            try:
                vacancy_id = int(vacancy_id)
            except Exception:
                pass

            name = vacancy.get('name', "")
            description = vacancy.get('description', "")
            combined_text = f"{name}. {description} "

            if isinstance(vacancy.get('key_skills'), list):
                skills = [
                    sk.get('name') if isinstance(sk, dict) else sk
                    for sk in vacancy['key_skills']
                    if isinstance(sk, (str, dict))
                ]
                if skills:
                    combined_text += " Ключевые навыки: " + ", ".join(skills)

            cleaned_text = clean_text(combined_text)

            vacancies.append({
                "id": vacancy_id,
                "text": cleaned_text,
                "name": name,
                "description": clean_text(description),
            })

        if vacancies:
            print("Первая вакансия:")
            for key, value in vacancies[0].items():
                print(f"{key}: {value}")

    return vacancies


def load_ground_truth(file_path: str) -> Dict[int, Set[int]]:
    """
    Загружает пары релевантности (вакансия → подходящие резюме) из CSV или JSON-файла.

    :param file_path: Путь к файлу.
    :return: Словарь соответствий: vacancy_id → множество resume_id.
    """
    global ground_truth
    ground_truth.clear()

    if file_path.endswith(".json"):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for key, value in data.items():
                try:
                    vac_id = int(key)
                    resume_ids = {int(rid) for rid in value}
                    ground_truth[vac_id] = resume_ids
                except Exception:
                    continue

    elif file_path.endswith(".csv"):
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            first_line = next(reader, None)

            if first_line and all(item.isdigit() for item in first_line[:2]):
                file.seek(0)
                reader = csv.reader(file)
                header = None
            else:
                header = [col.lower() for col in first_line] if first_line else None

            if header:
                try:
                    vac_idx = header.index("vacancy_id")
                except ValueError:
                    vac_idx = 0
                try:
                    res_idx = header.index("resume_id")
                except ValueError:
                    res_idx = 1
                label_idx = next((i for i, h in enumerate(header) if h in ("label", "relevant", "rel")), None)

                for row in reader:
                    if not row:
                        continue
                    try:
                        vac_id = int(row[vac_idx])
                        res_id = int(row[res_idx])
                        label = float(row[label_idx]) if label_idx is not None and len(row) > label_idx else 1.0
                        if label > 0:
                            ground_truth.setdefault(vac_id, set()).add(res_id)
                    except Exception:
                        continue
            else:
                for row in reader:
                    if not row:
                        continue
                    try:
                        vac_id = int(row[0])
                        res_id = int(row[1])
                        label = float(row[2]) if len(row) > 2 else 1.0
                        if label > 0:
                            ground_truth.setdefault(vac_id, set()).add(res_id)
                    except Exception:
                        continue
    else:
        raise ValueError("Поддерживаются только форматы .csv и .json")

    return ground_truth
