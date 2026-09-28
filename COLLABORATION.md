# Collaboration Workflow

We have **one `main` branch**. Nobody pushes to `main` directly — all changes go through a
**Pull Request (PR)** that at least one teammate reviews and merges. This keeps `main` always working.

## One-time setup (each person)
```bash
git clone https://github.com/<org-or-teddy>/Ecosort-Waste-Management-System.git
cd Ecosort-Waste-Management-System
git config user.name  "Your Name"
git config user.email "you@example.com"
```
On the first `git push`, GitHub asks for a password — use a **Personal Access Token**, not your
GitHub password (GitHub → Settings → Developer settings → Personal access tokens → Fine-grained
or classic with `repo` scope). Paste the token as the password.

## Everyday cycle
```bash
# 1. Always start from the latest main
git checkout main
git pull origin main

# 2. Make your own branch for your part
git checkout -b dennis-cnn        # jeff-text / eglen-rag / teddy-data / teddy-integration

# 3. Work, then stage + commit small logical chunks
git add src/cnn_model.py notebooks/02_cnn_image_model.ipynb
git commit -m "CNN: add MobileNetV2 baseline + confusion matrix"

# 4. Push YOUR branch (never straight to main)
git push origin dennis-cnn
```

## Opening a Pull Request (required to reach main)
1. After pushing, GitHub shows a **“Compare & pull request”** button — click it.
2. Base = `main`, compare = your branch. Add a short description of what you did.
3. Tag a teammate as reviewer.
4. Once approved, click **Merge pull request** → **Confirm merge**.
5. Everyone then runs `git checkout main && git pull origin main` to get the update.

> **Rule of thumb:** if you are NOT merging into your own branch, you MUST open a PR.
> Only merge to `main` through a reviewed PR.

## Keeping your branch up to date (avoid big conflicts)
```bash
git checkout main && git pull origin main
git checkout your-branch
git merge main          # pull main's latest into your branch; resolve conflicts here
```
Do this often — small, frequent merges beat one giant painful one at the end.

## Resolving a merge conflict
Git marks conflicts with `<<<<<<<`, `=======`, `>>>>>>>`. Open the file, keep the correct
lines, delete the markers, then:
```bash
git add <file>
git commit                # completes the merge
```

## Do / Don't
- ✅ Pull `main` before starting; work on a branch; open a PR; write clear commit messages.
- ✅ Keep the function signatures in `src/config.py` and the integration contract fixed.
- ❌ Don't commit `realwaste.zip`, `RealWaste/`, or trained model files (`.keras`, `.faiss`, …) — they're gitignored. Share those via GitHub Releases.
- ❌ Don't push directly to `main`.
- ❌ Don't hard-code the category list — import it from `src/config.py`.
