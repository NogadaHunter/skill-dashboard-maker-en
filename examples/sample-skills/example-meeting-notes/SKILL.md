---
name: example-meeting-notes
description: "(Made-up skill for the example) Turns meeting notes or a transcript into minutes with decisions and action items, saved as a DOCX. Use this skill when the user: - asks to write up meeting minutes (\"write up the minutes\") - wants notes turned into minutes (\"turn these notes into meeting minutes\") - asks for a document of a meeting (\"make a document of this meeting\")"
---

# example-meeting-notes

A made-up skill that exists only to show what skill-dashboard-maker produces.

## Input
- Meeting notes, a transcript (TXT or DOCX), or a chat log

## Steps
1. Find the attendees, date and agenda. Mark anything missing as [to confirm].
2. Group the discussion by agenda item and separate decisions from open issues.
3. Pull action items with an owner and a due date into a table.
4. Save one minutes DOCX.

## Modes
- Standard minutes
- One-page summary for a report
- Action items only
