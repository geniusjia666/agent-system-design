# Contributing

[README](README.md) · [Sync notes](SYNC.md)

Issues and pull requests are welcome for factual corrections, broken links, and unclear installation notes.

## Keep the methodology intact

This repository is the English full edition. [agent-system-design-cn](https://github.com/geniusjia666/agent-system-design-cn) is the Chinese full edition of the same methodology, not a different product. Both describe the same 7 steps, 4 architecture tiers, 21 patterns, 21 review dimensions, and handoff contract.

- Do not "simplify" a design by adding agents, frameworks, or scores the skill tells the reader to justify or omit.
- Sample scores do not belong in documentation. The worked example stays illustrative and unscored.
- Framework notes may be updated when maintenance or API facts change. Cite the source and the date you read it. Leave ADK, LangGraph, CrewAI, and AutoGen described as mapping scaffolds unless a change records an actual test and its limits.
- If a change alters the method, update the Chinese edition as well and give both repositories the same new version number. [SYNC.md](SYNC.md) states the criteria. There is no automated sync, and this repository cannot commit to the other one.

## Keep discovery working

`SKILL.md` frontmatter `name` must match the skill directory name `agent-system-design`. The description must stay within 1024 characters. The English description is already close to that limit.

Do not reintroduce `__MACOSX`, `.DS_Store`, or AppleDouble files. Do not add the Chinese skill tree here; it belongs in the sibling repository.

## What this repository does not need

Runtime orchestration, a website, release automation, hosted deployment, git tags, GitHub Releases, badges, download counters, and star campaigns are out of scope. Methodology version 0.1.0 in [VERSION](VERSION) is a shared edition number, not a release.

The code blocks inside the framework chapter are part of the skill's documentation. The repository check does not execute them, and a contribution should not add a dependency just to run them.

## Before opening a pull request

```bash
python3 scripts/validate_repo.py
```

The script uses only the Python standard library. If you change an imported skill file on purpose, regenerate `scripts/source-manifest.json` with the same SHA-256 fields the checker reads, and say why the bytes changed. Accidental edits should fail the check instead.

Do not rewrite [LICENSE](LICENSE). Copyright there is Skyler, 2026. Repository ownership by geniusjia666 is separate and is stated in the README.
