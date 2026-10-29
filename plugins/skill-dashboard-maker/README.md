# skill-dashboard-maker

A plugin that reads every skill installed in your Claude and builds **one HTML skill dashboard**.
For each skill it writes a plain-language name, a one-line summary, inputs and outputs, and copy-ready default and situational prompts. The dashboard has search, 8 category filters, light and dark mode, and a mobile layout.
Attach a previous dashboard and only the skills that were added, changed or removed are rewritten, with the changes listed at the top.

## Install

```text
/plugin marketplace add NogadaHunter/skill-dashboard-maker-en
/plugin install skill-dashboard-maker@peopleware-skill-dashboard-en
```

## Usage

- First dashboard: `Make my skill dashboard`
- With your name: `Make a skill dashboard under the name [your name]`
- Update: (attach your previous `skill-dashboard.html`) `Update my skill dashboard`

On Claude Code it reads your personal skill folder (`~/.claude/skills`). For another location, tell Claude "my skills are in [path]".

## Requirements

Python 3 (standard library only, nothing else to install)

Details and an example: https://github.com/NogadaHunter/skill-dashboard-maker-en
