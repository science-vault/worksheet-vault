#!/usr/bin/env python3
"""Index committed worksheets, retaining reviewed SCSA placements and cached previews."""
import collections,concurrent.futures,hashlib,json,re,subprocess,tempfile
from pathlib import Path
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[1]
UPLOADS=ROOT/'uploads'; OUTPUT=ROOT/'catalogue/worksheets.json'
EXTENSIONS={'.pdf','.doc','.docx','.txt','.rtf','.odt','.png','.jpg','.jpeg'}
META_FILE=ROOT/'catalogue/resource-metadata.json'
META=json.loads(META_FILE.read_text()) if META_FILE.exists() else {}
# Reviewed batches are additive so interrupted uploads retain their checkpoint.
for batch_metadata in sorted((ROOT/'catalogue/metadata-batches').glob('*.json')):
 META.update(json.loads(batch_metadata.read_text()))
# Descriptive display titles and downloaded filenames survive catalogue rebuilds.
NAMES_FILE=ROOT/'catalogue/resource-names.json'
if NAMES_FILE.exists():
 for path,naming in json.loads(NAMES_FILE.read_text()).items():
  if path in META and META[path].get('hash')==naming.get('hash'):
   META[path].update({k:naming[k] for k in ('title','downloadName')})
STOP=set('the and for are with this that from your you name date class worksheet what which how when where these they have will into using their each write answer answers students student page year science biological sciences question questions following below above activity sheet not can all has was were its use one two three www com https http org pdf doc school label labels john wiley sons australia workbook chapter copyright'.split())
def url(p):return '/'.join(quote(s,safe='') for s in p.relative_to(ROOT).parts)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()[:20]
def document_assets(p,h):
 assets=ROOT/'catalogue/previews';assets.mkdir(parents=True,exist_ok=True)
 pdf=p if p.suffix.lower()=='.pdf' else assets/(h+'.pdf');image=assets/(h+'.png')
 if p.suffix.lower() in {'.png','.jpg','.jpeg'}:
  if not pdf.exists():
   from PIL import Image
   Image.open(p).convert('RGB').save(pdf,'PDF',resolution=100)
 elif p.suffix.lower()!='.pdf' and not pdf.exists():
  with tempfile.TemporaryDirectory() as td:
   subprocess.run(['soffice','-env:UserInstallation=file://'+td+'/profile','--headless','--convert-to','pdf','--outdir',td,str(p)],check=True,capture_output=True,timeout=120)
   converted=Path(td)/(p.stem+'.pdf')
   if not converted.exists():raise RuntimeError('No PDF produced')
   pdf.write_bytes(converted.read_bytes())
 if not image.exists():subprocess.run(['pdftoppm','-f','1','-singlefile','-scale-to','700','-png',str(pdf),str(image.with_suffix(''))],check=True,capture_output=True,timeout=90)
 return dict(thumbnail=url(image),previewUrl=url(pdf))
