# Multi-Agent Collaboration

Use this reference when Step 4 of the main process requires multiple Agents, or when reviewing overlapping roles, information loss at handoffs, shared-write conflicts, and orphaned tasks. Reuse architecture-selection and orchestration conclusions first. This chapter adds role, dispatch, state, and acceptance boundaries; see the orchestration chapter for patterns. Digital-employee platforms are outside its scope.

## Contents

1. Decide Who Needs to Exist Independently
2. Define Responsibilities and Least Privilege
3. Choose Coordination Structures and Delegation Boundaries
4. Build Self-Contained Dispatch with Seven Elements
5. Return Results and Perform Handoff Acceptance
6. Design Shared State and Communication
7. Handle Concurrency, Message Acknowledgments, and Late Results
8. Design Priority Scheduling as Needed
9. Codify Collaboration in SOPs and Map to Frameworks
10. Minimal Examples, Delivery Checks, and Anti-Patterns

## 1. Decide Who Needs to Exist Independently

Different responsibilities are a signal for splitting, not sufficient justification. For each additional Agent, identify what genuinely requires isolation, why on-demand loading, staged prompts, or restricted tool calls within one Agent are insufficient, and the added latency, cost, and handoff risks.

| Isolation Dimension | Questions to Answer | Simpler Alternatives to Consider First |
|---|---|---|
| Context and data | Would independent investigations produce extensive irrelevant traces, or would domain material, task state, or necessary working rules be unsuitable for one shared context? | On-demand loading, pruning, notes, and independent task nodes; long-term memory only as needed |
| Tools and execution capabilities | Do significantly different tools, SOPs, or environments cause incorrect capability selection, state contamination, or unstable execution when mixed? | Stage-restricted tools, Skill reuse, and restricted functions; start here when only adding tools |
| Permissions and trust boundaries | Must reads/writes, business authorization, or sensitive-data scope be separated? Does the reviewer need read-only access to source artifacts? | Host-enforced scopes and execution identities; retain necessary security boundaries separately even if the other two dimensions match |

One actual isolation need can justify splitting, but still compare with simpler candidates; dimension counts do not earn points. Consider decision preferences only when they form necessary working rules. Job titles such as engineering or QA are references only; decide whether to combine QA and security from actual isolation needs.

Count role templates, task nodes, and instances separately. One implementation Agent may perform design, coding, and repair in sequence; multiple research instances may share a role template while keeping separate task contexts. A fixed multi-role pipeline remains a workflow; role count does not change control mode. Reduce roles when they can be merged, retaining those needing isolation.

Anti-patterns: splitting by file count or organization chart; requiring differences in three or two dimensions before splitting; giving every Agent a persona and long-term memory; renaming roles while sharing all history and tools; assuming multiple Agents are more reliable by default.

## 2. Define Responsibilities and Least Privilege

Write a Role Charter for each role: responsibilities, exclusions, artifacts and checking criteria, and dispute escalation. Every work item has a definite owner and acceptor. The same role may handle compatible tasks; owners have write permissions only within assigned scope.

| Candidate Role | Typical Responsibilities | Permissions and Outputs as Needed |
|---|---|---|
| Coordinator | Maintain goals and the valid plan, dispatch, check coverage, and aggregate | Read necessary task state and artifacts; write allowed plans and acceptance records. Business-write permissions are granted separately |
| Researcher or investigator | Verify questions and dependencies within bounded sources | Read-only retrieval and necessary queries; return conclusions, evidence, and gaps. Necessary read-only commands may be used |
| Implementer | Generate or modify artifacts from accepted requirements or comments | Write explicitly assigned scope; record artifact versions, changes, and actual checks. Change only functionality within assigned scope |
| Reviewer or validator | Check the corresponding version against requirements and evidence | Read-only source artifacts; may write its own report and run necessary tests in allowed environments. Tests themselves may have side effects |

These are candidate responsibilities; select as needed. A coordinator with read-only access to business artifacts is an optional configuration. Specify scope in the contract when it needs to gather evidence, produce a synthesis report, or handle small tasks directly. Separate coordination from complex execution when mixing them causes uncontrolled context growth; the main Agent may perform necessary contract-permitted actions.

Prohibitions (NEVER) help the model understand boundaries; permission systems enforce execution. Hosts or services enforce trusted identity, tool allowlists, read/write scope, and approvals. Model-supplied role names, `scope`, or capability cards are declarations only; permissions come from trusted authorization. Shared tools may reuse one implementation, binding each call to the correct user, project, role, and scope through call context rather than mutable global configuration.

