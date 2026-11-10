# Design Pattern Index

Use this reference to find design locations by pattern name, or choose candidate combinations for new designs, existing-system reviews, or local changes. This chapter provides indexing and matching guidance only. Engineering refactoring and runtime recommenders are out of scope; select patterns as needed.

## Contents

1. Usage Order and Pattern Layers
2. Overview of 21 Patterns and Self-Review Mapping
3. Trace Engineering Clues to Actual Behavior
4. Assess Whether Combinations Are Valid
5. Minimal Candidate Combinations for Six Scenario Categories
6. Write into Existing Design Documents and Validate Benefits
7. Commonly Confused Concepts and Anti-Patterns
8. Delivery Checks and Sources

## 1. Usage Order and Pattern Layers

For pattern-name lookup, go directly to Section 2 and read necessary detailed locations. For selection or changes, first read [Architecture Selection](01-architecture-selection.md) to assess whether ordinary code, existing services, or a single model call suffice. When orchestration is needed, read [Orchestration Patterns](05-orchestration-patterns.md) for control structures. Matching a pattern here is a clue only; complete selection rationale before creating Agents.

1. Verify goals, success criteria, actual inputs, existing safeguards, and gaps. Clarify vague goals, obtain missing material, and explore actual unknowns only.
2. Identify the simplest control mode first, then decide whether multiple task roles or independent Agents are needed. Workflow and Multi-Agent may both apply.
3. Find corresponding patterns in Section 2 and read directly relevant detailed locations only, loading chapters as needed. Mark unnecessary patterns as "None."
4. Usually validate one primary orchestration pattern first, adding supporting capabilities for specific gaps only. Retain existing systems meeting criteria; changes require actual gaps.
5. For each candidate, state location, dependencies, benefit hypotheses, costs, and validation actions. With design rationale only, mark "Candidate / To be verified"; effects require empirical testing.

The 21 patterns retain the legacy design-advice Skill's retrieval categories for discoverability. They are an indexing taxonomy, not an official unified classification or complete architecture standard. They span different layers and may combine.

| Layer | Typical Items in This Index | Usage |
|---|---|---|
| Control and task organization | 1 Prompt Chaining, 2 Routing, 3 Parallelization, 4 Reflection, 6 Planning, 7 Multi-Agent Collaboration, 21 Exploration and Discovery | Determine task progression. Planning/exploration are capabilities and collaboration is structure; they occupy different layers |
| Information and action capabilities | 5 Tool Use, 8 Memory Management, 14 Knowledge Retrieval, 17 Reasoning Techniques | Add material, feedback, or execution capabilities needed for completion only; configure each node as needed |
| Standardized integration | 10 MCP, 15 the A2A option for inter-Agent communication | Verify protocols and contracts separately; adopt standard protocols for tool calls or communication as needed |
| Goals, safeguards, and improvement | 9 Learning and Adaptation, 11 Goal Setting and Monitoring, 12 Exception Handling and Recovery, 13 Human-in-the-Loop, 16 Resource-Aware Optimization, 18 Guardrails/Safety Patterns, 19 Evaluation and Monitoring, 20 Prioritization | Cover actual risks, constraints, and reuse needs; prefer existing roles and platforms |

