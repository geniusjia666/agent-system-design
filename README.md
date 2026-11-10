# Agent System Design

**Design the right agent system—not just more agents.**

[中文说明](README.zh-CN.md)

This repository publishes one agent-design methodology in English and Chinese. It is a reviewable design procedure: decide whether an agent is warranted, choose the smallest architecture that can meet the need, and write down roles, contracts, handoffs, safeguards, and evaluation before anyone picks a framework.

The GitHub owner of this repository is [geniusjia666](https://github.com/geniusjia666). The license file remains the MIT license already in the repository. See [Provenance](PROVENANCE.md).

## What you can produce with it

Used as an Agent Skill, the method asks an assistant to turn a request into a design document rather than into a running system. A finished design includes:

- A stated architecture tier, and a reason the simpler tiers are not enough.
- One task contract per agent or workflow step: inputs, output structure, done criteria, and a stop condition.
- Tool, context, and memory decisions limited to what that step needs.
- Handoffs that a host can validate: a seven-field dispatch, a structured result, and a gate.
- Human-intervention, failure, budget, and security boundaries where the tier requires them.
- An evaluation plan with cases for the main path, a boundary, and a failure.
- A self-review against the dimensions that apply. A document score is not a success rate and not permission to ship.

The worked example is a fixed **generate, review, and fix** code workflow. It explains why that shape is a workflow with isolated review, not a reason to add more agents. The example is illustrative. It was not executed, and it has no performance score. See [the English example](examples/en/code-generation-review-fix.md).

## Highlights

Both language editions describe the same method:

| Piece | Where it lives |
|---|---|
| 7-step process: requirements, architecture, individual design, orchestration, safeguards, evaluation, delivery | `SKILL.md` |
| 4 tiers: Prompt, Workflow, Single Agent, Multi-Agent | `SKILL.md` and the architecture reference |
| 21 patterns, indexed to where they are designed and to review dimensions | `references/10-*` |
| 21-dimension design review, scored 0–5 only when a review is actually done | `assets/` self-review checklist |
| Handoff contract: `dispatch`, `handoff`, and `gate` | `assets/` JSON template |

Pattern numbers and review-dimension numbers are not the same order. The index says so. Use the dimension number in a review report.

## Boundaries

This is a methodology and a design-review aid. The skill text itself says it does not perform runtime orchestration, business-code refactoring, repository harnessing, deployment, or publication.

The notes on Google ADK, LangGraph, CrewAI, and AutoGen are documentation scaffolds for mapping one contract onto those APIs. They are not tested integrations. Details and dates are in [Framework mapping](#framework-mapping).

## Repository layout

```text
skills/agent-system-design/        English skill. Directory name matches frontmatter name.
skills/agent-system-design-cn/     Chinese skill. Directory name matches frontmatter name.
examples/en/                       English sample prompts and one full illustrative design
examples/zh-CN/                    Chinese sample prompts and the same illustrative design
scripts/validate_repo.py           Local checks. Python standard library only.
scripts/source-manifest.json       SHA-256 of every imported skill file
PROVENANCE.md                      How the archives were imported
CONTRIBUTING.md                    How to propose a change
LICENSE                            MIT, unchanged from the initial commit
```

Each skill directory is a self-contained Agent Skill:

```text
skill-name/
├── SKILL.md
├── references/     # read on demand; ten chapters, 01 through 10
└── assets/         # design template, handoff JSON, self-review checklist
```

The Chinese chapter and asset filenames are the original Chinese names, stored as UTF-8. Links inside that skill point at those names.

## Install

Installation here means putting a skill directory where your agent host already looks for skills. This repository does not register itself with a product, and cloning it does not by itself enable a skill.

These steps follow the [Agent Skills specification](https://agentskills.io/specification) as published on agentskills.io and read for this repository on 2026-11-10:

1. Choose one language. Each skill is complete. Loading both is optional and not required.
2. Keep the directory name equal to the `name` field in `SKILL.md`.
   - English: [skills/agent-system-design](skills/agent-system-design/SKILL.md) (`name: agent-system-design`)
   - Chinese: [skills/agent-system-design-cn](skills/agent-system-design-cn/SKILL.md) (`name: agent-system-design-cn`)
3. Copy or symlink that directory into the skills location your host documents. The specification defines the folder and the frontmatter. It does not define one install path for every product.
4. Ask for a design, an architecture choice, or a review of an existing design. [Sample prompts](examples/en/sample-prompts.md) are starting points, not required phrasing.

```bash
# Replace DESTINATION with the directory your host actually scans.
# The last path component must stay the skill name.
mkdir -p DESTINATION
cp -R skills/agent-system-design DESTINATION/agent-system-design
# Chinese edition:
cp -R skills/agent-system-design-cn DESTINATION/agent-system-design-cn
```

### Cursor, as documented, not as tested here

Cursor's Agent Skills page, <https://cursor.com/docs/skills>, was read on 2026-11-10. It lists these discovery directories:

| Location | Scope, as that page describes it |
|---|---|
| `.agents/skills/` | Project |
| `.cursor/skills/` | Project |
| `~/.agents/skills/` | User, on that machine |
| `~/.cursor/skills/` | User, on that machine |

The same page says Cursor also loads `.claude/skills/`, `.codex/skills/`, `~/.claude/skills/`, and `~/.codex/skills/` for compatibility, and that a GitHub repository is not imported as skills on its own unless it is packaged as a plugin. Copying the skill folder is the direct method described above.

This publishing pass did not launch Cursor, Claude Code, or Codex, and did not install the skill into any of those directories. Nothing here is a certification or a compatibility claim for those products. Treat the table as a citation of Cursor's documentation, then confirm it against the current page before you rely on it.

## Use

1. Install one skill directory using the steps above.
2. For a new system, ask the agent to follow the skill from requirements through the design document. If ordinary code is enough, the skill stops at architecture selection and does not fill the full template.
3. For an existing design, ask for an evaluation report only. The skill reserves the full template for new designs and redesigns.
4. Let the agent open `references/` and `assets/` when a step needs them. The skill is written so those files stay unloaded until then.
5. Treat framework chapters as optional mapping notes after the contract exists.

A host that supports the specification loads `name` and `description` first, then `SKILL.md` when the request matches, then individual reference files if the instructions point to them. Product behavior beyond that was not measured here.

## Framework mapping

[English chapter](skills/agent-system-design/references/09-framework-implementation-mapping.md) and [Chinese chapter](skills/agent-system-design-cn/references/09-框架落地映射.md) map the same generate, review, and repair contract onto four libraries. They state that the chapter is a Python construction scaffold, that production runners are out of scope, and that the libraries were not installed for that chapter.

The chapters record a reading date rather than a result from this repository. This publishing pass did not reinstall the packages or re-audit upstream repositories. The notes below are what those chapters say, not a new compatibility test:

- Supplementary reading is dated 2026-11-01, after official material the chapter says was archived on 2026-10-30.
- Candidate pins recorded from package indexes that day: `google-adk==2.13.0`, `langgraph==1.2.19`, `crewai==1.15.33`, `autogen-core==0.7.5`. The chapter says these await compatibility validation.
- ADK: the chapter says official documentation treats 2.0 graph workflows as the replacement for traditional template workflows, and that the 2.13.0 source marks `SequentialAgent` deprecated. The scaffold still shows `SequentialAgent` so existing systems can be mapped. New work is told to check current graph docs.
- LangGraph and CrewAI: the chapter says typed state, task outputs, and framework callbacks are carriers. Business validation, permissions, and acceptance stay in the host. It also says some older CrewAI result attributes in the archive are outdated.
- AutoGen: the chapter says the current official repository is archived, no longer maintained, and receives no security fixes. It keeps the Core mapping for existing systems and research, and tells new production selections to look elsewhere. It says legacy 0.2, Core, and AgentChat APIs should not be mixed. Any successor framework is explicitly out of scope for that chapter.

Do not cite those version pins as versions tested by this repository.

## Checks

From a clone:

```bash
python3 scripts/validate_repo.py
```

The script uses the Python standard library only. It checks UTF-8, JSON parsing, `SKILL.md` frontmatter, local Markdown links and heading anchors, the 7-step / 4-tier / 21-pattern / 21-dimension / handoff markers, and SHA-256 equality with the imported skill files. It does not execute code samples inside the skill.

## Contributing

Corrections, link fixes, and sourced updates belong in a pull request. Read [CONTRIBUTING.md](CONTRIBUTING.md). Please keep the English and Chinese methodologies aligned when a change applies to both.

## Star

If this checklist helps you decide not to add an agent, a star makes the repository easier for other people to find. A star is not evidence that a design is correct, and this project does not offer support, reviews, or compatibility in exchange for one.

## License

[MIT License](LICENSE). Copyright (c) 2026 Skyler, as stated in that file. The file was not modified for this publication.
