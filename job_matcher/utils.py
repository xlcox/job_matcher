from sentence_transformers import SentenceTransformer, util
from functools import lru_cache
from pathlib import Path


@lru_cache()
def get_model():
    model_path = Path(
        __file__).resolve().parent.parent.parent / "ml_models" / "fine_tuned_model"
    return SentenceTransformer(str(model_path))


def match_vacancy(vacancy_text, resumes):
    model = get_model()
    scores = []
    for resume in resumes:
        emb_vac, emb_res = model.encode([vacancy_text, resume.text])
        score = util.cos_sim(emb_vac, emb_res).item()
        scores.append((resume, round(score * 100, 2)))
    return sorted(scores, key=lambda x: x[1], reverse=True)
