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
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'},
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


def _workspace_member_name(member_name: Optional[Dict[str, Any]]) -> str:
    return _full_name(member_name)


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


def _currency_input(amount: Optional[float], currency: Optional[str]) -> Optional[Dict[str, Any]]:
    if amount is None and not currency:
        return None
    return compact({'amountMicros': int((amount or 0) * 1_000_000), 'currencyCode': currency or 'USD'})


def _print_json(data: Any) -> int:
    print(json.dumps(data, indent=2))
    return 0


def cmd_list_companies(args: argparse.Namespace) -> int:
    query = '''
    query ListCompanies($first: Int!, $offset: Int!) {
      companies(first: $first, offset: $offset, orderBy: [{name: AscNullsLast}]) {
        totalCount
        edges { node { id name domainName { primaryLinkUrl primaryLinkLabel } employees linkedinLink { primaryLinkUrl primaryLinkLabel } xLink { primaryLinkUrl primaryLinkLabel } idealCustomerProfile createdAt updatedAt } }
      }
    }
    '''
    data = gql(query, {'first': args.limit, 'offset': args.offset})['companies']
    print(f"totalCount: {data['totalCount']}")
    for i, edge in enumerate(data['edges'], start=1 + args.offset):
        node = edge['node']
        print(f"{i}. {node['name']} | id={node['id']} | domain={_link_value(node.get('domainName'))} | employees={node.get('employees') or '-'} | ICP={node.get('idealCustomerProfile')} | linkedin={_link_value(node.get('linkedinLink'))}")
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
        edges { node { id name domainName { primaryLinkUrl primaryLinkLabel } employees idealCustomerProfile } }
      }
    }
    '''
    data = gql(query, {'term': f"%{args.term}%", 'first': args.limit})['companies']
    print(f"matches: {data['totalCount']}")
    for edge in data['edges']:
        node = edge['node']
        print(f"- {node['name']} | id={node['id']} | domain={_link_value(node.get('domainName'))} | employees={node.get('employees') or '-'} | ICP={node.get('idealCustomerProfile')}")
    return 0


def cmd_get_company(args: argparse.Namespace) -> int:
    filter_input = {'id': {'eq': args.id}} if args.id else {'name': {'ilike': args.name}}
    query = '''
    query GetCompany($filter: CompanyFilterInput!) {
      company(filter: $filter) {
        id name domainName { primaryLinkUrl primaryLinkLabel } employees linkedinLink { primaryLinkUrl primaryLinkLabel } xLink { primaryLinkUrl primaryLinkLabel } idealCustomerProfile createdAt updatedAt
        people(first: 20) { totalCount edges { node { id name { firstName lastName } emails { primaryEmail } jobTitle } } }
        accountOwner { id }
      }
    }
    '''
    return _print_json(gql(query, {'filter': filter_input})['company'])


def cmd_create_company(args: argparse.Namespace) -> int:
    mutation = '''mutation CreateCompany($data: CompanyCreateInput!) { createCompany(data: $data) { id name domainName { primaryLinkUrl primaryLinkLabel } employees idealCustomerProfile createdAt } }'''
    data = compact({'name': args.name, 'domainName': _links_input(args.domain_label, args.domain_url), 'linkedinLink': _links_input(args.linkedin_label, args.linkedin_url), 'xLink': _links_input(args.x_label, args.x_url), 'employees': args.employees, 'idealCustomerProfile': args.icp})
    return _print_json(gql(mutation, {'data': data})['createCompany'])


def cmd_update_company(args: argparse.Namespace) -> int:
    mutation = '''mutation UpdateCompany($id: UUID!, $data: CompanyUpdateInput!) { updateCompany(id: $id, data: $data) { id name domainName { primaryLinkUrl primaryLinkLabel } employees linkedinLink { primaryLinkUrl primaryLinkLabel } xLink { primaryLinkUrl primaryLinkLabel } idealCustomerProfile updatedAt } }'''
    data = compact({'name': args.name, 'domainName': _links_input(args.domain_label, args.domain_url), 'linkedinLink': _links_input(args.linkedin_label, args.linkedin_url), 'xLink': _links_input(args.x_label, args.x_url), 'employees': args.employees, 'idealCustomerProfile': args.icp})
    return _print_json(gql(mutation, {'id': args.id, 'data': data})['updateCompany'])


def cmd_list_people(args: argparse.Namespace) -> int:
    filter_input = {'companyId': {'eq': args.company_id}} if args.company_id else None
    query = '''
    query ListPeople($first: Int!, $offset: Int!, $filter: PersonFilterInput) {
      people(first: $first, offset: $offset, filter: $filter, orderBy: [{createdAt: DescNullsLast}]) {
        totalCount
        edges { node { id name { firstName lastName } emails { primaryEmail } jobTitle city company { id name } createdAt } }
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


def cmd_list_team(args: argparse.Namespace) -> int:
    query = '''
    query ListWorkspaceMembers($first: Int!, $offset: Int!, $filter: WorkspaceMemberFilterInput) {
      workspaceMembers(first: $first, offset: $offset, filter: $filter, orderBy: [{userEmail: AscNullsLast}]) {
        totalCount
        edges { node { id name { firstName lastName } userEmail timeZone avatarUrl } }
      }
    }
    '''
    filter_bits = []
    if args.term:
        term = f"%{args.term}%"
        filter_bits.append({'or': [
            {'userEmail': {'ilike': term}},
            {'name': {'firstName': {'ilike': term}}},
            {'name': {'lastName': {'ilike': term}}},
        ]})
    filter_input = {'and': filter_bits} if len(filter_bits) > 1 else (filter_bits[0] if filter_bits else None)
    data = gql(query, {'first': args.limit, 'offset': args.offset, 'filter': filter_input})['workspaceMembers']
    print(f"totalCount: {data['totalCount']}")
    for i, edge in enumerate(data['edges'], start=1 + args.offset):
        node = edge['node']
        print(f"{i}. {_workspace_member_name(node.get('name'))} | id={node['id']} | email={node.get('userEmail') or '-'} | timezone={node.get('timeZone') or '-'}")
    return 0


def cmd_create_person(args: argparse.Namespace) -> int:
    mutation = '''mutation CreatePerson($data: PersonCreateInput!) { createPerson(data: $data) { id name { firstName lastName } emails { primaryEmail } jobTitle city company { id name } createdAt } }'''
    data = compact({'name': _full_name_input(args.first_name, args.last_name), 'emails': _emails_input(args.email), 'jobTitle': args.job_title, 'city': args.city, 'companyId': args.company_id, 'linkedinLink': _links_input(args.linkedin_label, args.linkedin_url), 'xLink': _links_input(args.x_label, args.x_url), 'avatarUrl': args.avatar_url})
    return _print_json(gql(mutation, {'data': data})['createPerson'])


def cmd_update_person(args: argparse.Namespace) -> int:
    mutation = '''mutation UpdatePerson($id: UUID!, $data: PersonUpdateInput!) { updatePerson(id: $id, data: $data) { id name { firstName lastName } emails { primaryEmail } jobTitle city company { id name } updatedAt } }'''
    data = compact({'name': _full_name_input(args.first_name, args.last_name), 'emails': _emails_input(args.email), 'jobTitle': args.job_title, 'city': args.city, 'companyId': args.company_id, 'linkedinLink': _links_input(args.linkedin_label, args.linkedin_url), 'xLink': _links_input(args.x_label, args.x_url), 'avatarUrl': args.avatar_url})
    return _print_json(gql(mutation, {'id': args.id, 'data': data})['updatePerson'])


def cmd_list_notes(args: argparse.Namespace) -> int:
    filters = []
    if args.company_id:
        filters.append({'targetCompanyId': {'eq': args.company_id}})
    if args.person_id:
        filters.append({'targetPersonId': {'eq': args.person_id}})
    query = '''
    query ListNoteTargets($first: Int!, $filter: NoteTargetFilterInput) {
      noteTargets(first: $first, filter: $filter, orderBy: [{createdAt: DescNullsLast}]) {
        totalCount
        edges { node { id createdAt targetCompany { id name } targetPerson { id name { firstName lastName } } note { id title createdAt bodyV2 { markdown } } } }
      }
    }
    '''
    filter_input = {'or': filters} if len(filters) > 1 else (filters[0] if filters else None)
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
    note = gql('''mutation CreateNote($data: NoteCreateInput!) { createNote(data: $data) { id title createdAt } }''', {'data': {'title': args.title, 'bodyV2': {'markdown': args.body}}})['createNote']
    target = None
    if args.company_id or args.person_id:
        target_data = compact({'noteId': note['id'], 'targetCompanyId': args.company_id, 'targetPersonId': args.person_id})
        target = gql('''mutation CreateNoteTarget($data: NoteTargetCreateInput!) { createNoteTarget(data: $data) { id note { id title } targetCompany { id name } targetPerson { id name { firstName lastName } } } }''', {'data': target_data})['createNoteTarget']
    return _print_json({'note': note, 'target': target})


def cmd_update_note(args: argparse.Namespace) -> int:
    data = compact({'title': args.title, 'bodyV2': {'markdown': args.body} if args.body is not None else None})
    return _print_json(gql('''mutation UpdateNote($id: UUID!, $data: NoteUpdateInput!) { updateNote(id: $id, data: $data) { id title updatedAt bodyV2 { markdown } } }''', {'id': args.id, 'data': data})['updateNote'])


def cmd_delete_note(args: argparse.Namespace) -> int:
    return _print_json(gql('''mutation DeleteNote($id: UUID!) { deleteNote(id: $id) { id title deletedAt } }''', {'id': args.id})['deleteNote'])


def cmd_list_tasks(args: argparse.Namespace) -> int:
    filters = []
    if args.company_id:
        filters.append({'targetCompanyId': {'eq': args.company_id}})
    if args.person_id:
        filters.append({'targetPersonId': {'eq': args.person_id}})
    if args.opportunity_id:
        filters.append({'targetOpportunityId': {'eq': args.opportunity_id}})
    if args.status:
        task_filter = {'status': {'eq': args.status}}
    else:
        task_filter = None
    query = '''
    query ListTasks($first: Int!, $taskFilter: TaskFilterInput, $targetFilter: TaskTargetFilterInput) {
      taskTargets(first: $first, filter: $targetFilter, orderBy: [{createdAt: DescNullsLast}]) {
        totalCount
        edges { node { id targetCompany { id name } targetPerson { id name { firstName lastName } } targetOpportunity { id name } task { id title status dueAt createdAt bodyV2 { markdown } } } }
      }
      tasks(first: $first, filter: $taskFilter, orderBy: [{createdAt: DescNullsLast}]) {
        totalCount
        edges { node { id title status dueAt createdAt bodyV2 { markdown } } }
      }
    }
    '''
    target_filter = {'or': filters} if len(filters) > 1 else (filters[0] if filters else None)
    data = gql(query, {'first': args.limit, 'taskFilter': task_filter, 'targetFilter': target_filter})
    if target_filter:
        out = data['taskTargets']
        print(f"totalCount: {out['totalCount']}")
        for edge in out['edges']:
            node = edge['node']
            task = node.get('task')
            if not task:
                continue
            target = (node.get('targetCompany') or {}).get('name') or _full_name((node.get('targetPerson') or {}).get('name')) or (node.get('targetOpportunity') or {}).get('name') or '-'
            body = ((task.get('bodyV2') or {}).get('markdown') or '').replace('\n', ' ')[:100]
            print(f"- {task['title']} | taskId={task['id']} | status={task['status']} | dueAt={task.get('dueAt') or '-'} | target={target} | body={body}")
    else:
        out = data['tasks']
        print(f"totalCount: {out['totalCount']}")
        for edge in out['edges']:
            task = edge['node']
            body = ((task.get('bodyV2') or {}).get('markdown') or '').replace('\n', ' ')[:100]
            print(f"- {task['title']} | taskId={task['id']} | status={task['status']} | dueAt={task.get('dueAt') or '-'} | body={body}")
    return 0


def cmd_create_task(args: argparse.Namespace) -> int:
    data = compact({'title': args.title, 'bodyV2': {'markdown': args.body} if args.body else None, 'dueAt': args.due_at, 'status': args.status})
    task = gql('''mutation CreateTask($data: TaskCreateInput!) { createTask(data: $data) { id title dueAt status createdAt } }''', {'data': data})['createTask']
    target = None
    if args.company_id or args.person_id or args.opportunity_id:
        target_data = compact({'taskId': task['id'], 'targetCompanyId': args.company_id, 'targetPersonId': args.person_id, 'targetOpportunityId': args.opportunity_id})
        target = gql('''mutation CreateTaskTarget($data: TaskTargetCreateInput!) { createTaskTarget(data: $data) { id task { id title } targetCompany { id name } targetPerson { id name { firstName lastName } } targetOpportunity { id name } } }''', {'data': target_data})['createTaskTarget']
    return _print_json({'task': task, 'target': target})


def cmd_update_task(args: argparse.Namespace) -> int:
    data = compact({'title': args.title, 'bodyV2': {'markdown': args.body} if args.body is not None else None, 'dueAt': args.due_at, 'status': args.status, 'assigneeId': args.assignee_id})
    return _print_json(gql('''mutation UpdateTask($id: UUID!, $data: TaskUpdateInput!) { updateTask(id: $id, data: $data) { id title status dueAt updatedAt assignee { id name { firstName lastName } userEmail } bodyV2 { markdown } } }''', {'id': args.id, 'data': data})['updateTask'])


def cmd_list_opportunities(args: argparse.Namespace) -> int:
    filter_bits = []
    if args.company_id:
        filter_bits.append({'companyId': {'eq': args.company_id}})
    if args.person_id:
        filter_bits.append({'pointOfContactId': {'eq': args.person_id}})
    if args.stage:
        filter_bits.append({'stage': {'eq': args.stage}})
    if args.term:
        filter_bits.append({'name': {'ilike': f"%{args.term}%"}})
    filter_input = {'and': filter_bits} if len(filter_bits) > 1 else (filter_bits[0] if filter_bits else None)
    query = '''
    query ListOpportunities($first: Int!, $filter: OpportunityFilterInput) {
      opportunities(first: $first, filter: $filter, orderBy: [{closeDate: AscNullsLast}]) {
        totalCount
        edges { node { id name closeDate stage company { id name } pointOfContact { id name { firstName lastName } } owner { id name { firstName lastName } userEmail } amount { amountMicros currencyCode } } }
      }
    }
    '''
    data = gql(query, {'first': args.limit, 'filter': filter_input})['opportunities']
    print(f"totalCount: {data['totalCount']}")
    for edge in data['edges']:
        node = edge['node']
        amount = node.get('amount') or {}
        amount_str = f"{amount.get('currencyCode','USD')} {((amount.get('amountMicros') or 0)/1_000_000):,.2f}" if amount else '-'
        company = (node.get('company') or {}).get('name') or '-'
        poc = _full_name((node.get('pointOfContact') or {}).get('name'))
        owner = _workspace_member_name((node.get('owner') or {}).get('name'))
        owner_email = (node.get('owner') or {}).get('userEmail') or '-'
        print(f"- {node['name']} | id={node['id']} | stage={node['stage']} | closeDate={node.get('closeDate') or '-'} | company={company} | pointOfContact={poc} | owner={owner} <{owner_email}> | amount={amount_str}")
    return 0


def cmd_create_opportunity(args: argparse.Namespace) -> int:
    data = compact({'name': args.name, 'closeDate': args.close_date, 'stage': args.stage, 'amount': _currency_input(args.amount, args.currency), 'companyId': args.company_id, 'pointOfContactId': args.person_id, 'ownerId': args.owner_id})
    return _print_json(gql('''mutation CreateOpportunity($data: OpportunityCreateInput!) { createOpportunity(data: $data) { id name closeDate stage company { id name } pointOfContact { id name { firstName lastName } } owner { id name { firstName lastName } userEmail } amount { amountMicros currencyCode } createdAt } }''', {'data': data})['createOpportunity'])


def cmd_update_opportunity(args: argparse.Namespace) -> int:
    data = compact({'name': args.name, 'closeDate': args.close_date, 'stage': args.stage, 'amount': _currency_input(args.amount, args.currency), 'companyId': args.company_id, 'pointOfContactId': args.person_id, 'ownerId': args.owner_id})
    return _print_json(gql('''mutation UpdateOpportunity($id: UUID!, $data: OpportunityUpdateInput!) { updateOpportunity(id: $id, data: $data) { id name closeDate stage company { id name } pointOfContact { id name { firstName lastName } } owner { id name { firstName lastName } userEmail } amount { amountMicros currencyCode } updatedAt } }''', {'id': args.id, 'data': data})['updateOpportunity'])


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
        'team.list': cmd_list_team,
        'note.list': cmd_list_notes,
        'note.create': cmd_create_note,
        'note.update': cmd_update_note,
        'note.delete': cmd_delete_note,
        'task.list': cmd_list_tasks,
        'task.create': cmd_create_task,
        'task.update': cmd_update_task,
        'opportunity.list': cmd_list_opportunities,
        'opportunity.create': cmd_create_opportunity,
        'opportunity.update': cmd_update_opportunity,
    }


def cmd_rpc(args: argparse.Namespace) -> int:
    payload = json.loads(args.json) if args.json else json.load(sys.stdin)
    func = build_rpc_map().get(payload['operation'])
    if not func:
        raise RuntimeError(f"Unknown operation: {payload['operation']}")
    params = payload.get('params', {})
    defaults = {
        'limit': 25,
        'offset': 0,
        'company_id': None,
        'person_id': None,
        'owner_id': None,
        'opportunity_id': None,
        'status': None,
        'term': None,
        'name': None,
        'id': None,
        'title': None,
        'body': None,
        'due_at': None,
        'assignee_id': None,
        'close_date': None,
        'stage': None,
        'amount': None,
        'currency': 'USD',
        'domain_label': None,
        'domain_url': None,
        'linkedin_label': None,
        'linkedin_url': None,
        'x_label': None,
        'x_url': None,
        'employees': None,
        'icp': None,
        'first_name': None,
        'last_name': None,
        'email': None,
        'job_title': None,
        'city': None,
        'avatar_url': None,
    }
    defaults.update(params)
    return func(argparse.Namespace(**defaults))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='MetaDyn Twenty CRM helper')
    sub = parser.add_subparsers(dest='command', required=True)

    p = sub.add_parser('list-companies'); p.add_argument('--limit', type=int, default=25); p.add_argument('--offset', type=int, default=0); p.set_defaults(func=cmd_list_companies)
    p = sub.add_parser('search-companies'); p.add_argument('term'); p.add_argument('--limit', type=int, default=25); p.set_defaults(func=cmd_search_companies)
    p = sub.add_parser('get-company'); g = p.add_mutually_exclusive_group(required=True); g.add_argument('--id'); g.add_argument('--name'); p.set_defaults(func=cmd_get_company)
    p = sub.add_parser('create-company'); p.add_argument('--name', required=True); p.add_argument('--domain-label'); p.add_argument('--domain-url'); p.add_argument('--linkedin-label'); p.add_argument('--linkedin-url'); p.add_argument('--x-label'); p.add_argument('--x-url'); p.add_argument('--employees', type=float); p.add_argument('--icp', action='store_true'); p.set_defaults(func=cmd_create_company)
    p = sub.add_parser('update-company'); p.add_argument('--id', required=True); p.add_argument('--name'); p.add_argument('--domain-label'); p.add_argument('--domain-url'); p.add_argument('--linkedin-label'); p.add_argument('--linkedin-url'); p.add_argument('--x-label'); p.add_argument('--x-url'); p.add_argument('--employees', type=float); p.add_argument('--icp', action='store_true'); p.set_defaults(func=cmd_update_company)
    p = sub.add_parser('list-people'); p.add_argument('--company-id'); p.add_argument('--limit', type=int, default=25); p.add_argument('--offset', type=int, default=0); p.set_defaults(func=cmd_list_people)
    p = sub.add_parser('list-team'); p.add_argument('--term'); p.add_argument('--limit', type=int, default=25); p.add_argument('--offset', type=int, default=0); p.set_defaults(func=cmd_list_team)
    p = sub.add_parser('create-person'); p.add_argument('--first-name'); p.add_argument('--last-name'); p.add_argument('--email'); p.add_argument('--job-title'); p.add_argument('--city'); p.add_argument('--company-id'); p.add_argument('--linkedin-label'); p.add_argument('--linkedin-url'); p.add_argument('--x-label'); p.add_argument('--x-url'); p.add_argument('--avatar-url'); p.set_defaults(func=cmd_create_person)
    p = sub.add_parser('update-person'); p.add_argument('--id', required=True); p.add_argument('--first-name'); p.add_argument('--last-name'); p.add_argument('--email'); p.add_argument('--job-title'); p.add_argument('--city'); p.add_argument('--company-id'); p.add_argument('--linkedin-label'); p.add_argument('--linkedin-url'); p.add_argument('--x-label'); p.add_argument('--x-url'); p.add_argument('--avatar-url'); p.set_defaults(func=cmd_update_person)
    p = sub.add_parser('list-notes'); p.add_argument('--company-id'); p.add_argument('--person-id'); p.add_argument('--limit', type=int, default=25); p.set_defaults(func=cmd_list_notes)
    p = sub.add_parser('create-note'); p.add_argument('--title', required=True); p.add_argument('--body', required=True); p.add_argument('--company-id'); p.add_argument('--person-id'); p.set_defaults(func=cmd_create_note)
    p = sub.add_parser('update-note'); p.add_argument('--id', required=True); p.add_argument('--title'); p.add_argument('--body'); p.set_defaults(func=cmd_update_note)
    p = sub.add_parser('delete-note'); p.add_argument('--id', required=True); p.set_defaults(func=cmd_delete_note)
    p = sub.add_parser('list-tasks'); p.add_argument('--company-id'); p.add_argument('--person-id'); p.add_argument('--opportunity-id'); p.add_argument('--status', choices=['TODO','IN_PROGRESS','DONE']); p.add_argument('--limit', type=int, default=25); p.set_defaults(func=cmd_list_tasks)
    p = sub.add_parser('create-task'); p.add_argument('--title', required=True); p.add_argument('--body'); p.add_argument('--due-at'); p.add_argument('--status', default='TODO', choices=['TODO','IN_PROGRESS','DONE']); p.add_argument('--company-id'); p.add_argument('--person-id'); p.add_argument('--opportunity-id'); p.set_defaults(func=cmd_create_task)
    p = sub.add_parser('update-task'); p.add_argument('--id', required=True); p.add_argument('--title'); p.add_argument('--body'); p.add_argument('--due-at'); p.add_argument('--status', choices=['TODO','IN_PROGRESS','DONE']); p.add_argument('--assignee-id'); p.set_defaults(func=cmd_update_task)
    p = sub.add_parser('list-opportunities'); p.add_argument('--company-id'); p.add_argument('--person-id'); p.add_argument('--stage', choices=['NEW','SCREENING','MEETING','PROPOSAL','CUSTOMER']); p.add_argument('--term'); p.add_argument('--limit', type=int, default=25); p.set_defaults(func=cmd_list_opportunities)
    p = sub.add_parser('create-opportunity'); p.add_argument('--name', required=True); p.add_argument('--close-date'); p.add_argument('--stage', default='NEW', choices=['NEW','SCREENING','MEETING','PROPOSAL','CUSTOMER']); p.add_argument('--amount', type=float); p.add_argument('--currency', default='USD'); p.add_argument('--company-id'); p.add_argument('--person-id'); p.add_argument('--owner-id'); p.set_defaults(func=cmd_create_opportunity)
    p = sub.add_parser('update-opportunity'); p.add_argument('--id', required=True); p.add_argument('--name'); p.add_argument('--close-date'); p.add_argument('--stage', choices=['NEW','SCREENING','MEETING','PROPOSAL','CUSTOMER']); p.add_argument('--amount', type=float); p.add_argument('--currency', default='USD'); p.add_argument('--company-id'); p.add_argument('--person-id'); p.add_argument('--owner-id'); p.set_defaults(func=cmd_update_opportunity)
    p = sub.add_parser('rpc'); p.add_argument('--json'); p.set_defaults(func=cmd_rpc)
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