def main():
 entries=[];failures=[];withheld=[]
 for p in sorted(UPLOADS.rglob('*'),key=lambda p:str(p).lower()):
  if not p.is_file()or p.suffix.lower()not in EXTENSIONS:continue
  path=p.relative_to(ROOT).as_posix();h=digest(p);m=META.get(path,{})
  valid=m.get('hash')==h
  if valid and m.get('included') is False:
   withheld.append(dict(path=path,reason=m.get('qualityNote','Excluded after review')))
   continue
  if not valid:
   withheld.append(dict(path=path,reason='New or changed upload awaiting content, usefulness and curriculum review.'))
   continue
  entries.append(dict(path=path,p=p,h=h,meta=m))
 groups=collections.defaultdict(list)
 for e in entries:groups[e['meta'].get('pairId',e['path'])].append(e)
 rows=[];matched=set()
 for e in entries:
  m=e['meta'];group=groups[m.get('pairId',e['path'])]
  students=[a for a in group if not a['meta'].get('isAnswer')]
  if m.get('isAnswer') and students:continue
  keys=[a for a in group if a['meta'].get('isAnswer')]
  answer=None
  if not m.get('isAnswer')and keys and m.get('answerPath'):
   preferred=m.get('answerPath')
   answer=next((k for k in keys if k['path']==preferred),None) or sorted(keys,key=lambda k:(k['p'].suffix.lower()!='.pdf',k['path']))[0]
   matched.add(answer['path'])
  text=m.get('searchText','')
  words=[w for w,c in collections.Counter(re.findall(r'[a-z]{4,}',text.lower())).most_common(120)if w not in STOP][:14]
  kws=list(dict.fromkeys(m.get('keywords',[])+words))[:32]
  rows.append(dict(id='github:'+e['path'],title=m['title']+(' - Answer Key'if m.get('isAnswer')else ''),publisher=m.get('publisher','Uncredited source'),publisherCategory=m.get('publisherCategory','Uncredited source'),resourceTypes=m.get('resourceTypes',['Worksheet']),reviewStatus=m.get('reviewStatus','Reviewed'),year=m.get('year','7–10'),years=m.get('years',[m.get('year','')]),area=m.get('area','Science'),subject=m.get('subject','Science'),pathway=m.get('pathway',''),unit=m.get('unit',''),strand=m.get('strand','Extra Worksheets'),topic=m.get('topic','Extra Worksheets'),supportingTopic=m.get('supportingTopic',''),collection=m.get('collection','extra'),description=m.get('description',''),keywords=kws,searchText=text[:60000],curriculumSource=m.get('curriculumSource',''),classificationNote=m.get('classificationNote',''),originalFilename=Path(m.get('originalPath',e['path'])).name,resourceType=m.get('resourceType','Worksheet'),worksheet=dict(name=m.get('downloadName',e['p'].name),url=url(e['p'])),answer=dict(name=answer['meta'].get('downloadName',answer['p'].name),url=url(answer['p']))if answer else None,source='github',_entry=e))
 def render(row):
  e=row.pop('_entry')
  try:row.update(document_assets(e['p'],e['h']))
  except Exception as exc:
   failures.append(dict(path=e['path'],error=str(exc)))
   row['previewError']='Preview unavailable; the original document can still be downloaded.'
  return row
 # Separate office profiles permit parallel conversion without locking a shared process.
 with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:rows=list(pool.map(render,rows))
 rows.sort(key=lambda r:(r['collection']=='extra',int(r['year'])if r['year'].isdigit()else 99,r['strand'],r['title'].lower()))
 OUTPUT.parent.mkdir(exist_ok=True,parents=True);OUTPUT.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
 (ROOT/'catalogue/preview-status.json').write_text(json.dumps(dict(worksheets=len(rows),linkedAnswerKeys=len(matched),failures=failures,withheldFiles=len(withheld)),indent=2)+'\n')
 (ROOT/'catalogue/withheld-resources.json').write_text(json.dumps(dict(files=withheld),ensure_ascii=False,indent=2)+'\n')
 # Mark a batch complete only after every catalogue preview has validated.
 if not failures:
  progress_path=ROOT/'catalogue/upload-progress.json'
  if progress_path.exists():
   progress=json.loads(progress_path.read_text())
   completed={b['batch'] for b in progress.get('completedBatches',[])}
   for report_path in sorted((ROOT/'catalogue/batches').glob('batch-*.json')):
    report=json.loads(report_path.read_text())
    if report['batch'] in completed:continue
    previous=progress['catalogueCount']
    summary={k:report[k] for k in ('batch','processedFiles','includedFiles','excludedFiles')}
    summary.update(addedCatalogueEntries=len(rows)-previous,catalogueCount=len(rows))
    progress['completedBatches'].append(summary)
    progress['processedFiles']+=report['processedFiles']
    progress['remainingFiles']=max(0,progress['pendingAtStart']-progress['processedFiles'])
    progress['catalogueCount']=len(rows)
    report.update(summary,status='completed-preview-validated')
    report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    completed.add(report['batch'])
   progress_path.write_text(json.dumps(progress,indent=2)+'\n')
 print(f'Indexed {len(rows)} resources; linked {len(matched)} answer files; {len(failures)} preview failures')
 if failures:raise SystemExit('Preview failures recorded in catalogue/preview-status.json; fix before publishing')
if __name__=='__main__':main()
