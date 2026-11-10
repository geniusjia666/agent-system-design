# Design Self-Review Checklist

Use for Step 7 self-review and reviews of existing designs. Determine Agent types and select dimensions first, then check, score, and classify issues item by item.

## Contents

1. Usage
2. Type and Dimension Selection
3. Score Levels
4. Basic Dimensions 1-7 (Check for All Agents)
5. Advanced Dimensions 8-14 (Select by Type)
6. Extended Dimensions 15-21 (Select as Needed)
7. Pre-Delivery Hard Checks
8. Review Report Format

## 1. Usage

1. Determine Agent types (multiple selections permitted), then select dimensions under Section 2.
2. Check each dimension against its items. Answer "Met / Partially met / Unmet / Not applicable" for each, citing evidence locations in the design document.
3. Score 0 to 5 under each dimension's criteria, with evidence for every score. Score design omissions as missing. If user-provided material is insufficient to judge, mark "To be verified," do not score or include in averages, and list required material.
4. Check anti-pattern lists and record matches under "Identified Anti-Patterns."
5. Classify issues into three severities:
   - Serious: causes incorrect results, security incidents, uncontrolled costs, or inability to launch; must fix.
   - Moderate: affects quality, stability, or maintainability; recommended to fix.
   - Minor: optional improvements.
6. Perform Section 7 hard checks; record failed checks directly as serious issues.

Do not score or average not-applicable or to-be-verified dimensions. State reasons for non-applicability and material needed for verification separately. Label evidence as design statements, walkthroughs, or actual validation. Document scores assess documents only, separately from model success rates and release permission. Record unexecuted and invalidly scored checks separately; neither counts as passed. Judge serious hard failures separately.

## 2. Type and Dimension Selection

| Agent Type | Typical Features | Required Dimensions |
|---|---|---|
| Single-task Agent | One task category, no complex workflow | 1-7 |
| Workflow Agent | Multi-step execution chains, conditional branches | 1-7, 10, 11 |
| Tool-using Agent | External APIs, tools, databases | 1-7, 10, 13, 15 |
| Retrieval-augmented Agent | Retrieval-dependent generation | 1-7, 8, 17 |
| Conversational Agent | Multi-turn dialogue, context maintenance | 1-7, 8, 13 |
| Multi-Agent system | Multiple collaborating Agents | 1-7, 10, 11, 18, 20 |
| Autonomous or adaptive Agent | Learning, planning, self-improvement | 1-7, 9, 12, 16, 21 |
| Production-grade Agent | Production deployment, high reliability | 1-7, 10, 11, 13, 14, 19 |

Always check basic dimensions 1 to 7, first determining whether each capability is needed. If unnecessary with reasons (for example, single calls need no tools, planning, or reflection; single Agents need no collaboration), mark Not applicable without scoring. Score low only for necessary missing capabilities. Scores of 0 in dimension tables apply only when "needed but missing."

## 3. Score Levels

| Score | Level | Meaning |
|---|---|---|
| 0 | Missing | Not considered at all |
| 1 | Novice | Awareness exists but approach is inappropriate |
| 2 | Basic | Basic implementation with clear defects |
| 3 | Good | Core is sound, some advanced features missing |
| 4 | Excellent | Complete and reasonable |
| 5 | Exemplary | Best practice, suitable as an example |

Overall score is the arithmetic mean of scored dimensions, rounded to one decimal place. Assign levels using the overall score rounded to an integer (for example, 3.6 rounds to 4, Excellent). If serious issues remain unresolved, append "Not passed" to the level.

## 4. Basic Dimensions 1-7

### Dimension 1: Task Decomposition (Prompt Chaining)

Assess only tasks needing fixed multi-step decomposition. Split steps by meaningful artifacts; expert roles, independent Agents, and JSON bodies are optional.

Checks:
- [ ] Multi-step decomposition has explicit benefits, clear node responsibilities and artifacts; ordinary transformations may use code directly
- [ ] Critical control fields have types and validation, with body formats suited to consumers
- [ ] Explicitly transfer dependencies, original goals, hard constraints, and necessary earlier artifacts; references are readable and versions verifiable
- [ ] Necessary gates separate format, business, and artifact usability; failures are locatable with bounded handling and termination exits
- [ ] Information is sufficient and concise at each step; downstream receives more than the previous step's retelling

Anti-patterns: nodes merely retell; sequence substitutes for data dependencies; original goals missing; format passing treated as factual correctness; adding expert personas or independent Agents for scores.

| Score | Criteria |
|---|---|
| 0 | Necessary multi-step decomposition is missing |
| 1 | Vague steps, unclear dependencies or critical data |
| 2 | Basic decomposition with clear artifact, input, or validation gaps |
| 3 | Clear responsibilities/dependencies, but necessary gates or failure exits insufficient |
| 4 | Complete decomposition, inputs, handoffs, validation, context, and failure limits |
| 5 | Beyond 4, validated missing-dependency, error-propagation, and exceeded-limit boundaries; expert roles and multiple Agents optional |

### Dimension 2: Routing

