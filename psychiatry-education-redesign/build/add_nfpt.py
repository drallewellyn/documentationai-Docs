#!/usr/bin/env python3
import pathlib, re
p = pathlib.Path(__file__).resolve().parent.parent / 'redesign-report.md'
t = p.read_text(encoding='utf-8')

# version bump + legend
t = t.replace('Version 6.0', 'Version 7.0')
t = t.replace(
 '**Version 7.0 — 17 June 2026**',
 '**Version 7.0 — 17 June 2026**\n\n*★ marks references newly added from the NFPT (Dean’s) literature review — flagged for your review.*')

R = '★ '  # new-paper marker

new = {
1: [
 f"| {R}Jurd et al. Introducing a competency based Fellowship programme for psychiatry in Australia and New Zealand. *Australas Psychiatry.* 2015;23(6):699–705 | [doi](https://doi.org/10.1177/1039856215600898) | The foundational RANZCP paper introducing the competency-based Fellowship program — the local origin of the CBF/EPA model now being redesigned. | Theory |",
 f"| {R}Alharbi. Evaluating competency-based medical education: a systematized review of current practices. *BMC Med Educ.* 2024;24:612 | [doi](https://doi.org/10.1186/s12909-024-05609-6) | A systematized review of how CBME is actually implemented internationally — a stocktake of current practice. | Evidence |",
],
3: [
 f"| {R}Schwartzstein et al. The Harvard Medical School Pathways Curriculum. *Acad Med.* 2020;95(11):1687–1695 | [doi](https://doi.org/10.1097/ACM.0000000000003270) | A worked example of redesigning a curriculum for contemporary learners — developmentally staged and integrated. | Theory |",
 f"| {R}Ellaway, Wyatt, Kelly. Grim fairy tales of curriculum change in medical education. *Med Educ.* 2026;60(1):25–27 | [doi](https://doi.org/10.1111/medu.15681) | A cautionary reflection on how curriculum-change efforts founder — a standing warning on implementation risk. | Theory |",
 f"| {R}Mark, Poole, Agrawal. Integration of neuroscience into psychiatric training and practice. *BJPsych Bull.* 2025;49(4):278–284 | [doi](https://doi.org/10.1192/bjb.2024.24) *(confirm pages)* | Argues for embedding contemporary neuroscience in the psychiatry curriculum — a content-scope decision. | Theory |",
 f"| {R}Kerr et al. Unpacking neuropsychiatry and behavioural neurology training: scoping review. *BJPsych Bull.* 2025 *(online-first)* | [doi](https://doi.org/10.1192/bjb.2025.10184) | Scoping review of neuropsychiatry syllabus components — a subspecialty content gap. | Evidence |",
 f"| {R}Costello et al. A national survey of neuropsychiatry training experiences. *BJPsych Bull.* 2025 *(online-first)* | [doi](https://doi.org/10.1192/bjb.2025.34) | Survey evidence of neuropsychiatry training gaps. | Evidence |",
 f"| {R}Evans et al. 'See one, do one, teach one': leadership and management training in Australian medical curricula. *Australas Psychiatry.* 2022;30(1):136 | [doi](https://doi.org/10.1177/10398562211029949) | Argues leadership and management belong in the curriculum, not only clinical skills. | Theory |",
 f"| {R}Till, Sen, Crimlisk. Psychiatric leadership development in postgraduate medical education and training. *BJPsych Bull.* 2022;46(3):174–181 | [doi](https://doi.org/10.1192/bjb.2021.32) | Psychiatry-specific leadership development across training. | Theory |",
],
4: [
 f"| {R}Blamey et al. Simulated virtual on-call training programme… out-of-hours psychiatry. *BJPsych Bull.* 2023;47(5):287–295 | [doi](https://doi.org/10.1192/bjb.2022.40) | Simulation improves junior doctors' confidence in psychiatry — evidence for simulation-based teaching. | Evidence |",
 f"| {R}Hewson, Foster, Sanderson. Socially distanced and online simulation training… psychiatry. *BJPsych Bull.* 2023;47(4):235–241 | [doi](https://doi.org/10.1192/bjb.2022.18) | Online/distanced simulation for psychiatry trainees — a delivery-mode option. | Evidence |",
 f"| {R}Gill et al. 'I, robot, can help you': generative AI in RANZCP psychiatry training. *Australas Psychiatry.* 2025;33(4) | [doi](https://doi.org/10.1177/10398562251344470) *(confirm pages)* | RANZCP-specific survey of generative-AI applications in psychiatry training. | Evidence |",
 f"| {R}Gauld et al. AI-generated visualisations to improve teaching of psychiatric symptom characterisation. *Br J Psychiatry.* 2025 *(online)* | [doi](https://doi.org/10.1192/bjp.2025.10464) | An AI teaching tool for symptom characterisation. | Evidence |",
],
5: [
 f"| {R}van der Vleuten et al. A model for programmatic assessment fit for purpose. *Med Teach.* 2012;34(3):205–214 | [doi](https://doi.org/10.3109/0142159X.2012.652239) | The operational model of programmatic assessment (its guidelines) — the design template for the CCPR. | Theory |",
 f"| {R}Schuwirth & van der Vleuten. Programmatic assessment: from assessment of learning to assessment for learning. *Med Teach.* 2011;33(6):478–485 | [doi](https://doi.org/10.3109/0142159X.2011.565828) | The paradigm shift (of→for learning) underpinning programmatic assessment. | Theory |",
 f"| {R}Harris et al. (ICBME). Evolving concepts of assessment in a competency-based world. *Med Teach.* 2017;39(6):603–608 | [doi](https://doi.org/10.1080/0142159X.2017.1315071) | The international CBME consensus on how assessment must change. | Theory |",
 f"| {R}Holmboe et al. The role of assessment in competency-based medical education. *Med Teach.* 2010;32(8):676–682 | [pubmed](https://pubmed.ncbi.nlm.nih.gov/20662580/) | A foundational statement on assessment's role in CBME. | Theory |",
 f"| {R}Cook & Lineberry. Consequences validity evidence: evaluating the impact of educational assessments. *Acad Med.* 2016;91(6):785–795 | [doi](https://doi.org/10.1097/ACM.0000000000001114) | Extends Kane: the *consequences* of an assessment are part of its validity — central when adding or removing high-stakes exams. | Theory |",
 f"| {R}Sidhu & Fleming. Re-examining single-moment-in-time high-stakes examinations in specialist training: a critical narrative review. *Med Teach.* 2024;46(4):528–536 | [doi](https://doi.org/10.1080/0142159X.2023.2260081) | A critique of single-moment high-stakes exams — supports the OSCE→portfolio shift. | Theory |",
 f"| {R}Ryan et al. How well do workplace-based assessments support summative entrustment decisions? A multi-institutional generalisability study. *Med Educ.* 2024;58(7):825–837 | [doi](https://doi.org/10.1111/medu.15291) | Empirical: how reliably WBAs support entrustment decisions — the rigour question for the CCPR. | Evidence |",
 f"| {R}Rietmeijer, Watling, Teunissen. Rethinking workplace-based assessment: the costly illusion of authenticity. *Acad Med.* 2025 | [pubmed](https://pubmed.ncbi.nlm.nih.gov/40680201/) *(DOI to confirm)* | Challenges the assumption that WBA is inherently 'authentic' — a caution for portfolio assessment. | Theory |",
 f"| {R}Bhanji et al. Competence by Design: the role of high-stakes examinations in a CBME system. *Perspect Med Educ.* 2024;13(1):68–74 | [doi](https://doi.org/10.5334/pme.965) | Argues high-stakes exams retain a defensible role within CBME — a counterpoint to wholesale OSCE removal. | Theory |",
 f"| {R}Pearce & Prideaux. When I say … programmatic assessment in postgraduate medical education. *Med Educ.* 2019;53(11):1074–1076 | [doi](https://doi.org/10.1111/medu.13949) | A concise conceptual primer on programmatic assessment (companion to Pearce's 'assessment burden'). | Theory |",
],
6: [
 f"| {R}Phinney et al. Beyond checking boxes: tensions with a workplace-based assessment tool for formative assessment in clerkships. *Acad Med.* 2022;97(10):1511–1520 | [doi](https://doi.org/10.1097/ACM.0000000000004774) | Trainee/faculty tensions with WBA tools — the 'tick-box' problem in practice. | Evidence |",
],
7: [
 f"| {R}Atkinson, Watling, Brand. Feedback and coaching. *Eur J Pediatr.* 2022;181(2):441–446 | [doi](https://doi.org/10.1007/s00431-021-04118-8) | A concise, practical account of reframing feedback as coaching. | Theory |",
],
9: [
 f"| {R}Seth et al. The impact of coaching on professional identity development in postgraduate medical trainees: a scoping review. *Med Educ.* 2025 *(online-first)* | [doi](https://doi.org/10.1111/medu.70106) | Scoping review linking coaching to professional identity formation. | Evidence |",
],
10: [
 f"| {R}Rousseau, Gomez-Carrillo, Cénat. Safe enough? Rethinking the concept of cultural safety in healthcare and training. *Br J Psychiatry.* 2022;221(4):587–588 | [doi](https://doi.org/10.1192/bjp.2022.102) | An editorial rethinking what 'cultural safety' should mean — critical framing for the redesign. | Theory |",
 f"| {R}Newton-Howes et al. Does a comprehensive service user-led education programme…? (comparative cohort study). *ANZJP.* 2021;55(9):903–910 | [doi](https://doi.org/10.1177/0004867420987886) | Evidence that lived-experience (service-user-led) education shifts trainee attitudes toward recovery. | Evidence |",
 f"| {R}Ahir-Knight et al. Growing the lived experience voice in psychiatry education and research. *ANZJP.* 2024;58(10):825–828 | [doi](https://doi.org/10.1177/00048674241274278) | An academic department's journey embedding lived experience in education. | Evidence |",
 f"| {R}Leandre, Diaz-Fernandez, Ginory. Are medical students and residents receiving an appropriate education on LGBTQ+ health? *ANZJP.* 2021;55(4):426–427 | [doi](https://doi.org/10.1177/0004867420982069) | Flags LGBTQ+ health as an under-taught equity gap. | Evidence |",
 f"| {R}Stanyon et al. Diversity in psychiatry education and patient and public involvement: roundtable analysis. *BJPsych Bull.* 2025 *(DOI to confirm)* | [cambridge](https://www.cambridge.org/core/journals/bjpsych-bulletin/article/diversity-in-psychiatry-education-and-patient-and-public-involvement-roundtable-analysis/D74B4267ED05AB473F10E9B70BE39554) | Diversity and public involvement in psychiatry education. | Theory |",
 f"| {R}Prashar, Schulze, Furlano. Addressing disparities in eating disorders… training deficiencies among males and men. *Br J Psychiatry.* 2026;228(1) | [doi](https://doi.org/10.1192/bjp.2025.70) *(confirm pages)* | An equity/training-gap example (men and eating disorders). | Theory |",
 f"| {R}Chang et al. The Pasifika Veilomani Project: a pilot online training programme… *Australas Psychiatry.* 2022;30(6):762–767 | [doi](https://doi.org/10.1177/10398562211045090) | A Pacific/Pasifika-specific, culturally-adapted training programme. | Evidence |",
],
11: [
 f"| {R}Vara et al. Developing a culturally informed telepsychiatry competency framework for Aotearoa New Zealand. *Australas Psychiatry.* 2025;33(6):902–908 | [doi](https://doi.org/10.1177/10398562251345313) | A culturally-informed competency framework for Aotearoa New Zealand — directly relevant to embedding cultural safety in the curriculum. | Evidence |",
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

# new Section 15 (Workforce & System Needs) before the AI statement
s15 = """## 15. Workforce & System Needs

The redesign does not sit in a vacuum: workforce shortages, training bottlenecks, subspecialty gaps, rural and remote access, trainee wellbeing and the safety of the learning environment all shape what a sustainable program must deliver. The references below — largely Australasian and RANZCP-specific — map that system context, plus two international training-model comparators. *(These are papers from the NFPT review that concern the training system rather than education methodology per se; ★ marks them as newly added.)*

| Reference | Link | What it tells us | Category |
|---|---|---|---|
| ★ Looi, Bastiampillai, Allison. Psychiatrist workforce planning: contexts, considerations and recommendations. *Australas Psychiatry.* 2022 | [doi](https://doi.org/10.1177/10398562211042367) | RANZCP-relevant framing of psychiatrist workforce planning. | Theory |
| ★ Northwood et al. Understanding the drivers of bottlenecks in RANZCP training: modelling and a calculator to determine sustainable trainee intake. *Australas Psychiatry.* 2021 | [doi](https://doi.org/10.1177/1039856220975281) | RANZCP-specific: models training bottlenecks and sustainable trainee intake. | Evidence |
| ★ Lundin et al. Addiction experts: the discrepancy between expectations and reality of generalist psychiatry training. *Australas Psychiatry.* 2023;31(2):224–227 | [doi](https://doi.org/10.1177/10398562231153015) | A subspecialty (addiction) training gap between expectation and reality. | Evidence |
| ★ Hill et al. Addiction psychiatry training in rural Australia: a Victorian initiative. *Australas Psychiatry.* 2021;29(2):230–233 | [doi](https://doi.org/10.1177/1039856220946593) | A rural addiction-training model. | Evidence |
| ★ Coleman et al. Remote supervision in psychiatry training: unlocking capacity and technology. *Australas Psychiatry.* 2022;30(6):768–770 | [doi](https://doi.org/10.1177/10398562221127825) | Remote supervision to expand rural/remote training capacity. | Evidence |
| ★ Coleman. Whose rural? Shaping rural psychiatry training in Aotearoa New Zealand. *Australas Psychiatry.* 2025;33(6) | [doi](https://doi.org/10.1177/10398562251377324) *(confirm)* | Rural psychiatry training in Aotearoa New Zealand. | Theory |
| ★ Orlik et al. Transforming the journey together: …psychiatry trainee experiences of training and wellbeing. *Australas Psychiatry.* 2022;30(3):391–397 | journals.sagepub.com *(DOI to confirm)* | A co-designed study of trainee wellbeing. | Evidence |
| ★ Wilkes et al. Bullying within specialist medical training in Australia: analysis of the medical training survey, 2020–2023. *Australas Psychiatry.* 2024;32(5):459–466 | [doi](https://doi.org/10.1177/10398562241269123) | Evidence on bullying — the safety of the learning environment. | Evidence |
| ★ Tian et al. Increasing demand and persistent gaps in perceived need for mental health care: national findings 2007–2021. *ANZJP.* 2026 | [doi](https://doi.org/10.1177/00048674251393164) *(confirm)* | System demand/need context underpinning workforce planning. | Evidence |
| ★ Molina-Ruiz et al. Training in neuropsychiatry: views of early career psychiatrists from across the world. *BJPsych Bull.* 2024;48(2):78–84 | [doi](https://doi.org/10.1192/bjb.2023.32) | International early-career perspectives on (neuro)psychiatry training. | Evidence |
| ★ Booth et al. Toward a new model of training in Canadian forensic psychiatry. *J Am Acad Psychiatry Law.* 2021;49(3):381–395 | [doi](https://doi.org/10.29158/JAAPL.200112-20) | An international CBME-based subspecialty training-model comparator. | Theory |

---

## AI use statement"""

t = t.replace('## AI use statement', s15, 1)
t = re.sub(r'\n{3,}', '\n\n', t)
p.write_text(t, encoding='utf-8')
print('done')
