#!/usr/bin/env python3
"""Append-only, local evidence notebook. Checks provenance, not truth."""
import argparse
import hashlib
import json
from pathlib import Path
import sqlite3
import sys
from datetime import datetime, timezone
from urllib.parse import urlparse

FIELDS = {'claim', 'source_url', 'passage', 'source_version', 'assessment',
          'qualification', 'open_question', 'retrieved_at', 'supersedes'}
ASSESSMENTS = {'supported', 'inference', 'disputed', 'unresolved'}


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def validate(record):
    if not isinstance(record, dict):
        raise ValueError('record must be a JSON object')
    if set(record) - FIELDS:
        raise ValueError(f'unknown fields: {sorted(set(record) - FIELDS)}')
    for field, value in record.items():
        if field != 'supersedes' and not isinstance(value, str):
            raise ValueError(f'{field} must be a string')
    if not record.get('claim', '').strip():
        raise ValueError('claim must be nonempty')
    if record.get('assessment') not in ASSESSMENTS:
        raise ValueError(f'assessment must be one of {sorted(ASSESSMENTS)}')
    if 'supersedes' in record and (type(record['supersedes']) is not int or record['supersedes'] < 1):
        raise ValueError('supersedes must be a positive integer')
    if record.get('source_url'):
        url = urlparse(record['source_url'])
        if url.scheme not in ('http', 'https') or not url.netloc or url.username or url.password:
            raise ValueError('source_url must be an HTTP(S) URL without credentials')
    if record.get('retrieved_at'):
        when = datetime.fromisoformat(record['retrieved_at'].replace('Z', '+00:00'))
        if when.tzinfo is None:
            raise ValueError('retrieved_at must include a timezone')
    return record


def rows(conn, history=False):
    query = 'SELECT * FROM entries'
    if not history:
        query += ' WHERE id NOT IN (SELECT supersedes FROM entries WHERE supersedes IS NOT NULL)'
    query += ' ORDER BY id'
    result = []
    for row in conn.execute(query):
        item = json.loads(row['record'])
        item.update(id=row['id'], created_at=row['created_at'],
                    snapshot_sha256=row['snapshot_sha256'], snapshot=row['snapshot'])
        result.append(item)
    return result


def audit(items):
    problems = []
    for item in items:
        reasons = []
        for field in ('source_url', 'passage'):
            if not item.get(field, '').strip():
                reasons.append(f'missing {field}')
        snapshot = item['snapshot']
        if snapshot is None:
            reasons.append('missing snapshot; passage not checked')
        else:
            if digest(snapshot) != item['snapshot_sha256']:
                reasons.append('snapshot digest mismatch')
            passage = ' '.join(item.get('passage', '').split())
            if passage and passage not in ' '.join(snapshot.split()):
                reasons.append('passage not found in snapshot')
        if item['assessment'] in ('unresolved', 'disputed'):
            reasons.append(f"assessment: {item['assessment']}")
        if item.get('open_question', '').strip():
            reasons.append('open question: ' + item['open_question'])
        if reasons:
            problems.append({'id': item['id'], 'issues': reasons})
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', required=True, type=Path)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('init')
    add = sub.add_parser('add')
    add.add_argument('--record', required=True, type=Path)
    add.add_argument('--snapshot', type=Path)
    listing = sub.add_parser('list')
    listing.add_argument('--all', action='store_true')
    sub.add_parser('export')
    sub.add_parser('check')
    find = sub.add_parser('find')
    find.add_argument('query')
    args = parser.parse_args()
    try:
        record = snapshot = None
        if args.command == 'add':
            record = validate(json.loads(args.record.read_text(encoding='utf-8')))
            snapshot = args.snapshot.read_text(encoding='utf-8') if args.snapshot else None
        if args.command != 'init' and not args.db.is_file():
            raise ValueError('notebook does not exist; run init first')
        if args.command == 'init':
            args.db.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(args.db, timeout=30) as conn:
            conn.row_factory = sqlite3.Row
            if args.command == 'init':
                conn.execute('''CREATE TABLE IF NOT EXISTS entries (
                    id INTEGER PRIMARY KEY, record TEXT NOT NULL,
                    created_at TEXT NOT NULL, snapshot TEXT, snapshot_sha256 TEXT,
                    supersedes INTEGER UNIQUE REFERENCES entries(id))''')
                print(json.dumps({'db': str(args.db.resolve())}))
                return 0
            if args.command == 'add':
                conn.execute('BEGIN IMMEDIATE')
                old_id = record.get('supersedes')
                if old_id is not None:
                    active = {item['id'] for item in rows(conn)}
                    if old_id not in active:
                        raise ValueError('supersedes must reference a current record')
                now = datetime.now(timezone.utc).isoformat()
                record['retrieval_time_basis'] = 'provided' if record.get('retrieved_at') else 'entry_time'
                record.setdefault('retrieved_at', now)
                if not record['retrieved_at']:
                    record['retrieved_at'] = now
                cursor = conn.execute('''INSERT INTO entries
                    (record, created_at, snapshot, snapshot_sha256, supersedes)
                    VALUES (?, ?, ?, ?, ?)''',
                    (json.dumps(record, ensure_ascii=False), now, snapshot,
                     digest(snapshot) if snapshot is not None else None, old_id))
                print(json.dumps({'id': cursor.lastrowid}))
                return 0
            items = rows(conn, args.command == 'export' or getattr(args, 'all', False))
            if args.command == 'check':
                problems = audit(items)
                print(json.dumps({'checked': len(items), 'issues': problems,
                                  'scope': 'traceability only; semantic support requires review'}, indent=2))
                return 1 if problems else 0
            if args.command == 'find':
                items = [i for i in items if args.query.casefold() in json.dumps(i, ensure_ascii=False).casefold()]
            if args.command != 'export':
                items = [{k: v for k, v in item.items() if k != 'snapshot'} for item in items]
            print(json.dumps(items, ensure_ascii=False, indent=2))
            return 0
    except (ValueError, OSError, sqlite3.Error) as exc:
        print(f'error: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
