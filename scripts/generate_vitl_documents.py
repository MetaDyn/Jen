from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.sax.saxutils import escape

base = Path('/home/jza/.openclaw/workspace/docs/projects/vitl-medical')
base.mkdir(parents=True, exist_ok=True)

DOCS = {
    'VITL-Product-Snapshot-2026-04-07': {
        'title': 'VITL Product Snapshot',
        'subtitle': 'MetaDyn — 2026-04-07',
        'sections': [
            ('Overview', [
                'VITL is a Unity-based medical simulation product surface on the MetaDyn platform.',
                "The current scenario centers on a pediatric infant UTI case where a learner interacts with the infant's concerned mother by text or voice.",
                'The current near-term goal is Milestone 1: proving a coherent end-to-end learner loop rather than over-claiming full clinical assessment coverage.'
            ]),
            ('Current Product Shape', [
                'AI delivery layer: MetaDynVoiceController handles learner input, transcription, LLM response flow, text-to-speech, and hidden prompt delivery.',
                'Simulation-state layer: VITLSimulationManager owns lifecycle state, activity progression, timers, inactivity escalation, learner-turn storage, and hidden simulation overlay logic.',
                'Assessment/intake layer: model-backed communication scoring plus a planned structured patient-history intake flow for Activity 2.'
            ]),
            ('Milestone 1 Proof', [
                'Mother opens with concern.',
                'Learner responds by text or voice.',
                'Learner communication is scored.',
                'Simulation state updates before the mother response.',
                'Activity 1 completes through authored thresholds when appropriate.',
                'Activity 2 begins as structured patient-history capture.'
            ]),
            ('Key Decisions', [
                'The simulation manager remains the authority for activity progression.',
                'Conversation history is not the same thing as structured patient history.',
                'The learner-entered intake UI should become the canonical structured history record for Activity 2.',
                'Fallback scoring is a resilience mechanism, not the intended long-term assessment layer.',
                'Milestone 1 should stay focused and avoid scope creep into full clinical grading, automatic structured extraction from dialogue, or broad event-system rewrites.'
            ]),
            ('Immediate Next Steps', [
                'Lock the canonical Activity 1 to Activity 2 demo path.',
                'Define and implement the first pass of VITLPatientIntakeRecord and VITLPatientIntakeController.',
                'Add required-fields plus learner-confirmation completion behavior for Activity 2.',
                'Add analytics-safe milestone events without over-expanding scope.'
            ])
        ]
    },
    'VITL-Project-Brief-2026-04-07': {
        'title': 'VITL Project Brief',
        'subtitle': 'Internal working brief',
        'sections': [
            ('Project Summary', [
                'VITL is evolving from a simple conversational prototype into a structured simulation product with scenario logic, learner assessment, and structured documentation flows.',
                'The active case is a pediatric infant UTI encounter focused on communication with the infant\'s mother.'
            ]),
            ('What Matters Right Now', [
                'Simulation-aware routing between MetaDynVoiceController and VITLSimulationManager is a central part of the current design.',
                'Model-backed communication scoring through OpenRouter is the intended primary scoring path, with fallback scoring preserved for resilience.',
                'Activity 2 should capture learner-entered patient history as structured runtime data rather than inferred LLM extraction.'
            ]),
            ('Milestone 1 Scope', [
                'Greeting / rapport flow.',
                'Threshold-based activity progression.',
                'Simulation-aware mother response after scoring.',
                'Structured history intake as a distinct Activity 2 flow.',
                'Analytics-safe milestone events where useful.'
            ]),
            ('Out of Scope', [
                'Full automated clinical grading.',
                'Automatic extraction of structured history from mother dialogue.',
                'Complete reporting/export stack.',
                'Large-scale rewrite of string-based event surfaces.'
            ]),
            ('Operational Read', [
                'The strongest architectural line in the current VITL material is separation of concerns: conversation history, learner scoring, simulation state, and patient-history documentation should remain distinct layers with clear ownership.',
                'That separation should stay intact as implementation moves forward.'
            ])
        ]
    },
    'VITL-Stakeholder-System-Summary-2026-04-07': {
        'title': 'VITL Stakeholder System Summary',
        'subtitle': 'Stakeholder-facing summary',
        'sections': [
            ('Executive Summary', [
                'VITL is a MetaDyn medical simulation experience where a learner communicates with the mother of an infant patient in a guided pediatric UTI scenario.',
                'The product is moving beyond a simple AI conversation into a structured simulation with activity progression, communication scoring, and planned patient-history capture.'
            ]),
            ('Why It Matters', [
                'VITL demonstrates a higher-value MetaDyn product direction: scenario-driven immersive training that combines AI interaction with explicit simulation-state control.',
                'This creates a path toward more credible teaching, review, and assessment workflows over time.'
            ]),
            ('Current Milestone', [
                'The current milestone is to validate a working learner loop from greeting and rapport into structured patient-history intake.',
                'The first milestone is intentionally bounded to prove the experience flow before expanding into heavier assessment or reporting capabilities.'
            ]),
            ('System Components', [
                'Voice/controller layer for text, voice, transcription, model responses, and speech output.',
                'Simulation manager for activity flow, state, scoring hooks, escalation, and hidden scenario context.',
                'Communication scoring service for rubric-based learner scoring.',
                'Planned patient-intake layer for structured documentation of learner-collected history.'
            ]),
            ('Bottom Line', [
                'The near-term value is a coherent simulation loop where communication quality affects progression and structured history capture begins to look like a real training product instead of a chatbot demo.'
            ])
        ]
    }
}

