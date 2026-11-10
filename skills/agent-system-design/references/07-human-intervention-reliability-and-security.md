# Human Intervention, Reliability, and Security

Read this reference in Step 5 of the main process when designing clarification, approval, exception fallbacks, and execution guardrails. Tailor it to actual error consequences: even pure generation must address data leakage, output use, and resource budgets. Add corresponding facilities for tools, asynchronous actions, or resumed work. Select Managers, sandbox services, message queues, and tracing platforms only as needed.

## Contents

1. Define Risks, Allowed Actions, and Execution Responsibilities First
2. Design Necessary Human Intervention Points
3. Bind Actual Requests to Trusted Decisions
4. Classify Errors and Select Bounded Recovery
5. Bound Retries, Loops, and Repeated Side Effects
6. Save, Resume, Cancel, and Degrade
7. Enforce Shared Resource Budgets
8. Enforce Permissions, Identity, and Security Boundaries
9. Record Events and Verify Gates Take Effect
10. Minimal Examples and Delivery Checks

## 1. Define Risks, Allowed Actions, and Execution Responsibilities First

Reliability asks whether failures can end or continue correctly; security asks which principals may do what within which scope. Hosts or services enforce both. Model self-reports and after-the-fact logs are clues only. List actual data, resources, read/write actions, intended recipients, error consequences, and existing protections before adding necessary controls.

| Boundary | Minimal Design |
|---|---|
| Permitted execution | Tools, objects, resource scopes, trusted identities, necessary approvals, and prohibited actions |
| Failure handling | Stable error types, whether actions occurred, recovery conditions, attempt or time limits, and termination exits |
| Human decisions | Triggers, owners, actual material, allowed choices, validity periods, and resume nodes |
| Execution safeguards | Host- or service-enforced permissions, parameters, budgets, cancellation, state, and necessary audits |

Reuse existing services and execution boundaries, verifying that implementation covers real execution paths. Completing a table establishes design only. Mark unsupported capabilities as to be implemented and provide safe exits that do not depend on them. When safe automation is impossible, produce drafts only, retain human handling, or stop. Limit infrastructure work to what is necessary.

## 2. Design Necessary Human Intervention Points

Choose supervision, supplementation, approval, correction, or takeover in Human-in-the-Loop (HITL) according to risk and business needs. Place humans only at these points; execute routine tasks directly under confirmed requirements and SOPs. Low-risk, authorized actions with clear boundaries may run automatically. Actions requiring approval always follow approval procedures; model-reported confidence does not change this.

| Intervention Type | Typical Triggers | What Humans See and May Decide | No Reply or Rejection |
|---|---|---|---|
| Clarification | Missing critical inputs, ambiguous goals, or multiple objects without a unique match | Original question, known facts, and minimal necessary questions; supplement inputs or narrow scope | Block work depending on missing items; independent authorized parts may continue under rules |
| Design or stage confirmation | Direction choices, high rework costs, stage acceptance, or policy requirements | Corresponding artifact version, rationale, check results, and gaps; accept, request changes, or stop | Pause downstream steps depending on confirmation; recheck after changes |
| Action approval | External sending, deletion, publication, or other actions requiring approval under actual policy | Actual targets, parameters, changes or message body, and consequences; approve or reject a specific action | Keep execution unapproved; treat timeout as rejection |
| Exception escalation | Repeated failures, stagnation, insufficient budget, missing permissions, or unknown outcomes | Exception type, location, actual current state, evidence, and permitted suggestions; supplement inputs, take over, or end | Return usable parts, blockers, and owner; resume only after an explicit reply |

Unify task association, decision records, and recovery rules. Reception may use multiple controlled interfaces or a coordinating Agent. Controlled entry points share a trusted registry through which all executor approvals pass. Stop requests and incident takeover reach the host directly and remain available if the coordinating Agent fails.

