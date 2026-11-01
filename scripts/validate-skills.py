#!/usr/bin/env python3
"""Validate the small set of skill metadata maintained in this repository."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
for path in sorted((root / 'skills').glob('*/SKILL.md')):
    text = path.read_text()
    assert text.startswith('---\n'), f'{path}: missing frontmatter'
    header = text.split('---', 2)[1]
    name = re.search(r'^name: (.+)$', header, re.M)
    description = re.search(r'^description: (.+)$', header, re.M)
    assert name and name[1] == path.parent.name, f'{path}: name mismatch'
    assert description and description[1].strip(), f'{path}: missing description'
    assert re.fullmatch(r'[a-z0-9-]{1,64}', name[1]), f'{path}: invalid name'
    for link in re.findall(r'\]\(([^)]+)\)', text):
        if '://' not in link:
            assert (path.parent / link).is_file(), f'{path}: broken link {link}'
    print(f'Valid: {path.parent.name}')
