#!/usr/bin/env python3
import json
import sys
import urllib.request
from pathlib import Path

API_URL = 'https://crm.metadyn.xyz/graphql'
TOKEN_PATH = Path('/home/jza/.openclaw/.secrets/metadyn-crm-api-key')

QUERY = '''
query ListCompanies($first: Int!, $offset: Int!) {
  companies(first: $first, offset: $offset, orderBy: [{name: AscNullsLast}]) {
    totalCount
    edges {
      node {
        id
        name
        domainName {
          primaryLinkUrl
          primaryLinkLabel
        }
        employees
        linkedinLink {
          primaryLinkUrl
          primaryLinkLabel
        }
        xLink {
          primaryLinkUrl
          primaryLinkLabel
        }
        idealCustomerProfile
        createdAt
        updatedAt
      }
    }
  }
}
'''


def main() -> int:
    first = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    offset = int(sys.argv[2]) if len(sys.argv) > 2 else 0

    token = TOKEN_PATH.read_text().strip()
    payload = json.dumps({
        'query': QUERY,
        'variables': {'first': first, 'offset': offset},
    }).encode()
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
        print(json.dumps(data, indent=2))
        return 1

    companies = data['data']['companies']
    print(f"totalCount: {companies['totalCount']}")
    for i, edge in enumerate(companies['edges'], start=1 + offset):
        node = edge['node']
        domain = (node.get('domainName') or {}).get('primaryLinkLabel') or (node.get('domainName') or {}).get('primaryLinkUrl') or ''
        linkedin = (node.get('linkedinLink') or {}).get('primaryLinkUrl') or ''
        print(f"{i}. {node['name']} | id={node['id']} | domain={domain or '-'} | employees={node.get('employees') or '-'} | ICP={node.get('idealCustomerProfile')} | linkedin={linkedin or '-'}")

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
