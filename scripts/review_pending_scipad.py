#!/usr/bin/env python3
"""Check recently uploaded sciPAD PDFs and group each student page with its key.

Unmatched NZ course content stays in Extra Worksheets without an invented WA year.
"""
import concurrent.futures
import hashlib
import json
import re
import subprocess
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'uploads/science/Scipad'
BATCH = ROOT / 'catalogue/metadata-batches/scipad-other-reviewed-2026-11-21.json'

def pair_key(path):
    parts = path.relative_to(SOURCE).parts
    if parts[-2] in ('Answers', 'Worksheets'):
        stem = re.sub(r'\s*-\s*(?:Answers|Answer Key|Worksheet)\.pdf$', '', parts[-1], flags=re.I)
        return ('/'.join(parts[:-2]), stem)
    return ('/'.join(parts[:-1]), parts[-2])

def inspect(path, partner):
    raw = path.read_bytes()
    if not raw.startswith(b'%PDF-'):
        raise ValueError(f'Invalid PDF: {path}')
    read = subprocess.run(['pdftotext','-f','1','-l','2',str(path),'-'], capture_output=True, text=True, timeout=45)
    if read.returncode:
        raise ValueError(f'PDF could not be read: {path}')
    body = ' '.join(read.stdout.split())
    if len(body) < 30:
        raise ValueError(f'Insufficient readable content: {path}')
    rel = path.relative_to(ROOT).as_posix()
    is_answer = path.parent.name == 'Answers' or path.stem.endswith('Answer Key')
    stem = re.sub(r'^\d+\s*-\s*', '', path.stem)
    title = re.sub(r'\s*-\s*(?:Answers|Answer Key|Worksheet)$', '', stem, flags=re.I).strip()
    group = path.relative_to(SOURCE).parts[0]
    subject = 'Biology' if 'Biology' in group or group == 'Genetics' else 'Chemistry' if 'Chemistry' in group else 'Physics' if 'Physics' in group or group == 'Mechanics' else 'Science'
    topic = re.sub(r'^\d+\s*-\s*', '', group).replace(' External','').replace(' Internal','')
    pair = '/'.join(pair_key(path))
    return rel, dict(originalPath=rel, hash=hashlib.sha256(raw).hexdigest()[:20],
        reviewDate=str(date.today()),reviewStatus='PDF checked; extra resource',included=True,
        searchText=body[:1400],year='',years=[],area='Science',subject=subject,
        strand='Extra Worksheets',topic=topic,supportingTopic=topic,collection='extra',
        keywords=[title,topic,'sciPAD',subject],classificationNote='NZ sciPAD course resource; WA SCSA year placement not confirmed.',
        title=title,publisher='sciPAD',publisherCategory='Commercial publisher',
        resourceTypes=['Worksheet'],resourceType='Worksheet',isAnswer=is_answer,
        pairId=pair,answerPath=partner.relative_to(ROOT).as_posix() if not is_answer else '',
        downloadName=f'{title} - '+('Answer Key' if is_answer else 'Worksheet')+'.pdf')

def main():
    reviewed = json.loads(BATCH.read_text()) if BATCH.exists() else {}
    existing = set(json.loads((ROOT/'catalogue/resource-metadata.json').read_text()))
    for batch in (ROOT/'catalogue/metadata-batches').glob('*.json'):
        existing.update(json.loads(batch.read_text()))
    paths = sorted(p for p in SOURCE.rglob('*.pdf') if p.relative_to(ROOT).as_posix() not in existing)
    if not paths:
        print(f'No new sciPAD PDFs; kept {len(reviewed)} existing reviews')
        return
    groups = {}
    for path in paths:
        groups.setdefault(pair_key(path), []).append(path)
    unmatched = {str(k): [str(p) for p in v] for k,v in groups.items() if len(v)!=2}
    if unmatched:
        raise ValueError(f'{len(unmatched)} groups do not have exactly one worksheet and answer: {list(unmatched.items())[:3]}')
    work = [(p,next(x for x in groups[pair_key(p)] if x!=p)) for p in paths]
    new_reviews = {}
    rejected = set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        tasks = {pool.submit(inspect,*pair): pair[0] for pair in work}
        for task in concurrent.futures.as_completed(tasks):
            try:
                key, value = task.result()
                new_reviews[key] = value
            except (ValueError,subprocess.TimeoutExpired) as error:
                rejected.add(pair_key(tasks[task]))
                print(f'Withholding unreadable pair: {error}')
    for key in rejected:
        for path in groups[key]:
            new_reviews.pop(path.relative_to(ROOT).as_posix(), None)
    reviewed.update(new_reviews)
    BATCH.write_text(json.dumps(reviewed,ensure_ascii=False,indent=2)+'\n')
    print(f'Reviewed {len(new_reviews)//2} new pairs; withheld {len(rejected)} unreadable pairs; saved {BATCH.name}')

if __name__=='__main__':main()
