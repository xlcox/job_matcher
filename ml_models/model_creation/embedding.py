"""Функции для загрузки, использования и тонкой настройки модели эмбеддингов."""

from typing import List, Tuple, Optional
import os

import numpy as np
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader

DEFAULT_MODEL_NAME = "sergeyzh/LaBSE-ru-turbo"


def load_model(model_name: Optional[str] = None, fine_tuned_path: Optional[str] = None) -> SentenceTransformer:
    """
    Загружает модель SentenceTransformer для получения эмбеддингов.
    При наличии пути к обученной модели загружает её, иначе загружает базовую модель по имени.

    :param model_name: Название модели в HuggingFace или путь (по умолчанию используется русская LaBSE-модель).
    :param fine_tuned_path: Путь к директории с тонко настроенной моделью (если есть).
    :return: Экземпляр модели SentenceTransformer.
    """
    if fine_tuned_path and os.path.isdir(fine_tuned_path):
        model = SentenceTransformer(fine_tuned_path)
    else:
        selected_model_name = model_name or DEFAULT_MODEL_NAME
        model = SentenceTransformer(selected_model_name)
    return model


def embed_texts(texts: List[str], model: SentenceTransformer, batch_size: int = 32) -> np.ndarray:
    """
    Генерирует эмбеддинги для списка текстов с использованием переданной модели.

    :param texts: Список строк (текстов) для преобразования в эмбеддинги.
    :param model: Модель SentenceTransformer, которая используется для кодирования.
    :param batch_size: Размер батча при обработке (по умолчанию 32).
    :return: Массив numpy размером (len(texts), embedding_dim) с эмбеддингами.
    """
    if model is None:
        raise ValueError("Модель не загружена. Пожалуйста, передайте корректный экземпляр SentenceTransformer.")

    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=False,
        convert_to_numpy=True
    )
    return embeddings


def fine_tune_model(
    model: SentenceTransformer,
    training_pairs: List[Tuple[str, str]],
    epochs: int = 1,
    output_path: Optional[str] = None,
    batch_size: int = 16
) -> SentenceTransformer:
    """
    Выполняет тонкую настройку модели эмбеддингов на парах текстов (например, вакансия и соответствующее резюме).
    Используется функция потерь MultipleNegativesRankingLoss для сближения положительных пар.

    :param model: Модель SentenceTransformer для дообучения.
    :param training_pairs: Список кортежей (текст1, текст2) — обучающие пары.
    :param epochs: Количество эпох обучения (по умолчанию 1).
    :param output_path: Путь для сохранения тонко настроенной модели (опционально).
    :param batch_size: Размер батча при обучении (по умолчанию 16).
    :return: Тонко настроенная модель.
    """
    if not all([SentenceTransformer, InputExample, losses]):
        raise ImportError("Необходима библиотека sentence-transformers для выполнения тонкой настройки.")

    train_examples = [
        InputExample(texts=[text_1, text_2], label=1.0)
        for text_1, text_2 in training_pairs
    ]
    data_loader = DataLoader(train_examples, batch_size=batch_size, shuffle=True)
    loss_function = losses.MultipleNegativesRankingLoss(model)

    total_steps = len(data_loader) * epochs
    warmup_steps = max(1, int(0.1 * total_steps))

    model.fit(
        train_objectives=[(data_loader, loss_function)],
        epochs=epochs,
        warmup_steps=warmup_steps,
        show_progress_bar=True,
        output_path=output_path or None
    )

    if output_path:
        try:
            print(f"Сохранение тонко настроенной модели в: {output_path}")
            model.save(output_path, safe_serialization=False)
        except Exception as error:
            print(f"⚠️ Ошибка при сохранении модели в '{output_path}': {error}")
            print("Подсказка: Удалите модель перед сохранением новой.")

    return model
