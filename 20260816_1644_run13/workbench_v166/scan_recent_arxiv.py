from __future__ import annotations

import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


def main() -> None:
    query = 'cat:cs.AI AND (all:agent OR all:tool)'
    url = 'https://export.arxiv.org/api/query?' + urllib.parse.urlencode(
        {
            'search_query': query,
            'start': 0,
            'max_results': 100,
            'sortBy': 'submittedDate',
            'sortOrder': 'descending',
        }
    )
    with urllib.request.urlopen(url, timeout=30) as response:
        root = ET.fromstring(response.read())

    namespace = {'atom': 'http://www.w3.org/2005/Atom'}
    entries = root.findall('atom:entry', namespace)
    print(f'COUNT\t{len(entries)}')
    for entry in entries:
        title = ' '.join(entry.find('atom:title', namespace).text.split())
        summary = ' '.join(entry.find('atom:summary', namespace).text.split())
        published = entry.find('atom:published', namespace).text[:10]
        identifier = entry.find('atom:id', namespace).text.rsplit('/', 1)[-1]
        print(f'{published}\t{identifier}\t{title}\t{summary[:360]}')


if __name__ == '__main__':
    main()
