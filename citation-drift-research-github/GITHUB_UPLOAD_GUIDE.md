# Publish this project on GitHub (Mac)

## 1. Create the repository

1. Sign in at https://github.com.
2. Click **New repository** (the `+` menu, top-right).
3. Repository name: `detecting-citation-drift`
4. Description: `Research scaffold and documentation for evaluating citation support in AI-generated scientific literature summaries.`
5. Choose **Private** initially. Dataset, paper, and model licenses have not all been verified; make it public only after checking permissions.
6. Do **not** initialize with a README, `.gitignore`, or license (this folder already contains project files).
7. Click **Create repository**.

## 2. Download and extract the ZIP

Download `citation-drift-research-github.zip` from this chat and extract it. Open Terminal and move into the extracted folder. For example, if it is in Downloads:

```bash
cd ~/Downloads/citation-drift-research-github
```

If Finder extracted it into a folder with a slightly different name, use `cd ` and drag the folder into Terminal to insert its exact path.

## 3. Configure Git (only if not already configured)

```bash
git --version
git config --global user.name "Your Name"
git config --global user.email "YOUR_GITHUB_EMAIL"
```

Replace the two quoted values with your own details. These are commit metadata, not your GitHub password.

## 4. Upload the project

On the newly created GitHub repository page, copy its HTTPS URL. It will look like `https://github.com/YOUR-USERNAME/detecting-citation-drift.git`.

Run these commands from inside the extracted project folder:

```bash
git init
git add .
git status
git commit -m "Add citation drift research project scaffold"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/detecting-citation-drift.git
git push -u origin main
```

Replace the remote URL with the exact URL GitHub shows you. If GitHub asks you to authenticate, complete its browser/device sign-in flow; do not paste a password or token into this README or commit it to the repository.

## 5. Check the upload

Refresh the GitHub repository page. You should see `README.md`, `src/`, `scripts/`, `configs/`, `notebooks/`, `docs/`, `reports/`, and `paper/`.

## Important research-status notes

- The SciFact + DeBERTa-v3 experiment is a separately reported preliminary run. Its reported metrics are not results from the AlignScore pipeline.
- The AlignScore scaffold is not verified end-to-end; its import, checkpoint inference, and tests still require execution.
- The only JSONL data in the scaffold is a two-record synthetic example. No real dataset is bundled.
- Do not upload downloaded model checkpoints, restricted datasets, API keys, `.env` files, or private annotations.
- Dataset and model licenses have not all been verified. Keep the repository private until you confirm what may be redistributed.
- No open-source license is included. Do not add an MIT/Apache license unless you have the right to license all content you own and have checked third-party material.