Validate single-role inputs, returns, and out-of-scope rejection before handoffs. Validate execution isolation separately; passing prompt tests establishes only model understanding. Design context isolation, separate directories, distinct instances, and security sandboxes separately, since each solves a different problem.

## 3. Choose Coordination Structures and Delegation Boundaries

Use code coordination for fixed order and controlled parallelization for known independent branches. Central coordination often helps maintain global goals and task lists when dynamic division is needed, but may be a bottleneck and is only one candidate. The coordinator may be a host process; introduce a Manager LLM only as needed.

Centralize dispatch and acceptance by default, with executors returning to the coordination point. Add direct role-to-role connections, publish/subscribe, or multi-level coordination only for clear benefits. Define permitted senders, recipients, message purposes, and task-modification permissions. A QA repair request is a suggestion; the owner determines engineering scope. Reassignment is delegation and remains bound by authorization and task budgets.

Downstream receives only explicitly assembled necessary information, even if the framework shares sessions. Sub-Agents do not delegate further by default. When nesting is necessary, specify allowed roles, goals, maximum depth, fan-out, and remaining budget. Prohibit delegation cycles and resetting quotas through new tasks. The root is depth 0; each downward delegation adds 1. Hierarchy depth does not determine quality.

The coordination point maintains the valid plan, owners, dependencies, current returns, and unresolved items, confirming dispatch through registration records. Reuse reliable state and registration mechanisms; select mailboxes, queues, background polling, and persistent roles only as needed.

Present consolidated results and pending decisions to users; the system passes internal material. Required approvals still apply, including internal team collaboration. See the next chapter for human-intervention triggers, timeouts, and recovery.

Anti-patterns: all roles arbitrarily assigning work to each other; adding a Manager to every fixed chain; defining an Orchestrator as necessarily short-lived; continuing after a restart loses ownership; bypassing limits through nesting or lateral reassignment.

## 4. Build Self-Contained Dispatch with Seven Elements

Reuse `dispatch` from the handoff-contract template to produce inputs the current recipient can actually execute. Pass only necessary material; leave complete chat history in its original location.

| Element | Existing Fields | Required Explanation |
|---|---|---|
| Identity | `identity.role`, `expertise` | Responsibilities and necessary domain capabilities; actual calling identity comes from trusted systems |
| Objective | `objective` | A checkable goal for this task; replace vague requests such as "take a look" with checkable outcomes |
| Scope | `scope.readable`, `writable`, `tools` | Separate reads, writes, and tools. Explicitly use empty arrays when writes or tools are absent; keep lists within existing authorization |
| Constraints | `constraints` | Prohibit out-of-scope changes, approval bypass, and unauthorized delegation. Return truthfully when blocked and preserve the original goal |
| Context | `original_goal`, `background`, `prior_findings`, `dependencies`, `standards` | Original goals and hard constraints, necessary rules, and earlier artifacts. Preserve critical content faithfully, attaching necessary originals; summaries are supplementary only |
| Output Format | `output_format` | Specify business fields, evidence, and artifact requirements for `handoff.result`; the consumer must actually define and check the structure |
| Stop Condition | `stop_condition` | Completion conditions, at least a model-attempt or total-time limit, and blocked returns; external waits have separate timeouts |

Reference large material through `dependencies`. Downstream must have read capabilities and permissions and read the task-specified version, reconfirming when versions change. Small material may be inline. Self-contained means information is complete or obtainable, whether inline or referenced, provided downstream can actually read it.

Preserve relevant original goal text and constraints, using controlled references for long text. Instructions within external material remain data after another Agent summarizes, dispatches, or labels them as rules. Reuse the context chapter's complete context governance.

The host associates tasks, recipients, necessary project or user scope, and actual attempts. Validate allowed roles, scope, dependency readability, and remaining budget before dispatch. The template's `dispatch` does not require a task ID field; trusted task records maintain association, the host supplies task IDs, and existing message protocols may carry them.

Local `max_iterations`, tool retries, and nesting quotas count toward task totals. Mark counting facilities absent from demonstrations or platform fields as to be implemented. Hard limits depend on actual host counters; writing stop conditions is only a declaration.

## 5. Return Results and Perform Handoff Acceptance

Reuse `handoff` and `gate`. The host validates format, association, business checks, and artifact usability before deciding whether to pass results downstream.