When waiting for a person, save necessary state and release expensive execution resources. Short synchronous confirmations also work; select mailboxes and background polling only as needed. Define reply deadlines, reminder and escalation limits, owners, and late-reply rules. State separately whether human waits count toward total time limits; consumed resources continue accumulating during pauses.

Anti-patterns: approving every output; ownerless critical decisions; showing only a model's passing summary; equating notification receipt with approval; turning one interface into a single point of failure; requiring automatic learning for high scores.

## 3. Bind Actual Requests to Trusted Decisions

Approval is an additional gate within authorized scope; check authentication and business authorization separately. Prohibitions take precedence: `DENY` remains effective after approval. `ASK` must block execution until a valid decision; alerts are supplementary notifications only.

The host first creates a trusted request record binding at least task and caller scope, action, target, actual parameters or artifact version, approver eligibility, expiry, usage limits, and allowed choices. The model writes explanations only; the host registers trusted approval facts, approver identity, and credentials.

The body, changes, and objects shown to humans match the request to execute. Displays may redact information but must preserve substantive differences affecting decisions. Changes to targets, bodies, critical parameters, or versions after approval require reconfirmation. Before execution, revalidate authorization, prerequisite versions, decision validity, and remaining budget. Approval interfaces also require authorization. Trust only decisions registered through controlled entry points; a model's retelling that "the user said yes" is a clue only.

Use explicit decisions to distinguish pending, approved, rejected, expired or invalidated, and consumed states. These are host business states, recorded separately from generic `handoff.status`. `read=true` means read only; record rejection reasons and feedback separately. Approval comes only from an explicit approval decision. Repeated clicks affect the same request only. Late, revoked, or consumed approvals are invalid and must not start new actions.

Races may still occur between approval and execution. When one-time guarantees are needed, the service coordinates decision consumption, version checks, and action registration. Atomic approval consumption guarantees only one use of the decision; exactly-once external action execution needs separate verification. On a lost response, verify action outcomes first rather than blindly resending under an old approval.

Reuse `gate.on_fail = escalate_human` to locate escalation. Existing hosts carry pause, approval, and resume records; define necessary business fields separately. Generic handoff Schema covers handoff structure only.

## 4. Classify Errors and Select Bounded Recovery

Exception Handling and Recovery first uses actual responses and interface semantics, then routes accordingly. HTTP status codes, process exit codes, and timeouts are clues only; verify whether business actions occurred according to interface semantics.

| Situation | Permitted Handling |
|---|---|
| Temporary unavailability or rate limiting with confirmed non-execution | Wait under interface policy and retry within remaining limits; honor `Retry-After` when applicable |
| Invalid request parameters or output format | Return specific fields and allowed values; perform bounded corrected execution or generation when repairable, correcting invalid inputs on each retry |
| Missing authentication or authorization, or policy prohibition | Stop the action and involve an authorized user or maintainer; retain the original identity, configuration, and execution channel |
| Context limit exceeded | Prune or compact under the context chapter, preserving constraints and action state, then reassess; do not retry unchanged |
| Inadequate quality, conflicting criteria, or missing evidence | Correct using valid feedback, supply material, or escalate; checker failure means invalid scoring |
| Timeout or disconnection after a write/send, or ambiguous service results | Mark the outcome unknown; query state or use verified same-action deduplication first. Repeat side effects only after confirming non-execution |
| Failure of safety gates, required audits, or budget controls themselves | Block new actions depending on those safeguards by default and report the failure; handle as a security failure, separately from transient business errors |

429 or 5xx indicates only a possible temporary failure. Before retrying writes, confirm non-execution or reliable idempotency protection; legitimate state conflicts may require reading the latest version first. Read-only query timeouts may be retried under read semantics, considering costs for expensive or side-effecting queries.

Count transient retries, format corrections, content repairs, fallback, and replanning separately, but constrain all by total budget. Every path has completion, unrecoverable, exceeded-limit, or blocked exits. Select the necessary path by error type; use fallback and full rollback only when business needs require them.

