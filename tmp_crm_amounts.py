import json, urllib.request
from pathlib import Path

API_URL='https://crm.metadyn.xyz/graphql'
token=Path('/home/jza/.openclaw/.secrets/metadyn-crm-api-key').read_text().strip()

items = [
    {
        'name': 'DATALAND',
        'amount': 120000,
        'confidence': 'High',
        'concept': 'Founding digital member world and programming layer for exhibitions, artist events, and remote community participation.',
        'demo': 'One exhibition-linked browser world with event room, member login continuity, and analytics-enabled participation.',
        'rationale': 'New institution, strong fit, and likely need for a high-quality continuity layer around flagship immersive installations.'
    },
    {
        'name': 'National Geographic Museum of Exploration',
        'amount': 180000,
        'confidence': 'Medium-High',
        'concept': 'Exploration-themed browser-first companion world for education, public programming, sponsor extensions, and post-visit engagement.',
        'demo': 'A pilot expedition hub with one educational journey, live event space, and persistent visitor identity.',
        'rationale': 'Enterprise-scale institution with clear immersive ambition; first engagement likely substantial but still narrower than a district-scale platform.'
    },
    {
        'name': 'KC2026 ecosystem',
        'amount': 150000,
        'confidence': 'Medium',
        'concept': 'Kansas City fan and visitor discovery world with sponsor zones, neighborhood previews, multilingual onboarding, and event continuity.',
        'demo': 'A World Cup preview world focused on districts, sponsor storytelling, and fan orientation.',
        'rationale': 'Big upside and urgency, but more stakeholders and coordination risk; pricing assumes a scoped activation rather than full regional platform ownership.'
    },
    {
        'name': 'Atlas9',
        'amount': 18000,
        'confidence': 'High',
        'concept': 'Digital companion world extending lore, clues, community events, and ticket-holder engagement beyond the venue.',
        'demo': 'A compact browser experience tied to one storyline, one event mode, and one social replay loop.',
        'rationale': 'Small operator, strong alignment, and likely best entry point is a focused pilot rather than a large custom platform sale.'
    },
    {
        'name': 'UBS Digital Art Museum Hamburg',
        'amount': 140000,
        'confidence': 'Medium',
        'concept': 'International companion environment for multilingual orientation, member/community programming, and remote audience participation.',
        'demo': 'One remote-access exhibition layer with member event space and guided orientation journey.',
        'rationale': 'Large cultural opportunity with clear fit, but likely partnership/procurement complexity suggests a sizable yet still first-phase amount.'
    },
    {
        'name': 'Union Station / EDCKC World Cup marketplace',
        'amount': 85000,
        'confidence': 'Medium',
        'concept': 'Exhibit and event companion world for cultural programming, sponsor tie-ins, school/group access, and World Cup discovery use cases.',
        'demo': 'One flagship exhibit companion space or visitor-discovery environment with lightweight analytics and social access.',
        'rationale': 'Institutional fit is solid, but a first engagement likely lands as a pilot around a single program or seasonal activation.'
    },
    {
        'name': 'Nelson-Atkins Museum of Art',
        'amount': 110000,
        'confidence': 'Medium-High',
        'concept': 'Digital belonging layer for expansion storytelling, donor/member previews, curator-led events, and educational access.',
        'demo': 'A future-campus preview and member engagement world tied to one campaign or exhibition narrative.',
        'rationale': 'Strong institutional fit with meaningful upside; amount reflects a serious pilot or pre-expansion digital layer rather than full transformation.'
    },
    {
        'name': 'Gymshark NYC Flagship',
        'amount': 70000,
        'confidence': 'Medium-High',
        'concept': 'Browser-first digital flagship extending community events, creator activations, launches, and identity continuity.',
        'demo': 'A creator event and product-drop hub with persistent member profiles and social event participation.',
        'rationale': 'Brand/community use case is strong, but likely first sale is a campaign or flagship extension rather than a full ongoing platform engagement.'
    },
    {
        'name': 'VEVOR U.S. flagship',
        'amount': 55000,
        'confidence': 'Medium',
        'concept': 'Spatial showroom and product-learning environment connecting demos, tutorials, workshops, and measurable buyer journeys.',
        'demo': 'A category showroom pilot with workshop continuity and QR-linked product education paths.',
        'rationale': 'Useful omnichannel fit, but first budget likely constrained to a practical demo/sales-enablement pilot.'
    },
    {
        'name': 'Crystal Bridges Museum of American Art',
        'amount': 90000,
        'confidence': 'Medium',
        'concept': 'Participatory digital arts and education companion world tied to the Learning and Engagement Hub.',
        'demo': 'A youth/community showcase environment or digital arts studio companion space.',
        'rationale': 'Good fit with the expansion, but likely first project is programmatic and education-oriented rather than a massive enterprise build.'
    },
    {
        'name': 'Lucas Museum of Narrative Art',
        'amount': 130000,
        'confidence': 'Medium',
        'concept': 'Narrative participation world for educational storytelling, public programming, and social exhibition extensions.',
        'demo': 'A story-world pilot tied to one narrative theme or pre-opening public engagement track.',
        'rationale': 'Big institution and unusually strong conceptual fit, but timing and procurement suggest first engagement would still be a phased initiative.'
    },
    {
        'name': 'Canary Islands digital-twin tourism initiative / EMOTUR Lab',
        'amount': 160000,
        'confidence': 'Medium-High',
        'concept': 'Public-facing tourism twin layer for stakeholder collaboration, visitor previews, training, and destination storytelling.',
        'demo': 'A collaborative destination twin pilot with stakeholder rooms and public-facing exploration surfaces.',
        'rationale': 'High strategic fit and real digital-twin momentum; value likely sits above a simple pilot because of multi-stakeholder scope.'
    },
    {
        'name': 'MoN Takanawa',
        'amount': 95000,
        'confidence': 'Medium',
        'concept': 'Seasonal companion world for cultural programming, international audience participation, and recurring narrative events.',
        'demo': 'A season-linked event space and digital participation layer around one theme cycle.',
        'rationale': 'Strong category fit, but likely starts as a curated seasonal program extension rather than a broad platform mandate.'
    },
    {
        'name': 'Wake The Tiger London expansion',
        'amount': 60000,
        'confidence': 'Medium-High',
        'concept': 'Persistent fandom and lore world with clue drops, community spaces, digital memberships, and recurring online activations.',
        'demo': 'A digital lore-and-events layer with one membership or ticket-holder access mode.',
        'rationale': 'Worldbuilding alignment is excellent; first commercial motion likely sits between a creative pilot and a meaningful retention/community product.'
    },
    {
        'name': 'Rabbit hOle',
        'amount': 25000,
        'confidence': 'Medium',
        'concept': 'Story-world classroom and family companion experience for one literary property or rotating educational program.',
        'demo': 'A small browser-first story space for one book world with classroom/family entry points.',
        'rationale': 'Very aligned but likely budget-sensitive; best entry is a small pilot proving educational and donor/member value.'
    },
    {
        'name': 'Negro Leagues Baseball Museum',
        'amount': 65000,
        'confidence': 'Medium-High',
        'concept': 'Shared heritage and education environment for tours, community events, archival storytelling, and sponsor-backed programming.',
        'demo': 'A living-history pilot space supporting school access, community events, and one sponsor/donor activation path.',
        'rationale': 'Excellent storytelling fit with real institutional value, but likely enters through a targeted program rather than a large enterprise rollout.'
    },
    {
        'name': 'Cleveland Museum of Art / ArtLens relaunch',
        'amount': 125000,
        'confidence': 'Medium-High',
        'concept': 'Online continuation layer for ArtLens with social tours, community programming, and post-visit identity continuity.',
        'demo': 'A web-native ArtLens extension supporting shared tours and event-driven digital engagement.',
        'rationale': 'A strong timing-based opportunity where active redesign may support a substantial complementary digital layer.'
    },
    {
        'name': 'West AlabamaWorks',
        'amount': 80000,
        'confidence': 'Medium',
        'concept': 'Persistent workforce campus for employer showcases, onboarding, collaborative training, and career exploration.',
        'demo': 'A manufacturing-career or employer-onboarding world bridging beyond isolated simulator experiences.',
        'rationale': 'There is already immersive acceptance in the org, which supports a meaningful pilot, though public-sector/workforce budgets may still be phased.'
    },
    {
        'name': 'Visit KC',
        'amount': 90000,
        'confidence': 'Medium',
        'concept': 'City-preview and visitor discovery environment for neighborhoods, conventions, major events, and partner storytelling.',
        'demo': 'A World Cup-era destination preview with district and partner modules.',
        'rationale': 'Good event-driven use case and commercial clarity, but first engagement likely tied to one campaign or event horizon.'
    },
    {
        'name': 'Department of Culture and Tourism Abu Dhabi / Saadiyat cultural ecosystem',
        'amount': 250000,
        'confidence': 'Low-Medium',
        'concept': 'District-scale digital continuity layer across cultural destinations, multilingual visitor orientation, and branded/community experiences.',
        'demo': 'A Saadiyat pilot zone proving cross-venue orientation and persistent visitor identity.',
        'rationale': 'Potential value is very large, but certainty is lower; amount reflects strategic enterprise scope rather than immediate probability.'
    },
]

