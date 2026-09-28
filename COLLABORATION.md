# Collaboration Workflow

One `main` branch. **Teddy is the maintainer and the only person who merges to `main`.**
Everyone else works on their own branch and opens a Pull Request; Teddy reviews and merges it.
This keeps `main` always working, and keeps the final notebook assembly in one pair of hands.

## One-time setup (each person)
After you **accept the repo invitation** from GitHub, you already have access — no token setup needed. Just clone and work; VS Code signs you in when you first push.
```bash
git clone https://github.com/Ted-star7/Ecosort-Waste-Management-System.git
cd Ecosort-Waste-Management-System
git config user.name  "Your Name"
git config user.email "you@example.com"
```

## Everyday cycle
```bash
git checkout main && git pull origin main       # 1. start from latest main
git checkout -b dennis-cnn                       # 2. your branch: jeff-text / eglen-rag
# 3. work ONLY in your own section notebook, e.g. sections/part2_cnn.ipynb
git add sections/part2_cnn.ipynb
git commit -m "CNN: MobileNetV2 baseline + confusion matrix"
git push origin dennis-cnn                        # 4. push YOUR branch (never main)
```

## Opening a Pull Request (required to reach main)
1. After pushing, GitHub shows **"Compare & pull request"** — click it.
2. Base = `main`, compare = your branch. Describe what you did.
3. Add **Teddy** as reviewer.
4. **Teddy** reviews and clicks **Merge pull request → Confirm merge**.
5. Everyone then runs `git checkout main && git pull origin main`.

> Rule: nobody pushes to `main` directly. All changes reach `main` through a PR that Teddy merges.

## Why section notebooks (important)
Jupyter notebooks are JSON and are **painful to merge** if two people edit the same one. So each
person edits **only their own** `sections/partX_*.ipynb`. That way PRs almost never conflict.
Teddy assembles the finished cells into `waste_management_summative.ipynb` for submission (Part 5).

## Assembling the final submission (Teddy)
1. Once each section is approved and merged, open the master `waste_management_summative.ipynb`.
2. Copy each person's finished cells into the matching `## Part N` placeholder.
3. Run the notebook **top-to-bottom** so every function/model is defined in order.
4. Confirm the RUBRIC.md checklist, then submit.

## Keeping your branch current (avoid big conflicts)
```bash
git checkout main && git pull origin main
git checkout your-branch && git merge main     # resolve any conflicts here, early and often
```

## Do / Don't
- ✅ Pull `main` before starting; edit only your section notebook; open a PR; clear commit messages.
- ✅ Use `sorted(folder names)` for categories; keep the grader function names/signatures fixed.
- ❌ Don't commit `realwaste.zip`, `RealWaste/`, or model files — they're gitignored (share via Releases).
- ❌ Don't push to `main`; don't edit someone else's section notebook.