Assess only when different inputs/states need different handling paths. Use one reliable method directly when sufficient; hybrid classification, layered routing, and dynamic extensions are optional.

Checks:
- [ ] Permitted categories and classification methods match handler responsibilities; validate returned enums and do not execute arbitrary model-generated entry points
- [ ] Explicit fallbacks cover unknown, ambiguous, multiple-intent, invalid-output, and classification-failure cases
- [ ] Routing judgments and business responsibilities are separately checkable; pass original requests and necessary material to handlers
- [ ] Handlers still check permissions and approvals; check business-action authorization separately
- [ ] Examples validate accuracy and applicable thresholds; use self-reported confidence as probability only after calibration

Anti-patterns: different categories but identical handling; silently losing multiple intents; unknown requests defaulting to high-risk actions; combining methods for scores; routing bypassing approval.

| Score | Criteria |
|---|---|
| 0 | Paths need distinction but effective routing is absent |
| 1 | Branches exist but responsibilities/categories unclear |
| 2 | Basic usable classification with clear fallback or critical-input gaps |
| 3 | Clear classification/responsibilities, but applicable multiple-intent, failure, or authorization boundaries insufficient |
| 4 | Complete necessary classification, permitted sets, responsibilities, fallbacks, inputs, and permission boundaries |
| 5 | Beyond 4, validated necessary classification quality/boundaries; multiple methods, layered routing, and dynamic extensions optional |

### Dimension 3: Parallelization

Assess only independent subtasks with actual concurrency benefits in latency or coverage; include repeated executions of one task followed by voting. Mark Not applicable when serial execution suffices or dependencies are tight. Scores do not depend on whether parallelism is used.

Checks:
- [ ] Correctly identify independent subtasks that do not depend on other steps
- [ ] Define result aggregation after parallel execution
- [ ] Use asynchronous or concurrent execution
- [ ] Keep dependent steps sequential, independent steps parallel
- [ ] Reliably pass parallel results to downstream steps
- [ ] Define handling for individual parallel-branch failures

Anti-patterns: forcing dependent steps into parallelism, causing inconsistent data; ignoring concurrency's debugging/logging complexity; keeping many independent subtasks entirely serial.

| Score | Criteria |
|---|---|
| 0 | Parallel benefits needed but everything remains serial without consideration |
| 1 | Parallelism recognized, but incorrect implementation or missing aggregation |
| 2 | Basic parallelism with incorrect independence judgments or aggregation logic |
| 3 | Correct identification/concurrent execution and aggregation, but missing state management or error handling |
| 4 | Accurate independence judgments, async execution, clear aggregation, reliable state transfer |
| 5 | Beyond 4, validated branch failures, partial-result aggregation, and concurrency limits; set parallelism as needed |

### Dimension 4: Reflection (Evaluator-Optimizer)

Assess only with explicit criteria, actionable feedback, and iteration value. Separate production and checks, using code, tests, separate model reviews, or humans. Permanent reviewer Agents are optional. When correction is needed, iterate only genuinely problematic outputs.

Checks:
- [ ] Reviews use original requirements, constraints, corresponding-version candidates, and necessary evidence, not generator statements instead of acceptance
- [ ] Feedback gives specific locations, issues, and suggestions; control conclusions have field definitions; format errors count as not passed
- [ ] Recheck corresponding versions after changes; do not attach old scores to new candidates
- [ ] Passing, unrepairable, stalled, and exceeded-limit outcomes have destinations; local iterations and total task budgets have hard boundaries
- [ ] Retain necessary versions/unresolved items, reserve final-check budgets, and do not claim unchecked new artifacts passed

Anti-patterns: judging every single generation wrong; self-reported satisfaction as passing; reviews unable to see required facts/tests; old scores accepting new versions; infinite loops; high scores requiring multiple Agents.

| Score | Criteria |
|---|---|
| 0 | Feedback-based correction needed but effective mechanisms absent |
| 1 | Self-checking exists but criteria or trusted checks insufficient |
| 2 | Review/change exists with clear feedback, version, or budget gaps |
| 3 | Clear responsibilities/feedback, but necessary final checks or stop exits insufficient |
| 4 | Complete criteria, evidence, versions, feedback, final checks, and budget boundaries |
| 5 | Beyond 4, validated necessary iteration effects/failure boundaries; different models and independent Agents optional |

### Dimension 5: Tool Use

Models request external capabilities as needed; hosts execute them actually, returning results to models when further processing is necessary. Assess needed capabilities only; scores do not depend on tool counts, chained calls, or additional model integration.

Checks:
- [ ] Every tool states functions, outputs, triggers, and boundaries; hosts validate parameter types, ranges, and defaults
- [ ] Separate tool execution from model decisions; hosts/services constrain side effects, identities, read/write scopes, and necessary approvals
- [ ] Returns distinguish empty results, truncation, failures, and unknown outcomes; errors guide permitted next steps
- [ ] Results are actual and suited to consumers; return them to models when further processing is needed, otherwise deliver artifacts directly
- [ ] Systems manage credentials and trusted call identities, without model generation or inclusion in prompts
- [ ] Returns have size limits, necessary evidence, and continued-read entry points; external calls have timeouts

