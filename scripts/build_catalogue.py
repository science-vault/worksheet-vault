#!/usr/bin/env python3
"""Build the public Worksheet Vault catalogue from committed files."""
import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
UPLOADS = ROOT / "uploads"
OUTPUT = ROOT / "catalogue" / "worksheets.json"
EXTENSIONS = {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"}
KEY_WORDS = re.compile(r"(?i)(?:^|[\s_.-])(answer(?:s)?|answer[\s_-]*key|marking[\s_-]*key|solutions?|memo)(?:$|[\s_.-])")
KEY_FOLDERS = {"answer-keys", "answer_keys", "answers", "marking-keys", "solutions"}
IGNORE = {"worksheets", "answer-keys", "answer_keys", "answers", "marking-keys", "solutions"}

def human(s):
    return re.sub(r"[-_]+", " ", s).strip().title()

def clean_stem(s):
    s = re.sub(r"(?i)\b(answer(?:s)?|key|marking|solution(?:s)?|memo|teacher|student|worksheet|ws)\b", " ", s)
    return re.sub(r"[^a-z0-9]+", "", s.lower())

def url(path):
    return "/".join(quote(part, safe="") for part in path.relative_to(ROOT).parts)

def classify(path):
    parts = path.relative_to(UPLOADS).parts
    dirs = list(parts[:-1])
    year = next((m.group(1) for d in dirs if (m := re.fullmatch(r"year-(7|8|9|10|11|12)", d.lower()))), "")
    senior = "senior-secondary" in dirs
    if senior:
        i = dirs.index("senior-secondary")
        pathway = human(dirs[i+2]) if len(dirs)>i+2 else ""
        area = human(dirs[i+3]) if len(dirs)>i+3 else ""
        subject = human(dirs[i+4]) if len(dirs)>i+4 else area
        tail = dirs[i+5:]
    else:
        i = next((j for j,d in enumerate(dirs) if re.fullmatch(r"year-(7|8|9|10)",d.lower())), -1)
        if i >= 0:
            area = human(dirs[0]) if i >= 1 else ""
            subject = human(dirs[i-1]) if i >= 2 else area
            tail = dirs[i+1:]
        else:
            area = human(dirs[0]) if dirs else ""
            subject = area
            tail = dirs[1:]
        pathway = ""
    tail = [x for x in tail if x.lower() not in IGNORE]
    strand = human(tail[0]) if tail else "General"
    topic = human(tail[-1]) if len(tail)>1 else strand
    return dict(year=year, area=area, subject=subject, pathway=pathway, strand=strand, topic=topic)

def main():
    files = sorted((p for p in UPLOADS.rglob("*") if p.is_file() and p.suffix.lower() in EXTENSIONS), key=lambda p: str(p).lower())
    keys, worksheets = [], []
    for p in files:
        is_key = any(d.lower() in KEY_FOLDERS for d in p.parts) or bool(KEY_WORDS.search(p.stem))
        (keys if is_key else worksheets).append(p)
    matched = set()
    rows = []
    for p in worksheets:
        meta = classify(p)
        candidates = []
        for k in keys:
            if k in matched: continue
            km = classify(k)
            if (meta["year"],meta["subject"],meta["strand"]) != (km["year"],km["subject"],km["strand"]): continue
            if clean_stem(p.stem) and clean_stem(p.stem)==clean_stem(k.stem):
                candidates.append(k)
        answer = candidates[0] if len(candidates)==1 else None
        if answer: matched.add(answer)
        rows.append({
            "id": "github:" + p.relative_to(ROOT).as_posix(),
            "title": p.stem.replace("_"," ").strip(),
            **meta,
            "description": "",
            "worksheet": {"name":p.name, "url":url(p)},
            "answer": {"name":answer.name,"url":url(answer)} if answer else None,
            "source": "github"
        })
    # Standalone answer keys remain unlinked until a confident match is found.
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"Indexed {len(rows)} worksheets; matched {len(matched)} answer keys; {len(keys)-len(matched)} unmatched keys")

if __name__ == "__main__":
    main()
