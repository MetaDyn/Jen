#!/usr/bin/env python3
import argparse
import json
import sys
import urllib.request
from pathlib import Path
from typing import Any, Dict, Optional

API_URL = 'https://crm.metadyn.xyz/graphql'
TOKEN_PATH = Path('/home/jza/.openclaw/.secrets/metadyn-crm-api-key')


def gql(query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    token = TOKEN_PATH.read_text().strip()
    payload = json.dumps({'query': query, 'variables': variables or {}}).encode()
    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}',
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    if 'errors' in data:
        raise RuntimeError(json.dumps(data['errors'], indent=2))
    return data['data']


def compact(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: compact(v) for k, v in obj.items() if v is not None}
    if isinstance(obj, list):
        return [compact(v) for v in obj if v is not None]
    return obj


def _link_value(obj: Optional[Dict[str, Any]]) -> str:
    obj = obj or {}
    return obj.get('primaryLinkLabel') or obj.get('primaryLinkUrl') or '-'


def _full_name(person_name: Optional[Dict[str, Any]]) -> str:
    person_name = person_name or {}
    return ' '.join(x for x in [person_name.get('firstName'), person_name.get('lastName')] if x) or '-'


def _links_input(label: Optional[str], url: Optional[str]) -> Optional[Dict[str, Any]]:
    if not label and not url:
        return None
    return compact({'primaryLinkLabel': label, 'primaryLinkUrl': url})


def _emails_input(primary: Optional[str]) -> Optional[Dict[str, Any]]:
    if not primary:
        return None
    return {'primaryEmail': primary}


def _full_name_input(first: Optional[str], last: Optional[str]) -> Optional[Dict[str, Any]]:
    if not first and not last:
        return None
    return compact({'firstName': first, 'lastName': last})


def cmd_list_companies(args: argparse.Namespace) -> int:
    query = '''
    query ListCompanies($first: Int!, $offset: Int!) {
      companies(first: $first, offset: $offset, orderBy: [{name: AscNullsLast}]) {
        totalCount
        edges {
          node {
            id
            name
            domainName { primaryLinkUrl primaryLinkLabel }
            employees
            linkedinLink { primaryLinkUrl primaryLinkLabel }
            xLink { primaryLinkUrl primaryLinkLabel }
            idealCustomerProfile
            createdAt
            updatedAt
          }
        }
      }
    }
    '''
    data = gql(query, {'first': args.limit, 'offset': args.offset})['companies']
    print(f"totalCount: {data['totalCount']}")
    for i, edge in enumerate(data['edges'], start=1 + args.offset):
        node = edge['node']
        print(
            f"{i}. {node['name']} | id={node['id']} | domain={_link_value(node.get('domainName'))} | "
            f"employees={node.get('employees') or '-'} | ICP={node.get('idealCustomerProfile')} | "
            f"linkedin={_link_value(node.get('linkedinLink'))}"
        )
    return 0


def cmd_search_companies(args: argparse.Namespace) -> int:
    query = '''
    query SearchCompanies($term: String!, $first: Int!) {
      companies(first: $first, filter: { or: [
        { name: { ilike: $term } },
        { domainName: { primaryLinkLabel: { ilike: $term } } },
        { domainName: { primaryLinkUrl: { ilike: $term } } }
      ]}, orderBy: [{name: AscNullsLast}]) {
        totalCount
        edges {
          node {
            id
            name
            domainName { primaryLinkUrl primaryLinkLabel }
            employees
            idealCustomerProfile
          }
        }
      }
    }
    '''
    term = f"%{args.term}%"
    data = gql(query, {'term': term, 'first': args.limit})['companies']
    print(f"matches: {data['totalCount']}")
    for edge in data['edges']:
        node = edge['node']
        print(f"- {node['name']} | id={node['id']} | domain={_link_value(node.get('domainName'))} | employees={node.get('employees') or '-'} | ICP={node.get('idealCustomerProfile')}")
    return 0


def cmd_get_company(args: argparse.Namespace) -> int:
    if args.id:
        filter_input = {'id': {'eq': args.id}}
    else:
        filter_input = {'name': {'ilike': args.name}}
    query = '''
    query GetCompany($filter: CompanyFilterInput!) {
      company(filter: $filter) {
        id
        name
        domainName { primaryLinkUrl primaryLinkLabel }
        employees
        linkedinLink { primaryLinkUrl primaryLinkLabel }
        xLink { primaryLinkUrl primaryLinkLabel }
        idealCustomerProfile
        createdAt
        updatedAt
        people(first: 20) {
          totalCount
          edges { node { id name { firstName lastName } emails { primaryEmail } jobTitle } }
        }
        accountOwner { id }
      }
    }
    '''
    node = gql(query, {'filter': filter_input})['company']
    print(json.dumps(node, indent=2))
    return 0


