# Sample prompts

[中文提示词](../zh-CN/sample-prompts.md) · [Illustrative design](code-generation-review-fix.md)

These prompts assume the English skill `agent-system-design` is installed. They show the kind of request the skill is written to accept. They are not magic phrases, and they do not produce a measured score.

## 1. New design, with the simplest tier left open

```text
Use the agent-system-design skill. Design a system that turns a short product FAQ into a cited answer for a support agent.

Start from the requirements. Choose Prompt, Workflow, Single Agent, or Multi-Agent, and say why each simpler option is or is not enough. If ordinary code is enough, stop there.

Deliver the design document from the skill template. Do not deploy anything, do not modify a repository, and do not invent a numeric self-review score. Mark anything you did not verify as to be confirmed.
```

## 2. Push back on an agent count

```text
Use the agent-system-design skill. I want five agents: a planner, a researcher, a coder, a tester, and a manager, to add a word-count function to a Python file.

Decide whether that split is justified. Prefer the simplest tier that can meet the need. If you keep more than one role, name the context, tool, or permission isolation that requires it. Produce the design document, not the code and not a running pipeline.
```

## 3. Review an existing design

```text
Use the agent-system-design skill. Review the design below. Do not rewrite it into a new system.

Output only an Agent Design Evaluation Report. Start with the current state you can actually see and the items you still need. Select the dimensions that apply. Do not fill in scores for dimensions you cannot check, and do not treat a document score as permission to ship.

Design:
- One agent has the repository, the shell, and the production database.
- It writes code, runs tests, and decides that the tests passed.
- There is no stop condition and no separate review.
```

## 4. Ask for the worked shape, without treating the example as a result

```text
Use the agent-system-design skill. Design a fixed generate, then review, then fix workflow for this specification:

Implement word_counts(text: str) -> dict[str, int]. Lowercase the text. A word is a maximal run of Unicode word characters. Punctuation is ignored. Empty and punctuation-only input returns an empty dict.

The host must validate handoffs. The reviewer must see the original specification and the exact code version, and must not share the writer's scratch notes. Do not execute the candidate. Follow the skill's design-document template. Leave self-review scores blank and label the design illustrative unless you actually run the checks.
```

The repository's filled example for prompt 4 is [code-generation-review-fix.md](code-generation-review-fix.md). It is a format and reasoning sample, not a result to paste as measured performance.
