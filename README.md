# EcoSort — Waste Management System

An integrated AI assistant for Metro City that (1) identifies waste from **images** (CNN),
(2) classifies waste from **text descriptions** (text model), and (3) generates
**recycling instructions** grounded in city policy documents (RAG). The three models
are combined into one assistant.

## The 9 waste categories
`Cardboard · Food Organics · Glass · Metal · Miscellaneous Trash · Paper · Plastic · Textile Trash · Vegetation`
These match **exactly** between the RealWaste image folders and `waste_descriptions.csv`.
They live in `src/config.py` — never hard-code them anywhere else.

## Team & module ownership
| Part | Module | Notebook | Owner |
|------|--------|----------|-------|
| 1 · Data exploration & prep | `src/data_prep.py` | `notebooks/01_data_exploration.ipynb` | **Teddy** |
| 2 · CNN image classifier | `src/cnn_model.py` | `notebooks/02_cnn_image_model.ipynb` | **Dennis** |
| 3 · Text classification | `src/text_classifier.py` | `notebooks/03_text_classification.ipynb` | **Jeff** |
| 4 · RAG instruction generation | `src/rag_system.py` | `notebooks/04_rag_recycling.ipynb` | **Eglen** |
| 5 · Integrated assistant | `src/assistant.py` | `notebooks/05_integrated_assistant.ipynb` | **Teddy** |

Parts 2, 3, 4 are **independent** — each touches only its own data (images / CSV / policy JSON)
and can be built and tested in isolation. Part 1 is shared groundwork; Part 5 depends on all three.

## The integration contract (agree on this — do not change signatures)
```
cnn_model.predict_image(image_path)          -> category (str)      # Dennis
text_classifier.predict_text(description)    -> category (str)      # Jeff
rag_system.generate_instructions(category, query) -> (text, docs)   # Eglen
assistant.assist(image_path=|description=)   -> result dict         # Teddy
```

## Repo layout
```
├── src/            # importable modules (the contract lives here)
├── notebooks/      # one notebook per part (run in VS Code OR Colab)
├── data/           # csv + json tracked in git; realwaste.zip & RealWaste/ are gitignored
├── models/         # trained models (gitignored — share via GitHub Releases)
├── docs/
├── requirements.txt
├── COLLABORATION.md  # git workflow: branches, pull, PR, merge to main
└── RUBRIC.md         # grading checklist — follow it
```

## Setup — VS Code / local
```bash
git clone <repo-url>
cd Ecosort-Waste-Management-System
python -m venv .venv && .venv\Scripts\activate     # Windows
pip install -r requirements.txt
# put realwaste.zip in data/  (see "Dataset" below), then:
python -m src.data_prep        # sanity check
```
Open any notebook in VS Code; the first cell handles paths automatically.

## Setup — Google Colab (fast, no Drive)
Open any notebook in Colab and **run the first cell** — it clones the repo, installs deps,
and downloads the dataset to Colab's local disk. Set `DATASET_URL` in that cell to the
`realwaste.zip` **GitHub Release** asset (see below). Enable a GPU for Parts 2 & 4:
`Runtime → Change runtime type → T4 GPU`.

## Dataset
`realwaste.zip` (~688 MB) is **too big for git**. Distribute it as a **GitHub Release asset**
(Releases allow up to 2 GB): create a release, upload `realwaste.zip`, copy the asset URL into
the notebook's `DATASET_URL`. Trained models are shared the same way (attach to a release) —
keep them out of git.

## Sources
Dataset: RealWaste (UCI ML Repository / github.com/sam-single/realwaste).
