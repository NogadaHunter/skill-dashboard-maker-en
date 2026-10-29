#!/usr/bin/env python3
"""Checks the repository structure before uploading (a quick check for when the claude CLI is not available).
If you have the claude CLI, also run `claude plugin validate .`.

  python tools/check_repo.py
"""
import json
import os
import re
import sys
import zipfile

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = "skill-dashboard-maker"
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RESERVED = re.compile(r"^(claude|anthropic|anthropics|cc-plugin)(-|$)|claude-code|official")
errors, warns = [], []


def load(path):
    try:
        with open(os.path.join(ROOT, path), encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        errors.append(f"{path}: file not found")
    except json.JSONDecodeError as e:
        errors.append(f"{path}: invalid JSON ({e})")
    return None


mk = load(".claude-plugin/marketplace.json")
if mk:
    for k in ("name", "owner", "plugins"):
        if k not in mk:
            errors.append(f"marketplace.json: missing '{k}'")
    if mk.get("name") and (not KEBAB.match(mk["name"]) or RESERVED.search(mk["name"])):
        errors.append(f"marketplace.json: name '{mk['name']}' is not allowed (kebab-case, no reserved words)")
    if not (mk.get("owner") or {}).get("name"):
        errors.append("marketplace.json: missing owner.name")
    for i, p in enumerate(mk.get("plugins", [])):
        src = p.get("source", "")
        if ".." in str(src):
            errors.append(f"plugins[{i}]: source must not contain '..'")
        if isinstance(src, str):
            pdir = os.path.join(ROOT, src)
            if not os.path.isdir(pdir):
                errors.append(f"plugins[{i}]: source folder not found ({src})")
                continue
            man = load(os.path.join(src, ".claude-plugin", "plugin.json"))
            if man:
                if man.get("name") != p.get("name"):
                    errors.append(f"plugins[{i}]: marketplace name '{p.get('name')}' differs from plugin.json name '{man.get('name')}'")
                if not KEBAB.match(man.get("name", "")):
                    errors.append(f"plugin.json: name '{man.get('name')}' must be kebab-case")
                for k in ("version", "description", "author"):
                    if k not in man:
                        warns.append(f"plugin.json: missing '{k}'")
            sdir = os.path.join(pdir, "skills")
            for s in sorted(os.listdir(sdir)) if os.path.isdir(sdir) else []:
                sk = os.path.join(sdir, s, "SKILL.md")
                if not os.path.isfile(sk):
                    errors.append(f"skills/{s}: SKILL.md not found")
                    continue
                head = open(sk, encoding="utf-8").read().split("---")
                if len(head) < 3:
                    errors.append(f"skills/{s}/SKILL.md: no --- front matter at the top")
                    continue
                fm = head[1]
                nm = re.search(r"^name:\s*(.+)$", fm, re.M)
                ds = re.search(r"^description:\s*(.+)$", fm, re.M)
                if not nm or nm.group(1).strip() != s:
                    errors.append(f"skills/{s}/SKILL.md: name must match the folder name")
                if not ds:
                    errors.append(f"skills/{s}/SKILL.md: missing description")
                elif len(ds.group(1).strip()) > 1024:
                    warns.append(f"skills/{s}/SKILL.md: description is {len(ds.group(1).strip())} characters (1,024 or fewer recommended for Claude.ai upload)")
                for root, dirs, files in os.walk(os.path.join(sdir, s)):
                    if "__pycache__" in dirs:
                        warns.append(f"delete {os.path.relpath(root, ROOT)}/__pycache__ before uploading")

dist = os.path.join(ROOT, "dist", NAME + ".skill")
if os.path.isfile(dist):
    with zipfile.ZipFile(dist) as z:
        names = z.namelist()
    if f"{NAME}/SKILL.md" not in names:
        errors.append(f"dist/*.skill does not contain {NAME}/SKILL.md")
    src_count = sum(len(f) for _, _, f in os.walk(os.path.join(ROOT, "plugins", NAME, "skills", NAME)))
    if len(names) != src_count:
        warns.append(f"dist/*.skill has {len(names)} files but the skill folder has {src_count} → python tools/build_skill.py")
else:
    errors.append(f"dist/{NAME}.skill not found → python tools/build_skill.py")

for need in ("README.md", "LICENSE"):
    if not os.path.isfile(os.path.join(ROOT, need)):
        errors.append(f"{need} not found")

print("■ Repository check")
for e in errors:
    print("  ✖", e)
for w in warns:
    print("  ⚠", w)
print("  ✔ Passed" if not errors else f"  Failed: {len(errors)} problem(s)")
sys.exit(1 if errors else 0)