Anti-patterns: vague tool descriptions; model text simulating execution; silent failures/truncation; model parameters establishing authorization; blind retries on unknown write outcomes; adding tools or unnecessary model integration for high scores.

| Score | Criteria |
|---|---|
| 0 | External capabilities needed but absent or unable to execute actually |
| 1 | Tools exist but vague descriptions/boundaries and guessed critical parameters |
| 2 | Basic capability fit with clear validation, error, or result-handling gaps |
| 3 | Clear contracts/execution, but applicable permission, failure, or timeout boundaries incomplete |
| 4 | Complete necessary tools, parameter validation, actual returns, error destinations, permissions, and timeouts |
| 5 | Beyond 4, representative, boundary, and failure cases validate necessary tool behavior; multiple tools/chained calls optional |

### Dimension 6: Planning

Assess only when requests/environments must generate tasks/dependencies; mark mature fixed workflows Not applicable. Planning, validation, and execution are logical stages that one Agent may handle. Replan only when evidence invalidates the plan.

Checks:
- [ ] Explain dynamic-plan necessity; tasks, inputs, artifacts, acceptance, and dependencies are executable
- [ ] Before dispatch, validate identities, references, dependencies, scopes, task counts, and budgets; trusted systems alone grant permissions
- [ ] Execute only dependency-ready items in the currently valid plan
- [ ] When evidence invalidates assumptions/routes, state revision reasons, recalculate order, and assess completed-item validity
- [ ] Do not reset goals, approvals, or total budgets; confirm scope changes first, and do not merely replace plan variables inside old traversal lists

Anti-patterns: mandatory Planners for simple tasks; rewriting entire plans after failures; mechanically executing invalid initial plans; dynamic dependencies executed in old order; replanning expands goals/permissions.

| Score | Criteria |
|---|---|
| 0 | Planning needed but only aimless immediate reactions exist |
| 1 | Listed steps without executable dependencies |
| 2 | Basic usable plans with clear validation, dependency, or scope gaps |
| 3 | Clear plans/execution, but necessary change or budget handling insufficient |
| 4 | Complete necessary dynamic plans, validation, ready-task scheduling, revisions, and scope/budget boundaries |
| 5 | Beyond 4, validated dependency changes, invalidated assumptions, and exceeded-limit boundaries; independent Planners and per-iteration replanning optional |

### Dimension 7: Multi-Agent Collaboration

Assess only designs genuinely needing multiple Agents. Distinguish roles, nodes, and instances; scores do not depend on hybrid patterns, persistent personas, extensibility, or permanent coordination/validation role counts.

Checks:
- [ ] Every Agent has actual context, tool, or permission isolation needs and reasons simpler alternatives are insufficient; clear responsibilities, artifact owners, and acceptors
- [ ] Coordination matches tasks; hosts may coordinate fixed chains, with allowed relationships, depth, and shared-budget constraints on transfers/nesting
- [ ] Self-contained dispatch retains seven elements, original goals, necessary standards, and readable earlier artifacts, without assumed history inheritance
- [ ] Verify handoff business fields, trusted task/instance/scope, evidence, and necessary versions; business acceptance is separate from execution success
- [ ] Clear shared-state owners, read/write scopes, publication entry points, and necessary concurrency rules; permissions do not rely only on prompts
- [ ] Necessary failures/gaps have return destinations; missing critical artifacts do not silently degrade to complete success. Accept duplicate/late results under applicable rules

Anti-patterns: division by job titles/file counts; Agents merely retell to each other; paths without reading capabilities; mixed tasks/versions; infinite transfers; high scores requiring hybrid interaction/cross-system protocols.

| Score | Criteria |
|---|---|
| 0 | Collaboration necessary but effective division/handoffs absent |
| 1 | Multiple Agents with unclear responsibilities/coordination |
| 2 | Basic usable division with clear input, handoff, or permission gaps |
| 3 | Reasonable responsibilities/interactions, but applicable acceptance, state, or failure boundaries insufficient |
| 4 | Complete necessary roles, dispatch, association, version acceptance, state permissions, and budget boundaries |
| 5 | Beyond 4, validated necessary role/handoff boundaries; hybrid patterns, permanent Managers, and cross-system communication optional |

## 5. Advanced Dimensions 8-14

### Dimension 8: Memory Management

Assess current context, session state, task notes, and long-term memory by need. Do not deduct for absent long-term components when conversation continuity or task resumption alone is needed; mark Not applicable when no state reuse is needed. Check necessary long-term memory and types only.

Checks:
- [ ] Distinguish current context, persistable task state, stable memory, and formal knowledge, stating necessary layers/reasons
- [ ] Define effective budgets and necessary loading, pruning, or compaction, retaining goals, constraints, evidence, and action states
- [ ] For resumption, save/recover actual progress, unresolved items, and remaining budgets under control; do not blindly repeat external actions
- [ ] For long-term memory, admit writes with durable value and trusted evidence, deduplicate first, and do not record unverified inferences as facts
- [ ] Authorize reading, writing, and output by trusted scopes; retrieve necessary memory by references, keywords, or semantics
- [ ] Govern applicable updates, conflicts, freshness, sources, deletion, and index synchronization

