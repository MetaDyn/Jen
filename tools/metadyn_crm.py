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


def _link_value(obj: Optional[Dict[str, Any]]) -> str:
    obj = obj or {}
    return obj.get('primaryLinkLabel') or obj.get('primaryLinkUrl') or '-'


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
        name = ' '.join(x for x in [node['name'].get('firstName'), node['name'].get('lastName')] if x) or '-'
        email = (node.get('emails') or {}).get('primaryEmail') or '-'
        company = (node.get('company') or {}).get('name') or '-'
        print(f"{i}. {name} | id={node['id']} | email={email} | title={node.get('jobTitle') or '-'} | city={node.get('city') or '-'} | company={company}")
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

    p = sub.add_parser('list-people', help='List people, optionally scoped to a company')
    p.add_argument('--company-id')
    p.add_argument('--limit', type=int, default=25)
    p.add_argument('--offset', type=int, default=0)
    p.set_defaults(func=cmd_list_people)

    p = sub.add_parser('create-note', help='Create a note and optionally attach it to a company/person')
    p.add_argument('--title', required=True)
    p.add_argument('--body', required=True)
    p.add_argument('--company-id')
    p.add_argument('--person-id')
    p.set_defaults(func=cmd_create_note)

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
