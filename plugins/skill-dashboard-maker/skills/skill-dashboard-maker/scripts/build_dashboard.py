#!/usr/bin/env python3
"""Builds the skill dashboard HTML and, for updates, compares it with the previous dashboard. Standard library only.

1) Prepare an update (when a previous dashboard HTML exists)
   python3 build_dashboard.py plan --raw skills_raw.json --previous previous.html --out-dir /tmp/skill-dashboard
   → writes reuse.json (entries to keep) and todo.txt (skills that need a new entry), prints added/updated/removed

2) Build the dashboard
   python3 build_dashboard.py build --raw skills_raw.json --data reuse.json --data new_01.json [--data new_02.json ...]
        [--previous previous.html] [--owner "User Name"] [--title "Whole title"] --out /mnt/user-data/outputs/skill-dashboard.html

   Title: --title as is → otherwise --owner gives "<Name>'s Skill Dashboard"
        → with neither, an update keeps the previous name and title → otherwise "My Skill Dashboard"
"""
import argparse, datetime, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "assets", "dashboard-template.html")
MAKER_VERSION = "v1.0"
DEFAULT_TITLE = "My Skill Dashboard"
PLACEHOLDER = re.compile(r"^(\[.*\]|<.*>|x{2,}|_{2,}|your ?name|user ?name|my ?name|name|no ?name|none|n/?a|-)$", re.I)
CATEGORY_ORDER = ["Documents & Reports", "Content & Marketing", "Education & Training", "Books & Publishing",
                  "Planning & Analysis", "Video & Design", "Data & Automation", "Other"]
REQUIRED = ["name", "display_name", "category", "summary", "prompt"]
LISTS = ["triggers", "formats", "tips", "related"]


def load_json(p):
    return json.load(open(p, encoding="utf-8"))


def extract_previous(html_path):
    """Pulls the data embedded in a previous dashboard HTML."""
    html = open(html_path, encoding="utf-8").read()
    m = re.search(r'<script type="application/json" id="skill-data">(.*?)</script>', html, re.S)
    if not m:
        sys.exit("PREVIOUS_INVALID: no dashboard data found in this file. Check that it is an HTML file made by skill-dashboard-maker.")
    return json.loads(m.group(1).replace("<\\/", "</"))


def entries_from(files):
    items = []
    for f in files:
        d = load_json(f)
        items.extend(d["skills"] if isinstance(d, dict) and "skills" in d else d)
    return items


def key(name):
    return str(name or "").strip().lower()


def clean_owner(value):
    """Keeps only a name the user gave. Empty or a placeholder ([your name], xxx, ...) becomes an empty string."""
    v = re.sub(r"\s+", " ", str(value or "")).strip().strip("'\"“”‘’")
    return "" if not v or PLACEHOLDER.match(v) else v[:30]


def source_label(root):
    """Keeps a generic label instead of the skill folder path, so account names on the PC never reach the dashboard."""
    r = str(root or "").replace("\\", "/")
    if r.startswith("/mnt/skills"):
        return "claude.ai skills"
    if "/.claude/skills" in r:
        return "Claude Code personal skills"
    return "skill folder"


def diff(raw, prev):
    """Pairs skills by name (case-insensitive) to find added, removed and updated (SKILL.md hash changed) skills."""
    prev_by = {key(s["name"]): s for s in prev.get("skills", [])}
    now_by = {key(s["name"]): s for s in raw["skills"]}
    added = sorted(now_by[k]["name"] for k in now_by if k not in prev_by)
    removed = sorted(prev_by[k]["name"] for k in prev_by if k not in now_by)
    updated = sorted(now_by[k]["name"] for k in now_by if k in prev_by and prev_by[k].get("hash") != now_by[k]["hash"])
    return added, removed, updated, prev_by


