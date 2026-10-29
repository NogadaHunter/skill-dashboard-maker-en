---
name: skill-dashboard-maker
description: "Builds a single-file HTML skill dashboard from every skill installed in the user's Claude: a plain-language name, one-line summary, inputs and outputs, and copy-ready default and situational prompts for each skill, with search, category filters, light and dark mode, and a mobile layout. When the user attaches a dashboard made earlier, only the skills that were added, changed or removed are rewritten, and the changes are listed at the top. Use this skill when the user: - asks to make, build or show a skill dashboard (\"make my skill dashboard\", \"show me a dashboard of my skills\") - wants their installed skills listed or organized with how to use them (\"what skills do I have?\", \"organize my skills\", \"how do I use my skills?\") - wants a prompt collection for their skills (\"give me prompts for each of my skills\") - attaches a dashboard HTML and asks to update or refresh it (\"update my skill dashboard\") - mentions skill-dashboard-maker"
---

# skill-dashboard-maker

Collect the installed skill folders with a script, read each SKILL.md, write a short usage entry for every skill,
and pour the entries into `assets/dashboard-template.html` to produce **one skill dashboard HTML file**.
The template owns the design, so do not design anything new. Your job is to describe each skill accurately.

Output: `skill-dashboard.html` (a single file that opens offline, with search, category filters, skill details, prompt copy buttons, light and dark mode, and a mobile layout)

---

## Before you start

- This skill needs code execution (file creation). If it is off, tell the user "Please turn on code execution and file creation under Settings → Capabilities, then ask again" and stop.
- Script paths are relative to the folder that holds this SKILL.md. Below, `$SKILL` means that folder (for example `/mnt/skills/user/skill-dashboard-maker`).
- On Claude Code, use a temporary folder that exists on the user's system instead of `/tmp`, and save the result in the current working folder instead of `/mnt/user-data/outputs`.

---

## STEP 0. Choose the dashboard title

The title uses **the name of the person who will use the dashboard**: "<Name>'s Skill Dashboard".
This skill contains no personal or company names. The title only ever uses a name that came from the user.

Decide the name in this order:
1. If this request includes a name, use it (for example "make it under the name Alex Kim"). If the user gives a whole title ("call it 'Marketing Team Skills'"), use that title as is.
2. If this is an update with a previous dashboard attached, reuse the `OWNER` printed by `plan` in STEP 2. Do not ask again.
3. If you already know the user's name from this conversation, their profile or memory, use it, and say in your first message: "I'll title it '<Name>'s Skill Dashboard'. Tell me if you'd like a different title."
4. Otherwise, ask once before collecting: "What name should go in the dashboard title? Say 'no name' to leave it out." If the answer is 'no name' or no name is given, use "My Skill Dashboard".

Rules:
- Never put a name from this skill's examples or documents in the title or body. Do not add company names, affiliations or contact details (unless the user explicitly asks for them in the title).
- Pass the chosen name to STEP 4 as `--owner`. If you received a whole title, pass it as `--title`.

## Language

- The dashboard interface (buttons, labels, categories) is always English.
- Write the skill entries in English by default. If the user asks for another language, or is clearly writing to you in another language, write the entries (names, summaries, prompts, tips) in that language. Prompts should be in the language the user will type them in.

---

## STEP 1. Collect installed skills

```bash
python3 $SKILL/scripts/collect_skills.py --out /tmp/skill-dashboard/skills_raw.json
```

- By default it looks in `/mnt/skills/user` (claude.ai), then `~/.claude/skills` (Claude Code). This skill itself is left out of the list.
- If you see `NO_SKILLS_ROOT`: run `ls /mnt/skills/` to check for another location and rerun with `--root` if you find one. If there is none, tell the user "I couldn't find any installed skills. Please check that your skills are turned on under Settings → Capabilities (or Customize → Skills)." and stop.
- Tell the user the count and names in one line (for example "I found 23 installed skills. I'll read and summarize each one.").

## STEP 2. Check whether this is an update (only when a previous dashboard is attached)

If the user attached a `skill-dashboard.html` made earlier:

```bash
python3 $SKILL/scripts/build_dashboard.py plan --raw /tmp/skill-dashboard/skills_raw.json \
  --previous /mnt/user-data/uploads/skill-dashboard.html --out-dir /tmp/skill-dashboard
```

- Unchanged skills go into `reuse.json` as they are, and only the skills that need a new entry are listed in `todo.txt`.
- Tell the user the added, changed and removed skills first, briefly.
- Take the `OWNER` it prints (the name on the previous dashboard) as the STEP 0 name. If the user gave a different name this time, theirs wins.
- With no attachment, skip this step and write entries for every skill (running `plan` without `--previous` is also fine).

## STEP 3. Write an entry for each skill (the core of the work)

Read `references/writing-guide.md` first, then write one entry per skill in that format and to that standard.

- For each skill, read the SKILL.md at its `path` in `skills_raw.json` **to the end**. `trigger_hints` is only a starting point.
- Save entries in batches of 8 to 10 as JSON arrays in `/tmp/skill-dashboard/new_01.json`, `new_02.json`, … and check that each file parses as JSON when you save it.
- Report progress in one line per batch (for example "10 of 20 skills done").
- If something can't be learned from the SKILL.md, leave it empty or keep it general. Do not invent anything.

## STEP 4. Build the dashboard

```bash
python3 $SKILL/scripts/build_dashboard.py build \
  --raw /tmp/skill-dashboard/skills_raw.json \
  --data /tmp/skill-dashboard/reuse.json --data /tmp/skill-dashboard/new_01.json [--data … every batch file] \
  [--previous /mnt/user-data/uploads/skill-dashboard.html] \
  [--owner "<name chosen in STEP 0>"] [--title "<whole title given by the user>"] \
  --out /mnt/user-data/outputs/skill-dashboard.html
```

- Title rule: `--title` is used as is; otherwise `--owner` gives "<Name>'s Skill Dashboard". With neither, an update keeps the previous title, and a first build uses "My Skill Dashboard". Check that the title on the first line of the output matches STEP 0.
- On a first build there is no `reuse.json`, so leave that `--data` out and pass only the batch files.
- If you see `MISSING` or `INCOMPLETE`, add or complete those entries in a batch file and run it again. Do not use `--force`.
- Do not edit the template's HTML, CSS or script. Only edit the result file when the user asks for different wording or design.

## STEP 5. Deliver

- Give the user `/mnt/user-data/outputs/skill-dashboard.html` as a file (present_files). If artifacts are available, also show the same HTML as an artifact.
- Keep the closing message short and include:
  1. The dashboard title, the number of skills and categories, and for an update the number added, changed and removed
  2. How to use it: search or click a category, pick a skill, then press Copy on a prompt and paste it into the chat
  3. How to keep it handy: save the file, or pin the artifact in the sidebar
  4. How to update it: after changing skills, attach this file and say "update my skill dashboard" (it does not update itself)

---

## Quality checklist

- Every collected skill is on the dashboard (the skill count from build equals the count from STEP 1)
- Every default prompt fits the skill's real triggers and inputs
- Every category is one of the 8 categories
- No company names, people's names or numbers were invented
- The title and body contain no personal, company or affiliation details other than the name the user gave

## Error handling

| Situation | What to do |
|---|---|
| Code execution is off | Explain how to turn it on and stop |
| NO_SKILLS_ROOT | Check other locations; if none, explain how to turn skills on |
| Zero skills | Say "You don't have any installed skills yet" and stop |
| PREVIOUS_INVALID | The attachment wasn't made by this skill; ask whether to build a new dashboard from scratch |
| Very many skills (40 or more) | Work in batches and report progress after each batch |
| SKILL.md empty or broken | Fill that entry briefly from the name and description and add "Check this skill's SKILL.md" to its tips |

## Files

```
skill-dashboard-maker/
├── SKILL.md
├── scripts/
│   ├── collect_skills.py      ← collects installed skills (skills_raw.json)
│   └── build_dashboard.py     ← update check (plan) · dashboard build (build)
├── assets/
│   └── dashboard-template.html ← dashboard design template (do not edit)
└── references/
    └── writing-guide.md       ← entry format, standards and categories
```
