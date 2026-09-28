"""
Part 1 - Dataset Exploration & Preparation   [Owner: Teddy]

Shared data utilities used by every other part:
  - unzip/locate the RealWaste images
  - build train/val/test splits for images (via tf.data or Keras generators)
  - load & split the waste_descriptions.csv for the text model
  - load the policy documents for the RAG system
Run `python -m src.data_prep` for a quick sanity check.
"""
import os, json, zipfile, shutil
import numpy as np
import pandas as pd
from . import config as C


# --------------------------------------------------------------------- images
def ensure_images_extracted(zip_path=None):
    """Unzip data/realwaste.zip into data/RealWaste/<category>/ if not present."""
    if os.path.isdir(C.IMAGE_DIR) and any(os.scandir(C.IMAGE_DIR)):
        return C.IMAGE_DIR
    zip_path = zip_path or os.path.join(C.DATA_DIR, "realwaste.zip")
    if not os.path.exists(zip_path):
        raise FileNotFoundError(
            f"{zip_path} not found. See README for how to download the dataset.")
    tmp = os.path.join(C.DATA_DIR, "_tmp_extract")
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(tmp)
    # The zip nests images under realwaste-main/RealWaste/<category>/
    src = None
    for root, dirs, _ in os.walk(tmp):
        if os.path.basename(root) == "RealWaste":
            src = root; break
    shutil.move(src, C.IMAGE_DIR)
    shutil.rmtree(tmp, ignore_errors=True)
    return C.IMAGE_DIR


def image_class_counts():
    """Return {category: n_images} — useful for EDA and class-imbalance analysis."""
    counts = {}
    for cat in C.CATEGORIES:
        d = os.path.join(C.IMAGE_DIR, cat)
        counts[cat] = len(os.listdir(d)) if os.path.isdir(d) else 0
    return counts


def make_image_datasets(img_size=C.IMG_SIZE, batch_size=C.BATCH_SIZE, seed=C.SEED):
    """
    Returns (train_ds, val_ds, test_ds, class_names) as tf.data.Datasets.
    Uses an 70/15/15 split via image_dataset_from_directory (val+test carved out).
    """
    import tensorflow as tf
    ensure_images_extracted()
    # first split: train vs (val+test)
    train_ds = tf.keras.utils.image_dataset_from_directory(
        C.IMAGE_DIR, labels="inferred", label_mode="int",
        class_names=C.CATEGORIES, image_size=img_size, batch_size=batch_size,
        validation_split=C.VAL_SPLIT + C.TEST_SPLIT, subset="training", seed=seed)
    holdout = tf.keras.utils.image_dataset_from_directory(
        C.IMAGE_DIR, labels="inferred", label_mode="int",
        class_names=C.CATEGORIES, image_size=img_size, batch_size=batch_size,
        validation_split=C.VAL_SPLIT + C.TEST_SPLIT, subset="validation", seed=seed)
    # split holdout into val / test
    n_batches = tf.data.experimental.cardinality(holdout).numpy()
    n_val = n_batches // 2
    val_ds  = holdout.take(n_val)
    test_ds = holdout.skip(n_val)
    AUTOTUNE = tf.data.AUTOTUNE
    return (train_ds.prefetch(AUTOTUNE), val_ds.prefetch(AUTOTUNE),
            test_ds.prefetch(AUTOTUNE), C.CATEGORIES)


# ---------------------------------------------------------------------- text
def load_descriptions(split=True):
    """Load waste_descriptions.csv. If split, returns train/val/test DataFrames
    (stratified by category); else the full DataFrame."""
    df = pd.read_csv(C.DESCRIPTIONS_CSV)
    df = df.dropna(subset=["description", "category"]).reset_index(drop=True)
    assert set(df["category"]) <= set(C.CATEGORIES), "unexpected category label!"
    if not split:
        return df
    from sklearn.model_selection import train_test_split
    train, hold = train_test_split(df, test_size=C.VAL_SPLIT + C.TEST_SPLIT,
                                   stratify=df["category"], random_state=C.SEED)
    val, test = train_test_split(hold, test_size=0.5,
                                 stratify=hold["category"], random_state=C.SEED)
    return train.reset_index(drop=True), val.reset_index(drop=True), test.reset_index(drop=True)


# -------------------------------------------------------------------- policies
def load_policies():
    """Load the 14 policy documents (list of dicts) for the RAG system."""
    with open(C.POLICY_JSON, encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    print("Categories:", C.CATEGORIES)
    df = load_descriptions(split=False)
    print("Descriptions:", len(df), "rows")
    print(df["category"].value_counts())
    print("Policies:", len(load_policies()), "documents")
    try:
        print("Image counts:", image_class_counts())
    except Exception as e:
        print("Images not extracted yet:", e)