def make_rtf(title, subtitle, sections):
    def esc(t):
        return t.replace('\\', r'\\').replace('{', r'\{').replace('}', r'\}')
    out = [r'{\rtf1\ansi\deff0', r'{\fonttbl{\f0 Arial;}}', r'\fs24']
    out.append(r'\b\fs32 ' + esc(title) + r'\b0\fs24\par')
    out.append(esc(subtitle) + r'\par\par')
    for heading, bullets in sections:
        out.append(r'\b ' + esc(heading) + r'\b0\par')
        for b in bullets:
            out.append(r'\tab\bullet\tab ' + esc(b) + r'\par')
        out.append(r'\par')
    out.append('}')
    return ''.join(out)

def para_xml(text):
    t = escape(text)
    return f'<w:p><w:r><w:t xml:space="preserve">{t}</w:t></w:r></w:p>'

def bullet_xml(text):
    t = escape(text)
    return '<w:p><w:pPr><w:pStyle w:val="ListParagraph"/><w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr></w:pPr><w:r><w:t xml:space="preserve">' + t + '</w:t></w:r></w:p>'

def make_docx(path, title, subtitle, sections):
    content_types = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/><Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/></Types>'
    rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>'
    doc_rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/></Relationships>'
    styles = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style><w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:sz w:val="32"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:sz w:val="28"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="ListParagraph"><w:name w:val="List Paragraph"/><w:basedOn w:val="Normal"/></w:style></w:styles>'
    numbering = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:abstractNum w:abstractNumId="0"><w:lvl w:ilvl="0"><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr></w:lvl></w:abstractNum><w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num></w:numbering>'
    core = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>{escape(title)}</dc:title><dc:creator>Jen</dc:creator></cp:coreProperties>'
    app = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>OpenClaw</Application></Properties>'
    body = ['<w:p><w:pPr><w:pStyle w:val="Title"/></w:pPr><w:r><w:t>' + escape(title) + '</w:t></w:r></w:p>', para_xml(subtitle)]
    for heading, bullets in sections:
        body.append('<w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>' + escape(heading) + '</w:t></w:r></w:p>')
        for b in bullets:
            body.append(bullet_xml(b))
        body.append(para_xml(''))
    document = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" mc:Ignorable="w14"><w:body>' + ''.join(body) + '<w:sectPr/></w:body></w:document>'
    with ZipFile(path, 'w', ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', content_types)
        z.writestr('_rels/.rels', rels)
        z.writestr('word/_rels/document.xml.rels', doc_rels)
        z.writestr('word/document.xml', document)
        z.writestr('word/styles.xml', styles)
        z.writestr('word/numbering.xml', numbering)
        z.writestr('docProps/core.xml', core)
        z.writestr('docProps/app.xml', app)

def pdf_escape(text):
    return text.replace('\\', r'\\').replace('(', r'\(').replace(')', r'\)')

def make_pdf(path, title, subtitle, sections):
    lines = [title, subtitle, '']
    for heading, bullets in sections:
        lines.append(heading)
        for b in bullets:
            lines.append('- ' + b)
        lines.append('')
    content = ['BT', '/F1 18 Tf', '50 800 Td', f'({pdf_escape(title)}) Tj', 'ET', 'BT', '/F1 11 Tf', '50 784 Td', f'({pdf_escape(subtitle)}) Tj', 'ET']
    y = 750
    for line in lines[3:]:
        if y < 50:
            break
        size = 12 if line and not line.startswith('- ') else 10
        content += ['BT', f'/F1 {size} Tf', f'50 {y} Td', f'({pdf_escape(line)}) Tj', 'ET']
        y -= 16 if size == 12 else 14
    stream = '\n'.join(content).encode('latin-1', 'replace')
    objs = []
    def add(obj): objs.append(obj)
    add(b'<< /Type /Catalog /Pages 2 0 R >>')
    add(b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>')
    add(b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>')
    add(b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>')
    add(f'<< /Length {len(stream)} >>\nstream\n'.encode() + stream + b'\nendstream')
    out = bytearray(b'%PDF-1.4\n')
    xref = [0]
    for i, obj in enumerate(objs, start=1):
        xref.append(len(out))
        out += f'{i} 0 obj\n'.encode() + obj + b'\nendobj\n'
    xref_start = len(out)
    out += f'xref\n0 {len(xref)}\n'.encode()
    out += b'0000000000 65535 f \n'
    for off in xref[1:]:
        out += f'{off:010d} 00000 n \n'.encode()
    out += f'trailer\n<< /Size {len(xref)} /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF'.encode()
    path.write_bytes(out)

for name, meta in DOCS.items():
    (base / f'{name}.doc').write_text(make_rtf(meta['title'], meta['subtitle'], meta['sections']), encoding='utf-8')
    make_docx(base / f'{name}.docx', meta['title'], meta['subtitle'], meta['sections'])
    make_pdf(base / f'{name}.pdf', meta['title'], meta['subtitle'], meta['sections'])

for p in sorted(base.glob('VITL-*.*')):
    print(p.name)