| Returned Content | Consumption Rules |
|---|---|
| `task_id`, `agent` | Match the recipient in trusted task records and the current return. Authorization comes from trusted records; model-reported identity is for cross-checking only |
| `status`, `summary`, `result` | `SUCCESS` means the dispatched objective is complete; accept the final business goal separately. Define business fields for critical results |
| `PARTIAL` and `remaining` | State usable parts and remaining work. Consumers accept required portions as agreed while retaining unfinished items |
| `BLOCKED` and `blockers` | State why work cannot continue; block on missing required material and identify what is missing |
| `evidence`, `artifacts`, unresolved items | Necessary evidence supports conclusions; artifacts can be retrieved and their versions verified; preserve gaps explicitly |
| `verdict` | A validation task may execute successfully and return `FAIL`; an explicit acceptor judges `CONDITIONAL_PASS` conditions |
| `metrics`, `confidence` | Diagnostic or reference information only; actual host records determine budgets, and check results determine acceptance |

The handoff template is a definition library: validate against the corresponding `$defs`. The root object has no constraints and does not perform validation. Generic `result` permits arbitrary objects; completeness requires specific business-field definitions. When version mix-ups must be prevented, make optional fields such as `artifact_ref.version` required in the business contract and check them in the host. Generic Schema guarantees structure only.

`gate.required_fields` and `business_rules` describe rules to execute; the host must actually execute them. Code checks formats and executable conditions, with separate review or humans for necessary subjective judgments. The host reads actual decisions before routing; a checker other than the generator executes business rules.

Confirm artifacts and returns are usable before registering acceptance and passing downstream. Location existence establishes findability only; check body correctness separately. Tool success establishes call completion only; separately verify expected file changes. After upstream versions change, reassess downstream artifacts and check validity. Pause responsible nodes when required dependencies are missing, retaining critical failures truthfully in aggregation.

Handle validation failures through existing `on_fail` options: correct the current step, return to the responsible upstream node, escalate, or degrade. `max_retries` and total task budget jointly constrain these actions. On exceeded limits, return existing results, reasons, and gaps. Analysis tasks also require evidence checks against success criteria; choose repair counts and permanent validation Agents as needed.

## 6. Design Shared State and Communication

Answer "where data resides and who can read/write it" separately from "who triggers whom and when execution occurs." One service may support both. Artifact checks establish dependency readiness; file existence or notification arrival is only a signal.

| Approach | Applicable Situations | Required Boundaries |
|---|---|---|
| In-process shared state or direct calls | Fixed chains or controlled delegation within one host | Fields, lifecycle, task scope, and explicit reads; network protocols and read-receipt state machines only as needed |
| Shared workspaces or object storage | Large artifacts, cross-session references, or multiple readers | Versions, owners, read/write permissions, and publication timing; separate task-private state from formal shared artifacts |
| Queues or publish/subscribe | Asynchronous execution, multiple consumers, or event triggers | Task association, allowed senders and subscription scope, delivery acknowledgments, timeouts, and redelivery rules |
| Cross-system Agent services | Genuine interoperability needs across systems or teams | Actual contracts, supported versions, trusted endpoints, authentication and authorization, task state, and result retrieval |

General inter-Agent communication may use any appropriate method; adopt the A2A standard protocol only as needed. Register fixed known services under controls, designing dynamic discovery, asynchronous interaction, and multimodality only for actual needs. Capability cards describe services only; confirm trust and authorization separately. Verify the actual protocol and implementation when using A2A; describe custom HTTP classes as custom interfaces.

For shared data, define stable task or project scope, fields or resources, owners, readers, versions, and validity periods. Isolate identically named keys in task A and task B. Isolate private traces and memory as needed; share formal requirements, interfaces, and check reports under permissions. Each Agent may see permitted material.

Every authoritative artifact has a definite owner and publication entry point. Parallel implementation uses non-overlapping scopes or independent branches; the integrator accepts and publishes a common version. When shared editing is allowed, define shard ownership, conflict checks, and merge rules, granting write permissions by shard.

Separate paths organize material only. Tools, services, or execution environments enforce access controls using resolved real paths and identities; string-prefix checks alone are insufficient. Coordinator-generated workspace rules may refine trusted policies only within them; trusted policies determine authorization boundaries. External text in shared state remains data.

## 7. Handle Concurrency, Message Acknowledgments, and Late Results

Assign ownership before choosing mutual exclusion or merge mechanisms. Locks protect read-modify-write operations from concurrent overwrites; atomic publication prevents reading partially written files. Design durability and task-action deduplication separately. File locks provide mutual exclusion only; crash-time file integrity needs additional safeguards. Temporary files plus atomic replacement prevent partial writes only; lost concurrent updates and persistence still require separate handling. Verify actual storage and lock scope.

