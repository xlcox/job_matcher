import sys

import data_loader
import embedding as embedding_module


def main():
    """
    Главная функция для тонкой настройки модели на основе данных резюме и вакансий.
    Загружает данные, подготавливает пары текста, обучает модель и сохраняет результат.
    """
    print("Запуск тонкой настройки модели с использованием обучающих данных...")

    # Загрузка данных резюме и вакансий
    resumes_data = data_loader.load_resumes("data/resumes.csv")
    vacancies_data = data_loader.load_vacancies("data/vacancies.json")

    if not resumes_data or not vacancies_data:
        print("Отсутствуют данные резюме или вакансий для обучения. "
              "Пожалуйста, убедитесь, что файлы данных присутствуют.")
        sys.exit(1)

    # Загрузка базовой или ранее обученной модели
    model = embedding_module.load_model(fine_tuned_path="models/fine_tuned_model")

    # Загрузка обучающих пар из файла
    ground_truth_pairs = data_loader.load_ground_truth("data/train_pairs.csv")

    # Подготовка текстовых пар для обучения
    training_text_pairs = []
    for vacancy_id, resume_ids in ground_truth_pairs.items():
        # Поиск текста вакансии по ID
        vacancy_entry = next((vacancy for vacancy in vacancies_data if vacancy['id'] == vacancy_id), None)
        if not vacancy_entry:
            continue
        vacancy_text = vacancy_entry['text']

        for resume_id in resume_ids:
            # Поиск текста резюме по ID
            resume_entry = next((resume for resume in resumes_data if resume['id'] == resume_id), None)
            if not resume_entry:
                continue
            resume_text = resume_entry['text']
            training_text_pairs.append((vacancy_text, resume_text))

    if not training_text_pairs:
        print("Не найдено обучающих пар. Завершение работы.")
        sys.exit(1)

    # Тонкая настройка модели
    model = embedding_module.fine_tune_model(
        model,
        training_text_pairs,
        epochs=1,
        output_path="models/fine_tuned_model",
        batch_size=16
    )

    print("Тонкая настройка модели завершена. "
          "Обученная модель сохранена в папке models/fine_tuned_model/")


if __name__ == "__main__":
    main()
