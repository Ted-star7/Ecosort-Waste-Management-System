# EcoSort — Waste Management System

An integrated AI assistant for Metro City that (1) identifies waste from **images** (CNN),
(2) classifies waste from **text descriptions**, and (3) generates **recycling instructions**
grounded in city policy documents (RAG). The three are combined into one assistant.
 
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



## The 9 waste categories 
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
git clone https://github.com/Ted-star7/Ecosort-Waste-Management-System.git && cd Ecosort-Waste-Management-System
python -m venv .venv && .venv\Scripts\activate     # Windows
pip install -r requirements.txt
# put realwaste.zip in data/ ; the first notebook cell unzips it
```