## 5. Bound Retries, Loops, and Repeated Side Effects

Distinguish initial attempts from additional retries: `max_retries=2` means at most 1 initial call plus 2 additional calls. Each attempted model call counts as one iteration, including failures, final generation, review, and correction. Assign SDK, gateway, framework, and host retries to one explicit responsible layer, or jointly count actual attempts to avoid multiplication across layers.

Use capped backoff and appropriate jitter, keeping all delays within task deadlines. Correct only repairable parts, returning concise errors and evidence-reading entry points. Choose retry counts, intervals, and trial periods from risk and validation data. A universal three retries, fixed two seconds, or a week of permissive production trials are case-specific configurations only.

For side effects, define action identity, deduplication scope, parameter binding, retention period, status queries, and conflict handling first. Retries of the same business action reuse the same Idempotency Key; changed parameters must not execute a different action under the same key. Trusted execution records generate keys, and services must actually enforce deduplication. Business idempotency requires server-side enforcement; passing a key, message acknowledgment, and cached returns are only parts of it.

For unknown external outcomes, query existing operation records. Retry under rules when non-execution is confirmed; accept actual results when completion is confirmed. If outcomes cannot be confirmed and the interface lacks reliable idempotency, block or request human verification. Resume using original action identity and key. After deduplication retention expires, missing records mean "unknown" only.

Isolate loop detection by task and instance, combining goals, normalized actions, necessary input versions, actual results, and progress changes. Legitimate polling and staged writes may return the same values; identical tool outputs indicate possible stagnation only. Hashing `tool_name + output` alone causes false positives. Give asynchronous waits their own intervals and deadlines; detect multi-step oscillation separately if needed. Hashes identify repetition, not safety or completion.

Only tasks with autonomous loops need loop detectors. When needed, stop early on stagnation signals, with attempt or total-time limits as a backstop. Include tool requests, model calls, and framework-internal retries in detection and counting across actual execution paths, not just final-answer callbacks.

## 6. Save, Resume, Cancel, and Degrade

Use Checkpoint Recovery as needed; short generation may simply rerun. Save trusted tasks and scopes, goals and constraints, current valid plans and completed items, dependency and artifact versions, check verdicts, pending approvals, action records, remaining budgets, and resume nodes. Keep credentials in credential systems, separate from task snapshots.

Before resuming, verify snapshot sources, authorization and current policy, dependency versions, and approval expiry. Acquire current execution ownership and first verify in-progress or unknown-outcome actions. Accept results of confirmed completed actions directly; reassess downstream validity after upstream version changes. Restarts, model switches, returning to earlier nodes, and human continuation retain accumulated usage. Stop if usage is lost and cannot be reconstructed.

State rollback affects controlled local state or genuinely supported transactions only; irreversible outcomes such as sent notifications remain recorded as having occurred. Handle cross-service failures through business-appropriate compensation, partial results, or human checks. Compensation can fail and have side effects too; require permissions, records, and boundaries, truthfully recording that original actions occurred.

On stop requests, first prohibit new dispatches and side effects, then cancel running work as capabilities allow and collect results. Verify whether external actions stopped after cancellation requests. Executors losing ownership may submit only results pending verification; current owners publish authoritative results. Verify late results by action identity and retain evidence, keeping the current new version effective. Notification or remote-cancellation failures also need termination exits.

Degrade only to authorized candidates satisfying required privacy and output constraints, such as drafts or partial evidence with explicit gaps. Required safety checks still apply. Confirm scope or acceptance-criteria changes; report partial completion as partial, reusing `PARTIAL/remaining` or `BLOCKED/blockers`. Record unknown business actions truthfully as unknown in specific `result` fields.

## 7. Enforce Shared Resource Budgets

Resource-Aware Optimization first satisfies quality, privacy, tool compatibility, and deadlines, then compares costs. Use one fixed model directly when sufficient. Introduce model tiers, dynamic routing, critic Agents, and automatic switching only as needed. Validate fallback models too; do not bypass refusals or permission errors by switching models. Extra calls and regeneration count toward the same task.