def cmd_plan(a):
    raw = load_json(a.raw)
    os.makedirs(a.out_dir, exist_ok=True)
    if a.previous:
        prev = extract_previous(a.previous)
        added, removed, updated, prev_by = diff(raw, prev)
        reuse = [prev_by[key(s["name"])] for s in raw["skills"] if key(s["name"]) in prev_by and s["name"] not in updated]
        todo = added + updated
        print(f"PREVIOUS {prev.get('generated_at', '?')}: unchanged {len(reuse)} / added {len(added)} / updated {len(updated)} / removed {len(removed)}")
        print(f"OWNER {clean_owner(prev.get('owner')) or '(none)'} | TITLE {prev.get('title', DEFAULT_TITLE)}")
        for label, lst in (("Added", added), ("Updated", updated), ("Removed", removed)):
            if lst:
                print(f"  {label}: {', '.join(lst)}")
    else:
        reuse, todo = [], [s["name"] for s in raw["skills"]]
        print(f"NEW: all {len(todo)} skills need an entry.")
    json.dump(reuse, open(os.path.join(a.out_dir, "reuse.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(os.path.join(a.out_dir, "todo.txt"), "w", encoding="utf-8").write("\n".join(todo))
    print(f"TODO {len(todo)} -> {os.path.join(a.out_dir, 'todo.txt')}")


def normalize(e, raw_by):
    e = dict(e)
    if not e.get("display_name") and e.get("ko_name"):  # entries from the Korean edition
        e["display_name"] = e.pop("ko_name")
    for k in LISTS:
        v = e.get(k, [])
        if isinstance(v, str):
            v = [x.strip() for x in re.split(r"\s*(?:/|,|\n)\s*", v) if x.strip()]
        e[k] = v
    sit = e.get("situations") or []
    e["situations"] = [x for x in sit if isinstance(x, dict) and x.get("prompt")]
    r = raw_by.get(key(e.get("name")))
    if r:  # facts from the collection step win
        e["name"] = r["name"]
        e["hash"] = r["hash"]
        e["files"] = r["files"]
    if e.get("category") not in CATEGORY_ORDER:
        e["category"] = "Other" if not e.get("category") else e["category"]
    return e


def cmd_build(a):
    raw = load_json(a.raw)
    raw_by = {key(s["name"]): s for s in raw["skills"]}
    merged = {}
    for e in entries_from(a.data):
        merged[key(e.get("name"))] = e  # later files win
    problems, skills = [], []
    for s in raw["skills"]:
        e = merged.get(key(s["name"]))
        if not e:
            problems.append(f"MISSING {s['name']}: no entry was written")
            continue
        e = normalize(e, raw_by)
        miss = [k for k in REQUIRED if not str(e.get(k, "")).strip()]
        if miss:
            problems.append(f"INCOMPLETE {s['name']}: {', '.join(miss)} empty")
        skills.append(e)
    extra = sorted(merged[k].get("name", k) for k in set(merged) - set(raw_by))
    if extra:
        print("IGNORED (not installed): " + ", ".join(extra))
    if problems:
        print("\n".join(problems))
        if not a.force:
            sys.exit("BUILD_STOPPED: complete the skills above and run again (use --force to build anyway).")

    present = {s["category"] for s in skills}
    cats = [c for c in CATEGORY_ORDER if c in present] + sorted(present - set(CATEGORY_ORDER))
    skills.sort(key=lambda s: (cats.index(s["category"]), (s.get("display_name") or s["name"]).lower()))

    prev = extract_previous(a.previous) if a.previous else None
    owner = clean_owner(a.owner) if a.owner is not None else clean_owner((prev or {}).get("owner"))
    title = (a.title or "").strip() or (prev.get("title") if prev and a.owner is None else "") or (f"{owner}'s Skill Dashboard" if owner else DEFAULT_TITLE)
    data = {
        "title": title[:60],
        "owner": owner,
        "generated_at": a.date or datetime.date.today().isoformat(),
        "source": source_label(raw.get("root", "")),
        "maker_version": MAKER_VERSION,
        "categories": cats,
        "skills": skills,
    }
    if prev:
        added, removed, updated, _ = diff(raw, prev)
        data["changes"] = {"previous_date": prev.get("generated_at", ""), "added": added, "removed": removed, "updated": updated}

    tpl = open(a.template, encoding="utf-8").read()
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = tpl.replace("__SKILL_DATA__", payload).replace("__TITLE__", data["title"].replace("&", "&amp;").replace("<", "&lt;"))
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    open(a.out, "w", encoding="utf-8", newline="\n").write(html)
    print(f"BUILT {a.out}  '{data['title']}' · {len(skills)} skills · {len(cats)} categories · {round(len(html.encode('utf-8')) / 1024)}KB")
    if "changes" in data:
        c = data["changes"]
        print(f"  Changes: added {len(c['added'])} / updated {len(c['updated'])} / removed {len(c['removed'])}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan")
    p.add_argument("--raw", required=True)
    p.add_argument("--previous")
    p.add_argument("--out-dir", default="/tmp/skill-dashboard")
    b = sub.add_parser("build")
    b.add_argument("--raw", required=True)
    b.add_argument("--data", action="append", required=True)
    b.add_argument("--previous")
    b.add_argument("--owner", help="the user's name for the dashboard title (only a name the user gave)")
    b.add_argument("--title", help="only when the user gave the whole title")
    b.add_argument("--date")
    b.add_argument("--template", default=TEMPLATE)
    b.add_argument("--out", default="/mnt/user-data/outputs/skill-dashboard.html")
    b.add_argument("--force", action="store_true")
    a = ap.parse_args()
    {"plan": cmd_plan, "build": cmd_build}[a.cmd](a)


if __name__ == "__main__":
    main()
