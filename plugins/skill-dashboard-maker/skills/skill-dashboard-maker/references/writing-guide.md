# How to write skill entries (used in STEP 3)

Write one JSON entry per skill in the format below. Always read that skill's SKILL.md to the end and base the entry on the inputs, triggers, outputs and steps written there. Never add features the SKILL.md does not describe.

## Entry format

The example below is a **made-up skill** that only shows the format. Real entries come only from the user's SKILL.md files.

```json
{
  "name": "example-meeting-notes",
  "display_name": "Meeting Notes Writer",
  "category": "Documents & Reports",
  "summary": "Turns meeting notes or a transcript into minutes with decisions and action items, as a DOCX.",
  "inputs": "Meeting notes, transcript, chat log",
  "outputs": "1 minutes DOCX + action item table",
  "formats": ["DOCX"],
  "triggers": ["Write up the minutes", "Turn these notes into meeting minutes", "Make a document of this meeting"],
  "prompt": "(Attach: [meeting notes].txt)\nTurn this meeting into minutes.\nThe meeting is [meeting name] on [date].",
  "situations": [
    {"title": "One-page summary for a report", "prompt": "(Attach: [transcript].docx)\nWrite one-page minutes that focus on the decisions."},
    {"title": "Action items only", "prompt": "Pull only the action items with an owner and a due date from these notes, as a table."}
  ],
  "tips": ["Give the attendees and the date for an accurate header.", "Without a template it uses a standard minutes layout."],
  "related": ["example-email-summary"]
}
```

You do not need to add `hash` or `files`; the build script fills them in.

## Field standards

| Field | Standard |
|---|---|
| name | Exactly the `name` in the SKILL.md front matter (must match the name in skills_raw.json) |
| display_name | A plain-language name that says what the tool does, about 2 to 5 words. Not a word-for-word copy of the folder name |
| category | Exactly one of the 8 categories below |
| summary | One sentence that shows input → result, 120 characters or fewer |
| inputs / outputs | 70 characters or fewer each. In outputs, give the file format and how many files |
| formats | Upper-case format list: DOCX PDF PPTX XLSX HWPX HTML MD TXT PNG MP4 and so on. If the skill makes no file, use ["Chat reply"] |
| triggers | 3 to 5 trigger phrases from the SKILL.md description, written the way a user would actually type them |
| prompt | A default prompt the user can copy as is. Put the parts to change in [square brackets]. If a file is needed, start with "(Attach: …)" |
| situations | 2 or 3 situational prompts. If the skill supports several modes or types, one per mode |
| tips | 2 to 4 tips: connectors, API keys or web search it needs, supported file types, common mistakes |
| related | 0 to 3 skills that work well with it. Only names that appear in skills_raw.json |

## The 8 categories

| Category | Skills like |
|---|---|
| Documents & Reports | Reports, meeting minutes, memos, official letters, email summaries, slide decks |
| Content & Marketing | Blog posts, newsletters, social media, card news, ad copy, landing page copy |
| Education & Training | Lesson plans, curricula, course materials, e-learning scripts, training proposals |
| Books & Publishing | Book proposals, outlines, manuscript writing, style editing, publishing layouts |
| Planning & Analysis | Proposals, PRDs, research, analysis reports, chatbot and agent prompts |
| Video & Design | Video scripts, shorts, motion graphics, thumbnails, design |
| Data & Automation | Data analysis, spreadsheets, stock market, scraping, recurring reports, workflow automation |
| Other | Only when none of the above fits |

## Style rules

- Descriptions are short, plain sentences. Prompts are written the way a user talks to Claude ("Write…", "Make…", "Turn this into…").
- No em dashes (—), no piles of emoji, no marketing words like "revolutionary" or "game-changing".
- If you don't know the user's context, use general examples. Do not invent company names or people's names.
- Write in English unless the user asked for another language (see "Language" in SKILL.md). Category names always stay in English.

## Working through many skills

- Read 8 to 10 skills at a time and save each batch as a JSON array, such as `/tmp/skill-dashboard/new_01.json`, `new_02.json`, ….
- After saving, check the JSON with `python3 -c "import json;json.load(open('FILE'))"`.
