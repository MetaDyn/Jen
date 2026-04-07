from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.sax.saxutils import escape

base = Path('/home/jza/.openclaw/workspace/docs/projects/vitl-medical')
out_path = base / 'VITL-Comprehensive-Project-Brief-2026-04-07.docx'

title = 'VITL Comprehensive Project Brief'
subtitle = 'MetaDyn — 2026-04-07'
sections = [
    ('Executive Summary', [
        'VITL is a Unity-based medical simulation product surface on the MetaDyn platform.',
        'The current scenario centers on a pediatric infant UTI case where a learner interacts with the infant\'s concerned mother by text or voice.',
        'The current near-term target is a bounded Milestone 1 that proves a coherent end-to-end learner loop rather than over-claiming full clinical assessment automation.'
    ]),
    ('Product Snapshot', [
        'VITL is no longer just a chatbot-style interaction. It is taking shape as a structured simulation product with explicit scenario logic, activity progression, communication assessment, and planned structured patient-history capture.',
        'The system is organized around three layers: AI delivery, simulation-state control, and assessment/intake.',
        'The immediate value is a believable training flow where communication quality affects progression and documented history begins to look like a real product surface.'
    ]),
    ('Current Milestone Definition', [
        'Mother opens with concern.',
        'Learner responds by text or voice.',
        'Learner communication is scored through a model-backed rubric.',
        'Simulation state updates before the mother response is generated.',
        'Activity 1 completes through authored thresholds when appropriate.',
        'Activity 2 begins as structured patient-history capture.'
    ]),
    ('Current System Architecture', [
        'MetaDynVoiceController is the AI delivery layer. It handles learner text input, voice transcription, LLM request/response flow, text-to-speech, and hidden prompt delivery.',
        'VITLSimulationManager is the simulation-state authority. It owns lifecycle, activity progression, timers, inactivity escalation, learner-turn storage, score integration, and hidden simulation overlay logic.',
        'VITLCommunicationScoringService is the model-backed scoring layer. It sends structured scoring requests, parses numeric results, and supports fallback behavior if model scoring fails.',
        'The planned Activity 2 intake layer should use runtime session data and a dedicated intake controller rather than mixing structured patient history directly into freeform conversation state.'
    ]),
    ('Current Case Structure', [
        'Activity 1 focuses on greeting and rapport. The learner should introduce themselves, acknowledge the mother\'s concern, explain that they will help assess the baby, and communicate calmly and clearly.',
        'Activity 2 focuses on history taking. The current structured field scope includes symptom onset, urine concerns, fever history, feeding changes, diaper history, behavior changes, and freeform notes.'
    ]),
    ('Key Product and Architecture Decisions', [
        'The simulation manager remains the authority for activity completion and progression. Model scoring informs progression, but authored thresholds decide completion.',
        'Conversation history is not the same thing as structured patient history. The learner-entered intake UI should become the canonical structured history record for Activity 2.',
        'Activity 2 should start simple: required fields plus learner confirmation first, correctness comparison later.',
        'Fallback scoring is a resilience mechanism, not the intended long-term assessment model.',
        'Structured payload migration should happen gradually and should not become Milestone 1 scope creep.'
    ]),
    ('What Is Confirmed vs. What Is Not', [
        'Confirmed from the uploaded docs: simulation-aware routing between MetaDynVoiceController and VITLSimulationManager has been implemented and manually validated, project compilation succeeded after scorer assignment, and the scoring service plus model configuration were assigned for manual testing.',
        'Also confirmed from the docs: fallback scoring exists, Activity 2 is intended to use learner-entered structured form data as the authoritative patient-history record, and the current milestone is intentionally bounded.',
        'Important caveat: this brief is document-grounded, not yet a code-verified implementation audit. It reflects the uploaded VITL materials rather than an independent source-code verification pass.'
    ]),
    ('Milestone 1 Scope', [
        'Greeting and rapport flow.',
        'Model-backed communication scoring.',
        'Threshold-based activity progression.',
        'Simulation-aware mother response after scoring.',
        'Activity 2 structured intake UI and runtime record pattern.',
        'Analytics-safe milestone events where useful.'
    ]),
    ('Explicitly Out of Scope for Milestone 1', [
        'Full automated clinical grading.',
        'Automatic extraction of structured patient history from AI dialogue.',
        'Full reporting/export stack.',
        'Large-scale rewrite of all string-based event surfaces.',
        'Complex branching scenarios beyond the first canonical Activity 1 to Activity 2 path.'
    ]),
    ('Risks and Constraints', [
        'The biggest architecture risk is blurring together learner conversation, learner scoring, simulation state, and patient-history documentation. Those should remain distinct layers with clear ownership.',
        'The current brief should not be mistaken for a code-grounded implementation audit.',
        'Future orchestration of server-level agents for deeper code analysis is expected, but that is not yet part of the active workflow and should not be assumed in current-state summaries.'
    ]),
    ('Recommended Next Steps', [
        'Lock the canonical Activity 1 to Activity 2 demo path.',
        'Define and implement the first pass of VITLPatientIntakeRecord and VITLPatientIntakeController.',
        'Implement required-fields plus learner-confirmation completion behavior for Activity 2.',
        'Add analytics-safe intake milestone events without over-expanding scope.',
        'When useful, produce a separate code-verified snapshot that distinguishes implemented, wired-but-unverified, and planned.'
    ])
]

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

make_docx(out_path, title, subtitle, sections)
print(out_path.name)