Anti-patterns: long windows treated as persistence; task progress treated as long-term preferences; unsourced/cross-user memory; summaries elevate external instructions; compaction loses constraints/resets budgets; writes without governance; adding all long-term components/types for scores.

| Score | Criteria |
|---|---|
| 0 | Continuity, resumption, or memory reuse needed but absent |
| 1 | History/records exist but boundaries unclear and critical state easily lost |
| 2 | Basic usability with clear applicable budget, update, recovery, or scope gaps |
| 3 | Clear needed information layers/access, but applicable compaction, trusted writes, or governance incomplete |
| 4 | Complete necessary budgets, loading, retention, scopes, and applicable recovery/memory governance |
| 5 | Beyond 4, validated necessary policy effects/failure boundaries; long-term memory, all memory types, and reflective improvement optional |

### Dimension 9: Learning and Adaptation

Assess only necessary behavior updates from cross-task experience or change. In-task correction is short-term improvement, separate from cross-task learning. Maintainers may improve static policies offline; autonomous coding, independent supervisory Agents, diversity search, long-term memory, and fine-tuning are optional.

Checks:
- [ ] Specify necessary adaptation; distinguish signals, actual results, root-cause hypotheses, and improvement goals. Do not treat feedback/approval directly as correctness labels
- [ ] Clear signal sources/scopes, authorization, versions, and necessary data governance; do not ignore sample bias/uncertainty
- [ ] Proposals have verifiable evidence, targets/baselines, concrete changes, validation, risks, and owners. Root causes may be unknown/multiple; enums do not guarantee correctness
- [ ] Trusted layers restrict change scope/activation, selecting isolation/approval by actual risk; only trusted layers adjust goals, permissions, scorers, and gates
- [ ] Compare changes on target failure categories, other necessary categories, and data not used for tuning; retain failures, resources, and coverage rather than cherry-picking best results
- [ ] Record versions, effects, and rollback/dependency conditions; consolidate duplicate/invalid rules as needed; bound iterations by budgets/stop exits

Anti-patterns: static means zero score; autonomous Agents require fine-tuning; memory automatically safe by filenames; approval equals quality; self-modifying scorers to turn green; activating without validation; mandatory learning squads; single-rule rollback ignoring subsequent dependencies.

| Score | Criteria |
|---|---|
| 0 | Cross-task adaptation necessary but effective signals/update paths absent |
| 1 | Scattered feedback only, unclear goals/evidence |
| 2 | Basic adjustment with clear evaluation, governance, or activation-boundary gaps |
| 3 | Clear improvement flow, but applicable independent validation, authorization, or rollback insufficient |
| 4 | Complete necessary signal checks, evidence-backed proposals, controlled activation, version comparisons, and stop/rollback boundaries |
| 5 | Beyond 4, validated necessary adaptation effects/regression boundaries; autonomous modification, multiple Agents, and weight training optional |

### Dimension 10: Exception Handling and Recovery

Assess actual external calls, resumption, and side effects; configure rollback, compensation, self-correction, and permanent runtime facilities as needed. Correct stopping or permitted partial delivery is reliable behavior too.

Checks:
- [ ] Classify by actual formats, errors, and execution semantics; distinguish unexecuted, executed, and unknown outcomes. Actions may occur despite timeouts or 5xx
- [ ] Separately define transient retries, format correction, quality repair, and rollback; initial/additional calls and layered retries have unified counts/stop exits
- [ ] Before retrying side effects, verify incurred actions or actual idempotency guarantees; distinguish action keys, parameters, scopes, and deduplication expiry
- [ ] For recovery, save trusted tasks, versions, approvals, actions, and remaining budgets; revalidate authorization/execution ownership, without redoing completed items or resetting quotas
- [ ] Define degradation, cancellation, late results, transactional rollback, or compensation as needed. Truthfully record irreversible side effects as incurred and critical failures as failures
- [ ] Necessary gate failures block dependent actions; errors/gaps are locatable with owners or explicit returns

Anti-patterns: retrying all errors; timeout treated as failed and resent; multiplying layered retries; new action keys repeating old side effects; reset budgets on restart; transactional rollback for every failure; only continuous execution considered reliable.

| Score | Criteria |
|---|---|
| 0 | Failure handling needed but effective detection/exits absent |
| 1 | Exception catching only, unclear facts/continuation |
| 2 | Basic usable handling with clear classification, action-semantic, or limit gaps |
| 3 | Clear handling paths, but applicable unknown-outcome, recovery, or degradation boundaries insufficient |
| 4 | Complete necessary classification, bounded handling, action verification, state, and safe-ending boundaries |
| 5 | Beyond 4, validated necessary failure/recovery paths; rollback/compensation optional, safe interruption permitted under high uncertainty |

### Dimension 11: Human-in-the-Loop