Define counting scope and hard limits for actual model attempts, tool attempts, input/output tokens, service charges, total time, concurrency, and necessary storage or execution resources. All task branches, retries, delegation, and aggregation share applicable totals. Control RPM requests, TPM tokens, and concurrency separately. Request counts are useful but cannot alone guarantee spending limits.

Before calls, centrally check and reserve possible actual consumption; settle afterward, counting actual costs even on failure or timeout. Conservatively reserve unknown usage and reconcile later. Reserve for final delivery and necessary checks; when budget is insufficient, end under controls using existing information, with final summaries within reserved limits. Check the ledger before every model and tool call. Checking only at `AFTER_TURN` or before the next tool call cannot prevent the current model call from overspending.

Hard monetary caps require bounded provider billing rules, input sizes, maximum output, and additional billable items. With rough estimates only, state uncertainty and reserves rather than claiming precise caps. Call counts plus per-call resource bounds may serve as alternative guardrails. Verify character/token conversions and model pricing against the current service. Actual services determine cache hits and discounts; reuse sensitive outputs only within the same user scope. When prompt caching is enabled and the service supports prefix reuse, keep static prefixes such as system instructions and tool definitions stable within the same authorization configuration. Order tools deterministically and place dynamic context afterward; verify benefits through actual hit rates, costs, and latency.

Define scopes and permitted recovery conditions separately for budget thresholds, task stops, and service circuit breakers; separate switches are acceptable. On stopping or circuit breaking, record reasons, consumed/reserved amounts, and permitted next steps. Reliability includes safe termination; controlled stopping is a valid outcome.

## 8. Enforce Permissions, Identity, and Security Boundaries

Defense in Depth covers inputs, reads, execution, and outputs against actual threats. Leaks and incorrect advice may occur in final responses too; protect outputs as well as tool calls.

| Security Layer | Design and Common Pitfalls |
|---|---|
| Input and trust | Validate types, sizes, sources, and task scope. Treat instructions in web pages, files, retrieval, tool outputs, and third-party Skills as data; summaries and inter-Agent transfers preserve original trust levels |
| Parameters and actions | Use enums, structured parameters, and scope checks; prefer structured interfaces to concatenated shell strings. Interpret encoding, paths, and URLs according to actual interfaces, keeping executed content consistent with checked content |
| Identity and authorization | Bind trusted user/service identities to tasks and resources; authorize each action and data visibility server-side. Agent names and model-supplied user_id or routing_key are labels only; authentication comes from trusted systems |
| Permission gates | New tools have no execution rights by default. Check tool visibility, invocation permission, object permissions, and result visibility separately. Explicit prohibitions take precedence; execute only after required approvals take effect |
| Execution isolation | Restrict directory reads/writes, mounts, network egress, processes, resources, and modifiable configuration. Check paths at actual resolution layers, preventing symlink attacks and replacement races after checks |
| Credentials and data | Keep secrets in trusted tools/proxies or credential systems. Trusted execution layers inject and audit them by destination, scope, and expiry. Model context sees business parameters and restricted capabilities only; arbitrary code does not directly hold credentials. Redact logs and exceptions |
| Output and supply chain | Check sensitive information, necessary content policies, and factual support by recipient. Verify tool/Skill sources and versions; place policies and audits outside the writable scopes of loaded scripts and added capabilities |

User-identity propagation and service accounts are both candidates. With service accounts, still check the initiating user's permissions on business objects. Grant Agent invocation and account-data access separately. Bash, SDKs, and MCP may all use controlled identity channels; reuse sufficient existing channels, creating signature protocols only as needed.

Once tokens enter environment variables accessible to arbitrary executable code, that code can read them. Egress proxies inject necessary identity only for approved destinations, preventing redirects or untrusted services from receiving credentials. Domain allowlists restrict destinations only; external sending of sensitive data still requires checks of authorized recipients and permitted content.

