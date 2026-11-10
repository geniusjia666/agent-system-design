---
name: agent-system-design
description: English-language methodology for single-agent and multi-agent system design. From requirements, determine whether an Agent is needed; choose Prompt, Workflow, Single Agent, or Multi-Agent; design roles, task contracts, tools, context and memory, orchestration, handoffs, human intervention, reliability, security, and evaluation. Produce a fixed-structure design document and score it across 21 review dimensions. Integrates 21 Agentic design patterns. Use when users need to (1) design an Agent, multi-agent system, Agent workflow, or pipeline from scratch; (2) select or combine patterns such as prompt chaining, routing, parallelization, reflection, orchestrator-workers, or planning; (3) design inter-Agent handoffs or divide roles; (4) review, diagnose, or score an existing Agent design; or (5) design necessary evolution of an existing LLM application. Does not perform runtime orchestration, business-code refactoring, repository harnessing, deployment, or publication.
---

# Agent System Design

Turn a business requirement into an implementable, reviewable Agent system design document. The four tiers, Prompt, Workflow, Single Agent, and Multi-Agent, share one process, with depth tailored to the selected tier. Deliver design or review only; running business operations, modifying code, deploying, or publishing requires a separate user request.

## Contents

1. Core Principles
2. Three Entry Points
3. Design Process (Steps 1 to 7)
4. Reference Navigation
5. Common Mistakes

## Core Principles

1. **Start with the simplest approach.** If one LLM call can solve the task, do not build a workflow; if fixed steps suffice, do not introduce an autonomous Agent; if one Agent is enough, do not split it into multiple Agents. Every additional step, increase in autonomy, or increase in Agent count must state its rationale, benefits, and costs (latency, cost, and controllability).
2. **Design handoff data before choosing a framework.** Most multi-agent system failures occur between steps: repeated retelling distorts information, constraints are lost, or downstream steps cannot access the required original material. Frameworks are implementation tools, not the design itself.
3. **Use contracts instead of verbal descriptions.** Give every Agent a clear role and boundaries, every task a structured output definition and completion criteria, and every handoff verifiable fields.
4. **Context is a finite budget.** Give each step only the minimum high-signal information needed to complete it; start with on-demand loading, pruning, compaction, or note-taking. Use sub-Agents only when extensive independent exploration genuinely requires isolation, and collect their conclusions, evidence, and gaps. Establish long-term memory as needed.
5. **Enforce critical constraints in code.** Enforce permissions, loop limits, cost limits, and required-field validation in the orchestration or tool layer. Prompts only explain the rules.
6. **Designs must be evaluable.** A design without success criteria and an evaluation method is incomplete.

## Three Entry Points

First determine which situation applies, then enter the process:

| Entry Point | User-Provided Information | Approach |
|---|---|---|
| New design | Business requirements or an idea | Follow the full process from Step 1 to Step 7 |
| Review an existing design | Design documents, prompts, tool lists, architecture diagrams, or code | Reconstruct the known current state using the template structure; mark missing material as to be verified, and distinguish candidate designs from existing implementation. Read relevant references as needed, then perform the Step 7 self-review. Output only an Agent Design Evaluation Report, beginning with a short section on the reconstructed current state and items to be verified. Reserve the full design template for the new-design and redesign entry points |
| Redesign an existing system | An existing LLM application or codebase | First reconstruct the current state and use the Step 7 self-review to identify weaknesses, then restart from Step 2 and design only necessary changes. Output the full design template, marking unchanged sections as "Retain current implementation." Implementing code or configuration changes requires separate authorization; respect the existing architecture |

If information is insufficient, ask for clarification, with no more than three essential questions at a time. Do not ask the user for information that can be established by reading available material without modifying it.

## Design Process

Once a model is confirmed to be necessary, complete all seven steps. If ordinary code suffices, exit early at Step 2. Otherwise, tailor the depth of Steps 3 to 5 to the selected tier:

```
1 Requirements Clarification → 2 Architecture Selection → 3 Individual Agent Design → 4 Orchestration and Collaboration → 5 Intervention and Hardening → 6 Evaluation → 7 Delivery and Self-Review
```

