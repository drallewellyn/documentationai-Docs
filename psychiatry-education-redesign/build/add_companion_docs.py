#!/usr/bin/env python3
"""Add the 7 taskforce 'companion documents' as reference rows in their natural sections."""
import pathlib, re
p = pathlib.Path(__file__).resolve().parent.parent / 'redesign-report.md'
t = p.read_text(encoding='utf-8')

t = t.replace('Version 7.2', 'Version 7.3')

new = {
1: [
 "| RANZCP. *Strategic Plan 2026–2030.* RANZCP; 2026 | [ranzcp.org](https://www.ranzcp.org) | The College strategy the Fellowship Program is accountable to (vision, priorities, values); the curriculum taskforce maps its Program Outcomes directly to these priorities. | RANZCP internal |",
],
3: [
 "| AMC. *Digital Health in Medicine Capability Framework.* Australian Medical Council; 2021 | [amc.org.au (PDF)](https://www.amc.org.au/wp-content/uploads/2021/08/Digital-Health-in-Medicine-Capability-Framework-FINAL-19-August-2021.pdf) | The cross-specialty baseline for digital-health and AI capabilities expected of all Australian medical specialists — the source for the curriculum's digital-health/AI content. | Regulatory/AMC |",
 "| RANZCP. *Victorian Psychiatry Leadership Framework.* RANZCP; 2024 | [ranzcp.org](https://www.ranzcp.org/news-analysis/victorian-psychiatrist-leadership-framework) | A psychiatry-specific leadership framework (developed after the Victorian Royal Commission) supplying detailed leadership competencies and developmental milestones for the curriculum's leadership strand. | RANZCP internal |",
],
8: [
 "| Standardised Supervisor Training System (SSTS) — national framework, RANZCP-modified | [ranzcp.org](https://www.ranzcp.org) | The structured supervisor-training program adopted (with RANZCP modifications) for psychiatric supervisor development — the backbone of faculty development for the redesign. | RANZCP internal |",
],
9: [
 "| RANZCP. *Code of Ethics* (current edition; revision in progress, 2026) | [ranzcp.org](https://www.ranzcp.org) | The College's ethical standards anchoring professional-identity and ethical-practice outcomes; the revision is expected to strengthen cultural safety, structural ethics and responsible use of emerging technologies. | RANZCP internal |",
],
10: [
 "| Council of Medical Colleges & Te ORA. *Cultural Safety Training Plan for Vocational Medicine in Aotearoa.* CMC/Te ORA; 2023 | [cmc.org.nz (PDF)](https://www.cmc.org.nz/media/4xmpx1dz/cultural-safety-training-plan-for-vocational-medicine-in-aotearoa.pdf) | A cross-college cultural-safety training, teaching and assessment framework — with a proficiency rubric and self-assessment tool for registrars and fellows — a ready template for embedding Māori cultural safety in the curriculum. | Regulatory/AMC |",
],
15: [
 "| A Better Culture. *A Better Culture Curriculum.* A Better Culture; 2025 | [abetterculture.org.au](https://abetterculture.org.au/news-resources/curriculum/) | A cross-specialty curriculum on workplace culture, psychological safety and respectful behaviour (consulted with all medical schools, the medical colleges and the AMC) — the basis for the program's workforce-wellbeing and psychological-safety content. | Theory |",
],
}

def insert(lines, sec, rows):
    hi = next(i for i,l in enumerate(lines) if l.startswith(f'## {sec}. '))
    ti = next(i for i in range(hi, len(lines)) if lines[i].lstrip().startswith('|'))
    j = ti
    while j < len(lines) and lines[j].lstrip().startswith('|'):
        j += 1
    return lines[:j] + rows + lines[j:]

lines = t.split('\n')
for sec, rows in new.items():
    lines = insert(lines, sec, rows)
t = '\n'.join(lines)
t = re.sub(r'\n{3,}', '\n\n', t)
p.write_text(t, encoding='utf-8')
print('done')