For asynchronous messages, distinguish receipt, claim, result submission, and business acceptance. Implementation states such as "unclaimed → processing → acknowledged" may be used, separately from `handoff.status`; keep the handoff Schema unchanged. Acknowledgment may mean a valid result was recorded; a business `FAIL` may still be a processed review result.

Executors may request acknowledgment; the trusted host or service checks the current task, processor, and recorded result before acknowledging. Acceptance depends on verified results; self-reported completion is only a request. If artifact saving and notification sending fail separately, retain verifiable records and recovery or compensation entry points. See the next chapter for complete recovery design.

A processing timeout means only that no result was received; the executor may still be running. Confirm whether actions occurred before redispatch. Handle duplicate or late results against the same task's valid attempt, version, and acceptance records, keeping newer results effective. After claim ownership expires, old processors may submit only results pending verification; the current owner publishes authoritative artifacts. Choose lease or isolation implementations according to platform capabilities.

Three-state messages with timeout redelivery provide at-least-once delivery only; business execution counts require separate guarantees. Notification deduplication and business-action idempotency are different. Execution interfaces verify and constrain repeated writes, sends, and other side effects. Synchronous notifications plus polling are an optional combination; direct calls suffice for simple sequential chains. See the reliability chapter for specific idempotency, cancellation, and recovery facilities.

Check actual isolation under concurrency: instance tool identities, context, global hooks, and caches may be mixed across instances. A framework requiring a global lock is an implementation-specific issue; decide team serialization from actual needs. Document evidenced compatibility limits in implementation mapping.

## 8. Design Priority Scheduling as Needed

Add Prioritization only when resource contention, deadlines, or competing importance affect tasks. Use fixed dependencies or First-In, First-Out (FIFO) directly when sufficient; add model scoring, dynamic reordering, or complex queues only as needed.

First filter tasks lacking authorization, inputs, dependencies, resources, or budget, then select from the ready set under explicit rules. High-priority tasks must also wait for dependency readiness and approvals. Before selecting work, the host checks and reserves concurrency and budget centrally, preventing simultaneous over-dispatch by branches reading the same remaining budget.

When ranking is needed, define criteria, tie-breaking, and maximum-wait handling. Use urgency, business value, deadlines, and resource costs as needed; use rules directly when sufficient. Reorder only when new events actually change the criteria. Set maximum waits to prevent indefinite low-priority starvation; cancellation or preemption of running tasks needs separate permitted conditions.

Priority determines ready-task order, not goals or permissions. Retain selection reasons and task identity; internal chains of thought need not be disclosed. Reuse orchestration rules for limits and global counting.

## 9. Codify Collaboration in SOPs and Map to Frameworks

Standard Operating Procedures (SOPs) record goals, necessary stages, participating responsibilities, inputs and artifacts, acceptance, branch conditions, stopping, and escalation rules. They suit on-demand reuse through Skills. Hosts or services still enforce fixed executable constraints. SOPs guide the model in choosing allowed actions while code retains reliable fixed boundaries; "zero Python orchestration" is only a slogan.

When SOPs change, check compatibility of roles, fields, dependencies, and checks, with risk-appropriate review and regression. Check trusted rosters and permissions for new roles as well; verification establishes compatibility. See the evaluation chapter for team retrospectives and continuous improvement. Review memory, Skill, and code changes as needed.

Frameworks carry the same handoff design: ADK sequential execution uses `output_key` to store state, with downstream explicitly reading necessary keys; LangGraph uses State and conditional edges; CrewAI uses task outputs and necessary `context`; AutoGen uses typed messages and topic subscriptions. These mechanisms carry data only; the host still designs original-goal transfer, version validation, and business acceptance. See the framework chapter for specific versions and scaffolding code.

## 10. Minimal Examples, Delivery Checks, and Anti-Patterns

The following are design candidates and contract examples. Model, scheduling, and business effectiveness have not been measured; demonstration limits are illustrative only.

### Example 1: Generate → Review → Repair if Needed

This is a fixed workflow using multiple restricted Agents because generation/review contexts and source-code write permissions are separated. The code implementer may also perform repair; two roles suffice, with no additional Manager needed. The host controls order, shared versions, and acceptance.

Example repair dispatch to the implementer (state keys are logical locations; the host supplies read/write mappings):

