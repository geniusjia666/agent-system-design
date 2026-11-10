# Orchestration Patterns

Use this reference in Step 4 of the main process to select an execution structure, or to review lost dependencies, error propagation, incorrect parallelization, and uncontrolled loops. This chapter designs nodes and edges; running an orchestration engine is outside its scope. See the multi-agent chapter for complete role, dispatch, and shared-state design.

## Contents

1. Select a Primary Pattern Before Deciding Whether to Combine Patterns
2. Define Nodes, Data Dependencies, and Validation Boundaries
3. Prompt Chaining
4. Routing
5. Parallelization
6. Orchestrator-Workers
7. Evaluator-Optimizer and Reflection
8. Autonomous Agent Loops
9. Add Planning or Exploration as Needed
10. Minimal Examples, Delivery Checks, and Anti-Patterns

## 1. Select a Primary Pattern Before Deciding Whether to Combine Patterns

First ask whether one call can meet the criteria; if it can, use it directly. Otherwise, identify known steps, categories, dependencies, and the parts that genuinely require model decisions, then choose the simplest primary pattern.

| Pattern | Applicability Signals | What to Rule Out First | Required Control Points |
|---|---|---|---|
| Prompt Chaining | The task can be split in advance into clear, checkable sequential subtasks | One call is sufficient; steps merely retell information | Upstream/downstream inputs, necessary earlier artifacts, intermediate gates, and failure destinations |
| Routing | Categories genuinely need different handling, and classification can be performed reliably | All paths are essentially identical; rules suffice but a classification model is added anyway | Allowed categories, selection method, multi-intent and unknown handling, and fallback |
| Parallelization | Independent tasks can run concurrently, or comparing multiple candidates offers benefits | Unmet data dependencies; shared-write conflicts; extra calls without benefit | Concurrency limits, aggregation conditions, task identity, branch failures, and timeouts |
| Orchestrator-workers | Subtask content or count varies with input, requiring dynamic decomposition, delegation, and aggregation | Fixed decomposition or one Agent suffices; splitting Agents merely because there are many files | Plan validation, dispatch scope, dependencies, fan-out budget, and aggregate acceptance |
| Evaluator-optimizer | Criteria are clear, reviews provide actionable feedback, and iteration has measurable value | One generation plus checks suffices; only vague self-evaluation is possible | Review inputs and criteria, version correspondence, modification scope, and iteration limits |
| Autonomous Agent | Next actions depend on environment feedback, making fixed paths insufficient | Predefined branches or bounded loops suffice | Real observations, allowed actions, host validation, and completion and stopping conditions |

The first five are common workflow patterns; the sixth permits more action decisions. Workflows may use models for classification, dynamic task-list generation, or quality judgments, while code still bounds the allowed control structure. A process containing a model decision remains a workflow.

Assess pattern, control mode, and Agent count separately. A fixed multi-role pipeline is still a workflow; parallel tool calls may remain within one Agent; workers may be restricted LLM nodes, with autonomous loops configured only as needed. Dynamic subtasks are the defining feature of orchestrator-workers; roles, tools, and permissions may be predefined.

Add supporting patterns only for clear gaps, usually implementing one primary pattern first. Combine patterns after assessing benefits and costs. Scores do not depend on pattern count, framework features, or organizational role count.

## 2. Define Nodes, Data Dependencies, and Validation Boundaries

Define responsibilities, inputs, artifacts, and completion checks for each node. Prefer code for ordinary data transformations and executable checks; use LLM calls only at nodes requiring language capabilities.

| Boundary | Minimal Design |
|---|---|
| Data dependencies | Upstream/downstream nodes, transferred fields, and necessary original goals and earlier artifacts; references must be readable and their versions verifiable |
| Control conditions | Which results allow continuation, and which require correction, rollback, degradation, pausing, or termination |
| Validation gates (Gate) | Separate checks for required fields and formats, business conditions, and artifact usability; who performs them and which node is responsible for failures |
| Resources and failures | Node correction or retry limits, external-wait timeouts, and a task-wide budget covering all branches and nested loops |

