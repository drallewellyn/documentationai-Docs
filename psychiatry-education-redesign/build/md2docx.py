#!/usr/bin/env python3
# Markdown -> .docx (OOXML, no external deps). DOIs shown as visible, clickable text.
import re, zipfile, pathlib

def esc(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def esca(s):
    return esc(s).replace('"','&quot;')

def link_display(url):
    u = url.strip()
    if 'doi.org/' in u:
        return 'doi:' + u.split('doi.org/', 1)[1]
    return re.sub(r'^https?://', '', u)

EMPH_RE = re.compile(r'(`[^`]+`)|(\*\*[^*]+\*\*)|(\*[^*]+\*)')
LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

def parse_emph(text):
    runs = []; pos = 0
    for m in EMPH_RE.finditer(text):
        if m.start() > pos:
            runs.append({'text': text[pos:m.start()]})
        tok = m.group(0)
        if tok.startswith('`'):
            runs.append({'text': tok[1:-1], 'code': True})
        elif tok.startswith('**'):
            runs.append({'text': tok[2:-2], 'b': True})
        else:
            runs.append({'text': tok[1:-1], 'i': True})
        pos = m.end()
    if pos < len(text):
        runs.append({'text': text[pos:]})
    return [r for r in runs if r.get('text', '') != '']

def parse_inline(text):
    parts = []; pos = 0
    for m in LINK_RE.finditer(text):
        if m.start() > pos:
            parts.extend(parse_emph(text[pos:m.start()]))
        parts.append({'link': m.group(2)})
        pos = m.end()
    if pos < len(text):
        parts.extend(parse_emph(text[pos:]))
    return parts

class Rels:
    def __init__(self):
        self.items = {}; self.order = []; self.next = 1000
    def add(self, url):
        if url in self.items:
            return self.items[url]
        rid = f'rId{self.next}'; self.next += 1
        self.items[url] = rid; self.order.append((rid, url))
        return rid

def run(text, b=False, i=False, code=False, hyper=False, size=None):
    props = ''
    if hyper: props += '<w:rStyle w:val="Hyperlink"/>'
    if b: props += '<w:b/>'
    if i: props += '<w:i/>'
    if code: props += '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/>'
    if size: props += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    rpr = f'<w:rPr>{props}</w:rPr>' if props else ''
    return f'<w:r>{rpr}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>'

def runs_xml(parts, rels, size=None):
    out = []
    for p in parts:
        if 'link' in p:
            rid = rels.add(p['link'])
            out.append(f'<w:hyperlink r:id="{rid}">' + run(link_display(p['link']), hyper=True, size=size) + '</w:hyperlink>')
        else:
            out.append(run(p['text'], b=p.get('b'), i=p.get('i'), code=p.get('code'), size=size))
    if not out:
        out.append(run('', size=size))
    return ''.join(out)

def cells(l):
    l = l.strip()
    if l.startswith('|'): l = l[1:]
    if l.endswith('|'): l = l[:-1]
    return [c.strip() for c in l.split('|')]

def col_weights(header):
    nc = len(header); h = ' '.join(header).lower()
    if nc == 4 and 'what it tells us' in h:
        return (30, 13, 45, 12)
    if nc == 4:
        return (30, 14, 44, 12)
    return tuple([1] * nc)

TOTAL_TW = 9600
HEAD_MAP = {1: 'Title', 2: 'Heading1', 3: 'Heading2', 4: 'Heading3', 5: 'Heading4', 6: 'Heading4'}
BORDER = ('<w:tblBorders>'
          + ''.join(f'<w:{s} w:val="single" w:sz="4" w:space="0" w:color="B9A7CC"/>'
                    for s in ['top','left','bottom','right','insideH','insideV'])
          + '</w:tblBorders>')

def table_xml(header, rows, rels):
    weights = col_weights(header); s = sum(weights)
    tw = [round(w / s * TOTAL_TW) for w in weights]
    grid = '<w:tblGrid>' + ''.join(f'<w:gridCol w:w="{w}"/>' for w in tw) + '</w:tblGrid>'
    def cell(content, w, header=False):
        shd = '<w:shd w:val="clear" w:color="auto" w:fill="EFE9F4"/>' if header else ''
        parts = parse_inline(content)
        if header:
            for p in parts:
                if 'link' not in p: p['b'] = True
        body = '<w:p><w:pPr><w:spacing w:before="20" w:after="20" w:line="240" w:lineRule="auto"/></w:pPr>' + runs_xml(parts, rels, size=17) + '</w:p>'
        return f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>{shd}</w:tcPr>{body}</w:tc>'
    out = [f'<w:tbl><w:tblPr><w:tblW w:w="{TOTAL_TW}" w:type="dxa"/>{BORDER}<w:tblLook w:firstRow="1"/></w:tblPr>{grid}']
    out.append('<w:tr><w:trPr><w:tblHeader/></w:trPr>' + ''.join(cell(c, tw[j], True) for j, c in enumerate(header)) + '</w:tr>')
    for row in rows:
        row = (row + [''] * len(header))[:len(header)]
        out.append('<w:tr>' + ''.join(cell(c, tw[j]) for j, c in enumerate(row)) + '</w:tr>')
    out.append('</w:tbl><w:p/>')
    return ''.join(out)

def para(parts_xml, style=None, ind=None, extra_ppr=''):
    ppr = ''
    if style: ppr += f'<w:pStyle w:val="{style}"/>'
    if ind: ppr += f'<w:ind w:left="{ind}"/>'
    ppr += extra_ppr
    ppr = f'<w:pPr>{ppr}</w:pPr>' if ppr else ''
    return f'<w:p>{ppr}{parts_xml}</w:p>'

def build_body(md, rels):
    lines = md.split('\n'); i, n = 0, len(lines); out = []
    while i < n:
        line = lines[i]
        if line.lstrip().startswith('|') and i+1 < n and re.match(r'\s*\|?[\s:|-]+\|[\s:|-]*$', lines[i+1]) and '-' in lines[i+1]:
            header = cells(line); i += 2; rows = []
            while i < n and lines[i].lstrip().startswith('|'):
                rows.append(cells(lines[i])); i += 1
            out.append(table_xml(header, rows, rels)); continue
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            out.append(para(runs_xml(parse_inline(m.group(2)), rels), style=HEAD_MAP[len(m.group(1))])); i += 1; continue
        if re.match(r'^\s*---+\s*$', line):
            out.append('<w:p><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="4" w:space="1" w:color="CCCCCC"/></w:pBdr></w:pPr></w:p>'); i += 1; continue
        if re.match(r'^\s*>\s?', line):
            buf = []
            while i < n and re.match(r'^\s*>\s?', lines[i]):
                buf.append(re.sub(r'^\s*>\s?', '', lines[i])); i += 1
            txt = ' '.join(b for b in buf if b.strip())
            out.append(para(runs_xml(parse_inline(txt), rels), style='Quote')); continue
        lm = re.match(r'^(\s*)([-*]|\d+\.)\s+(.*)$', line)
        if lm:
            indent = 360 + (360 if len(lm.group(1)) >= 2 else 0)
            bullet = '•  ' if not re.match(r'\d+\.', lm.group(2)) else lm.group(2) + '  '
            inner = run(bullet) + runs_xml(parse_inline(lm.group(3)), rels)
            out.append(para(inner, ind=indent)); i += 1; continue
        if line.strip() == '':
            i += 1; continue
        buf = [line]; i += 1
        while i < n and lines[i].strip() != '' and not re.match(r'^(#{1,6}\s|\s*[-*]\s|\s*\d+\.\s|\s*>|\s*\|)', lines[i]) and not re.match(r'^\s*---+\s*$', lines[i]):
            buf.append(lines[i]); i += 1
        out.append(para(runs_xml(parse_inline(' '.join(b.strip() for b in buf)), rels)))
    return ''.join(out)

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="259" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:after="200"/></w:pPr><w:rPr><w:b/><w:color w:val="5B2A86"/><w:sz w:val="40"/><w:szCs w:val="40"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="240" w:after="80"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:color w:val="5B2A86"/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="200" w:after="60"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:color w:val="5B2A86"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="160" w:after="40"/><w:outlineLvl w:val="2"/></w:pPr><w:rPr><w:b/><w:color w:val="404040"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading4"><w:name w:val="heading 4"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="120" w:after="40"/><w:outlineLvl w:val="3"/></w:pPr><w:rPr><w:b/><w:color w:val="404040"/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Quote"><w:name w:val="Quote"/><w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:ind w:left="288"/><w:spacing w:before="60" w:after="60"/></w:pPr><w:rPr><w:i/><w:color w:val="595959"/></w:rPr></w:style>
<w:style w:type="character" w:styleId="Hyperlink"><w:name w:val="Hyperlink"/><w:rPr><w:color w:val="0563C1"/><w:u w:val="single"/></w:rPr></w:style>
</w:styles>'''

CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

base = pathlib.Path(__file__).resolve().parent.parent
md = (base / 'redesign-report.md').read_text(encoding='utf-8')
rels = Rels()
body = build_body(md, rels)
sectpr = '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="709" w:footer="709" w:gutter="0"/></w:sectPr>'
document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            f'<w:body>{body}{sectpr}</w:body></w:document>')
doc_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
            + ''.join(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target="{esca(url)}" TargetMode="External"/>'
                      for rid, url in rels.order)
            + '</Relationships>')

outp = base / 'build' / 'RANZCP-Psychiatry-Training-Redesign-Sectioned-Evidence-Report.docx'
outp.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(outp, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', CONTENT_TYPES)
    z.writestr('_rels/.rels', RELS)
    z.writestr('word/document.xml', document)
    z.writestr('word/styles.xml', STYLES)
    z.writestr('word/_rels/document.xml.rels', doc_rels)
print('wrote', outp, 'with', len(rels.order), 'hyperlinks')
