# Publishing to GitHub (for the repository owner)

## 0. Before you upload

```bash
python tools/build_skill.py    # rebuild dist/skill-dashboard-maker.skill
python tools/check_repo.py     # structure check (should print ✔ Passed)
```

If you have the Claude Code CLI, also run `claude plugin validate .`.

## Option 1. Upload in the GitHub web interface (nothing to install)

1. Sign in to github.com → **+ → New repository** in the top right
2. Repository name: `skill-dashboard-maker-en`, choose **Public**, leave "Add a README" and "Add a license" unchecked → **Create repository**
3. Click **uploading an existing file** and drag the contents of this folder in
   - Folders whose names start with a dot, such as `.claude-plugin`, are easy to lose when dragging. After uploading, make sure `.claude-plugin/marketplace.json` and `plugins/skill-dashboard-maker/.claude-plugin/plugin.json` are in the repository. Without them, Claude Code can't install the plugin.
   - If they are missing, use **Add file → Create new file**, type the whole path (`.claude-plugin/marketplace.json`) as the file name and paste the contents.
4. Commit message `First release (v1.0.0)` → **Commit changes**

## Option 2. Upload with git

```bash
cd skill-dashboard-maker-en
git init
git add .
git commit -m "First release (v1.0.0)"
git branch -M main
git remote add origin https://github.com/NogadaHunter/skill-dashboard-maker-en.git
git push -u origin main
```

## After uploading

- Click the gear next to **About** on the right of the repository. Description: `Turn every skill in your Claude into a one-page HTML dashboard with copy-ready prompts`. Topics: `claude`, `claude-skills`, `claude-code-plugin`, `dashboard`, `prompts`.
- **Releases → Create a new release** → tag `v1.0.0` → attach `dist/skill-dashboard-maker.skill` so Claude.ai users can download it easily.
- Install test in Claude Code: `/plugin marketplace add NogadaHunter/skill-dashboard-maker-en` → `/plugin install skill-dashboard-maker@peopleware-skill-dashboard-en`

## Making changes

1. Edit the files in `plugins/skill-dashboard-maker/skills/skill-dashboard-maker/`
2. Raise the `version` in `plugin.json` (for example 1.0.0 → 1.0.1). Without it, people who already installed it won't get the update
3. Add a line to `CHANGELOG.md`
4. `python tools/build_skill.py` → `python tools/check_repo.py` → upload
