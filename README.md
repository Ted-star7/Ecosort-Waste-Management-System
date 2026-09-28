# EcoSort — Waste Management System

An integrated AI assistant for Metro City that (1) identifies waste from **images** (CNN),
(2) classifies waste from **text descriptions**, and (3) generates **recycling instructions**
grounded in city policy documents (RAG). The three are combined into one assistant.

## How this repo is organized
The graded deliverable is a **single notebook**: `waste_management_summative.ipynb` (the assembly /
submission notebook). To avoid four people editing one notebook at once, **each person develops their
part in its own notebook under `sections/`**, then the finished cells are pasted into the matching
Part in the master notebook. Everyone imports the libraries they need inside their own notebook —
there is no shared package to install.

```
├── waste_management_summative.ipynb   # MASTER — assembled for submission (Teddy maintains)
├── sections/
│   ├── part1_data_prep.ipynb   # Teddy
│   ├── part2_cnn.ipynb          # Dennis
│   ├── part3_text.ipynb         # Jeff
│   ├── part4_rag.ipynb          # Eglen
│   └── part5_integration.ipynb  # Teddy
├── data/           # waste_descriptions.csv + waste_policy_documents.json (tracked)
│                   # realwaste.zip & RealWaste/ are gitignored (too big for git)
├── requirements.txt
├── COLLABORATION.md   # git workflow + how we assemble the final notebook
└── RUBRIC.md          # grading checklist — follow it
```

## Team & ownership
| Part | Owner | Section notebook |
|------|-------|------------------|
| 1 · Data exploration & prep | **Teddy** | `sections/part1_data_prep.ipynb` |
| 2 · CNN image classifier | **Dennis** | `sections/part2_cnn.ipynb` |
| 3 · Text classification | **Jeff** | `sections/part3_text.ipynb` |
| 4 · RAG instruction generation | **Eglen** | `sections/part4_rag.ipynb` |
| 5 · Integration + assembly | **Teddy** | `sections/part5_integration.ipynb` + master |

Parts 2, 3, 4 are **independent** — each touches only its own data. Teddy is the repo maintainer and
**merges everyone's Pull Requests** into `main`.

## The 9 waste categories (keep consistent everywhere)
`Cardboard · Food Organics · Glass · Metal · Miscellaneous Trash · Paper · Plastic · Textile Trash · Vegetation`
They match exactly between the image folders and `waste_descriptions.csv`. Every notebook derives them
with `sorted(folder names)` so the label order is identical across all parts — don't hard-code a
different order.

## The function names the grader expects (keep these signatures)
```
classify_waste_description(description)      -> category            # Part 3 (Jeff)
generate_recycling_instructions(category)    -> (text, docs)        # Part 4 (Eglen)
waste_management_assistant(input_data, input_type="image"|"text")   # Part 5 (Teddy)
classify_waste_image(image_path)  -> category   # Part 2 helper (Dennis) used by Part 5
```

## Run in VS Code / local
```bash
git clone <repo-url> && cd Ecosort-Waste-Management-System
python -m venv .venv && .venv\Scripts\activate     # Windows
pip install -r requirements.txt
# put realwaste.zip in data/ ; the first notebook cell unzips it
```

## Run in Google Colab (fast, no Drive)
Open any notebook in Colab and run the first cell — it clones the repo, installs deps, and downloads
the dataset to Colab's local disk. Set `DATASET_URL` in that cell to the `realwaste.zip` **GitHub
Release** asset. Enable a GPU for Parts 2 & 4: `Runtime → Change runtime type → T4 GPU`.

## Dataset & models
`realwaste.zip` (~688 MB) and trained models are **too big for git** — distribute them as **GitHub
Release assets** (up to 2 GB each) and paste the link into the notebooks' `DATASET_URL`.

Dataset: RealWaste (UCI ML Repository / github.com/sam-single/realwaste).