Sequential edges guarantee execution order only; explicitly pass dependency data. Even when a key exists in shared state, explicitly include its body in downstream input. Use types, enums, and required-field constraints for critical control fields. Human-readable bodies may use Markdown; use JSON where machine parsing is needed.

Handle missing, obsolete, unreadable, or insufficiently checked inputs before sending them downstream, and record the handling. Distinguish step completion from artifact acceptance: when a review task successfully returns `FAIL`, execution status may be `SUCCESS`, while the artifact is still handled as `FAIL`. Reuse existing handoff statuses and review verdicts.

Format correction, content repair, transient retry, and re-execution are four different actions; choose by error type and remaining budget. After upstream changes, reassess only affected downstream validity and retain the rest. Verify unknown write outcomes first; see the reliability chapter for complete recovery facilities.

Give every back edge a termination exit. The host must enforce at least an attempt or time limit, with separate timeouts for external waits; local limits count toward task totals. Follow the single-agent chapter's convention: each attempted model call counts as one iteration, including final generation, review, planning, and correction. Calls across nodes and parallel subtasks also accumulate; document mappings when frameworks count differently.

## 3. Prompt Chaining

Split a known task into a fixed sequence, with each LLM step processing upstream artifacts. Examples include extraction followed by generation, or an outline followed by body text. The aim is to trade added latency for steps that are easier to check; validate whether quality improves.

1. Decompose steps around meaningful business artifacts. Define each step's inputs, outputs, and necessary rules, with one checkable artifact per node.
2. Explicitly pass the original goal, hard constraints, and necessary earlier artifacts downstream; the previous node's summary is supplementary only.
3. Add gates at handoffs affecting downstream correctness, continuing only after checks pass. Add model reviews only where genuinely needed.
4. Route validation failures to the responsible node with specific errors for correction within budget. End or escalate when limits are exceeded or correction is impossible; bound backward jumps.

Stages may use different prompts, the same model, or code nodes. Introduce expert personas and independent Agents only as needed. Review comments supplement original material; refactoring requires both original code and comments.

Anti-patterns: many nodes that only retell information; packaging a fixed chain as autonomous planning; passing only the last sentence; claiming factual correctness from format checks alone; mechanically processing invalidated inputs downstream.

## 4. Routing

Select an appropriate handler by input category or current state. Prefer existing reliable rules, conventional classifiers, or model-based methods. Use one method directly if sufficient; add vectors or multi-model routing only as needed.

1. Define allowed categories, genuinely different responsibilities, and unified outputs. Specify single selection, multiple selection, or sequential handling of multiple intents.
2. Test classification and fallback with representative inputs. Validate model returns against allowed enums first, and select execution entry points only from the allowed set.
3. Define clarification, bounded degradation, or human paths for ambiguity, multiple intents, unknown categories, invalid output, or classification-service failure. Use these paths when uncertain; the closest category is a reference only.
4. Check permissions and approvals before handler execution. Routing into a refund workflow, for example, does not itself authorize the business action.

Validate low-confidence thresholds for the actual classification method. Calibrate model-reported confidence scores before treating them as probabilities. Routing logic and handler responsibilities may be checked separately; introduce independent services, multi-level routing, and dynamic registration only as needed.

Anti-patterns: all categories do the same thing; handling half a multi-intent request without explanation; defaulting unknown categories to high-risk actions; bypassing permissions based on similarity; combining classification methods for scores.

## 5. Parallelization

Distinguish Sectioning from Voting: sectioning performs different independent tasks; voting generates multiple candidates for the same task and compares them under defined rules. Concurrency suits waits such as I/O; execution resources determine whether computation actually occurs simultaneously.

Before concurrency, confirm that current inputs are ready, branches have no unmet data dependencies, and they will not compete to write the same unisolated resource. Establish shared interfaces or rules first; keep dependent tasks sequential. Multiple tool requests from one model still require dependency checks before parallel execution.

