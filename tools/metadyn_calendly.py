#!/usr/bin/env python3
import argparse
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import metadyn_crm as crm

API_BASE = 'https://api.calendly.com'
TOKEN_PATH = Path('/home/jza/.openclaw/.secrets/calendly-api-key')
FREE_EMAIL_DOMAINS = {
    'gmail.com', 'googlemail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'live.com',
    'icloud.com', 'me.com', 'msn.com', 'aol.com', 'proton.me', 'protonmail.com', 'pm.me'
}


class CalendlyClient:
    def __init__(self, token_path: Path = TOKEN_PATH):
        self.token_path = token_path
        self._token: Optional[str] = None
        self._me: Optional[Dict[str, Any]] = None

    @property
    def token(self) -> str:
        if self._token is None:
            self._token = self.token_path.read_text().strip()
        return self._token

    def _request(self, method: str, path: str, *, query: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = path if path.startswith('http') else f'{API_BASE}{path}'
        if query:
            pairs: List[Tuple[str, str]] = []
            for key, value in query.items():
                if value is None:
                    continue
                if isinstance(value, (list, tuple)):
                    for item in value:
                        if item is not None:
                            pairs.append((key, str(item)))
                else:
                    pairs.append((key, str(value)))
            if pairs:
                url += ('&' if '?' in url else '?') + urllib.parse.urlencode(pairs)
        payload = None if body is None else json.dumps(body).encode()
        req = urllib.request.Request(
            url,
            data=payload,
            method=method,
            headers={
                'Authorization': f'Bearer {self.token}',
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'User-Agent': 'Jen/1.0 (+MetaDyn Calendly integration)',
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read().decode()
                return json.loads(raw) if raw else {}
        except Exception as e:
            detail = ''
            if hasattr(e, 'read'):
                try:
                    detail = e.read().decode()
                except Exception:
                    detail = ''
            raise RuntimeError(f'Calendly API {method} {url} failed: {e}{(" :: " + detail) if detail else ""}')

    def get(self, path: str, **query: Any) -> Dict[str, Any]:
        return self._request('GET', path, query=query)

    def post(self, path: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', path, body=body)

    def paged_collection(self, path: str, *, limit: int = 25, **query: Any) -> List[Dict[str, Any]]:
        items: List[Dict[str, Any]] = []
        count = min(max(limit, 1), 100)
        next_page_token: Optional[str] = None
        while True:
            page = self.get(path, count=count, page_token=next_page_token, **query)
            items.extend(page.get('collection') or [])
            pagination = page.get('pagination') or {}
            next_page_token = pagination.get('next_page_token')
            if not next_page_token or len(items) >= limit:
                break
        return items[:limit]

    def me(self) -> Dict[str, Any]:
        if self._me is None:
            self._me = self.get('/users/me')['resource']
        return self._me

    def current_user_uri(self) -> str:
        return self.me()['uri']

    def current_org_uri(self) -> str:
        return self.me()['current_organization']


def _print_json(data: Any) -> int:
    print(json.dumps(data, indent=2))
    return 0


def _event_uuid_from_uri(uri: str) -> str:
    return uri.rstrip('/').split('/')[-1]


def _safe_domain(email: Optional[str]) -> Optional[str]:
    if not email or '@' not in email:
        return None
    domain = email.split('@', 1)[1].strip().lower()
    if not domain or domain in FREE_EMAIL_DOMAINS:
        return None
    return domain


def _split_name(name: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    name = (name or '').strip()
    if not name:
        return None, None
    parts = name.split()
    if len(parts) == 1:
        return parts[0], None
    return parts[0], ' '.join(parts[1:])


def _iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def _iso_after(hours: int) -> str:
    return (datetime.now(timezone.utc) + timedelta(hours=hours)).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def _parse_when(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    value = value.strip()
    if value.endswith('Z'):
        value = value[:-1] + '+00:00'
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        try:
            return parsedate_to_datetime(value)
        except Exception:
            return None


def _fmt_when(value: Optional[str]) -> str:
    dt = _parse_when(value)
    if not dt:
        return value or '-'
    return dt.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')


def _crm_find_person_by_email(email: str) -> Optional[Dict[str, Any]]:
    query = '''
    query FindPersonByEmail($email: String!) {
      people(first: 10, filter: { emails: { primaryEmail: { eq: $email } } }) {
        edges { node { id name { firstName lastName } emails { primaryEmail } company { id name } } }
      }
    }
    '''
    edges = crm.gql(query, {'email': email}).get('people', {}).get('edges', [])
    return edges[0]['node'] if edges else None


def _crm_find_company_by_domain(domain: str) -> Optional[Dict[str, Any]]:
    query = '''
    query FindCompanyByDomain($domain: String!) {
      companies(first: 10, filter: { or: [
        { domainName: { primaryLinkLabel: { eq: $domain } } },
        { domainName: { primaryLinkUrl: { ilike: $domain } } }
      ]}) {
        edges { node { id name domainName { primaryLinkLabel primaryLinkUrl } } }
      }
    }
    '''
    edges = crm.gql(query, {'domain': domain}).get('companies', {}).get('edges', [])
    return edges[0]['node'] if edges else None


def _crm_create_company(domain: str) -> Dict[str, Any]:
    label = domain.lower()
    data = {
        'name': label,
        'domainName': {'primaryLinkLabel': label, 'primaryLinkUrl': f'https://{label}'},
    }
    mutation = '''mutation CreateCompany($data: CompanyCreateInput!) { createCompany(data: $data) { id name domainName { primaryLinkLabel primaryLinkUrl } createdAt } }'''
    return crm.gql(mutation, {'data': data})['createCompany']


def _crm_create_person(name: Optional[str], email: str, company_id: Optional[str] = None) -> Dict[str, Any]:
    first_name, last_name = _split_name(name)
    data = crm.compact({
        'name': {'firstName': first_name, 'lastName': last_name} if first_name or last_name else None,
        'emails': {'primaryEmail': email},
        'companyId': company_id,
    })
    mutation = '''mutation CreatePerson($data: PersonCreateInput!) { createPerson(data: $data) { id name { firstName lastName } emails { primaryEmail } company { id name } createdAt } }'''
    return crm.gql(mutation, {'data': data})['createPerson']


def _crm_create_note(title: str, body: str, *, person_id: Optional[str], company_id: Optional[str]) -> Dict[str, Any]:
    note = crm.gql(
        '''mutation CreateNote($data: NoteCreateInput!) { createNote(data: $data) { id title createdAt } }''',
        {'data': {'title': title, 'bodyV2': {'markdown': body}}},
    )['createNote']
    target = None
    if person_id or company_id:
        target = crm.gql(
            '''mutation CreateNoteTarget($data: NoteTargetCreateInput!) { createNoteTarget(data: $data) { id note { id title } targetCompany { id name } targetPerson { id name { firstName lastName } } } }''',
            {'data': crm.compact({'noteId': note['id'], 'targetPersonId': person_id, 'targetCompanyId': company_id})},
        )['createNoteTarget']
    return {'note': note, 'target': target}


def _crm_create_task(title: str, body: str, due_at: Optional[str], *, person_id: Optional[str], company_id: Optional[str]) -> Dict[str, Any]:
    task = crm.gql(
        '''mutation CreateTask($data: TaskCreateInput!) { createTask(data: $data) { id title status dueAt createdAt } }''',
        {'data': crm.compact({'title': title, 'bodyV2': {'markdown': body}, 'dueAt': due_at, 'status': 'TODO'})},
    )['createTask']
    target = None
    if person_id or company_id:
        target = crm.gql(
            '''mutation CreateTaskTarget($data: TaskTargetCreateInput!) { createTaskTarget(data: $data) { id task { id title } targetCompany { id name } targetPerson { id name { firstName lastName } } } }''',
            {'data': crm.compact({'taskId': task['id'], 'targetPersonId': person_id, 'targetCompanyId': company_id})},
        )['createTaskTarget']
    return {'task': task, 'target': target}


def _crm_upsert_person_company(name: Optional[str], email: Optional[str]) -> Dict[str, Any]:
    if not email:
        raise RuntimeError('Invitee email is required to sync Calendly meeting into CRM.')
    person = _crm_find_person_by_email(email)
    company = None
    domain = _safe_domain(email)
    if person and person.get('company'):
        company = person['company']
    elif domain:
        company = _crm_find_company_by_domain(domain)
        if not company:
            company = _crm_create_company(domain)
    if not person:
        person = _crm_create_person(name, email, company.get('id') if company else None)
    return {'person': person, 'company': company}


def _find_contact_by_email(client: CalendlyClient, email: str) -> Optional[Dict[str, Any]]:
    email = email.strip().lower()
    for item in client.paged_collection('/contacts', limit=100):
        if (item.get('email') or '').strip().lower() == email:
            return item
    return None


def _event_summary_markdown(event: Dict[str, Any], invitee: Dict[str, Any], payload: Optional[Dict[str, Any]] = None) -> str:
    location = event.get('location') or {}
    questions = invitee.get('questions_and_answers') or []
    qa_lines = []
    for qa in questions:
        q = qa.get('question') or qa.get('name') or 'Question'
        a = qa.get('answer') or qa.get('value') or '-'
        qa_lines.append(f'- **{q}:** {a}')
    lines = [
        'Calendly meeting synced into CRM.',
        '',
        f"- **Event:** {event.get('name') or '-'}",
        f"- **Status:** {event.get('status') or '-'}",
        f"- **Start:** {_fmt_when(event.get('start_time'))}",
        f"- **End:** {_fmt_when(event.get('end_time'))}",
        f"- **Invitee:** {invitee.get('name') or '-'} <{invitee.get('email') or '-'}>",
        f"- **Calendly Event URI:** {event.get('uri') or '-'}",
        f"- **Calendly Invitee URI:** {invitee.get('uri') or '-'}",
    ]
    if event.get('event_type'):
        lines.append(f"- **Event Type:** {event['event_type']}")
    if location:
        loc_kind = location.get('type') or location.get('kind') or '-'
        loc_join = location.get('join_url') or location.get('location') or location.get('data') or '-'
        lines.append(f"- **Location:** {loc_kind} — {loc_join}")
    if invitee.get('cancel_reason'):
        lines.append(f"- **Cancel Reason:** {invitee.get('cancel_reason')}")
    if payload and payload.get('event'):
        lines.append(f"- **Webhook Event:** {payload.get('event')}")
    if qa_lines:
        lines += ['', '### Intake Notes', *qa_lines]
    return '\n'.join(lines)


def _fetch_event_and_invitees(client: CalendlyClient, event_uri: str) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    event = client.get(event_uri)['resource'] if event_uri.startswith('http') else client.get(event_uri)['resource']
    invitees = client.paged_collection(f"/scheduled_events/{_event_uuid_from_uri(event_uri)}/invitees", limit=100)
    return event, invitees


def cmd_whoami(args: argparse.Namespace) -> int:
    return _print_json(CalendlyClient().me())


def cmd_list_event_types(args: argparse.Namespace) -> int:
    client = CalendlyClient()
    owner = client.current_user_uri() if args.scope == 'user' else client.current_org_uri()
    key = 'user' if args.scope == 'user' else 'organization'
    items = client.paged_collection('/event_types', limit=args.limit, **{key: owner})
    if args.json:
        return _print_json(items)
    if not items:
        print('(no event types)')
        return 0
    for item in items:
        print(f"- {item.get('name')} | uri={item.get('uri')} | duration={item.get('duration')}m | active={item.get('active')} | url={item.get('scheduling_url')}")
    return 0


def cmd_list_contacts(args: argparse.Namespace) -> int:
    client = CalendlyClient()
    items = client.paged_collection('/contacts', limit=args.limit)
    if args.json:
        return _print_json(items)
    if not items:
        print('(no contacts)')
        return 0
    for item in items:
        name = ' '.join(part for part in [item.get('first_name'), item.get('last_name')] if part) or '-'
        print(f"- {name} | email={item.get('email')} | company={item.get('company') or '-'} | uri={item.get('uri')}")
    return 0


def cmd_create_contact(args: argparse.Namespace) -> int:
    client = CalendlyClient()
    existing = _find_contact_by_email(client, args.email)
    if existing:
        return _print_json({'resource': existing, 'meta': {'created': False, 'reason': 'contact already exists'}})
    body = crm.compact({
        'first_name': args.first_name,
        'last_name': args.last_name,
        'email': args.email,
        'phone': args.phone,
        'job_title': args.job_title,
        'company': args.company,
        'linkedin': args.linkedin,
        'time_zone': args.time_zone,
        'city': args.city,
        'state': args.state,
        'country': args.country,
    })
    return _print_json(client.post('/contacts', body))


def cmd_list_scheduled_events(args: argparse.Namespace) -> int:
    client = CalendlyClient()
    query: Dict[str, Any] = {
        'user': client.current_user_uri() if args.scope == 'user' else None,
        'organization': client.current_org_uri() if args.scope == 'organization' else None,
        'status': args.status,
        'min_start_time': args.min_start_time or (_iso_now() if args.upcoming else None),
        'max_start_time': args.max_start_time,
        'invitee_email': args.invitee_email,
        'sort': args.sort,
    }
    items = client.paged_collection('/scheduled_events', limit=args.limit, **query)
    if args.json:
        return _print_json(items)
    if not items:
        print('(no scheduled events)')
        return 0
    for item in items:
        print(f"- {item.get('name')} | status={item.get('status')} | start={_fmt_when(item.get('start_time'))} | end={_fmt_when(item.get('end_time'))} | uri={item.get('uri')}")
    return 0


def cmd_list_webhook_subscriptions(args: argparse.Namespace) -> int:
    client = CalendlyClient()
    items = client.paged_collection(
        '/webhook_subscriptions',
        limit=args.limit,
        organization=args.organization or client.current_org_uri(),
        scope='organization',
    )
    if args.json:
        return _print_json(items)
    if not items:
        print('(no webhook subscriptions)')
        return 0
    for item in items:
        print(f"- callback={item.get('callback_url')} | state={item.get('state')} | events={','.join(item.get('events') or [])} | uri={item.get('uri')}")
    return 0


def cmd_create_webhook_subscription(args: argparse.Namespace) -> int:
    client = CalendlyClient()
    body = {
        'url': args.callback_url,
        'events': args.event,
        'organization': args.organization or client.current_org_uri(),
        'scope': 'organization',
    }
    if args.signing_key:
        body['signing_key'] = args.signing_key
    if args.user:
        body['user'] = args.user
    return _print_json(client.post('/webhook_subscriptions', body))


def cmd_sync_event_to_crm(args: argparse.Namespace) -> int:
    client = CalendlyClient()
    event, invitees = _fetch_event_and_invitees(client, args.event_uri)
    if not invitees:
        raise RuntimeError('No invitees found for scheduled event.')
    results = []
    for invitee in invitees:
        upserted = _crm_upsert_person_company(invitee.get('name'), invitee.get('email'))
        body = _event_summary_markdown(event, invitee)
        note = _crm_create_note(
            title=f"Calendly: {event.get('name') or 'Meeting'}",
            body=body,
            person_id=upserted['person'].get('id') if upserted.get('person') else None,
            company_id=upserted['company'].get('id') if upserted.get('company') else None,
        )
        task = None
        if args.create_task:
            task_due = event.get('start_time') or _iso_after(24)
            task = _crm_create_task(
                title=f"Follow up: {event.get('name') or 'Calendly meeting'}",
                body=f"Follow up with {invitee.get('name') or invitee.get('email')} after Calendly meeting.\n\nEvent: {event.get('uri')}",
                due_at=task_due,
                person_id=upserted['person'].get('id') if upserted.get('person') else None,
                company_id=upserted['company'].get('id') if upserted.get('company') else None,
            )
        results.append({'invitee': invitee, 'crm': upserted, 'note': note, 'task': task})
    return _print_json({'event': event, 'results': results})


def cmd_sync_webhook_to_crm(args: argparse.Namespace) -> int:
    payload = json.loads(Path(args.file).read_text()) if args.file else json.load(sys.stdin)
    event_name = payload.get('event') or payload.get('trigger') or payload.get('type')
    outer = payload.get('payload') or payload
    invitee = outer.get('invitee') or {}
    scheduled_event = outer.get('scheduled_event') or {}
    client = CalendlyClient()
    event_uri = scheduled_event.get('uri') or args.event_uri
    if event_uri:
        try:
            fetched_event, fetched_invitees = _fetch_event_and_invitees(client, event_uri)
            event = fetched_event
            if invitee.get('uri'):
                matched = [i for i in fetched_invitees if i.get('uri') == invitee.get('uri')]
                invitee = matched[0] if matched else (fetched_invitees[0] if fetched_invitees else invitee)
            elif fetched_invitees:
                invitee = fetched_invitees[0]
        except Exception:
            event = scheduled_event
    else:
        event = scheduled_event
    if not invitee.get('email'):
        raise RuntimeError('Webhook payload did not contain an invitee email, and no fetchable event URI was available.')
    upserted = _crm_upsert_person_company(invitee.get('name'), invitee.get('email'))
    note = _crm_create_note(
        title=f"Calendly webhook: {event_name or event.get('status') or 'meeting update'}",
        body=_event_summary_markdown(event, invitee, payload),
        person_id=upserted['person'].get('id') if upserted.get('person') else None,
        company_id=upserted['company'].get('id') if upserted.get('company') else None,
    )
    task = None
    if args.create_task and event_name == 'invitee.created':
        task = _crm_create_task(
            title=f"Prep for meeting: {event.get('name') or 'Calendly meeting'}",
            body=f"Review context and prepare for {invitee.get('name') or invitee.get('email')}.\n\nWebhook event: {event_name}",
            due_at=event.get('start_time') or _iso_after(24),
            person_id=upserted['person'].get('id') if upserted.get('person') else None,
            company_id=upserted['company'].get('id') if upserted.get('company') else None,
        )
    return _print_json({'crm': upserted, 'note': note, 'task': task, 'event': event, 'invitee': invitee})


def cmd_push_crm_person_to_contact(args: argparse.Namespace) -> int:
    query = '''
    query GetPerson($id: UUID!) {
      person(filter: { id: { eq: $id } }) {
        id
        name { firstName lastName }
        emails { primaryEmail }
        jobTitle
        city
        company { id name domainName { primaryLinkLabel primaryLinkUrl } }
      }
    }
    '''
    person = crm.gql(query, {'id': args.person_id})['person']
    if not person:
        raise RuntimeError(f'CRM person not found: {args.person_id}')
    email = (person.get('emails') or {}).get('primaryEmail')
    if not email:
        raise RuntimeError('CRM person has no primary email; cannot push to Calendly contacts.')
    client = CalendlyClient()
    existing = _find_contact_by_email(client, email)
    if existing:
        return _print_json({'resource': existing, 'meta': {'created': False, 'reason': 'contact already exists'}})
    company = person.get('company') or {}
    body = crm.compact({
        'first_name': (person.get('name') or {}).get('firstName'),
        'last_name': (person.get('name') or {}).get('lastName'),
        'email': email,
        'job_title': person.get('jobTitle'),
        'company': company.get('name'),
        'city': person.get('city'),
    })
    return _print_json(client.post('/contacts', body))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description='MetaDyn Calendly direct API + CRM bridge')
    sub = p.add_subparsers(dest='command', required=True)

    s = sub.add_parser('whoami'); s.set_defaults(func=cmd_whoami)

    s = sub.add_parser('list-event-types'); s.add_argument('--scope', choices=['user', 'organization'], default='user'); s.add_argument('--limit', type=int, default=25); s.add_argument('--json', action='store_true'); s.set_defaults(func=cmd_list_event_types)
    s = sub.add_parser('list-contacts'); s.add_argument('--limit', type=int, default=25); s.add_argument('--json', action='store_true'); s.set_defaults(func=cmd_list_contacts)
    s = sub.add_parser('create-contact'); s.add_argument('--first-name', required=True); s.add_argument('--last-name'); s.add_argument('--email', required=True); s.add_argument('--phone'); s.add_argument('--job-title'); s.add_argument('--company'); s.add_argument('--linkedin'); s.add_argument('--time-zone'); s.add_argument('--city'); s.add_argument('--state'); s.add_argument('--country'); s.set_defaults(func=cmd_create_contact)

    s = sub.add_parser('list-scheduled-events'); s.add_argument('--scope', choices=['user', 'organization'], default='user'); s.add_argument('--status', choices=['active', 'canceled'], default='active'); s.add_argument('--limit', type=int, default=25); s.add_argument('--min-start-time'); s.add_argument('--max-start-time'); s.add_argument('--invitee-email'); s.add_argument('--sort', default='start_time:asc'); s.add_argument('--upcoming', action='store_true'); s.add_argument('--json', action='store_true'); s.set_defaults(func=cmd_list_scheduled_events)

    s = sub.add_parser('list-webhook-subscriptions'); s.add_argument('--organization'); s.add_argument('--limit', type=int, default=25); s.add_argument('--json', action='store_true'); s.set_defaults(func=cmd_list_webhook_subscriptions)
    s = sub.add_parser('create-webhook-subscription'); s.add_argument('--callback-url', required=True); s.add_argument('--event', action='append', required=True, help='Repeatable: invitee.created, invitee.canceled, etc.'); s.add_argument('--organization'); s.add_argument('--user'); s.add_argument('--signing-key'); s.set_defaults(func=cmd_create_webhook_subscription)

    s = sub.add_parser('sync-event-to-crm'); s.add_argument('--event-uri', required=True); s.add_argument('--create-task', action='store_true'); s.set_defaults(func=cmd_sync_event_to_crm)
    s = sub.add_parser('sync-webhook-to-crm'); s.add_argument('--file'); s.add_argument('--event-uri'); s.add_argument('--create-task', action='store_true'); s.set_defaults(func=cmd_sync_webhook_to_crm)
    s = sub.add_parser('push-crm-person-to-contact'); s.add_argument('--person-id', required=True); s.set_defaults(func=cmd_push_crm_person_to_contact)
    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except Exception as e:
        print(f'ERROR: {e}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
