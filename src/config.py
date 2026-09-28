"""
Shared configuration for the EcoSort Waste Management System.
Every module (Parts 1-5) imports from here so the whole team uses ONE
identical class list, paths, and constants. Do not hard-code categories
anywhere else.
"""
import os

# ---------------------------------------------------------------------------
# The 9 waste categories. Verified to match EXACTLY between the RealWaste
# image folders and the `category` column of waste_descriptions.csv.
# Order is fixed -> label index i always maps to CATEGORIES[i] in every model.
# ---------------------------------------------------------------------------
CATEGORIES = [
    "Cardboard",
    "Food Organics",
    "Glass",
    "Metal",
    "Miscellaneous Trash",
    "Paper",
    "Plastic",
    "Textile Trash",
    "Vegetation",
]
NUM_CLASSES = len(CATEGORIES)
CAT_TO_IDX = {c: i for i, c in enumerate(CATEGORIES)}
IDX_TO_CAT = {i: c for i, c in enumerate(CATEGORIES)}

# ---------------------------------------------------------------------------
# Paths (repo-relative, work in VS Code and Colab alike)
# ---------------------------------------------------------------------------
ROOT_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR   = os.path.join(ROOT_DIR, "data")
MODELS_DIR = os.path.join(ROOT_DIR, "models")

IMAGE_DIR      = os.path.join(DATA_DIR, "RealWaste")          # extracted images
DESCRIPTIONS_CSV = os.path.join(DATA_DIR, "waste_descriptions.csv")
POLICY_JSON      = os.path.join(DATA_DIR, "waste_policy_documents.json")

# Saved-model file names (written to MODELS_DIR)
CNN_MODEL_PATH  = os.path.join(MODELS_DIR, "cnn_waste_classifier.keras")
TEXT_MODEL_PATH = os.path.join(MODELS_DIR, "text_classifier.joblib")
RAG_INDEX_PATH  = os.path.join(MODELS_DIR, "policy_index.faiss")
RAG_CHUNKS_PATH = os.path.join(MODELS_DIR, "policy_chunks.joblib")

# ---------------------------------------------------------------------------
# Shared hyper-parameters / conventions
# ---------------------------------------------------------------------------
IMG_SIZE   = (224, 224)     # MobileNetV2 / EfficientNetB0 native input
BATCH_SIZE = 32
SEED       = 42
VAL_SPLIT  = 0.15
TEST_SPLIT = 0.15
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"   # sentence-transformers, Part 4
GEN_MODEL_NAME   = "google/flan-t5-base"  # generator, Part 4