| Aggregation Question | Rule |
|---|---|
| Which branches to wait for | Wait for all required items by default; explicitly define any allowance for partial success, the first valid result, or a quorum |
| Who produces what | Results carry stable task identity, status, artifacts, and necessary versions. Assemble by identity and business order; arrival order is incidental |
| Branch failure or timeout | Record gaps and retry, degrade, or block as agreed. Report partial completion or blockage when critical branches have not passed |
| Early termination | Define cancellation or cleanup of remaining tasks and acceptance of late results. After requesting cancellation, still verify whether external actions stopped |
| Concurrency resources | Limit simultaneous executions and total fan-out, reserving aggregation and acceptance budget; set thread counts according to concurrency limits |

For voting, define comparable outputs, valid-vote counts, and tie or disagreement handling. Calls may be correlated and fail together; the majority is only a reference. Send results only after safety screening completes, even if the business branch finishes first.

Parallel latency depends on the critical path, rate limits, queuing, and aggregation, and requires measurement; the slowest branch's duration is only a lower bound. Compare end-to-end results against a sequential baseline. Execute small, manageable tasks sequentially when sufficient.

Anti-patterns: parallelizing dependent work; presenting fixed branches as dynamic delegation; unbounded concurrency; mixing exception objects into normal results; claiming full completion after one result; assuming a shared append-only list guarantees business order.

## 6. Orchestrator-Workers

The orchestrator dynamically creates subtasks from current input, dispatches them under controls, and synthesizes results. Use when actual investigation is needed to determine material scope or work items; ordinary parallelization suffices for independent branches known in advance.

1. Obtain enough facts to decompose work first. Give the orchestrator appropriate tools when it needs read capabilities.
2. Plans state subtask goals, identities, dependencies, necessary material, artifacts, and acceptance criteria. The host checks reference existence, unique IDs, executable dependencies, absence of unintended dependency cycles, and compliant scope.
3. Enforce hard limits on dynamic task count, concurrency, nesting depth, and total budget. Select worker capabilities from trusted allowlists; trusted systems alone grant permissions.
4. Dispatch only dependency-ready work and track returns and missing items. Workers return conclusions, evidence, gaps, and readable artifacts; paths and completion notices are only part of the return.
5. Check plan coverage, conflicts, and critical dependencies before aggregation. Use deterministic assembly when sufficient, a model only when synthesis reasoning is needed, and validate the final goal.

Dynamic plans may use predefined executors, with role instances created as needed. A read-only coordinating main node is an optional role configuration; independent context isolates information only, while the host still enforces permissions.

Many tickets, many files, or long reports are only clues. Plan errors may propagate through the entire chain, so validate facts and constraints before dispatch. Add necessary independent review according to risk, with planning-review Agents introduced only as needed.

Anti-patterns: assuming an orchestrator replaces all fixed workflows; writing boundaries in an SOP without enforcing them; copying a contradictory example where "the main Agent is read-only but writes the architecture file itself"; treating path existence as sufficient work quality; endlessly expanding subtasks.

## 7. Evaluator-Optimizer and Reflection

Generate a candidate, evaluate it against explicit criteria, and use feedback for correction. Reflection may include self-checks, but acceptance depends on check results. In-task correction affects only the current task; long-term improvement needs separate design.

Use code checks and real tests directly when they can decide. For subjective evaluation, use a separate review call or human judgment against criteria. Separate production and review responsibilities. Different models, permanent Reviewer Agents, and evidence visibility are optional; separate context reduces only some shared bias.

Give reviewers original requirements, constraints, the candidate at the corresponding version, and necessary facts or test results. Evidence takes precedence; the generator's self-defense is a reference only. Minimal feedback includes the checked artifact or version, verdict, specific location, issue, repair suggestion, and unresolved items. Reuse the existing `verdict` field, defining structured business feedback when needed.