| Tier | Step 3 | Step 4 | Step 5 |
|---|---|---|---|
| Prompt | Task contract only: inputs, output structure, and completion criteria | Usually no orchestration; define minimal boundaries when preprocessing, postprocessing, or handoffs actually exist | Input/output protection and cost limits only; add confirmation points for external actions |
| Workflow | A task contract for every LLM step; tool design for steps that use tools | Step order, branches, and handoff validation | All |
| Single Agent | All | Internal loop and stop conditions only | All |
| Multi-Agent | All | All | All |

For sections or table rows omitted by tier tailoring, write one sentence at the start of the design-document section: "Not applicable under the selected [tier] scope." Do not fill every omitted row individually. If both Workflow and Multi-Agent apply, such as a fixed-order multi-agent pipeline, follow the Multi-Agent row for role isolation and handoffs; do not specify internal autonomous loops for nodes that have none.

Write each step's conclusions into the corresponding sections of the design document (template: `assets/design-document-template.md`).

### Step 1: Requirements Clarification

Establish the following. Mark missing information as "To be confirmed" rather than treating it as user-confirmed. If the user permits an initial candidate or an example trial, identify temporary assumptions and their impact, and consolidate them in Section 11. Assumptions do not authorize access to real data, tools, or business execution:

- Inputs: source, format, scale, and quality.
- Outputs: deliverable form and consumer (a person or a downstream system).
- Success criteria: measurable completion conditions, preferably directly convertible into evaluation cases.
- Constraints: latency, cost per run, call volume, compliance and data security, and acceptable consequences of errors.
- Current state: existing systems, data, tools, and manual processes.

Also assess requirement suitability using the business baseline, actual value, information availability, error costs, and total cost. Do not replace prerequisite checks with an aggregate score or a universal frequency threshold. Without validation, mark the approach as a candidate pending validation. See "Requirement Suitability" in `references/08-evaluation-and-iteration.md`.

### Step 2: Architecture Selection

Read `references/01-architecture-selection.md`. If ordinary code suffices, deliver the rationale and any necessary ordinary-code approach, then end the Agent design process without the full Agent template. Otherwise, choose the control mode (single call, fixed workflow, or model-directed autonomous decisions), then determine whether multiple Agents are needed. The following four common labels may overlap; explain why simpler candidates are insufficient.

| Label | Applicability Signals |
|---|---|
| Prompt (single call) | Inputs are complete; one call with prior retrieval or examples is a candidate for meeting the criteria |
| Workflow (fixed steps orchestrated in code) | Steps, branches, and loop boundaries can be defined in advance, with code controlling the path |
| Single Agent | The model needs to choose its next action autonomously from environment feedback; start with one Agent by default |
| Multi-Agent | There is a clear need for context, tool, or permission isolation, and simpler approaches are insufficient; complexity or step count alone is only a signal |

If performance constraints (latency, cost, and effective context budget) cannot be met, narrow the scope, degrade safely, or retain manual handling. Requirement-scope changes need user confirmation. Mark unvalidated selections as candidates, and distinguish walkthroughs from empirical tests.

A fixed-order multi-agent pipeline, such as generation, review, and refactoring, is also a Workflow; Step 4 must still design its handoffs as a multi-agent system. For single calls or fixed task nodes, configure autonomous planning, long-term memory, and Agent loops only as needed.

### Step 3: Individual Agent Design

Complete the following for each Agent in the system. Define LLM steps in fixed workflows as task nodes; they may simply be restricted model calls. For Prompt and Workflow tiers, complete only the items required by the tailoring table above:

- **Role**: responsibilities, general goals, necessary operating guidelines, capability boundaries, and prohibited actions. Include Backstory only as needed; fictional personas may be omitted. Read `references/02-individual-agent-design.md`.
- **Task contract**: inputs, output structure, completion criteria and checking mechanisms, and stop conditions (at least an attempt limit or total time limit; external waits require timeouts). Read `references/02-individual-agent-design.md`.
- **Tools**: required tool list, descriptions and parameter constraints, results and how to continue reading, error handling and next steps, read/write permissions and approvals, and timeouts. Explain why local functions, MCP, or Skills are integrated or combined. Read `references/03-tool-design.md`.
- **Context and memory**: effective budget, startup and on-demand loading, pruning or compaction, necessary task notes and recovery. Decide whether long-term memory and retrieval are needed, and define sources, scope, updates, and invalidation. Read `references/04-context-and-memory.md`.