The six primary patterns in [Orchestration Patterns](05-orchestration-patterns.md#1-select-a-primary-pattern-before-deciding-whether-to-combine-patterns) are prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer, and autonomous loops. Orchestrator-workers and autonomous loops have dedicated detailed locations but are not numbered 22 or 23 here. Enter their designs through planning, collaboration, or exploration.

Choose pattern count as needed. "Primary before supporting" means validating primary orchestration first. Necessary permissions, approvals, input checks, resource limits, and success checks take effect from the first execution. Reuse existing host/service implementations directly; none need separate Agent wrappers.

## 2. Overview of 21 Patterns and Self-Review Mapping

Table "signals" produce candidates only; selection conclusions require rationale. Linked chapters provide detailed rules. "Dimensions" are numbered in the [Design Self-Review Checklist](../assets/design-self-review-checklist.md), differently from this table. Select applicable dimensions by actual needs and evidence; scores do not depend on pattern counts.

| Number | Pattern and English Search Name | One-Sentence Definition and Applicability Signals | First Exclusions or Critical Boundaries | Detailed Location | Self-Review Dimension |
|---|---|---|---|---|---|
| 1 | Prompt Chaining | Split known tasks into a fixed sequence with artifact dependencies; consider when one call is insufficient and steps are checkable | Ordinary code or one call suffices; keep necessary original goals and earlier artifacts readable, using previous-node summaries as supplements only | [05 §3 Prompt Chaining](05-orchestration-patterns.md#3-prompt-chaining) | 1 |
| 2 | Routing | Select processing paths by permitted categories or current state; consider when classification actually changes handling | Paths are substantively identical; provide fallbacks for unknown, multiple-intent, and invalid categories, checking authorization separately | [05 §4 Routing](05-orchestration-patterns.md#4-routing) | 2 |
| 3 | Parallelization | Process independent tasks concurrently or generate/compare multiple candidates for one task; demonstrate end-to-end benefits | Dependencies not ready or shared-write conflicts; majority opinions are references only, and missing required branches require partial-completion reports | [05 §5 Parallelization](05-orchestration-patterns.md#5-parallelization) | 3 |
| 4 | Reflection | Correct candidates through valid evaluation feedback; consider with explicit criteria and measurable iteration value | Transient retries belong to exception recovery; checks determine acceptance, self-reported satisfaction is a clue only, and new versions need required checks anew | [05 §7 Evaluator-Optimizer](05-orchestration-patterns.md#7-evaluator-optimizer-and-reflection) | 4 |
| 5 | Tool Use | Read actual information or perform actions beyond language generation through controlled interfaces; consider for computation, queries, or operations | Inputs are complete and no actions needed; trusted layers check permissions and parameters before actual tool execution | [03 §1 Tool Set](03-tool-design.md#1-select-a-minimal-tool-set-with-clear-responsibilities) | 5 |
| 6 | Planning | Turn goals into tasks, dependencies, and execution plans; consider when facts must reveal or adjust routes | Fixed workflows suffice; planning, checking, and execution may be logical stages. Replanning reassesses dependencies and retains original permissions | [05 §9 Planning or Exploration](05-orchestration-patterns.md#9-add-planning-or-exploration-as-needed) | 6 |
| 7 | Multi-Agent Collaboration | Divide work among restricted task units with handoffs; consider actual context, tool, or permission isolation value | Specialist names, many steps, and complexity are clues only; compare single Agents, tool groups, and multiple calls first | [06 §1 Reasons for Independence](06-multi-agent-collaboration.md#1-decide-who-needs-to-exist-independently) | 7 |
| 8 | Memory Management | Manage context, task state, and reusable history as needed; consider conversation continuity, resumption, or stable experience reuse | Caches/storage are carriers only; design long-term memory separately. Cross-task retention requires admission, sources, scopes, and invalidation governance | [04 §1 Information Types](04-context-and-memory.md#1-distinguish-context-task-state-long-term-memory-and-knowledge-sources), [§6 Long-Term Governance](04-context-and-memory.md#6-design-long-term-memory-admission-and-governance) | 8 |
| 9 | Learning and Adaptation | Turn verified feedback into controlled cross-task improvement; consider stable failure categories or actual adaptation needs | Feedback collection and in-task repairs are short-term improvement; maintainers control changes to code, weights, and safety rules | [08 §9 Controlled Learning](08-evaluation-and-iteration.md#9-data-feedback-retrospectives-and-controlled-learning) | 9 |
| 10 | Model Context Protocol (MCP) | Discover/integrate external tools, resources, or prompt templates through standard interfaces; consider cross-client/service reuse or existing reliable services | A few local functions/SDKs suffice; separately verify authentication/authorization, business correctness, and client capability support | [03 §7 Integration Responsibilities](03-tool-design.md#7-assign-responsibilities-to-local-functions-mcp-and-skills) | 15 |
| 11 | Goal Setting and Monitoring | Associate goals, milestones, and completion checks, tracking progress; consider long tasks or staged delivery | Simple tasks need completion criteria only; measure progress by artifacts/checks, with existing hosts handling monitoring | [02 §4 Milestones](02-individual-agent-design.md#4-add-milestones-and-progress-monitoring-as-needed) | 16 |
| 12 | Exception Handling and Recovery | Choose bounded retries, degradation, escalation, or recovery by errors, action states, and remaining quotas | Actions may have occurred on timeout; verify unknown outcomes first. Recovery, model switches, and returning to nodes retain cumulative budgets | [07 §4 Error Classification](07-human-intervention-reliability-and-security.md#4-classify-errors-and-select-bounded-recovery), [§6 Recovery](07-human-intervention-reliability-and-security.md#6-save-resume-cancel-and-degrade) | 10 |
| 13 | Human-in-the-Loop (HITL) | Add clarification, stage confirmation, action approval, or exception takeover at necessary nodes | High model confidence never waives approval. Approval comes only from explicit decisions bound to actual requests; check authorization separately | [07 §2 Intervention Points](07-human-intervention-reliability-and-security.md#2-design-necessary-human-intervention-points), [§3 Request Binding](07-human-intervention-reliability-and-security.md#3-bind-actual-requests-to-trusted-decisions) | 11 |
| 14 | Knowledge Retrieval; Retrieval-Augmented Generation (RAG) | Obtain relevant evidence from authorized sources to support generation; consider material absent from current inputs or versions needing verification | Read supplied accessible material directly; RAG need not use vector databases. Verify whether citations support conclusions separately | [04 §7 Retrieval and Evidence](04-context-and-memory.md#7-choose-retrieval-methods-and-evidence-rules-for-the-task) | 17 |
| 15 | Inter-Agent Communication; Agent-to-Agent (A2A) as needed | Define who sends what to whom, task association, and result retrieval; choose direct calls, state, or messages as needed | Choose ordinary communication methods as needed, adopting A2A optionally. Capability cards describe services only; describe custom HTTP classes as custom interfaces. Separate acknowledgments from business acceptance | [06 §6 State and Communication](06-multi-agent-collaboration.md#6-design-shared-state-and-communication), [§7 Message Boundaries](06-multi-agent-collaboration.md#7-handle-concurrency-message-acknowledgments-and-late-results) | 18 |
| 16 | Resource-Aware Optimization | Manage calls, time, and costs within quality/privacy/compatibility constraints and compare necessary optimizations | One fixed model may suffice; all branches share quotas, reserve before calls, and explicitly label rough estimates | [07 §7 Shared Budgets](07-human-intervention-reliability-and-security.md#7-enforce-shared-resource-budgets) | 19 |
| 17 | Reasoning Techniques | Select stepwise analysis, actions driven by real feedback, or bounded candidate comparisons by task | Read actual material when facts are needed; no need to publish internal chains of thought. Select chain-of-thought, ReAct, or tree-of-thought as needed | [02 §5 Reasoning Approaches](02-individual-agent-design.md#5-select-necessary-reasoning-approaches) | 12 |
| 18 | Guardrails/Safety Patterns | Enforce trusted identity, authorization, data, and necessary isolation at input, reading, execution, and output boundaries | Prompts, regex, detectors, and containers each cover some risks only; required security-component failures deny dependent actions by default | [07 §8 Security Boundaries](07-human-intervention-reliability-and-security.md#8-enforce-permissions-identity-and-security-boundaries) | 13 |
| 19 | Evaluation and Monitoring | Check quality, actual terminal states, processes, and resources with explicit cases and production signals | Separate design scores, success rates, and release permission. Invalid scoring means undetermined; observability and execution guardrails complement each other | [08 §5 Scoring](08-evaluation-and-iteration.md#5-scoring-define-the-object-before-choosing-the-judge), [§8 Production Monitoring](08-evaluation-and-iteration.md#8-production-monitoring-derive-signals-from-business-goals) | 14 |
| 20 | Prioritization | Order authorized, dependency-ready tasks by explicit criteria; consider resource competition or deadlines | Fixed order/FIFO suffices; high priorities still satisfy dependencies, approvals, and budgets, with tie-breaking and maximum-wait rules | [06 §8 Priorities](06-multi-agent-collaboration.md#8-design-priority-scheduling-as-needed) | 20 |
| 21 | Exploration and Discovery | Form hypotheses on actual unknowns, find support/counterevidence, and validate; consider discovering methods or explanations | Retrieve ordinary facts directly; model opinions become discoveries only after verification. Define scope, evidence criteria, and stopping exits | [05 §9 Planning or Exploration](05-orchestration-patterns.md#9-add-planning-or-exploration-as-needed) | 21 |

Items 10 to 19 differ in order from self-review dimensions: MCP is pattern 10 but dimension 15; exception recovery is pattern 12 but dimension 10. Put self-review dimension numbers in review reports' dimension columns. English names and abbreviations aid retrieval; natural-language questions may map to multiple patterns.

## 3. Trace Engineering Clues to Actual Behavior

For existing systems, reconstruct inputs, processing, artifacts, actual execution paths, and safeguards before recommending necessary changes. Directories, class names, keywords, and frameworks are location clues only. Actual behavior determines pattern use, correctness, and upgrade needs.

| Searchable Clue | Facts Requiring Further Verification | Candidate Locations and Common Misjudgments |
|---|---|---|
| `pipeline`, `chain`, `workflow`, stage functions | Actual call order, artifact dependencies, LLM nodes, and failure gates | Prompt chaining; retain pure ETL or ordinary-code sequences directly |
| `registry`, `handler`, branch conditions | Permitted categories, genuinely different handling responsibilities, and unknown/multiple-intent paths | Routing; registries may merely implement dependency injection or plugin loading |
| `asyncio.gather`, thread pools, batch processing | Current input readiness, read/write conflicts, actual concurrency limits, and aggregation | Parallelization; distinguish batching from concurrency, and concurrency from Multi-Agent |
| `retry`, `refine`, repair loops | Service-failure retries versus valid quality feedback on versioned candidates | Exception recovery or reflection; the same retry word can describe different mechanisms |
| `client`, `caller`, tool definitions | Actual callers, input constraints, identities, object permissions, and returned evidence | Tool use; ordinary code may initiate external calls on fixed paths |
| `plan`, `decompose`, topological sorting | Fixed predefined graphs versus new tasks from current inputs; whether new evidence invalidates plans | Planning; DAGs may be predefined, and complexity still requires rationale before planners |
| Multiple `Agent` classes, `coordinator` | Actual instances, task relationships, isolation value, handoffs, and acceptors | Multi-Agent collaboration; class names and job counts are clues only |
| `memory`, `session`, `state`, `cache` | Current context, trusted task state, performance caches, or cross-task memory | Memory management; databases/vector databases are carriers only. Decide contents as needed |
| `feedback`, `train`, policy configuration | Verified signals, versioned proposals, validation, approval, and activation | Learning/adaptation; logs, likes, and A/B configuration are signals only, with learning effects separately validated |
| MCP configuration, service discovery, protocol clients | Actually loaded/called services, supported capabilities/versions, authorization, and call boundaries | MCP; actual calls establish connectivity and business compatibility |
| `confirm`, `approve`, `review` | Actual human involvement, approval sources and object/body/version binding, pre-execution blocking | Human-in-the-Loop; review functions may be automatic checks only |
| `retrieval`, `embedding`, indexes | Authorized sources, query filters, original results/versions, and citation support | Knowledge retrieval; separately verify factual correctness and read permissions. Vector similarity supports recall only |
| Messages, topics, subscriptions, endpoints/capability cards | Who may send/receive, instance association, delivery states, and business acceptance | Inter-Agent communication; microservices/event-driven systems adopt A2A as needed |
| `guard`, `validate`, filters | Actual nature of checks, failure destinations, and actual non-execution on rejection | Safety; format validation is one layer only. Check identity/authorization separately |
| `score`, `metric`, progress, deadline | Task milestones, case scoring, production monitoring, or ready-task scheduling; denominators/deadlines/owners | Goal monitoring, evaluation, priority, or resources; distinguish by actual use |

For code investigation, read entry points and actual call sites within user-specified scope, following evidence. Limit reads to specified material; secrets and software installation are out of scope. Discard the legacy guide's "high/medium weights," line-count thresholds, and fixed mappings from layered/microservice styles to patterns.

Without implementation or run evidence, state "To be verified" and necessary entry points. List design omissions only after confirming necessary missing mechanisms. Missing keywords mean not found yet; one log establishes one run only.

## 4. Assess Whether Combinations Are Valid

First define who controls the next step, which data must be ready, and who checks/accepts which version. Assess combinations pairwise; compatibility matrices and combination scores are unnecessary.

| Candidate Combination | Validity Conditions and Boundaries | Simplest Alternative When Invalid |
|---|---|---|
| Prompt Chaining + Routing | Continue passing original goals and required artifacts between nodes; define route responsibilities and fallbacks | Use one path or rule-based decisions directly when sufficient |
| Prompt Chaining + Parallelization | Parallelize dependency-ready branches only; aggregation checks identity, versions, and all required items | Run sequentially with ordering dependencies; obtain missing inputs first |
| Routing + Reflection | Branch candidates can be independently evaluated. Correct misclassification within permitted categories and recheck inputs/authorization | Routing may combine with reflection too; clarify insufficient evidence before deciding category changes |
| Parallelization + Reflection | Bind feedback to branches/versions. Share authorized standards/facts as permitted, isolating candidates/feedback by branch; checks determine passing | Review serially without independence or benefit; define review-context visibility as needed |
| Planning + Collaboration/Orchestrator-Workers | Hosts validate dynamic tasks; dispatch ready tasks only. Actual isolation/handoffs add value, and fan-out/delegation share budgets | Use fixed chains/parallelism for known tasks; one executor directly when sufficient |
| Knowledge Retrieval + Memory | Separate sources, freshness, scopes, and updates for authoritative knowledge versus personal/project history; load necessary evidence only | Read supplied material directly; session state suffices for current-conversation continuity |
| Human-in-the-Loop + Evaluation/Learning | Approval permits actions only; verify quality labels separately, activating updates only after validation/approval | Use manual checks or periodic retrospectives when sufficient; introduce automatic training as needed |
| Tools/MCP + Safety/Recovery/Resources | Trusted layers check actual identity, parameters, objects, request binding, and quotas; verify unknown side effects before deciding | Reuse existing SDKs/functions and safeguards, retain identity, and verify unknown outcomes first |

Every back edge has a termination exit. Local repairs, replanning, model/tool retries, delegation, and aggregation share applicable task quotas, reserving necessary final checks. Every business branch completes resource and security checks.

In the [Handoff Contract](../assets/handoff-contract-template.json), `SUCCESS` means a complete execution return and may coexist with `verdict=FAIL`. `PARTIAL/remaining` and `BLOCKED/blockers` indicate incomplete passing. Pattern recommendations retain existing generic states, fields, and protocols; define actual business fields per task separately.

## 5. Minimal Candidate Combinations for Six Scenario Categories

The six scenarios retain legacy Skill categories for retrieval. All following combinations are conditional design candidates, not empirically tested in this chapter; tailor them by scenario. Requirements determine architecture; industry/project names are references only. Necessary security, budgets, completion checks, and exception exits apply from the start in each example.

### Scenario A: Automated Testing Platform

- Simplest baseline: retain ordinary code when existing test runners execute and report sufficiently; use models only where language capabilities are genuinely needed.
- Primary candidate: consider prompt chaining for natural-language test generation; add routing only when inputs genuinely require different test paths.
- Conditional additions: testing/build tools; bounded reflection driven by valid failure feedback; parallel independent checks on the same version. Add planning/exploration only to discover unknown test routes.
- Required controls: retain requirements, test targets, code/environment versions. Record unexecuted cases, environment errors, and scoring errors separately; none counts as passed tests. Restrict test-environment networks, credentials, and writes; replace production side effects with controlled targets.
- Validation: compare coverage, defect detection, false positives, execution rates, and end-to-end time/cost against existing human/rule-based baselines; check timeouts, environment failures, and retesting after final repairs.

### Scenario B: Intelligent Customer Service

- Simplest baseline: use one classification/reply candidate directly when supplied tickets, categories, and FAQs suffice; use fixed routing workflows for genuinely different handling paths.
- Primary candidate: routing; add knowledge retrieval as needed when answers depend on unavailable trusted material. Introduce RAG and autonomous loops as needed.
- Conditional additions: controlled queries such as orders and multi-turn session state. Embed one Agent in investigation branches only when actual tool feedback determines next steps. Consider long-term memory only for stable cross-session preference reuse.
- Required controls: clarify or escalate unknown/multiple intents; check object permissions and actual approvals for refunds/external sends under policy. Read FAQs/customer data under recipient permissions; check refund authorization separately.
- Validation: known/unknown/multiple intents, missing material, wrong objects, unapproved actions, and unknown tool outcomes; verify answer support, human transfers, and actual side effects. Introduce multiple Agents, model routing, and learning platforms only as needed.

### Scenario C: Code Generation and Review

- Simplest baseline: retain deterministic templates or one generation plus checks when sufficient; use workflows for explicit stage dependencies.
- Primary candidate: prompt chaining; combine evaluator-optimizer when reviews provide valid feedback and repair adds value. Return unchanged when no issues exist.
- Conditional additions: controlled static-check/test tools; parallel independent checks on the same version. Split Agents only for actual isolation value. Orchestrate known steps directly; introduce Planners, long-term memory, and autonomous loops as needed.
- Required controls: review reads original requirements/code; repair reads original code, corresponding-version comments, and necessary tests together. Rerun required checks after changes; old reports concern old code only. Generated code receives necessary network, secret, and system permissions only.
- Validation: missing original code, wrong review versions, no-change cases, invalid reviews, failed repairs, and exhausted budgets. Deliver the same actually checked version; return an unchecked final candidate as not passed.

### Scenario D: Data Processing Pipeline

- Simplest baseline: use SQL, scripts, or existing ETL for deterministic extraction, transformation, and aggregation; start there even for large volumes.
- Primary candidate: prompt chaining when semantic extraction/rewriting is necessary; add parallelization for independent shards with end-to-end benefits.
- Conditional additions: stage goals/progress; prioritization only for competing quotas/deadlines. Reuse existing checkpoints/task records for recovery; introduce message queues as needed.
- Required controls: explicit shard identity, input/artifact versions, concurrency limits, aggregation completeness, and write ownership. Distinguish permitted partial success from required overall consistency. Handle duplicates, late/failed shards, and unknown outcomes; execution interfaces guarantee idempotent writes separately from acknowledgments.
- Validation: compare accuracy, throughput, end-to-end latency, and costs with sequential baselines. Check missing/out-of-order/duplicate shards, shared-write conflicts, and exceeded limits; report partial completion when critical shards fail.

### Scenario E: Multi-Agent Collaboration System

- Simplest baseline: first assess actual role-independence needs; use fixed nodes or one Agent directly when sufficient.
- Primary candidate: separately choose fixed chains/parallelization or orchestrator-workers as control modes. Multi-Agent collaboration describes structure; control mode determines execution order. Keep fixed development stages fixed; introduce dynamic delegation as needed.
- Conditional additions: actual communication. Use same-host shared state or direct calls when sufficient; verify A2A or similar standards for necessary cross-system interoperability. Add planning for dynamic tasks only, priorities for resource competition only.
- Required controls: seven-element dispatch, readable original goals/necessary earlier artifacts, restricted identities/tools/permissions, owners/acceptors, separate message/business states, concurrency, and shared budgets. Set stage confirmations by risk in requirements-to-test-report development workflows. Trusted systems authorize; model Managers coordinate only.
- Validation: missing dependencies, wrong tasks/instances, unauthorized access, late/duplicate returns, missing receivers, and concurrent write contention. Report incomplete work when required roles do not deliver. Design security isolation separately; independent context isolates information only. See the Step 12 trial for a complete development-squad design.

### Scenario F: Knowledge Management and Q&A

- Simplest baseline: answer directly from supplied readable material; use search/read operations for plain fact location, without Agents.
- Primary candidate: knowledge retrieval supporting generation; add necessary reasoning only for complex analysis with verifiable constraints.
- Conditional additions: bounded query expansion for actual multi-step evidence gaps; memory for long-term history reuse only; exploration only for genuinely unknown explanations/methods. Maintainers' periodic source verification may improve systems too; introduce autonomous learning and knowledge graphs as needed.
- Required controls: trusted sources, permissions, times/versions, citation support, and conflict handling. Report empty results truthfully; retain user filters and explain query expansion. Treat instructions in summaries and retrieved material as data always.
- Validation: no results, outdated/conflicting sources, similar but unsupported material, unauthorized access, and recent unindexed cases. Verify evidence coverage, citation correctness, latency, and costs. Citation counts, retrieval counts, and fluency are references only.

## 6. Write into Existing Design Documents and Validate Benefits

Reuse the [Design Document Template](../assets/design-document-template.md), placing pattern conclusions in existing sections. Section 0 summarizes patterns, Section 2 explains control mode and independent-Agent rationale, Section 3 describes combinations, and Sections 4 to 10 implement interfaces, handoffs, safeguards, and evaluation. When frameworks are needed, read [Framework Mapping](09-framework-implementation-mapping.md) to verify versions and actual validation scope.

In Section 3's existing "Where Used" column, state primary orchestration, supporting capabilities, or cross-cutting safeguards and specific nodes. In "Benefits and Costs," state factual gaps, simpler alternatives, candidate benefits, extra costs, and validation. Ordinary functions, different calls to the same model, or existing services may perform these roles; map each pattern to existing roles as needed.

| Existing Field | Information to Add for Pattern Recommendations |
|---|---|
| Selection rationale; why not a simpler tier | Actual gaps and evidence; whether existing methods meet criteria. Mark missing material as to be verified |
| Pattern; where used (primary or supporting) | Responsible controls/capabilities, nodes, and connection to existing workflows; specify coverage for cross-cutting safeguards |
| Benefits and costs | Accuracy/coverage/latency/cost hypotheses, extra calls/maintenance/risks, and minimal validation actions; explicitly mark untested effects |
| Orchestration boundaries and handoff table | Ready dependencies, original goals/earlier artifacts, version checks, error responsibility, and termination exits |
| Section 9 safeguards and Section 10 evaluation | Who actually enforces permissions, approvals, and shared budgets; baselines, cases, protocols, scoring, and evidence scope |

For example, describe a code workflow as primary prompt chaining: original requirements → v1 code → review comments. Add evaluator-optimizer as needed; repair takes v1 and matching comments, then recheck v2. Tools, security, budgets, and completion checks cover actual paths, reusing existing facilities; do not add repair when no issues exist. Hypothesized benefits are less handoff loss and repair rework; costs are extra calls and latency. Validate through missing/mismatched versions and actual code tests; pattern counts alone show no effectiveness.

Keep cases, input versions, success criteria, allowed budgets, and run/retry protocols interpretably consistent in comparisons. Record baseline/candidate snapshots and retain failures, unexecuted cases, invalid scoring, and every rerun. Check task success, resource constraints, and required security separately; judge hard failures independently. Averages or cherry-picked best results cannot hide them.

Design rationale, manual rule walkthroughs, static/in-memory checks, real integration, and business trials establish different scopes. Complete indexes, reachable links, code keywords, or valid Schema establish document-level correctness only. Model quality and production effects need actual evidence; execute under [Evaluation and Iteration](08-evaluation-and-iteration.md) when necessary. All benefit descriptions in this index await validation.

Reject, postpone, or return to simpler approaches for supporting patterns without benefit evidence; still check dependencies, safety, and business effects at rollback. Choose pattern counts, code scale, and team division by need. Do not retain the legacy guide's quota of 2-4 patterns first. Preserve all actually necessary safeguards when simplifying overdesign.

## 7. Commonly Confused Concepts and Anti-Patterns

| Confused Concepts | Distinction to Make Explicit |
|---|---|
| 21 patterns versus 21 review dimensions | Numbering serves separate purposes in different orders. Score dimensions by applicability/evidence, independently of pattern counts |
| Prompt chaining versus chain-of-thought | The former organizes multi-step artifacts/calls; the latter is an analysis method. Stepwise explanation is chain-of-thought; design multi-node pipelines separately |
| Reflection versus exception retries/learning | Separate feedback-based in-task quality correction, transient-failure recovery, and controlled cross-task improvement. Determine which a retry implements |
| Planning versus orchestrator-workers | Planning produces tasks/dependencies; orchestrator-workers dynamically dispatches/aggregates. They may combine; fixed task lists are predefined orchestration |
| Exploration versus knowledge retrieval | Exploration hypothesizes/verifies unknown explanations/methods. Retrieve ordinary facts first; search counts do not determine exploration |
| Goal monitoring versus evaluation monitoring | Goal monitoring tracks current task artifacts/progress; evaluation examines cases/production performance. Both establish completion through check evidence |
| Memory, knowledge, and caching | Memory reuses history, authoritative knowledge supplies current facts, and caches reduce repeated access. Manage sources/freshness/permissions separately even on shared storage media |
| Routing, tools, MCP, and A2A | Routing selects paths, tools supply actions, MCP standardizes integration, and A2A optionally enables cross-Agent interoperability. Define authorization/business contracts separately |
| Multi-Agent, parallelism, and microservices | Justify collaboration structure, execution mode, and deployment form separately. Assess role count versus parallelism, and service count versus Agent necessity separately |

Anti-patterns: high match scores from directories alone; fixed matrices treated as compatibility proof; filling fixed primary/supporting/optional quotas; making security or quality evaluation merely optional; requiring critic, Planner, or resource-router Agents; creating directories for every pattern; adding long-term memory, vector databases, A2A, queues, or automatic training for scores; model confidence waiving approval; attaching old green reports to new versions; static-checklist results treated as runtime effects; pattern recommendations implicitly authorizing code refactoring.

## 8. Delivery Checks and Sources

When delivering pattern selections, check the following and implement selected patterns only:

- State actual reasons ordinary code or single calls are insufficient; distinguish control modes, task roles, and instances.
- Find necessary detailed pattern locations. Separate this table's numbers from review dimensions; give reasons or required evidence for not-applicable and to-be-verified items.
- Map selected primary orchestration and supporting capabilities to concrete gaps, recording benefits, costs, and validation plans in existing templates.
- Ensure ready dependencies, readable original goals/necessary earlier artifacts, and matching versions/acceptance. Give back edges, aggregation, and unknown categories explicit exits.
- Cover first execution and all branches with necessary identity/authorization, approval, budgets, and success checks, enforced by trusted hosts/services.
- Trace engineering clues to behavior and evidence. Limit refactoring, scanning, and framework upgrades to user-authorized scope.
- Tailor six scenarios to actual inputs/paths, labeling combinations conditional and pending empirical testing.
- Keep detailed architecture, security, evaluation, and other rules authoritative in corresponding chapters. Record conflicts and correct under user authorization, retaining original boundaries.

Sources: The legacy design-advice Skill (agentic-design-advisor), including 21 pattern definitions, matching guidance, and six scenario combinations; Anthropic's Building Effective Agents, including simple approaches, five workflow categories, and autonomous loops; and this Skill's architecture, tool, context, orchestration, collaboration, security, and evaluation chapters. Retain legacy pattern names for retrieval. Layers, conditional combinations, dimension mappings, engineering-clue counterexamples, and benefit validation are engineering syntheses by this Skill. The 21 items form an indexing taxonomy, not an official standard. This chapter is an index only; pattern effectiveness remains to be verified.
