# Evidence notebook

Requires Python 3.10+; no external dependencies. Resolve `scripts/evidence.py` relative to this skill's directory. Use an absolute notebook path in the task workspace, not in the skill checkout. No network access is performed.

```sh
python3 scripts/evidence.py --db /path/to/task/research/evidence.sqlite init
python3 scripts/evidence.py --db /path/to/task/research/evidence.sqlite add --record /path/to/claim.json --snapshot /path/to/source.txt
python3 scripts/evidence.py --db /path/to/task/research/evidence.sqlite list
python3 scripts/evidence.py --db /path/to/task/research/evidence.sqlite find 'ownership'
python3 scripts/evidence.py --db /path/to/task/research/evidence.sqlite check
python3 scripts/evidence.py --db /path/to/task/research/evidence.sqlite export
```

`add` accepts a JSON object:

```json
{
  "claim": "A logical fleet runs one application.",
  "source_url": "https://example.org/docs/fleets",
  "passage": "A fleet runs one application.",
  "source_version": "release or commit if relevant; otherwise omitted",
  "assessment": "supported",
  "qualification": "This does not establish one application per physical cluster.",
  "open_question": "Can separate fleets share machines?"
}
```

Assessments: `supported`, `inference`, `disputed`, `unresolved`. Only claim and assessment are mandatory; missing evidence is retained and flagged. Supply `retrieved_at` as an ISO 8601 timestamp when capture predates entry; otherwise entry time is used and labeled. A snapshot is optional UTF-8 source text, copied into SQLite with its SHA-256 digest. Preserve relevant passages without unnecessarily copying whole copyrighted documents. Quote matching normalizes whitespace; it does not check semantic support or the authenticity of an agent-created snapshot.

To correct an entry, add a new record with `"supersedes": OLD_ID`. History is retained. Normal listing and checks use current records; `list --all` and `export` include history. Each record represents one claim/source relationship; add separate records for corroborating or conflicting sources.

`find` searches all record text case-insensitively. `export` writes JSON to stdout for handoff. `check` reports missing source/passage/snapshot, passage mismatches, digest mismatches, unresolved/disputed assessments, and open questions, returning exit code 1 when any need review. Missing version alone is not an error: assess version relevance yourself. JSON input errors return exit code 2 without adding a record. SQLite transactions protect concurrent writes; records and snapshots are append-only through this CLI.
