import json
from common import Contributor
import sys
from typing import List
from html import escape

def format_contributor(contributor: Contributor) -> str:
    return f'<td align="center"><sub><img src="{contributor.avatar_url}?size=100" width="100" height="100"><br><b>{escape(contributor.name)}</b><br>{", ".join(contributor.contributions)}</sub></td>'

def main():
    if len(sys.argv) < 3:
        print(f'Usage: {sys.argv[0]} <contributors file> <readme template>')
        exit(1)
    with open(sys.argv[1]) as f:
        contributors: List[Contributor] = Contributor.schema().loads(f.read(), many=True)
    with open(sys.argv[2]) as f:
        template = f.read()
    contributors.sort(key=lambda contributor: contributor.name)
    result = ['<table><tbody><tr>']
    for i, contributor in enumerate(contributors):
        if i != 0 and (i % 6) == 0:
            result.append('</tr><tr>')
        result.append(format_contributor(contributor))
    result.append('</tr></tbody</table>')
    with open('README.md', 'w') as f:
        contributors_table = '\n'.join(result)
        f.write(template.replace('{{ contributors }}', contributors_table))

if __name__ == '__main__':
    main()
