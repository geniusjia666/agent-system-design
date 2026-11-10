# Contributing

[中文](CONTRIBUTING.zh-CN.md) · [README](README.md)

Issues and pull requests are welcome for factual corrections, broken links, encoding mistakes, and unclear installation notes.

## Keep the methodology intact

The English and Chinese skill trees are the source method. They describe the same 7 steps, 4 architecture tiers, 21 patterns, 21 review dimensions, and handoff contract.

- A change to the method belongs in both languages, with the same meaning.
- Do not "simplify" a design by adding agents, frameworks, or scores the skill tells the reader to justify or omit.
- Sample scores do not belong in documentation. The worked example stays illustrative and unscored.
- Framework notes may be updated when maintenance or API facts change. Cite the source and the date you read it. Leave ADK, LangGraph, CrewAI, and AutoGen described as mapping scaffolds unless a change records an actual test and its limits.

## Keep discovery working

`SKILL.md` frontmatter `name` must match the skill directory name: `agent-system-design` or `agent-system-design-cn`. Descriptions must stay within 1024 characters. The English description is already close to that limit.

Chinese filenames stay UTF-8. If you add a link, point it at the real filename, including Chinese characters. Do not reintroduce `__MACOSX`, `.DS_Store`, or AppleDouble files.

## What this repository does not need

Runtime orchestration, a website, release automation, hosted deployment, badges, download counters, and star campaigns are out of scope. The code blocks inside the framework chapter are part of the skill's documentation. The repository check does not execute them, and a contribution should not add a dependency just to run them.

## Before opening a pull request

```bash
python3 scripts/validate_repo.py
```

The script uses only the Python standard library. If you change an imported skill file on purpose, regenerate `scripts/source-manifest.json` with the same SHA-256 fields the checker reads, and say why the bytes changed. Accidental edits should fail the check instead.

Do not rewrite [LICENSE](LICENSE). Copyright there is Skyler, 2026. Repository ownership by geniusjia666 is separate and is stated in the README.
