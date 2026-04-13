#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

CLI = Path(__file__).resolve().with_name('metadyn_crm.py')

TOOLS = [
    {'name': 'company.list', 'description': 'List companies', 'inputSchema': {'type': 'object', 'properties': {'limit': {'type': 'integer'}, 'offset': {'type': 'integer'}}}},
    {'name': 'company.search', 'description': 'Search companies by term', 'inputSchema': {'type': 'object', 'properties': {'term': {'type': 'string'}, 'limit': {'type': 'integer'}}, 'required': ['term']}},
    {'name': 'company.get', 'description': 'Get company by id or name', 'inputSchema': {'type': 'object', 'properties': {'id': {'type': 'string'}, 'name': {'type': 'string'}}}},
    {'name': 'company.create', 'description': 'Create company', 'inputSchema': {'type': 'object', 'properties': {'name': {'type': 'string'}}, 'required': ['name']}},
    {'name': 'company.update', 'description': 'Update company', 'inputSchema': {'type': 'object', 'properties': {'id': {'type': 'string'}}, 'required': ['id']}},
    {'name': 'person.list', 'description': 'List people', 'inputSchema': {'type': 'object', 'properties': {'company_id': {'type': 'string'}, 'limit': {'type': 'integer'}, 'offset': {'type': 'integer'}}}},
    {'name': 'person.create', 'description': 'Create person', 'inputSchema': {'type': 'object', 'properties': {}}},
    {'name': 'person.update', 'description': 'Update person', 'inputSchema': {'type': 'object', 'properties': {'id': {'type': 'string'}}, 'required': ['id']}},
    {'name': 'note.list', 'description': 'List notes attached to a company or person', 'inputSchema': {'type': 'object', 'properties': {'company_id': {'type': 'string'}, 'person_id': {'type': 'string'}, 'limit': {'type': 'integer'}}}},
    {'name': 'note.create', 'description': 'Create note', 'inputSchema': {'type': 'object', 'properties': {'title': {'type': 'string'}, 'body': {'type': 'string'}}, 'required': ['title', 'body']}},
    {'name': 'note.update', 'description': 'Update note', 'inputSchema': {'type': 'object', 'properties': {'id': {'type': 'string'}}, 'required': ['id']}},
    {'name': 'note.delete', 'description': 'Delete note', 'inputSchema': {'type': 'object', 'properties': {'id': {'type': 'string'}}, 'required': ['id']}},
    {'name': 'task.list', 'description': 'List tasks', 'inputSchema': {'type': 'object', 'properties': {'company_id': {'type': 'string'}, 'person_id': {'type': 'string'}, 'opportunity_id': {'type': 'string'}, 'status': {'type': 'string'}, 'limit': {'type': 'integer'}}}},
    {'name': 'task.create', 'description': 'Create task', 'inputSchema': {'type': 'object', 'properties': {'title': {'type': 'string'}}, 'required': ['title']}},
    {'name': 'task.update', 'description': 'Update task', 'inputSchema': {'type': 'object', 'properties': {'id': {'type': 'string'}}, 'required': ['id']}},
    {'name': 'opportunity.list', 'description': 'List opportunities', 'inputSchema': {'type': 'object', 'properties': {'company_id': {'type': 'string'}, 'person_id': {'type': 'string'}, 'stage': {'type': 'string'}, 'term': {'type': 'string'}, 'limit': {'type': 'integer'}}}},
    {'name': 'opportunity.create', 'description': 'Create opportunity', 'inputSchema': {'type': 'object', 'properties': {'name': {'type': 'string'}}, 'required': ['name']}},
    {'name': 'opportunity.update', 'description': 'Update opportunity', 'inputSchema': {'type': 'object', 'properties': {'id': {'type': 'string'}}, 'required': ['id']}},
]


def reply(msg_id, result=None, error=None):
    payload = {'id': msg_id}
    if error is not None:
        payload['error'] = error
    else:
        payload['result'] = result
    sys.stdout.write(json.dumps(payload) + '\n')
    sys.stdout.flush()


def handle(msg):
    msg_id = msg.get('id')
    method = msg.get('method')
    params = msg.get('params', {})
    if method == 'initialize':
        reply(msg_id, {'protocolVersion': '2026-04-13', 'serverInfo': {'name': 'metadyn-crm-mcp', 'version': '0.1.0'}, 'capabilities': {'tools': {}}})
        return
    if method == 'tools/list':
        reply(msg_id, {'tools': TOOLS})
        return
    if method == 'tools/call':
        name = params.get('name')
        arguments = params.get('arguments', {})
        proc = subprocess.run([str(CLI), 'rpc', '--json', json.dumps({'operation': name, 'params': arguments})], capture_output=True, text=True)
        if proc.returncode != 0:
            reply(msg_id, error={'code': -32000, 'message': proc.stderr.strip() or proc.stdout.strip() or 'tool call failed'})
        else:
            reply(msg_id, {'content': [{'type': 'text', 'text': proc.stdout.strip()}]})
        return
    reply(msg_id, error={'code': -32601, 'message': f'Unknown method: {method}'})


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
            handle(msg)
        except Exception as e:
            reply(None, error={'code': -32000, 'message': str(e)})


if __name__ == '__main__':
    main()
