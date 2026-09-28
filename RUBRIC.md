# Grading Rubric — Checklist (100 pts, follow this)

Each part is worth **20 pts**. Aim for the **Excelled** column. Check the box when done.

## Part 1 — Dataset Exploration & Preparation (20) — *Teddy*
- [ ] Comprehensive EDA with insightful visualizations (class distribution, sample images, text/vocab, policy structure)
- [ ] Advanced preprocessing addressing dataset-specific challenges (resolution/background/quality; text cleaning; doc chunking)
- [ ] Strategic train/val/test splits **with justification** (stratified; ratios stated)
- [ ] Documented biases/limitations (class imbalance: Plastic 921 vs Textile Trash 318 → imbalance ratio ~2.9)

## Part 2 — CNN Image Classification (20) — *Dennis*
- [ ] Transfer learning **with justification** for base-model choice (MobileNetV2 vs EfficientNetB0)
- [ ] Optimized hyperparameters with evidence of experimentation (dropout, dense units, fine-tune depth, LR)
- [ ] Confusion-matrix analysis + identification of challenging categories
- [ ] Class-imbalance handling (class weights / augmentation)

## Part 3 — Text Description Classification (20) — *Jeff*
- [ ] Advanced text preprocessing (tokenization, cleaning, normalization, embeddings/TF-IDF)
- [ ] Model with architecture justification (TF-IDF+LogReg baseline; DistilBERT for top tier)
- [ ] Misclassification analysis + challenging descriptions/confusion cases
- [ ] Optimization with evidence of experimentation
- [ ] `predict_text(description) -> category` function delivered

## Part 4 — RAG Instruction Generation (20) — *Eglen*
- [ ] Document preprocessing + advanced embeddings (sentence-transformers)
- [ ] Retrieval mechanism (FAISS index) with tuning
- [ ] RAG generation grounded in retrieved policy text (FLAN-T5); sampling params experimented
- [ ] Evaluation of factual consistency & readability of generated instructions
- [ ] `generate_instructions(category, query) -> (text, docs)` function delivered

## Part 5 — Integrated Assistant (20) — *Teddy*
- [ ] Seamless integration of all three models with robust error handling
- [ ] Clean interfaces between components (the contract in config/README)
- [ ] Comprehensive testing incl. challenging edge cases (image + text)
- [ ] Efficient architecture; (bonus) user-feedback mechanism
- [ ] Demonstrated on a real test-set image

## Before submission
- [ ] All notebooks run top-to-bottom without errors
- [ ] One combined submission notebook OR clearly organized set, per assignment instructions
- [ ] Everyone's part merged to `main` via PR