```json
{
  "identity": {"role": "Code Implementer", "expertise": "Python"},
  "objective": "Repair only issues identified in review; return the code unchanged when no modification is necessary",
  "scope": {
    "readable": ["state.generated_code", "state.review_comments"],
    "writable": ["state.refactored_code"],
    "tools": []
  },
  "constraints": ["Do not change requirement scope", "Do not delegate further", "Return BLOCKED when required inputs are missing"],
  "context": {
    "original_goal": "Implement a word-count function that correctly handles empty strings and punctuation",
    "dependencies": [
      {"name": "generated_code", "location": "state.generated_code", "version": "code-v1"},
      {"name": "review_comments", "location": "state.review_comments", "version": "review-v1"}
    ],
    "standards": "Review results must identify the checked version; recheck after repair"
  },
  "output_format": "handoff.result = {refactored_code: string, applied_comments: string[]}",
  "stop_condition": {"success": "Return complete code and how comments were addressed", "max_iterations": 1, "on_blocked": "Identify missing material"}
}
```

The host first reads and verifies both dependencies. The review's business result must carry `reviewed_version = code-v1`; comments without original code cause blockage. In this example, the host inlines verified material and saves returned artifacts, so no tools are called. If autonomous reading is needed, declare already-authorized read tools in `scope.tools`.

The demonstration allows at most 6 attempted model calls across the task and at most 1 repair, with timeouts for models and external checks. Review, repair, and re-review share the total. Return unchanged when there are no issues; deliver a new version as passed only after required checks finish.

### Example 2: Controlled Parallel Read-Only Investigation

Multiple independent sources genuinely require isolation of detailed traces. Use different instances of the same investigation role or different restricted tool configurations. The host coordinates; personas, long-term memory, and dynamic service discovery are unnecessary. Each dispatch retains the same original question, divides scope by source, and returns conclusions, evidence, and gaps. The coordinator checks conflicts and coverage.

Example return when a required source is unreadable:

```json
{
  "task_id": "investigate-source-b",
  "agent": "investigator-b",
  "status": "BLOCKED",
  "summary": "The required source is currently unavailable",
  "result": {},
  "blockers": ["Source access was denied; this branch's conclusion has not been verified"],
  "unresolved_questions": ["Whether the source contains evidence supporting or refuting the original question"]
}
```

The host associates task IDs with actual instances. The demonstration uses 2 branches, concurrency limit 2, at most 5 attempted model calls in total, and at most 2 per branch, reserving attempts for aggregation and setting timeouts for every external wait. Skip model aggregation when budget is insufficient. If a required branch is blocked, report overall partial completion or blockage, stating gaps when partial results are permitted. List evidence conflicts truthfully and judge evidence itself; majority votes are a reference only.

### Delivery Checks

In the design document, Section 4 defines roles and isolation reasons, Section 5 tool permissions, Section 7 handoffs, state, and delegation, and Section 9 unified budgets and failure rules. Without cross-system services or resource contention, mark communication-protocol and prioritization enhancements not applicable, with reasons.

- Check that role, node, and instance counts are clear, no responsibilities are orphaned, and each additional Agent has actual isolation and cost justification.
- Check that all seven dispatch elements, original goals, and earlier artifacts are complete or readable; trusted records associate tasks, instances, scopes, and versions.
- Check that business `result` and acceptance rules are actually defined, with corresponding business acceptance beyond valid JSON, message receipt, or execution success.
- Check explicit authoritative-artifact owners, parallel-write scopes, instance configuration, and publication entry points, with private state isolated across tasks.
- Check permitted destinations for necessary failures, duplicates, late results, timeouts, and nesting boundaries. All branches share applicable total budgets; truthfully label unverified implementations.

General anti-patterns: piling up roles by job title; splitting without isolation; treating prompts or directories as permissions; requiring a model scheduler; passing only the previous summary; providing unreadable paths alone; applying wrong-version comments to new code; mixing identically named state across tasks and users; arbitrary overwrites of authoritative artifacts by multiple Agents; claiming exactly-once behavior from three-state messages; equating read receipts with acceptance; high priority bypassing dependencies; local budgets exceeding global totals; unlimited work assignment through nesting or direct connections; adding A2A, dynamic discovery, or complex priorities to fixed chains for scores; substituting self-reported dispatch and completion for actual records.

Sources: Lessons 24-26 and 29 of The Essence of Enterprise-Grade Multi-Agent Design Methodology; role/SOP/structured communication in the MetaGPT paper; official sequential workflows from Google ADK, CrewAI, and AutoGen; Anthropic's context engineering; and the legacy coordination Skill and collaboration, communication, and prioritization patterns. Isolation-threshold trade-offs, trusted association, version acceptance, concurrency and message semantics, budget boundaries, and examples are engineering syntheses by this Skill, not verbatim source conclusions or measured effectiveness.
