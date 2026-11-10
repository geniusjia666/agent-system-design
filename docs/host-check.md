# Host check, 2026-11-10

This file records one attempt to run the English skill on an official Agent Skill host. It is not a certification of Cursor or of any other product. The design in [examples/code-generation-review-fix.md](../examples/code-generation-review-fix.md) was written by hand earlier. Nothing in that example is an output from the run below.

## Results

- 安装布局验证通过
- 宿主发现未验证
- 实际触发未验证

## Environment

Checked on 2026-11-10, without creating a login and without setting an API key.

| Item | What was observed |
|---|---|
| Cursor CLI | Official installer from [cursor.com/docs/cli/installation](https://cursor.com/docs/cli/installation): `curl https://cursor.com/install -fsS \| bash`. `agent --version` printed `2026.11.05-86047df`. `agent about` said that build was up to date and that the user email was not logged in. |
| Auth | `agent status` printed `Not logged in`. |
| One print-mode probe | `agent -p --trust --output-format text` with a one-word prompt exited 1. Standard error: `Authentication required. Please run 'agent login' first, or set CURSOR_API_KEY environment variable.` Login was not run, and no key was added. The probe was not retried. |
| Cursor editor server | Version 3.25.9 was present as `cursor-server`. Its help text is for serving the editor and managing extensions. It was not used to discover or trigger a skill. |
| Claude Code and Codex | Neither CLI was installed. Their documents were not read for this check. Cursor's skill page says Cursor can also load `.claude/skills/` and `.codex/skills/`. That sentence is Cursor's, and those products were not tested. |

The CLI install and the unauthenticated probe are not skill discovery and not a skill trigger.

## Layout check that passed

In an empty temporary workspace, outside this repository, the English skill directory was copied to the two project paths documented the same day at [cursor.com/docs/skills](https://cursor.com/docs/skills):

```bash
mkdir -p .cursor/skills
cp -R skills/agent-system-design .cursor/skills/agent-system-design

mkdir -p .agents/skills
cp -R skills/agent-system-design .agents/skills/agent-system-design
```

Both copies had 14 files. Each file's SHA-256 and byte size matched [scripts/source-manifest.json](../scripts/source-manifest.json). `SKILL.md` was present, and its frontmatter `name` was `agent-system-design`, the same as the parent folder. The temporary workspace was deleted. This checks the copy layout only. Cursor was not started against it, so discovery remains unverified.

User-level directories `~/.cursor/skills/` and `~/.agents/skills/` are also on that page. They were not used, so this machine's personal skill list was left unchanged.

## Trigger that was not run

The intended request, for a later logged-in host, is:

```text
build a PR review assistant that fetches a diff, checks a fixed checklist and returns human-review suggestions; read-only, no auto approvals/merges or posting
```

Two prompts were planned and not sent:

1. Explicit trigger, same request, preceded by an instruction to use the `agent-system-design` skill and to design only.
2. Natural-language match, the request alone, with no skill name, to see whether the host selects the skill from its description.

No design document, handoff, or gate was produced by a host. Do not treat the handwritten example as that output.

## Acceptance items, not applied

If a host run happens later, check only these items. Do not add a score or a success rate. One run still would not certify every host.

1. The output is a design, not a running automation, and it does not approve, merge, post, or edit another repository.
2. The selected tier is one of Prompt, Workflow, Single Agent, or Multi-Agent. If ordinary code is enough, the design stops there. Ordinary code is not a fifth tier.
3. A move to Multi-Agent states a context, tool, or permission isolation reason. A simpler tier does not need that reason. Not every step up requires a multi-agent split.
4. The design includes a structured handoff and a gate. Suggestions are for a person to review.
5. The 21 patterns are used as the skill's retrieval index, not as a claim that they are one official standard. A 21-dimension review, if present, describes the document. It is not a measured performance result. Framework names, if present, stay scaffolds.

## Gap

Host discovery and the actual trigger need a Cursor CLI or Cursor IDE session that is already logged in, with the skill copied as above, and then the two prompts. This check stopped at the authentication error. It did not open a browser login, did not create a credential, and did not call another model API in place of Cursor.
