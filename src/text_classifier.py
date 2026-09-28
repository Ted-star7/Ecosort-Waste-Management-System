"""
Part 3 - Waste Description Classification   [Owner: Jeff]

Option A baseline (recommended first): TF-IDF + Logistic Regression / Linear SVM.
Reliable, fast, no GPU. For the "Excelled" tier, add the DistilBERT variant in
the notebook (fine-tune all layers) and compare.

Exposes predict_text(description) -> category, the interface Part 5 calls.
"""
import os, re
import joblib
from . import config as C

_STOP = None
def _clean(text):
    """Lowercase, strip punctuation/digits, collapse whitespace."""
    text = str(text).lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def build_pipeline():
    from sklearn.pipeline import Pipeline
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    return Pipeline([
        ("tfidf", TfidfVectorizer(preprocessor=_clean, ngram_range=(1, 2),
                                  min_df=2, max_features=20000, stop_words="english")),
        ("clf", LogisticRegression(max_iter=1000, C=5.0, class_weight="balanced")),
    ])


def train(train_df, val_df=None):
    pipe = build_pipeline()
    pipe.fit(train_df["description"], train_df["category"])
    os.makedirs(C.MODELS_DIR, exist_ok=True)
    joblib.dump(pipe, C.TEXT_MODEL_PATH)
    return pipe


def evaluate(pipe, test_df):
    from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
    y_pred = pipe.predict(test_df["description"])
    y_true = test_df["category"]
    acc = accuracy_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred, labels=C.CATEGORIES)
    rep = classification_report(y_true, y_pred, labels=C.CATEGORIES)
    return acc, cm, rep


_pipe = None
def predict_text(description):
    """INTEGRATION INTERFACE (Part 5). Return predicted category str."""
    global _pipe
    if _pipe is None:
        _pipe = joblib.load(C.TEXT_MODEL_PATH)
    return str(_pipe.predict([description])[0])
