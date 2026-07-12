#!/usr/bin/env python3
# Convert a user-edited .docx back into redesign-report.md (their version becomes the source).
import zipfile, re, sys, pathlib
import xml.etree.ElementTree as ET

W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
R='{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'

path = sys.argv[1]
z = zipfile.ZipFile(path)
rels = {}
rroot = ET.fromstring(z.read('word/_rels/document.xml.rels'))
for rel in rroot:
    rels[rel.get('Id')] = rel.get('Target')
root = ET.fromstring(z.read('word/document.xml'))
body = root.find(W+'body')

def label_for(url):
    u = url
    if 'doi.org/' in u: return 'doi'
    if 'pubmed' in u: return 'pubmed'
    if 'cambridge.org' in u: return 'cambridge'
    if 'amc.org.au' in u: return 'amc.org.au (PDF)' if u.lower().endswith('.pdf') else 'amc.org.au'
    if 'royalcollege.ca' in u: return 'royalcollege.ca'
    if 'acgme.org' in u: return 'acgme.org'
    if 'niaa.gov.au' in u: return 'niaa.gov.au'
    if 'mentalhealth.inquiry' in u: return 'mentalhealth.inquiry.govt.nz'
    if 'wgtn.ac.nz' in u: return 'VUW repository'
    if 'ranzcp.org' in u: return 'ranzcp.org'
    host = re.sub(r'^https?://','',u).split('/')[0]
    return host

def run_fmt(r):
    rpr = r.find(W+'rPr')
    def on(tag):
        e = rpr.find(W+tag) if rpr is not None else None
        return e is not None and e.get(W+'val') not in ('0', 'false')
    return on('b'), on('i')

def inline(el, header=False):
    segs = []
    for child in el:
        tag = child.tag.split('}')[-1]
        if tag == 'r':
            t = ''.join(x.text or '' for x in child.iter(W+'t'))
            if t == '': continue
            b, i = run_fmt(child)
            if header: b = i = False
            segs.append([t, b, i, None])
        elif tag == 'hyperlink':
            url = rels.get(child.get(R+'id'), '')
            disp = ''.join(x.text or '' for x in child.iter(W+'t'))
            segs.append([disp, False, False, url or None])
    merged = []
    for s in segs:
        if merged and s[3] is None and merged[-1][3] is None and merged[-1][1] == s[1] and merged[-1][2] == s[2]:
            merged[-1][0] += s[0]
        else:
            merged.append(s)
    out = []
    for t, b, i, url in merged:
        if url is not None:
            out.append(f'[{label_for(url)}]({url})')
        else:
            x = t
            if b: x = f'**{x}**'
            elif i: x = f'*{x}*'
            out.append(x)
    return ''.join(out).strip()

STYLE_PREFIX = {'Title':'# ','Heading1':'## ','Heading2':'### ','Heading3':'#### ','Heading4':'##### '}

out = []
def emit(s=''):
    out.append(s)

for el in body:
    tag = el.tag.split('}')[-1]
    if tag == 'p':
        ppr = el.find(W+'pPr')
        style = None
        if ppr is not None:
            ps = ppr.find(W+'pStyle')
            if ps is not None: style = ps.get(W+'val')
        text = inline(el)
        has_border = ppr is not None and ppr.find(W+'pBdr') is not None
        if text == '':
            if has_border:
                emit(''); emit('---'); emit('')
            else:
                emit('')
            continue
        if style in STYLE_PREFIX:
            emit(''); emit(STYLE_PREFIX[style] + text); emit('')
        elif style == 'Quote':
            emit('> ' + text)
        else:
            if text.startswith('•'):
                emit('- ' + text.lstrip('•').strip())
            elif re.match(r'^\d+\.\s', text):
                emit(text)
            else:
                emit(text); emit('')
    elif tag == 'tbl':
        rows = el.findall(W+'tr')
        emit('')
        for ri, tr in enumerate(rows):
            tcs = tr.findall(W+'tc')
            cells = []
            for tc in tcs:
                ptexts = [inline(p, header=(ri == 0)) for p in tc.findall(W+'p')]
                cells.append(' '.join(t for t in ptexts if t))
            emit('| ' + ' | '.join(cells) + ' |')
            if ri == 0:
                emit('|' + '|'.join(['---'] * len(cells)) + '|')
        emit('')

md = '\n'.join(out)
md = re.sub(r'\n{3,}', '\n\n', md).strip() + '\n'
outp = pathlib.Path(__file__).resolve().parent.parent / 'redesign-report.md'
outp.write_text(md, encoding='utf-8')
print('wrote', outp, len(md), 'chars')
