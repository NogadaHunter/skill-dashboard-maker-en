# Prompt collection

Copy a prompt and change only the parts in `[ ]`.

## Before you start

- (Required) Claude.ai: turn on code execution under Settings → Capabilities, and turn this skill on under Customize → Skills
- (Required) At least one installed skill to put on the dashboard
- (For updates) The `skill-dashboard.html` you got last time

## Basic: your first dashboard

```text
Make my skill dashboard
```

The title is "<Name>'s Skill Dashboard". If Claude doesn't know your name, it asks once.

## Other situations

### 1. Choose the name

```text
Make a skill dashboard under the name [your name]
```

### 2. Choose the whole title

```text
Make a skill dashboard called '[Marketing Team Skills]'
```

### 3. No name

```text
Make my skill dashboard. Leave the name out.
```

The title becomes "My Skill Dashboard".

### 4. Update after changing skills

```text
(Attach: skill-dashboard.html)
Update my skill dashboard
```

Only the changed skills are rewritten, and the added, changed and removed skills are listed at the top. The title and name carry over from the previous dashboard.

### 5. Entries in another language

```text
Make my skill dashboard. Write the skill entries in [Spanish].
```

The interface stays in English; skill names, summaries, prompts and tips are written in the language you ask for.

### 6. Point to your skill folder (Claude Code)

```text
Make my skill dashboard. My skills are in [~/.claude/skills].
```

On Claude Code it looks in your personal skill folder (`~/.claude/skills`) first. Use this to summarize skills kept somewhere else.

## Using the dashboard

1. Type what you want to do in the search box, or click a category.
2. Pick a skill and its default prompt and situational prompts appear on the right.
3. Press **Copy**, paste it into the Claude chat and change the `[ ]` parts.

## Good to know

- The dashboard does not update itself. After adding, changing or removing skills, ask for an update as in 4 above.
- The file opens offline. Save it somewhere handy, or if Claude showed it as an artifact, pin it in the sidebar.
- With more than 40 skills, Claude works in batches of 8 to 10 and reports progress after each batch.
- The dashboard contains no personal or company details or folder paths from your computer, only the name you give.