| Result | Next Step |
|---|---|
| Required checks pass | Deliver the same checked version; rewriting requires new checks |
| Clearly repairable issues | Modify the responsible scope using feedback, then evaluate the changed version; proceed only with remaining attempts and total budget |
| Invalid review, conflicting criteria, or missing facts | Correct format, supply evidence, or escalate within budget; treat review-service failure as an invalid review |
| Stagnation, exceeded limits, or no feasible repair | Return the last actually validated result, usable parts, and gaps, truthfully marked as below criteria |

Every modification may introduce new problems; retain version-to-check correspondence. Old candidate scores apply only to old candidates. `CONDITIONAL_PASS` requires explicit conditions and an acceptor; treat it as not fully passed until conditions are met. Reserve final-check budget; return a newly modified result as accepted only after required checks finish.

Mark this pattern not applicable when no feedback-based correction is needed. Iterate repeatedly only for clear gains, determining iteration counts through actual trials. "Until perfect" and a universal three iterations are merely claims.

Anti-patterns: universally treating direct delivery after one generation as wrong; passing because a model praises itself; generating and proving correctness in the same call; using old scores for a new version; repeated repairs without new evidence; unlimited review loops.

## 8. Autonomous Agent Loops

The model chooses next actions from real observations, while the host controls capabilities, parameters, permissions, and budgets. Use for open-ended problems inadequately covered by fixed paths; handle exceptions with known branches directly through those branches.

This chapter defines loop entry, allowed actions, environment feedback, and exit boundaries only. Follow the single-agent chapter's internal sequence: execute requested actions for real, check the task after tool success, and perform acceptance after the model's final output.

Retain the original goal, hard constraints, current state, and necessary evidence at every decision. On missing inputs, repeated failure, no new information, or withheld required approval, clarify, pause, or end under the rules. Read material when evidence is missing.

A fixed skeleton may embed an autonomous loop in just one investigation node, with bounded entry scope and artifact checks before returning to the main process. Keep other stages fixed; the host enforces loop and spending limits.

Anti-patterns: calling a fixed tool sequence autonomous; recording success when the model stops requesting tools; treating denied approval as a retryable error; exceeding budget for an attractive final summary. See the later reliability chapter for safety, timeout, and recovery facilities.

## 9. Add Planning or Exploration as Needed

Planning converts goals into executable tasks and dependencies; add it as needed. Use predefined workflows directly when sufficient. Execute simple autonomous queries directly, introducing an independent Planner only as needed.

Separate plan creation, validation, and execution into logical stages, which the same Agent may handle. Execute only ready items in the current valid plan. Replan only when new evidence invalidates assumptions, dependencies, or routes; handle ordinary failures as errors.

Replanning states changes, reasons, whether completed items remain valid, and added costs. The host then checks scope and dependencies. Recompute executable order after dependency-graph changes, invalidating old traversal lists and updating `plan` together with the order. Preserve the original goal and approvals, and continue accumulating the total budget. Confirm changes affecting user goals or permissions first.

Exploration and Discovery applies to genuinely unknown tasks requiring hypotheses and validation; use direct retrieval for ordinary fact lookup. Record hypotheses, supporting and opposing evidence, validation methods, and current conclusions. Validate valuable hypotheses first and consider alternative explanations within authorization and budget. A model's new idea becomes a discovery only after verification.

End exploration when evidence meets the agreed goal or defined scope, budget, information-gain, or other stopping conditions trigger. Explicitly retain uncertainty for unverified hypotheses. Introduce multiple Agents, knowledge graphs, complex search algorithms, and continuous self-modification only as needed. Long-term learning, automated experiment platforms, and knowledge maintenance are outside this chapter's scope.

Anti-patterns: replanning every step; new plans automatically erasing completion records; calling topological sorting dynamic planning; treating unknowns as unlimited search; equating confidence scores with experimental validation; building graphs or exploration teams for scores.

## 10. Minimal Examples, Delivery Checks, and Anti-Patterns