def cmd_create_company(args: argparse.Namespace) -> int:
    mutation = '''
    mutation CreateCompany($data: CompanyCreateInput!) {
      createCompany(data: $data) {
        id
        name
        domainName { primaryLinkUrl primaryLinkLabel }
        employees
        idealCustomerProfile
        createdAt
      }
    }
    '''
    data = compact({
        'name': args.name,
        'domainName': _links_input(args.domain_label, args.domain_url),
        'linkedinLink': _links_input(args.linkedin_label, args.linkedin_url),
        'xLink': _links_input(args.x_label, args.x_url),
        'employees': args.employees,
        'idealCustomerProfile': args.icp,
    })
    result = gql(mutation, {'data': data})['createCompany']
    print(json.dumps(result, indent=2))
    return 0


def cmd_update_company(args: argparse.Namespace) -> int:
    mutation = '''
    mutation UpdateCompany($id: UUID!, $data: CompanyUpdateInput!) {
      updateCompany(id: $id, data: $data) {
        id
        name
        domainName { primaryLinkUrl primaryLinkLabel }
        employees
        linkedinLink { primaryLinkUrl primaryLinkLabel }
        xLink { primaryLinkUrl primaryLinkLabel }
        idealCustomerProfile
        updatedAt
      }
    }
    '''
    data = compact({
        'name': args.name,
        'domainName': _links_input(args.domain_label, args.domain_url),
        'linkedinLink': _links_input(args.linkedin_label, args.linkedin_url),
        'xLink': _links_input(args.x_label, args.x_url),
        'employees': args.employees,
        'idealCustomerProfile': args.icp,
    })
    result = gql(mutation, {'id': args.id, 'data': data})['updateCompany']
    print(json.dumps(result, indent=2))
    return 0


def cmd_list_people(args: argparse.Namespace) -> int:
    filter_input = None
    if args.company_id:
        filter_input = {'companyId': {'eq': args.company_id}}
    query = '''
    query ListPeople($first: Int!, $offset: Int!, $filter: PersonFilterInput) {
      people(first: $first, offset: $offset, filter: $filter, orderBy: [{createdAt: DescNullsLast}]) {
        totalCount
        edges {
          node {
            id
            name { firstName lastName }
            emails { primaryEmail }
            jobTitle
            city
            company { id name }
            createdAt
          }
        }
      }
    }
    '''
    data = gql(query, {'first': args.limit, 'offset': args.offset, 'filter': filter_input})['people']
    print(f"totalCount: {data['totalCount']}")
    for i, edge in enumerate(data['edges'], start=1 + args.offset):
        node = edge['node']
        email = (node.get('emails') or {}).get('primaryEmail') or '-'
        company = (node.get('company') or {}).get('name') or '-'
        print(f"{i}. {_full_name(node.get('name'))} | id={node['id']} | email={email} | title={node.get('jobTitle') or '-'} | city={node.get('city') or '-'} | company={company}")
    return 0


def cmd_create_person(args: argparse.Namespace) -> int:
    mutation = '''
    mutation CreatePerson($data: PersonCreateInput!) {
      createPerson(data: $data) {
        id
        name { firstName lastName }
        emails { primaryEmail }
        jobTitle
        city
        company { id name }
        createdAt
      }
    }
    '''
    data = compact({
        'name': _full_name_input(args.first_name, args.last_name),
        'emails': _emails_input(args.email),
        'jobTitle': args.job_title,
        'city': args.city,
        'companyId': args.company_id,
        'linkedinLink': _links_input(args.linkedin_label, args.linkedin_url),
        'xLink': _links_input(args.x_label, args.x_url),
        'avatarUrl': args.avatar_url,
    })
    result = gql(mutation, {'data': data})['createPerson']
    print(json.dumps(result, indent=2))
    return 0


def cmd_update_person(args: argparse.Namespace) -> int:
    mutation = '''
    mutation UpdatePerson($id: UUID!, $data: PersonUpdateInput!) {
      updatePerson(id: $id, data: $data) {
        id
        name { firstName lastName }
        emails { primaryEmail }
        jobTitle
        city
        company { id name }
        updatedAt
      }
    }
    '''
    data = compact({
        'name': _full_name_input(args.first_name, args.last_name),
        'emails': _emails_input(args.email),
        'jobTitle': args.job_title,
        'city': args.city,
        'companyId': args.company_id,
        'linkedinLink': _links_input(args.linkedin_label, args.linkedin_url),
        'xLink': _links_input(args.x_label, args.x_url),
        'avatarUrl': args.avatar_url,
    })
    result = gql(mutation, {'id': args.id, 'data': data})['updatePerson']
    print(json.dumps(result, indent=2))
    return 0