Assess clarification, approval, supervision, or takeover by risk/business need. Routine authorized low-risk actions may run automatically; per-task requirements signoff, a single Manager, all-human review, and continuous learning loops are optional.

Checks:
- [ ] Intervention has explicit triggers, owners, permitted decisions, wait deadlines, and rejection/late-reply exits
- [ ] Humans receive necessary original goals, actual artifacts/action parameters, versions, evidence, and gaps, not full history or model passing summaries as substitutes
- [ ] Associate requests with trusted tasks, scopes, qualified approvers, and valid decisions; approval comes only from explicit decisions. Record read receipts/change feedback separately
- [ ] Revalidate authorization, parameters/versions, and decision validity before execution. Prohibitions remain effective after approval; approval covers bound actions only
- [ ] Controlled entry points unify records/recovery; multiple entry points may exist without bypasses. Stopping/incident takeover do not depend on failed models
- [ ] Supply sensitive material within approver visibility, release expensive resources while waiting, and retain accumulated total budgets at resume

Anti-patterns: approval fatigue; self-reported confidence waives approval; read receipts equal approval; approving old bodies then sending new ones; humans carrying messages to every executor; one interface becomes a single point of failure.

| Score | Criteria |
|---|---|
| 0 | Necessary human decisions absent, no safe exits for high risk/ambiguity |
| 1 | Human involvement conceptual only, missing triggers/owners |
| 2 | Basic usable intervention with clear material, decision, or timeout-handling gaps |
| 3 | Clear triggers/material, but applicable trusted binding, rejection, or recovery insufficient |
| 4 | Complete necessary intervention, actual material, qualifications, decision binding, deadlines, authorization, and recovery |
| 5 | Beyond 4, validated necessary approval/intervention boundaries; expert-matching platforms, a single Manager, and learning loops optional |

### Dimension 12: Reasoning Techniques

Choose reasoning by task need; scores do not depend on method counts. Auditability means traceable evidence, actions, actual results, and key-decision summaries; internal chains of thought need not be published. Determine applicability per check first; if tools, correction, or multi-candidate comparison are unnecessary, state reasons and score normally.

Checks:
- [ ] Reasoning matches task needs; do not add loops for pattern quotas in simple tasks
- [ ] Use actual tool results for external facts rather than model fabrication
- [ ] When correction is necessary, use concrete validation, tests, or review feedback with attempt limits
- [ ] Key evidence, tool actions, actual results, and check conclusions are traceable
- [ ] Bound reasoning budgets; format correction and regeneration count toward totals

Anti-patterns: combining methods to prove sophistication; publishing full chains of thought as acceptance criteria; asking models to think more instead of checking necessary facts; repeated self-evaluation without feedback.

| Score | Criteria |
|---|---|
| 0 | Reasoning support needed but absent, critical conclusions unsupported |
| 1 | Generic "think step by step" prompts only, without task fit |
| 2 | Basic method fit, but applicable validation, traceability, or budget design clearly missing |
| 3 | Appropriate methods with evidence/check design, but applicable feedback/boundaries incomplete |
| 4 | Complete necessary methods, validation, traceability, and budget boundaries; combining methods optional |
| 5 | Beyond 4, representative/failure cases validate necessary method effects/boundaries |

### Dimension 13: Safety

Design necessary defenses by actual data, actions, and recipients. Content and execution both matter; add execution sandboxes as needed for generation-only applications. Regex, content filtering, containers, and prompts each cover some risks only.

Checks:
- [ ] Inputs, external material, and tool returns retain source/trust boundaries; validate types, ranges, and sizes. Summaries do not elevate instruction authority
- [ ] Check trusted identity and user/service object/data authorization at execution/output boundaries; new capabilities have no permissions by default
- [ ] Trusted gates constrain tools/actual parameters; explicit prohibitions take precedence, ASK blocks before valid approval; check authorization separately
- [ ] Restrict files, networks, mounts, processes, resources, and configuration writes as needed; constrain paths/URLs and post-check changes by actual execution semantics
- [ ] Manage secrets in trusted layers; consider environment variables readable by arbitrary code exposed. Protect sensitive outputs/logs by recipient scope
- [ ] Required security/audit components fail closed; Agents cannot alter their trusted policies or authoritative audit records
- [ ] Validate actual out-of-bound/rejected paths, with no tool execution on rejection; warnings/model statements alone are insufficient

Anti-patterns: regex guarantees no injection; ASK merely warns; user approval overrides DENY; service accounts share all data; sandboxes automatically secure credentials; append-only files treated as tamperproof; security failures permit actions.

| Score | Criteria |
|---|---|
| 0 | Actual risks lack necessary security boundaries |
| 1 | Prompt constraints only, no trusted execution safeguards |
| 2 | Partial defenses with clear identity, data, or execution-scope gaps |
| 3 | Clear layered design, but applicable credential, fail-closed, or audit boundaries insufficient |
| 4 | Complete necessary trust, identity/authorization, execution/output, credential, policy, and failure boundaries |
| 5 | Beyond 4, validated necessary adversarial/out-of-bound paths; specific sandboxes, real-time platforms, and full logs optional |

