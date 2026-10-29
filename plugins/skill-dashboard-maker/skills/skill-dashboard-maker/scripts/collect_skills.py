#!/usr/bin/env python3
"""Scans the installed skill folders and writes the skill list (skills_raw.json).

Usage:
  python3 collect_skills.py                      # finds the default location
  python3 collect_skills.py --root /mnt/skills/user --out /tmp/skills_raw.json

Per skill: name, description, path, files (files besides SKILL.md), file_list, size_kb, hash (first 12 chars of the SKILL.md SHA-1), trigger_hints
Standard library only.
"""
import argparse, hashlib, json, os, re, sys

DEFAULT_ROOTS = ["/mnt/skills/user", os.path.expanduser("~/.claude/skills")]
SKIP_NAMES = {"skill-dashboard-maker"}  # leave out this skill, which builds the dashboard
BULLET_TRIGGER = re.compile(r"\b(asks?|asked|requests?|says?|mentions?|wants?|needs?|make|create|write|generate|build|draft|turn|show|update)\b|[\"“”']", re.I)
SENTENCE_TRIGGER = re.compile(r"\b(use (this skill |it )?(when|whenever|for)|trigger(s|ed)? (when|on|by|include))\b", re.I)
NEGATIVE = re.compile(r"^(do not|don't|never|not for)\b", re.I)


def parse_frontmatter(text):
    """Reads only name and description from the YAML front matter (no external libraries)."""
    m = re.match(r"^﻿?---\s*\n(.*?)\n---\s*(\n|$)", text, re.S)
    if not m:
        return {}
    lines = m.group(1).splitlines()
    out, i = {}, 0
    while i < len(lines):
        line = lines[i]
        km = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not km:
            i += 1
            continue
        key, val = km.group(1), km.group(2).strip()
        if val in (">", "|", ">-", "|-", ">+", "|+", ""):
            block = []
            i += 1
            while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                block.append(lines[i].strip())
                i += 1
            joiner = "\n" if val.startswith("|") else " "
            out[key] = joiner.join(block).strip() if val != "" or block else ""
            continue
        if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
            val = val[1:-1]
        out[key] = val
        i += 1
    return out


def trigger_hints(desc, body):
    """Pulls trigger-like lines ("Use when the user asks…", bullet lists of requests) as hints. Only a starting point for the entry."""
    hints = []
    for src in (desc, body[:6000]):
        for line in src.splitlines():
            t = line.strip()
            if t.startswith(("- ", "* ", "• ")) and len(t) < 160 and BULLET_TRIGGER.search(t):
                hints.append(t[2:].strip())
    for sentence in re.split(r"(?<=[.!?])\s+(?=[A-Z\"“])", desc.replace('\\"', '"')):
        head, *inline_bullets = re.split(r"\s+-\s+", sentence)  # "...when the user: - asks to … - wants …"
        parts = [(head, SENTENCE_TRIGGER)] + [(b, BULLET_TRIGGER) for b in inline_bullets]
        for part, pattern in parts:
            s = part.strip()
            if 8 < len(s) < 220 and not s.endswith(":") and not NEGATIVE.match(s) and pattern.search(s):
                hints.append(s)
    seen, uniq = set(), []
    for h in hints:
        if h not in seen:
            seen.add(h)
            uniq.append(h)
    return uniq[:12]


def find_root(explicit):
    if explicit:
        return explicit if os.path.isdir(explicit) else None
    for r in DEFAULT_ROOTS:
        if os.path.isdir(r) and any(os.path.isfile(os.path.join(r, d, "SKILL.md")) for d in os.listdir(r)):
            return r
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", help="folder that holds the skill folders (default: /mnt/skills/user → ~/.claude/skills)")
    ap.add_argument("--out", default="/tmp/skill-dashboard/skills_raw.json")
    a = ap.parse_args()

    root = find_root(a.root)
    if not root:
        print("NO_SKILLS_ROOT: no installed skill folder found. Looked in: " + ", ".join([a.root] if a.root else DEFAULT_ROOTS))
        sys.exit(2)

    skills = []
    for d in sorted(os.listdir(root)):
        p = os.path.join(root, d)
        md = os.path.join(p, "SKILL.md")
        if not os.path.isfile(md):
            continue
        text = open(md, encoding="utf-8", errors="replace").read()
        fm = parse_frontmatter(text)
        name = (fm.get("name") or d).strip()
        if name.lower() in SKIP_NAMES or d.lower() in SKIP_NAMES:
            continue
        body = re.sub(r"^﻿?---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.S)
        files = []
        for r, _, fs in os.walk(p):
            for f in fs:
                rel = os.path.relpath(os.path.join(r, f), p).replace(os.sep, "/")
                if rel != "SKILL.md":
                    files.append(rel)
        skills.append({
            "name": name,
            "folder": d,
            "description": fm.get("description", "").strip(),
            "path": md,
            "files": len(files),
            "file_list": sorted(files)[:30],
            "size_kb": round(len(text.encode("utf-8")) / 1024, 1),
            "hash": hashlib.sha1(text.encode("utf-8")).hexdigest()[:12],
            "trigger_hints": trigger_hints(fm.get("description", ""), body),
        })

    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump({"root": root, "count": len(skills), "skills": skills}, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"FOUND {len(skills)} skills in {root} -> {a.out}")
    for s in skills:
        print(f"  - {s['name']}  ({s['size_kb']}KB, {s['files']} bundled files)")


if __name__ == "__main__":
    main()