def cmd_list_notes(args: argparse.Namespace) -> int:
    if not args.company_id and not args.person_id:
        raise RuntimeError('Provide --company-id or --person-id')
    filter_input = compact({
        'targetCompanyId': {'eq': args.company_id} if args.company_id else None,
        'targetPersonId': {'eq': args.person_id} if args.person_id else None,
    })
    query = '''
    query ListNoteTargets($first: Int!, $filter: NoteTargetFilterInput!) {
      noteTargets(first: $first, filter: $filter, orderBy: [{createdAt: DescNullsLast}]) {
        totalCount
        edges {
          node {
            id
            createdAt
            targetCompany { id name }
            targetPerson { id name { firstName lastName } }
            note {
              id
              title
              createdAt
              bodyV2 { markdown }
            }
          }
        }
      }
    }
    '''
    data = gql(query, {'first': args.limit, 'filter': filter_input})['noteTargets']
    print(f"totalCount: {data['totalCount']}")
    for edge in data['edges']:
        node = edge['node']
        note = node.get('note')
        if not note:
            continue
        target = (node.get('targetCompany') or {}).get('name') or _full_name((node.get('targetPerson') or {}).get('name'))
        markdown = ((note.get('bodyV2') or {}).get('markdown') or '').replace('\n', ' ')[:120]
        print(f"- {note['title'] or '(untitled)'} | noteId={note['id']} | target={target or '-'} | createdAt={note.get('createdAt')} | body={markdown}")
    return 0


def cmd_create_note(args: argparse.Namespace) -> int:
    create_note_mutation = '''
    mutation CreateNote($data: NoteCreateInput!) {
      createNote(data: $data) { id title createdAt }
    }
    '''
    note_data = {
        'title': args.title,
        'bodyV2': {'markdown': args.body},
    }
    note = gql(create_note_mutation, {'data': note_data})['createNote']

    target_mutation = '''
    mutation CreateNoteTarget($data: NoteTargetCreateInput!) {
      createNoteTarget(data: $data) {
        id
        note { id title }
        targetCompany { id name }
        targetPerson { id name { firstName lastName } }
      }
    }
    '''
    target_data: Dict[str, Any] = {'noteId': note['id']}
    if args.company_id:
        target_data['targetCompanyId'] = args.company_id
    if args.person_id:
        target_data['targetPersonId'] = args.person_id
    target = gql(target_mutation, {'data': target_data})['createNoteTarget'] if (args.company_id or args.person_id) else None

    print(json.dumps({'note': note, 'target': target}, indent=2))
    return 0


def cmd_create_task(args: argparse.Namespace) -> int:
    mutation = '''
    mutation CreateTask($data: TaskCreateInput!) {
      createTask(data: $data) {
        id
        title
        dueAt
        status
        createdAt
      }
    }
    '''
    data = compact({
        'title': args.title,
        'bodyV2': {'markdown': args.body} if args.body else None,
        'dueAt': args.due_at,
        'status': args.status,
    })
    task = gql(mutation, {'data': data})['createTask']

    target_mutation = '''
    mutation CreateTaskTarget($data: TaskTargetCreateInput!) {
      createTaskTarget(data: $data) {
        id
        task { id title }
        targetCompany { id name }
        targetPerson { id name { firstName lastName } }
      }
    }
    '''
    target_data = compact({
        'taskId': task['id'],
        'targetCompanyId': args.company_id,
        'targetPersonId': args.person_id,
    })
    target = gql(target_mutation, {'data': target_data})['createTaskTarget'] if (args.company_id or args.person_id) else None
    print(json.dumps({'task': task, 'target': target}, indent=2))
    return 0


def build_rpc_map() -> Dict[str, Any]:
    return {
        'company.list': cmd_list_companies,
        'company.search': cmd_search_companies,
        'company.get': cmd_get_company,
        'company.create': cmd_create_company,
        'company.update': cmd_update_company,
        'person.list': cmd_list_people,
        'person.create': cmd_create_person,
        'person.update': cmd_update_person,
        'note.list': cmd_list_notes,
        'note.create': cmd_create_note,
        'task.create': cmd_create_task,
    }