### Dimension 14: Evaluation and Monitoring

Assess quality assurance and actual deployment needs. Evaluation plans precede platforms; offline checks, periodic reviews, or human sampling may suffice. Real-time dashboards, A/B platforms, automatic alerts, and uniform metric counts are optional. Existing dimension-selection rules remain unchanged.

Checks:
- [ ] Business goals match system criteria; separate cases, execution, scoring, and acceptance, covering main flows, boundaries, and necessary failures
- [ ] Specify sources/versions/fixtures/execution protocols and necessary grouping, holdouts, and governance; historical/synthetic outputs are not inherently reference answers
- [ ] Verify necessary outputs, actual terminal states, processes, and resources; distinguish Mock/integration/user-acceptance evidence scopes
- [ ] Code scorers have positive/negative examples and missing-data checks; calibrate model scoring against criteria/human samples. Invalid scoring cannot pass business outcomes
- [ ] Retain planned/executed/validly scored counts, denominators, unexecuted/failure cases, and all reruns; correctly define repeated-trial metrics, independence assumptions, and uncertainty
- [ ] Comparable baseline/candidate/data/scoring versions; bind required checks to versions. Pending/old checks cannot accept new artifacts; averages do not offset hard failures
- [ ] Production monitoring specifies metric semantics, windows, sampling, missing data, owners, and responses by actual risk; changes support drill-down and verified-case feedback

Anti-patterns: HTTP200 only; text without actual-action checks; missing scoring data passes; pass^k treated as single-run success; cherry-picking best runs; averaging serious failures away; total scores replacing release permission; low scores without dashboards; failure-enriched samples estimating overall rates.

| Score | Criteria |
|---|---|
| 0 | Quality evaluation needed but effective criteria/checks absent |
| 1 | Logs/impressions only, without evaluation evidence |
| 2 | Basic usable metrics/cases with clear execution, scoring, denominator, or evidence gaps |
| 3 | Clear systems/comparisons, but applicable calibration, version gates, or production responses insufficient |
| 4 | Complete necessary cases/execution/scoring, statistics, version comparisons, acceptance, and applicable monitoring-feedback boundaries |
| 5 | Beyond 4, validated necessary evaluation/monitoring boundaries; real-time dashboards, A/B, and dedicated evaluation platforms optional |

## 6. Extended Dimensions 15-21

### Dimension 15: Standardized Tool Interfaces (MCP)

Assess only actual MCP use or explicit standardized cross-client/service integration needs. Mark Not applicable when a few local functions or existing SDKs suffice; do not deduct for absent protocols.

Checks:
- [ ] Integration has reuse/existing-service rationale; parameters/returns meet Agent needs. Do not rewrap clear existing interfaces unnecessarily
- [ ] Confirm supported client versions, service sources, and actual definitions; results/necessary evidence are readable
- [ ] Trusted systems supply credentials/identities; check tool allowlists and server authorization separately
- [ ] Explicit timeouts/error destinations; result checks determine completion, while connectivity/submission success is intermediate only
- [ ] Distinguish resources, tools, and prompt templates, using actual supported capabilities; select these three capabilities as needed

Anti-patterns: MCP for scoring in simple applications; protocol assumed automatically safe; exposing all service tools; descriptive templates treated as executed operations; guessing tool names/parameters without verification.

| Score | Criteria |
|---|---|
| 0 | Standardized integration explicitly needed but absent/unusable |
| 1 | Vague integration definitions, unchecked compatibility/tool contracts |
| 2 | Integrated but actual contracts, authorization, or error handling clearly incomplete |
| 3 | Reasonable connectivity/capability selection, but applicable security, timeouts, or failure handling incomplete |
| 4 | Complete compatibility scope, actual definitions, allowlists, authorization, returns, errors, and timeouts |
| 5 | Beyond 4, validated necessary integration, permission, and failure boundaries; multi-service combinations/dynamic extensions optional |

### Dimension 16: Goal Setting and Monitoring

Assess only long tasks, staged delivery, or progress-tracking needs. For simple tasks, checkable completion criteria suffice; mark Not applicable. Quantified metrics and independent monitoring mechanisms are optional.

Checks:
- [ ] Goals are specific, measurable, achievable, relevant, and time-bound
- [ ] Mechanisms independent of executors judge goal achievement
- [ ] Maximum iterations or timeouts exist
- [ ] Quantified metrics and success criteria exist
- [ ] Escalation or fallback exists when goals are not met

Anti-patterns: the same model executes and judges; unbounded monitoring loops; vague, unmeasurable goals.

| Score | Criteria |
|---|---|
| 0 | No goal concept |
| 1 | Implicit goals without monitoring/completion judgments |
| 2 | One "generate, evaluate" pass only, with vague criteria |
| 3 | Goals, progress, and completion judgments exist, but applicable acceptance, stop, or failure returns incomplete |
| 4 | Complete goal specifications, independent checks, attempt/time limits, failure destinations, and completion evidence |
| 5 | Beyond 4, validated goal-deviation, blocked, and exceeded-limit scenarios; multiple roles/replanning optional |