### Step 4: Orchestration and Collaboration Design

- **Select an orchestration pattern**: read `references/05-orchestration-patterns.md`. Choose a primary pattern from prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer, or an autonomous loop. Add planning and exploration only for actual gaps. Define dependencies, gates, aggregation conditions, failure exits, and a cross-node total budget. Scores do not depend on pattern or Agent count. Validate the primary pattern before adding necessary supporting capabilities; choose the number of patterns as needed. Required security, budget, and success checks take effect from the first execution. Read `references/10-design-pattern-index.md` to find candidates by the 21 pattern names, engineering signals, or six scenario categories. Distinguish control, capabilities, protocols, and safeguards; verify detailed design locations and self-review dimension numbers, whose ordering differs. Directory names are only clues.
- **Additional design for multi-agent systems** (read `references/06-multi-agent-collaboration.md`):
  - Role division: state actual context, tool, or permission isolation needs and why simpler alternatives are insufficient. Distinguish roles, nodes, and instances; name owners and acceptors. Divide work according to isolation needs, not a count of differences or job titles.
  - Dispatch and handoff: use the seven-element dispatch, handoff, and gate definitions in `assets/handoff-contract-template.json`. Keep the original goal and earlier artifacts readable; the host checks trusted task association and version acceptance.
  - Shared state and communication: choose necessary direct calls, state, or messaging, and define scope, versions, owners, and publication rules. Use A2A, priorities, and nesting only as needed; delegation does not expand authorization or reset budgets.
  - Handoff validation: check format, association, evidence, business requirements, and artifact usability. Separate successful execution from business acceptance. Give failed, duplicate, and late results explicit destinations; corrections and retries share the task budget.
- **For a single Agent**, define any necessary internal loop and the control boundaries of combined patterns. Even fixed steps handled by the same model need handoff, branching, or aggregation conditions.
- **For concrete framework mapping**, read `references/09-framework-implementation-mapping.md`. Map inputs, validation, stop counters, intervention, recovery, and permissions for the same contract. Verify SDK versions, deprecation and maintenance status, and the actual scope of validation. Distinguish construction scaffolds and interface test doubles from real execution acceptance; use frameworks as needed.

### Step 5: Human Intervention, Reliability, and Security

Read `references/07-human-intervention-reliability-and-security.md` and design:

- Human intervention points: clarification, stage confirmation, action approval, and exception escalation based on risk. Define owners, binding of actual requests to decisions, expiry, and recovery. Unify trusted records while allowing multiple reception interfaces; distinguish read receipts from approval, and approval from authorization.
- Reliability: choose bounded handling according to the error and whether an action occurred. Verify unknown outcomes first; retries and corrections share limits. Save trusted state as needed. Recovery reuses results of completed side effects and accumulated budget usage; cancellation and compensation must truthfully record that the original action occurred.
- Cost and resources: all branches and retries share a budget; reserve before calls, settle afterward, and end safely when limits are exceeded. Use model tiers and fallbacks as needed, explicitly labeling rough estimates as estimates.
- Security: trusted identity and object authorization, least privilege, necessary execution isolation, input/output boundaries, and sensitive-data boundaries. ASK blocks execution until approval; required security components fail closed. Prompts and regular expressions are supplementary defenses only.
- Observability: the host records actual actions, approvals, checks, resources, and necessary state. Store only necessary body content; manage sensitive content and internal chains of thought as needed. Verify that rejected requests do not execute the actual tool.

### Step 6: Evaluation Plan

Read `references/08-evaluation-and-iteration.md` and define:

- Evaluation cases: separate static definitions from execution and scoring records. Specify sources, versions, inputs or fixtures, mandatory criteria, and execution protocols. Cover at least the main flow, boundaries, and failures; reference answers are optional. Separate development/regression and holdout sets as needed.
- Evaluation levels and methods: check outputs, actual terminal states, required process steps, and resources as appropriate to the task. Specify where code, models, and humans are used; what Mock, real integration, and UAT establish; and how scorers are validated with positive/negative examples and human calibration.
- Aggregation and gates: report planned, executed, and validly scored counts; denominators; unexecuted, invalid, and failed cases; and all reruns. Define single-run, pass@k, or pass^k protocols and statistical assumptions; ensure version comparability. Judge hard failures separately; pending or old checks must not accept a new version.
- Post-launch monitoring and iteration: define metric semantics, windows, sampling, owners, and responses as needed. Verify signals and turn them into cases. Use root causes to drive controlled proposals, effective only after authorization and validation. Introduce real-time dashboards, A/B tests, automatic learning, and fine-tuning only as needed.

### Step 7: Delivery and Self-Review

1. Output the full design document using `assets/design-document-template.md`. Every section must contain content or "Not applicable" with a reason; handle items exempted by the tailoring table as described above.
2. Use `assets/design-self-review-checklist.md`: first determine the Agent type, select applicable dimensions, then check each item and score it from 0 to 5. Distinguish design, walkthrough, and actual validation evidence. Design scores assess the document only, separately from success rates and permission to publish. Record unexecuted and invalidly scored cases separately; neither counts as a pass.
3. Classify identified issues as serious, moderate, or minor, and list them at the end of the document. Serious issues must be resolved. While unresolved, mark the document "Candidate / Not passed" and list the issues and required decisions in Section 11; do not deliver it as a completed design.
4. Provide no more than five follow-up recommendations in priority order, stating the problem, cause, action, and expected benefit for each.

## Reference Navigation

Read references only when needed; do not load them all at once.

| File | When to Read |
|---|---|
| [references/01-architecture-selection.md](references/01-architecture-selection.md) | Step 2; questions such as "Do I need an Agent?" or "Single Agent or Multi-Agent?" |
| [references/02-individual-agent-design.md](references/02-individual-agent-design.md) | Step 3; roles, task contracts, stop conditions, and reasoning approaches |
| [references/03-tool-design.md](references/03-tool-design.md) | Designing or reviewing tools, MCP, or Skill integration |
| [references/04-context-and-memory.md](references/04-context-and-memory.md) | Long tasks, multi-turn conversations, cross-session memory, retrieval augmentation, or excessive context |
| [references/05-orchestration-patterns.md](references/05-orchestration-patterns.md) | Step 4; selecting orchestration patterns |
| [references/06-multi-agent-collaboration.md](references/06-multi-agent-collaboration.md) | Multi-agent role division, handoffs, communication, and sub-Agent dispatch |
| [references/07-human-intervention-reliability-and-security.md](references/07-human-intervention-reliability-and-security.md) | Step 5; production deployment or high-risk operations |
| [references/08-evaluation-and-iteration.md](references/08-evaluation-and-iteration.md) | Step 1 suitability assessment; Step 6 evaluation; post-launch iteration |
| [references/09-framework-implementation-mapping.md](references/09-framework-implementation-mapping.md) | The user specifies or needs to choose Google ADK, LangGraph, CrewAI, or AutoGen |
| [references/10-design-pattern-index.md](references/10-design-pattern-index.md) | Finding candidates by the 21 pattern names, engineering signals, or six scenario categories; verifying combination boundaries and self-review numbers |
| [assets/design-document-template.md](assets/design-document-template.md) | Step 7; document delivery |
| [assets/handoff-contract-template.json](assets/handoff-contract-template.json) | Inter-Agent handoff data and sub-Agent dispatch contracts |
| [assets/design-self-review-checklist.md](assets/design-self-review-checklist.md) | Step 7 self-review; reviewing existing designs |

## Common Mistakes

- Starting with multiple Agents or a framework without explaining why simpler alternatives are insufficient.
- Giving downstream steps only the preceding step's retelling, losing original requirements and constraints.
- Passing critical data between Agents as free text without field definitions and validation.
- Generating and proving correctness in the same call; required acceptance lacks tests, rules, separate review, or human checks for the corresponding version.
- Omitting stop conditions and iteration limits, allowing reflection or retry loops to run indefinitely.
- Giving every Agent every tool, or expressing safety constraints only in prompts.
- Delivering a design document without success criteria or evaluation cases.