def cmd_rpc(args: argparse.Namespace) -> int:
    payload = json.loads(args.json) if args.json else json.load(sys.stdin)
    operation = payload['operation']
    params = payload.get('params', {})
    ns = argparse.Namespace(**params)
    func = build_rpc_map().get(operation)
    if not func:
        raise RuntimeError(f'Unknown operation: {operation}')
    return func(ns)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='MetaDyn Twenty CRM helper')
    sub = parser.add_subparsers(dest='command', required=True)

    p = sub.add_parser('list-companies', help='List companies')
    p.add_argument('--limit', type=int, default=25)
    p.add_argument('--offset', type=int, default=0)
    p.set_defaults(func=cmd_list_companies)

    p = sub.add_parser('search-companies', help='Search companies by name/domain')
    p.add_argument('term')
    p.add_argument('--limit', type=int, default=25)
    p.set_defaults(func=cmd_search_companies)

    p = sub.add_parser('get-company', help='Get one company by id or name filter')
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument('--id')
    group.add_argument('--name')
    p.set_defaults(func=cmd_get_company)

    p = sub.add_parser('create-company', help='Create a company')
    p.add_argument('--name', required=True)
    p.add_argument('--domain-label')
    p.add_argument('--domain-url')
    p.add_argument('--linkedin-label')
    p.add_argument('--linkedin-url')
    p.add_argument('--x-label')
    p.add_argument('--x-url')
    p.add_argument('--employees', type=float)
    p.add_argument('--icp', action='store_true')
    p.set_defaults(func=cmd_create_company)

    p = sub.add_parser('update-company', help='Update a company')
    p.add_argument('--id', required=True)
    p.add_argument('--name')
    p.add_argument('--domain-label')
    p.add_argument('--domain-url')
    p.add_argument('--linkedin-label')
    p.add_argument('--linkedin-url')
    p.add_argument('--x-label')
    p.add_argument('--x-url')
    p.add_argument('--employees', type=float)
    p.add_argument('--icp', action='store_true')
    p.set_defaults(func=cmd_update_company)

    p = sub.add_parser('list-people', help='List people, optionally scoped to a company')
    p.add_argument('--company-id')
    p.add_argument('--limit', type=int, default=25)
    p.add_argument('--offset', type=int, default=0)
    p.set_defaults(func=cmd_list_people)

    p = sub.add_parser('create-person', help='Create a person')
    p.add_argument('--first-name')
    p.add_argument('--last-name')
    p.add_argument('--email')
    p.add_argument('--job-title')
    p.add_argument('--city')
    p.add_argument('--company-id')
    p.add_argument('--linkedin-label')
    p.add_argument('--linkedin-url')
    p.add_argument('--x-label')
    p.add_argument('--x-url')
    p.add_argument('--avatar-url')
    p.set_defaults(func=cmd_create_person)

    p = sub.add_parser('update-person', help='Update a person')
    p.add_argument('--id', required=True)
    p.add_argument('--first-name')
    p.add_argument('--last-name')
    p.add_argument('--email')
    p.add_argument('--job-title')
    p.add_argument('--city')
    p.add_argument('--company-id')
    p.add_argument('--linkedin-label')
    p.add_argument('--linkedin-url')
    p.add_argument('--x-label')
    p.add_argument('--x-url')
    p.add_argument('--avatar-url')
    p.set_defaults(func=cmd_update_person)

    p = sub.add_parser('list-notes', help='List notes attached to a company or person')
    p.add_argument('--company-id')
    p.add_argument('--person-id')
    p.add_argument('--limit', type=int, default=25)
    p.set_defaults(func=cmd_list_notes)

    p = sub.add_parser('create-note', help='Create a note and optionally attach it to a company/person')
    p.add_argument('--title', required=True)
    p.add_argument('--body', required=True)
    p.add_argument('--company-id')
    p.add_argument('--person-id')
    p.set_defaults(func=cmd_create_note)

    p = sub.add_parser('create-task', help='Create a task and optionally attach it to a company/person')
    p.add_argument('--title', required=True)
    p.add_argument('--body')
    p.add_argument('--due-at')
    p.add_argument('--status', default='TODO', choices=['TODO', 'IN_PROGRESS', 'DONE'])
    p.add_argument('--company-id')
    p.add_argument('--person-id')
    p.set_defaults(func=cmd_create_task)

    p = sub.add_parser('rpc', help='MCP-style JSON operation wrapper')
    p.add_argument('--json', help='JSON payload with operation + params; otherwise read from stdin')
    p.set_defaults(func=cmd_rpc)

    return parser


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
