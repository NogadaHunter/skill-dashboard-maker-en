# Example (4 made-up skills)

These **made-up skills** exist only to show what the dashboard looks like. None of them is a real skill, and every name starts with `example-`.

| File | Step | Contents |
|---|---|---|
| [`sample-skills/`](sample-skills/) | 1. Collect | SKILL.md files for 4 made-up skills, one each for documents, content, education and data |
| [`sample-entries.json`](sample-entries.json) | 3. Describe each skill | The entries Claude writes after reading each SKILL.md, in the `references/writing-guide.md` format |
| [`sample-skill-dashboard.html`](sample-skill-dashboard.html) | 4. Build | The finished dashboard. Download it and open it in a browser (works offline) |

GitHub shows HTML files as code. Open the file, click **Download raw file**, then double-click the download to see the dashboard.

## Run it yourself

From the top folder of the repository:

```bash
S=plugins/skill-dashboard-maker/skills/skill-dashboard-maker/scripts
python $S/collect_skills.py --root examples/sample-skills --out out/skills_raw.json
python $S/build_dashboard.py build --raw out/skills_raw.json --data examples/sample-entries.json \
  --title "Example Skill Dashboard" --out out/skill-dashboard.html
```

You can try an update too. Edit or delete one of the example skills, collect again, and pass the previous dashboard: only the changed skills are picked out.

```bash
python $S/build_dashboard.py plan --raw out/skills_raw.json \
  --previous examples/sample-skill-dashboard.html --out-dir out
```