### Dimension 17: Knowledge Retrieval (RAG)

Assess only when locating external knowledge to support generation is necessary. Mark Not applicable when complete material is supplied without retrieval needs. Choose reference reads, keywords, vectors, or hybrids by actual needs; technology counts/multi-step searches earn no extra points.

Checks:
- [ ] Sources/retrieval methods match questions; use simpler sufficient methods directly. Vectors, hybrids, and knowledge graphs optional
- [ ] Retain permissions and user-specified time/business conditions; explain expanded default assumptions
- [ ] Bound candidate counts, read scopes, and budgets; retain context and validate quality for necessary chunking/fusion
- [ ] Verify current body, summary, and index versions; specify applicable update, deletion, and delay handling
- [ ] Evidence actually supports conclusions; reread originals as needed, handling contradictions, stale material, empty results, and knowledge gaps
- [ ] Output concrete sources/evidence boundaries, label summaries as summaries, and separate similarity from correctness

Anti-patterns: vectors equal RAG; missing permission filters; silently removing user conditions for results; silently using old indexes; unsupported citations; claiming complete searches from snippets; complex retrieval for scoring.

| Score | Criteria |
|---|---|
| 0 | External knowledge needed but not obtained, critical conclusions unsupported |
| 1 | Retrieval exists but unclear sources/scopes/actual evidence |
| 2 | Basic method fit with clear quality-control, evidence, or freshness gaps |
| 3 | Clear retrieval/evidence chain, but applicable permission, conflict, version, or gap handling insufficient |
| 4 | Complete necessary scope, budgets, evidence references, and applicable update/failure handling |
| 5 | Beyond 4, validated necessary retrieval quality, citation support, and boundaries; vectors, hybrids, and multi-step retrieval optional |

### Dimension 18: Inter-Agent Communication (A2A as Needed)

Assess actual in-process, cross-process, or cross-system communication. Do not deduct for absent network protocols, dynamic discovery, async tasks, multimodality, or read-state machines when shared state/direct calls suffice. Mark Not applicable with reasons when no additional communication is needed.

Checks:
- [ ] Methods match necessary information exchange; specify permitted recipients, fields, task scopes, and result retrieval
- [ ] Define data sharing and task triggering separately; distinguish notification arrival, acknowledgment, and business acceptance
- [ ] Trusted systems authorize actual caller identities, endpoints, or state access; capability cards do not establish trust
- [ ] Explicit applicable version, timeout, failure, duplicate, and late handling; direct calls need no mailbox state machines
- [ ] For necessary standard protocols, verify supported versions/actual contracts; describe custom HTTP scaffolds as custom interfaces

Anti-patterns: A2A for scoring in simple chains; capability discovery equals authorization; notification arrival equals acceptance; three message states guarantee exactly-once; broadcast all material to every role.

| Score | Criteria |
|---|---|
| 0 | Necessary information cannot be reliably obtained or delivered |
| 1 | Information moves but unclear fields, recipients, or scopes |
| 2 | Basic usable communication with clear actual-contract, permission, or result-handling gaps |
| 3 | Clear information exchange, but applicable trigger, version, failure, or acknowledgment semantics insufficient |
| 4 | Complete necessary fields, trusted association, access scopes, result retrieval, and applicable async/compatibility boundaries |
| 5 | Beyond 4, validated necessary communication/failure boundaries; dynamic discovery, standard protocols, async, and multimodality optional |

### Dimension 19: Resource-Aware Optimization

Assess control of task quality, deadlines, usage, and cost. Do not deduct for absent dynamic selection, automatic fallback, load balancing, or caching when fixed models suffice.

Checks:
- [ ] Models/necessary fallbacks meet quality, privacy, tool compatibility, and deadlines; switches do not bypass rejection or reset quotas
- [ ] Define applicable call, token, spending, time, concurrency, and other limits and actual counting conventions; request counts alone do not guarantee spending bounds
- [ ] All branches, SDK/framework retries, delegation, and aggregation share totals; centrally reserve before calls, settle afterward, conservatively retain unknown usage reservations
- [ ] Reserve necessary delivery/checks; provide safe exits for exceeded limits or failed budget control. Pre-call enforcement guarantees caps
- [ ] Distinguish rough estimates from hard limits; hard spending limits require bounded billable maxima. Verify caches/discounts with actual services; for prefix caching, keep static prefixes/tool order stable and dynamic content last

Anti-patterns: one fixed model means zero score; blindly switching cheaper models bypasses privacy; branches double-spend quotas; checking model spending only before tools; fixed character conversions called exact billing; final summaries exceed budgets.

| Score | Criteria |
|---|---|
| 0 | Necessary resources unbounded, allowing uncontrolled consumption |
| 1 | Cost awareness but prompts/post-hoc records only |
| 2 | Basic usable budgets with clear counting, reservation, or stopping gaps |
| 3 | Clear selection/budgets, but applicable shared quotas, unknown usage, or fallbacks insufficient |
| 4 | Complete necessary quality/deadlines, global counting, reservations/settlement, soft/hard limits, and exceeded-limit exits |
| 5 | Beyond 4, validated necessary budget/performance trade-offs; multiple models, dynamic routing, and caching optional |