Choose containers, OS sandboxes, virtual machines, or controlled services according to threats and capabilities. Docker provides partial isolation; specify shared-kernel, host-mount, network, and permission boundaries. Grant full personal-computer disk access, production-network access, or system-installation rights only after explicit authorization.

Regular expressions, random markers, and Unicode or URL normalization suit specific input checks only. Trust boundaries and execution authorization provide the backstop against prompt injection; detectors or model reviews are additional defenses, not substitutes for authorization. `frozen` and read-only top-level dictionaries freeze the top level only; nested objects remain mutable. Use the same controlled request from gate to execution, or verify content consistency, preventing post-check modification.

When required security components are missing, fail, or required audits are unavailable, deny actions depending on them by default (Fail Closed). Optional telemetry failures may degrade under controls (Fail Open), recording missing data and notifying maintainers. Route these failures through separate exception paths. Hosts maintain trusted baselines; workspace configuration may only tighten them.

## 9. Record Events and Verify Gates Take Effect

Hosts, services, or controlled adapters record observable events. Model explanations are clues only; execution logs come from hosts. Keep audits outside model-modifiable scopes. Append-only JSONL is a write method only; tamper resistance also requires storage permissions, deletion permissions, and retention policies.

Record necessary task/scope, node, attempt or action IDs, timestamps, actual tools, redacted parameters or version references, execution states and errors, approval and policy versions, check results, and actual resource usage. Distinguish action requests, approvals, starts, completions, unknown outcomes, and acceptance. Request events establish requests only; corresponding execution and failure events establish those facts.

Map events as needed to task start, before/after model calls, tool requests/rejections/results, handoff acceptance, pause/resume, stop, and task end. The course's 5+2 Turn system is one mapping example. Frameworks may make several calls per turn, trigger only final callbacks, or swallow exceptions; verify actual versions and paths.

Critical tests verify that "the actual tool did not execute when rejected," using real action records. Exceptions, alerts, and interface text are supplementary. Missing policy-initialization dependencies must explicitly reject or raise configuration errors, exposing problems at startup. Required gates cover all execution entry points: swallowed framework exceptions, alternate tool entry points, sub-Agents, and direct SDK calls must pass through the same gates.

Settle incurred resources before deciding termination; record rejected actions and reasons too. Order events, ledgers, and policies by dependencies. Bound remote-trace waits; required audits may first save through permitted reliable local entry points.

Logs store necessary fields only by default. Never log credentials; record redacted identifiers or references only. Manage full prompts, bodies, artifacts, and internal chains of thought separately as needed. Govern necessary body content with authorization, redaction, size limits, and evidence references. Optional telemetry may be sampled; retain required approvals and safety audits in full, saving critical action facts immediately when they occur. Leave quality monitoring, evaluation sets, and long-term alert policies to the next chapter. Select Langfuse, OTel, and real-time dashboards only as needed.

## 10. Minimal Examples and Delivery Checks

The following are design walkthroughs and contract examples only. External actions, authentication/authorization, concurrency, recovery, and model effectiveness have not been tested; parameters are illustrative only.

### Example 1: Generate a Reply Draft and Send Externally After Approval

Single Agent or fixed workflow: read an authorized question → generate draft → check body and recipient → necessary human approval → host sends and verifies the result. These nodes suffice; no Manager, long-term memory, or dynamic model routing is needed. The demonstration allows at most 3 attempted model calls, 5 total tool attempts, 20 seconds per wait, and 120 seconds of active execution. Human approval expires after 1 hour; waiting is counted separately, while resource usage keeps accumulating.

The host binds task, sender, recipient, body v1, and one-time approval. An eligible approver registers the decision through a controlled entry point. Stop sending if the body changes to v2, the target changes, approval expires, or approval is denied. Service authorization failure also stops sending; approval is an additional gate only.