The following are design candidates; effectiveness, performance, and cost have not been measured. Both example budgets illustrate counting only.

### Example 1: Classify Tickets into Different Handling Paths

The primary pattern is a routing workflow: input → classification and enum checks → FAQ response draft, human refund review, or technical investigation → respective checks → unified return. Clarify unknown categories or unresolved multiple intents first. Refund routing only enters human review; a person performs the refund itself. Embed a read-only autonomous node in technical investigation if needed, keeping other paths fixed.

Pass the original ticket and necessary rules to the selected node along with its category. The demonstration allows at most 4 attempted model calls per task, shared across classification, generation, correction, and autonomous branches, with timeouts for each model or tool wait. Return gaps when limits are exceeded; do not send unchecked drafts externally.

Validation: normal categories reach their handlers; unknown and invalid categories use fallback; retain all intents or clarify explicitly; no side effects occur before approval; budgets keep accumulating across node changes. This example needs no multi-level classification, voting, Planner, or long-term memory.

### Example 2: Generate Code → Review → Repair if Needed → Test

The primary pattern is prompt chaining, combined with evaluator-optimizer when correction is necessary. Deliver directly when there are no issues and tests pass. One model may handle multiple restricted nodes, or multiple Agents may be used for established isolation needs. Order remains fixed, so this is still a workflow.

Review reads original requirements and code; repair reads code, comments, and relevant tests. Changes create a new version, and old pass records apply only to the old version. Deliver the same version actually checked. Static checks and independently executable tests may run in parallel, but tests depend on code already written; aggregate success only after all required checks finish.

The demonstration allows at most 6 attempted model calls in total and at most 1 repair, with external-wait timeouts. Generation, review, repair, and necessary final generation all count toward the total. Code tests consume time and resource budgets, not model iterations. If budget after the final repair is insufficient for required model review, deliver usable parts with an unverified notice and report that acceptance is incomplete.

Validation: deliver unchanged when no major issues exist; block when required original code is missing; recheck repaired versions; associate sequence and versions by identity, independently of arrival order; explicitly return exceeded limits, test failures, and invalid review results.

### Delivery Checks

In Section 3 of the design document, state primary and supporting patterns, their benefits, and control mode. Define nodes or Agents in Section 4, loops and data handoffs in Section 7, and unified budgets and failure policies in Section 9. Explain inapplicable patterns and reuse the existing template.

- Check that all required inputs have readable sources and dependencies exist and are executable. Fixed acyclic segments contain no unintended cycles; intentional loops have stopping exits.
- Check routing allowlists, unknown and multi-intent fallback, handler authorization, and hard boundaries for dynamic plans and fan-out.
- Check that concurrent dependencies are satisfied without write conflicts, aggregation identifies tasks and versions, and missing critical branches are reported as partial completion.
- Check that review feedback corresponds to artifact versions, budget remains for necessary final checks, and unaccepted modifications are treated as not passed.
- Check that all retries, corrections, replanning, and nested loops count toward applicable total budgets. Compare actual task success, latency, and cost against simpler baselines.

General anti-patterns: splitting work to complete a roster of roles or patterns; repeatedly retelling critical data; replacing data contracts with path order; equating valid Schema with business acceptance; confusing fixed branches with dynamic subtasks; treating orchestrators as the only correct architecture; treating independent context as permission isolation; passing file paths without checking artifacts; treating votes as factual proof; unlimited back edges; separate budgets at each level allowing uncontrolled totals; returning an unevaluated new artifact at the end of iteration.

Sources: Anthropic's Building Effective Agents; LangGraph's Workflows and Agents; Lessons 03 and 23 of The Essence of Enterprise-Grade Multi-Agent Design Methodology; and prompt chaining, routing, parallelization, reflection, planning, and exploration patterns from the legacy design-advice Skill. Dependency readiness, version acceptance, budget composition, boundary trade-offs, and examples are engineering syntheses by this Skill, not verbatim source conclusions or measured effectiveness.