### Dimension 20: Prioritization

Assess only when resource competition, deadlines, or conflicting importance require trade-offs. Mark Not applicable when fixed order/FIFO suffices. Use rules without model scores when sufficient; require reordering only for relevant condition changes.

Checks:
- [ ] Explicit ordering necessity/criteria; dependencies, permissions, inputs, resources, and budgets establish readiness first
- [ ] Schedule from ready sets; hosts centrally check/reserve necessary quotas before branch dispatch
- [ ] Explicit rules, tie-breaking, and applicable maximum waits; subjective model scores do not replace authorization/dependencies
- [ ] Necessary event changes may adjust order; preemption/cancellation of executed tasks have permitted boundaries, retaining goals/cumulative budgets

Anti-patterns: high priority bypasses approval/dependencies; branches simultaneously spend the same remaining quotas; indefinite low-priority starvation; dynamic reordering added for scoring in fixed tasks.

| Score | Criteria |
|---|---|
| 0 | Resource/deadline trade-offs needed but effective selection rules absent |
| 1 | Order exists but unclear criteria/readiness constraints |
| 2 | Basic usable ordering with clear resource, dependency, or fairness gaps |
| 3 | Clear criteria/scheduling, but applicable budget, wait, or change handling insufficient |
| 4 | Complete necessary ready filtering, ordering, tie-breaking, quotas, and applicable wait/reordering rules |
| 5 | Beyond 4, validated necessary trade-offs/failure boundaries; layered ordering, model scores, and dynamic reordering optional |

### Dimension 21: Exploration and Discovery

Assess only unknown questions needing hypotheses/validation; ordinary fact retrieval may be Not applicable. Multiple Agents, knowledge graphs, and complex search algorithms are optional.

Checks:
- [ ] Distinguish/trace hypotheses, support/counterevidence, validation methods, and current conclusions
- [ ] Consider alternative explanations by task need; new model opinions/confidence scores become evidence only after validation
- [ ] Validate within authorized scope; exploration does not expand tools, experiment risks, or business goals
- [ ] Explicit necessary evidence, scope, information-gain, or resource stop conditions; retain uncertainty in unverified judgments

Anti-patterns: unknowns trigger infinite search; hypotheses without validation; self-reported confidence replaces evidence; graphs/exploration squads for scoring.

| Score | Criteria |
|---|---|
| 0 | Unknowns need investigation but effective hypotheses not proposed/checked |
| 1 | Guesses without evidence/validation design |
| 2 | Basic usable investigation with clear validation/conclusion-boundary gaps |
| 3 | Clear hypotheses/evidence, but applicable alternatives or stop handling insufficient |
| 4 | Complete necessary hypotheses, validation, evidence traceability, uncertainty, scope, and stop rules |
| 5 | Beyond 4, validated exploration quality/boundaries; multiple Agents, graphs, and complex search algorithms optional |

## 7. Pre-Delivery Hard Checks

Mark any unmet item below as a serious issue:

- [ ] Explain why simpler architecture tiers were not selected
- [ ] Define measurable success criteria, draft main-flow/boundary/failure cases, and validation plans; label drafts as drafts, record unexecuted/invalid checks separately, and count neither as passing
- [ ] Every Agent has stop conditions; all loops (reflection, retries, Agent main loops) have attempt or time limits
- [ ] Every inter-Agent handoff has field definitions/validation rules
- [ ] Every Agent's tools/read-write permissions follow least privilege
- [ ] Irreversible/high-risk operations have policy-required approval or code blocking; bind valid approval to actual requests, checking identity/object authorization separately
- [ ] Cost or call-volume limits exist
- [ ] Failures are locatable through actual host events, necessary state, and artifact references; no need for model self-reports or full sensitive logs

## 8. Review Report Format

```markdown
# Agent Design Evaluation Report

## Basic Information
- Target:
- Agent types:
- Scored dimensions: N / 21 (M not applicable, K to be verified)
- Reviewer: author self-review / independent review

## Overall Assessment
- Overall score: X.X / 5.0
- Level:
- One-sentence conclusion:

## Dimension Scores
| Dimension | Score | Level | Key Findings | Evidence Type (Statement/Walkthrough/Empirical Test) | Evidence Location |
|---|---|---|---|---|---|

## Check Details
List only Unmet and Partially met items; for user-requested full audits, additionally attach item-by-item answers for every check.
| Dimension.Item | Check | Result | Evidence and Gaps |
|---|---|---|---|

## Hard Checks
| Check | Result | Explanation |
|---|---|---|

## To Be Verified
- Dimension: material needed

## Issues Found
### Serious (Must Fix)
1. Issue → recommendation
### Moderate (Recommended to Fix)
1. Issue → recommendation
### Minor (Optional Improvements)
1. Issue → recommendation

## Identified Anti-Patterns
- Anti-pattern name: specific manifestation

## Improvement Recommendations (By Priority, At Most 5)
1. Problem / cause / action / expected benefit
```
