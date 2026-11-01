#!/usr/bin/env python3
"""Link this checkout's skills into Codex without overwriting installations."""
import argparse
from pathlib import Path


def install(repo, destination):
    sources = sorted((repo / 'skills').glob('*/SKILL.md'))
    if not sources:
        raise ValueError('No skills found')
    pending = []
    for source_file in sources:
        source = source_file.parent.resolve()
        target = destination / source.name
        if target.is_symlink() and target.resolve() == source:
            continue
        if target.exists() or target.is_symlink():
            raise ValueError(f'Refusing to overwrite {target}')
        pending.append((source, target))
    destination.mkdir(parents=True, exist_ok=True)
    for source, target in pending:
        target.symlink_to(source, target_is_directory=True)
    return [destination / source.parent.name for source in sources]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path, default=Path.home() / '.agents/skills')
    args = parser.parse_args()
    try:
        for path in install(Path(__file__).resolve().parents[1], args.destination.expanduser().resolve()):
            print(f'{path} -> {path.resolve()}')
    except (OSError, ValueError) as exc:
        parser.exit(1, f'error: {exc}\n')