def gql(query, variables=None):
    payload=json.dumps({'query':query,'variables':variables or {}}).encode()
    req=urllib.request.Request(API_URL,data=payload,headers={'Content-Type':'application/json','Authorization':f'Bearer {token}'})
    with urllib.request.urlopen(req, timeout=60) as r:
        data=json.load(r)
    if data.get('errors'):
        raise RuntimeError(json.dumps(data['errors'], indent=2))
    return data['data']

list_q='''query ListOpportunities($first: Int!, $filter: OpportunityFilterInput) { opportunities(first: $first, filter: $filter) { edges { node { id name } } } }'''
update_q='''mutation UpdateOpportunity($id: UUID!, $data: OpportunityUpdateInput!) { updateOpportunity(id: $id, data: $data) { id name amount { amountMicros currencyCode } } }'''
create_note='''mutation CreateNote($data: NoteCreateInput!) { createNote(data: $data) { id title } }'''
create_note_target='''mutation CreateNoteTarget($data: NoteTargetCreateInput!) { createNoteTarget(data: $data) { id } }'''

results=[]
for item in items:
    edges = gql(list_q, {'first': 20, 'filter': {'name': {'ilike': f"%{item['name']}%"}}})['opportunities']['edges']
    node = next((e['node'] for e in edges if e['node']['name'] == item['name']), None)
    if not node:
        raise RuntimeError(f"Opportunity not found: {item['name']}")
    opp_id = node['id']
    gql(update_q, {'id': opp_id, 'data': {'amount': {'amountMicros': int(item['amount']*1_000_000), 'currencyCode': 'USD'}}})
    note_body = f"# Proposed MetaDyn scope and pricing anchor\n\n## Proposed project concept\n{item['concept']}\n\n## Suggested demo / first engagement shape\n{item['demo']}\n\n## Estimated amount anchor\nUSD {item['amount']:,}\n\n## Confidence\n{item['confidence']}\n\n## Pricing rationale\n{item['rationale']}\n\n## Notes\nThis amount is a working estimate for CRM prioritization and opportunity shaping, not a quoted budget or committed client forecast. It is meant to represent a plausible first MetaDyn engagement based on current research.\n"
    note = gql(create_note, {'data': {'title': f"MetaDyn scope + amount estimate — {item['name']}", 'bodyV2': {'markdown': note_body}}})['createNote']
    gql(create_note_target, {'data': {'noteId': note['id'], 'targetOpportunityId': opp_id}})
    results.append({'name': item['name'], 'amount': item['amount'], 'confidence': item['confidence'], 'opportunityId': opp_id, 'noteId': note['id']})

print(json.dumps({'updated': len(results), 'results': results}, indent=2))
