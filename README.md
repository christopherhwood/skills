# Personal agent skills

Personal skills for technical research, learning, and improving skills from past chats:

| Skill | Purpose | Tool |
| --- | --- | --- |
| [mechanism-first-research](skills/mechanism-first-research/SKILL.md) | Investigate mechanisms, check claims, and explain practical differences | Python evidence notebook |
| [technical-learning-profile](skills/technical-learning-profile/SKILL.md) | Explain progressively, refine mental models, and make mechanisms concrete | Pinned Mermaid diagram renderer |
| [skills-from-chats](skills/skills-from-chats/SKILL.md) | Extract lessons from past chats, update existing skills first, and evaluate changes | Instructions only |

Each skill works independently and allows automatic selection. The research and learning skills do not force tool use for simple questions. Evidence checks establish traceability, not truth. Rendered diagrams still need visual and conceptual inspection.

## Install and keep in sync with Codex

Requires Python 3.10+ and Node.js 22.13+ with npm for diagrams.

```sh
git clone https://github.com/christopherhwood/skills.git ~/Projects/skills
cd ~/Projects/skills
npm ci --prefix skills/technical-learning-profile
python3 scripts/link-skills.py
```

The installer links each skill directory into `~/.agents/skills`, the user-level discovery location documented by [Codex](https://learn.chatgpt.com/docs/build-skills). It refuses to overwrite another installation. The links point at this checkout, so updating it updates the installed skills:

```sh
git pull --ff-only
npm ci --prefix skills/technical-learning-profile
```

This is local synchronization, not automatic background pulling. Codex detects skill changes automatically; restart it if the skills do not appear. Invoke explicitly with `$mechanism-first-research`, `$technical-learning-profile`, or `$skills-from-chats`, or allow matching technical questions to select them.

For an existing Chrome installation, install with `PUPPETEER_SKIP_DOWNLOAD=true npm ci --prefix skills/technical-learning-profile`, then use the renderer's `--browser` option. See each skill's linked tool reference for commands and input formats. Keep research notebooks, source captures, and generated diagrams in the task workspace, not this repository.

## Development

```sh
python3 -m unittest discover -s tests -v
node --test tests/render-diagram.test.mjs
```

CI validates skill metadata, runs notebook and renderer tests, and renders real diagrams. Changes to `main` go through pull requests with the `validate` check passing. Force pushes and branch deletion are blocked. No independent approval is required for this personal repository.