If sending times out without reliable deduplication or result queries, stop repeated sending and record the outcome as unknown. Return using generic handoff definitions:

```json
{
  "task_id": "reply-1",
  "agent": "reply-worker",
  "status": "BLOCKED",
  "summary": "Sending outcome is unknown; repeated sending has stopped",
  "result": {"action_id": "send-1", "action_state": "UNKNOWN", "draft_version": "v1"},
  "blockers": ["Sending records require verification; reliable queries or deduplication are currently unavailable"],
  "unresolved_questions": ["Whether the recipient has already received the reply"]
}
```

Trusted records supply task and action IDs. `result` contains this example's business fields; generic status enums remain unchanged. Successful draft generation means only that the draft is complete; verified results determine sending state. The old approval has been used for this action. Verify it first when resuming, retaining the original sending action's deduplication identity.

### Example 2: Bounded Retries and Resumption for Read-Only Investigation

One read-only investigation node follows an existing explicit task. The demonstration allows at most 4 attempted model calls, 5 total tool attempts, 2 additional retries per query, 10 seconds per wait, and 90 seconds of active execution. All corrections and necessary aggregation share limits. Retry 429 according to service wait guidance within remaining deadlines; block directly on 403, retaining the original identity.

When pausing for a person to supply a critical source, save goals, verified conclusions and evidence versions, gaps, consumed model/tool quotas, and the resume node. Check permissions, source versions, and remaining quota before resuming. Reuse completed query results; reverify outdated evidence within budget. Legitimately waiting sources may return unchanged results for identical queries. Assess progress too; output hashes alone may falsely indicate an infinite loop.

If required sources remain unreadable, return partial completion or blockage. When partial delivery is allowed, use `PARTIAL` and list `remaining`. This example has no side effects and needs no transaction rollback, compensation service, approval mailbox, or multi-model fallback.

### Delivery Checks

In Section 8, define human triggers, owners, actual material, decision binding, deadlines, and resumption. In Section 9, define errors, action semantics, retries, budgets, state recovery, secure execution, and events. Keep specific tool rules in Section 5; reuse previous chapters for loop and delegation boundaries.

- Check that read receipts differ from approval, and approval from authorization. Parameter or version changes require new decisions; stop entry points remain independent of models.
- Check actual error facts and action states. Verify unknown outcomes first; retries, corrections, and fallback share limits and termination exits.
- Check that recovery reuses completed side-effect results and accumulated budgets. Rollback, compensation, and cancellation truthfully record irreversible actions as having occurred.
- Check pre-call resource reservation and post-call settlement. A fixed model may meet criteria; explicitly label rough estimates as estimates.
- Check trusted enforcement of identity, data scope, credentials, execution isolation, and audits. Required safeguard failures block by default; plan verification of actual rejection paths.

Anti-patterns: asking humans at every step; self-reported high confidence waiving approval; read receipts or feedback counted as approval; ASK only raising alerts; approval overriding DENY; timeout interpreted as non-execution; new idempotency keys repeating old actions; identical output hashes necessarily implying infinite loops; retries multiplying across layers; usage resetting on restart; rolling back sent messages; cheap model switches bypassing privacy; rough estimates and after-the-fact accounting claimed as hard caps; service accounts sharing all data; regex guaranteeing no injection; sandbox environment variables hiding secrets; append-only logs assumed tamper-proof; security-component failures allowing execution; printing rejection while tools still execute.

Sources: Lessons 27 and 30-33 of The Essence of Enterprise-Grade Multi-Agent Design Methodology; Anthropic's Building Effective Agents; exception handling, human collaboration, resource awareness, and security patterns from the legacy design-advice Skill; and legacy coordination templates. Approval binding, unknown action outcomes, idempotency/recovery/cancellation, resource reservations, and identity/logging boundaries are engineering syntheses by this Skill. Attack rates, prices, fixed thresholds, and project effectiveness in source material have not been verified; this chapter uses their design principles only.
