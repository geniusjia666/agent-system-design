# Evaluation and Iteration

Read this reference in Step 1 of the main process for requirement suitability, Step 6 for evaluation design, or when reviewing system quality and iteration mechanisms. Start with concrete cases, executable criteria, and baselines before adding necessary tools. Introduce real-time dashboards, A/B platforms, automatic learning, and fine-tuning only as needed.

## Contents

1. Requirement Suitability: Validate Value and Prerequisites First
2. Prototypes: Validate Critical Assumptions Within Minimal Scope
3. Evaluation Cases: Separate Definitions, Records, and Conclusions
4. Evaluation Execution: Prepare Environments for System Boundaries
5. Scoring: Define the Object Before Choosing the Judge
6. Aggregation: Interpret Success Rates and Repeated Trials Correctly
7. Change Gates: Fast Feedback and Trusted Release
8. Production Monitoring: Derive Signals from Business Goals
9. Data Feedback, Retrospectives, and Controlled Learning
10. Minimal Examples and Delivery Checks

## 1. Requirement Suitability: Validate Value and Prerequisites First

Suitability asks which problems are worth solving; it does not replace architecture selection. Identify users, triggers, current practices or unmet needs, actual frequency and duration, error costs, owners, and bottlenecks as the business grows. Verify using existing documents, actual workflows, and authorized data. Tasks without dedicated human job positions may still be valuable.

| Perspective | Record Evidence and Judge by Facts |
|---|---|
| Scale effects | Measurement scope, frequency, per-task duration, waiting, and repeated work; infrequent high-value tasks and existing tools may still be worthwhile |
| Task clarity | Inputs, outputs, business criteria, exceptions, and unsupported scope; first check whether ordinary code suffices for rule-definable parts |
| Error consequences | Affected parties, detectability/reversibility, review and correction costs, and necessary approvals; high benefits cannot offset prohibited actions |
| Information availability | Whether necessary sources exist, permit authorized reading, and have adequate quality and freshness; organization and integration costs. Verify structured data correctness too |
| Actual value and bottlenecks | What is saved, enhanced, or newly possible; how to confirm user adoption and business improvement |

The five-dimension table is a discussion framework; judge each item by evidence. Do not adopt the course's universal 25-point scale, 18-point project threshold, or 10-times-per-week cutoff. Resolve data, authorization, and acceptance blockers first, or narrow the pilot. Mark missing information as to be confirmed. Handle critical risks separately; high scores elsewhere do not remove them.

Compare humans, ordinary code, existing services, and the simplest model candidate. Estimate benefits, model/tool charges, deployment and maintenance, human review, and error-handling costs for the same business scope, quality requirements, and period, stating assumptions and scope. Convert saved time according to its actual use, recording it separately from cash benefits. Value may include time, quality, and new capabilities; "time × quality ÷ cost" is a rough comparison only, not a comparable financial return on investment.

Conclude that AI is unnecessary, prerequisites are insufficient and work should wait, a bounded pilot is appropriate, or evidence supports proceeding. When AI has value, separately assess the need for an autonomous Agent under the architecture chapter. Reuse that chapter's tiers for control mode and role count.

## 2. Prototypes: Validate Critical Assumptions Within Minimal Scope

Define users, when output is needed, whether AI recommends or executes, desired business changes, and minimum requirements. Single/multi-turn interaction, embedded assistance, event workflows, UI automation, and platforms are product forms and may combine; assess Agent count separately. Choose proactive, upload, or event triggers from actual workflows, validating the value of background triggers too.

Choose the unknown assumption most consequential to direction. Define what supports it, refutes it, or leaves insufficient evidence; list other assumptions as unverified. Passing one assumption is only one release prerequisite. Bound inputs, knowledge and state sources, output consumers, exclusions, budgets, and stopping conditions. Run representative scenarios with the simplest viable candidate and compare current practices.

Define verifiable reference facts or standards (Ground Truth, GT) before acceptance. GT may be checkable facts, structured targets, expected terminal states, or anchored quality criteria; a unique text answer is only one form. Align standards and I/O with each other and version them. Do not change answers after seeing candidates to make them pass.

User Acceptance Testing (UAT) validates real inputs, understanding, and workflow fit; complete offline correctness, security, and integration checks separately. Controlled prototypes may start with the main flow, but retain necessary permission and stopping guardrails from the first run involving real data or side effects. "Ignore exceptions initially" applies only to prototypes; complete exception handling before production.

Prototype findings include at least assumptions and evidence, baseline/candidate differences, annotation or data-quality issues, actual user behavior, unverified scope, and next steps. Choose sample sizes and periods by variation, risk, and available resources. 50/200/1000 cases and 1 day/2 weeks are reference scales only. This Skill designs validation plans only; mark unexecuted validation as to be verified.

## 3. Evaluation Cases: Separate Definitions, Records, and Conclusions

An Eval Case is a versioned static scenario. Execution records store actual outputs, tool events, state, duration, and costs. Scoring records bind cases, runs, scorer versions, and evidence. Release decisions are formed separately through gates. Expected definitions come from business criteria; actual failures or model-reported success belong only in execution records.

| Case Field | Minimal Design |
|---|---|
| Identity and classification | Stable ID, case version, function/scenario, source, risk or priority; difficulty as needed. Prioritize boundary cases by risk |
| Inputs and initial state | User requests, necessary context, trusted identity/scope, knowledge versions, and tool/environment fixtures; multi-turn cases add scripts or user goals |
| Scoring criteria | Required and prohibited outcomes, check methods and evidence, and necessary hard-failure items; reference answers are optional |
| Execution protocol | Tested boundary, isolation/reset, iteration/time/resource limits, and allowed retries; do not inject evaluation answers into tested context |
| Applicable process constraints | Necessary actions, dependencies, parameter/object scope, and terminal states; constrain only necessary actions and terminal states when multiple paths are valid |

These are evaluation business fields; leave generic dispatch/handoff/gate Schema unchanged. Keep large datasets in existing test or dataset-management systems. Design documents retain representative cases and references; build new platforms only when genuinely needed.

Combine sources: verified historical samples establish a foundation, experts cover high-consequence and unseen boundaries, synthetic variants fill gaps, and production records reveal real failures. Verify historical outputs, likes, and approvals before treating them as GT. Validate business semantics of synthetic questions and answers; another model's generation is another candidate, not evidence of authenticity.

Use a function × scenario matrix to cover the main flow, ambiguity/missing inputs, empty/multiple results, boundaries, permissions, security, service failures, and applicable recovery. Add samples by risk and choose counts per cell as needed; exactly 1 or at least 3 cases per cell are examples only. Retain semantically similar cases exposing distinct failures. Before similarity deduplication, check whether it would remove critical boundaries.

Separate development/tuning sets, baseline-protecting regression sets, and a Holdout Set not used for tuning. Training, prompt examples, retrieval material, and tuning records may leak answers. Split by source, template, task/user, or time groups to keep same-origin variants out of different sets. Repeated tuning on holdouts turns them into development sets; update under controls and retain old baselines.

Additions, corrections, deduplication, invalidation, and retirement create new versions, recording reasons, coverage changes, and owners. Keep historical results interpretable; sets may grow, change, or retire. Apply data governance for privacy minimization, redaction, source authorization, retention/deletion, and access scope. Handle user sessions under retention limits; using them as learning assets needs separate authorization.

## 4. Evaluation Execution: Prepare Environments for System Boundaries

| Tested System | Execution and Evidence |
|---|---|
| Single call | Actually execute input handling and necessary pre/postprocessing; retain outputs, format checks, usage, and failures. Include retrieval/tools in the boundary if present |
| Multi-turn conversation | Fixed user scripts help locate specific paths. Dynamic simulators advance from actual replies, defining user settings, hidden goals, stopping conditions, and simulator calibration; both cover only some real users |
| Fixed workflows/multi-agent chains | Check necessary node inputs, artifact versions, handoffs, aggregation, and terminal states. Check the actual graph for loops or conditions; also test missing artifacts and error propagation |
| Autonomous Agent | Actually execute permitted tools in authorized environments; record key decision summaries, actions, and results. Check goals, process limits, and real terminal states; completion notices are clues only |

Mock returns, contract tests, and controlled real services establish different scopes. Select by change impact: prompts can change write paths too, so choose validation levels for Prompt changes by actual impact. Passing mocks covers interface shape only; authentication, service semantics, concurrency, and real side effects need separate validation.

As needed, give each case or trial a separate scope, known initial state, isolated memory/cache/action records, verifiable fixtures, and cleanup rules. Keep unrelated initial state comparable; explicitly define state carryover when testing caching or resumption. Replace external sending, payments, and similar actions with controlled test targets. Reset isolated test resources only.

Reuse the security chapter's sandbox choices; Docker is one option. Inject applicable tool errors, timeouts, denied approvals, unknown outcomes, budget exhaustion, cancellation, and late results according to risk. Rejection tests establish actual non-execution; warnings are supplementary.

Record applicable code, prompts, actual model versions and parameters, tools/Skills, knowledge/indexes, environment fixtures, case sets, executors, scorers, policies, and run times. If services cannot lock snapshots, record obtainable identifiers, dependencies, and drift risks, truthfully noting unstable versions. `temperature=0` or fixed seeds reduce randomness only; validate end-to-end determinism separately.

Save actual attempts, failures, and budgets for every trial, counting maximum iterations under the defined convention. Separate repeated trials from business retries. On tool, service, or evaluation-executor failures, record actual states first and retain failures. Verify incurred side effects using original action keys.

## 5. Scoring: Define the Object Before Choosing the Judge

Distinguish output quality, task completion, permitted processes, and resource constraints. Use exact rules for field extraction/classification, necessary facts, coverage, relevance, and expression criteria for open generation, and actual objects/versions and terminal states for action tasks. Exit code 0, HTTP 200, correct formats, or citations alone cannot prove business correctness.

| Method | Applicability and Validation |
|---|---|
| Code assertions | Schema, allowed values, facts/sets, artifact usability, terminal states, ordering dependencies, permissions, and resources; validate assertions with positive, negative, boundary, and missing-data cases |
| LLM-as-a-Judge | Semantic/subjective dimensions difficult to encode as rules. Supply original tasks, necessary facts, criteria, anchors, candidates, and versions; return verdicts, brief rationale, and missing-evidence items |
| Human review | Domain judgment, actual user value, high-risk acceptance, scorer calibration, or disputes; may serve as the main review method |

Prefer reliable code checks where possible. Keyword presence, BLEU/ROUGE similarity, or "contains no UUID" establishes the defined narrow rule only; semantic correctness and sensitive information need separate checks. Early hard failures may skip expensive scoring. Retain "not run" for skipped checks and record each dimension separately.

Process evaluation asserts required invariants, partial-order dependencies, parameter scope, and prohibited actions. Compare complete sequences only when fixed SOPs genuinely require them. A current-version "golden trajectory" is a reference path only; other valid paths remain valid. Assess tool-use frequency changes alongside outcomes before diagnosing regression.

Hide candidate origins from model judges and control position, length, and style preferences. Swap order in pairwise comparisons; record conflicting results as uncertain or re-review, deciding winners by evidence. Self-evaluation and same-family models risk bias; execute independently, calibrate, and state limitations when used. Multiple different judges may still fail together.

Use verified human-labeled samples covering good/bad, boundary, and high-consequence categories. Examine confusion matrices, failure-detection rates, and false-positive rates, choosing thresholds by category/risk. Consider class imbalance alongside overall agreement. For binary metrics, define the positive class and precision/recall denominators. Recalibrate after Judge, rubric, or distribution changes. Do not claim reliability from a universal 85% agreement rate; judge it from calibration results.

Give each scale level distinguishable anchors. Pairwise comparisons define better/equal/worse and uncertain outcomes. Require brief auditable rationale and evidence, not internal chains of thought. Scorer-generated reference answers are candidates only; authoritative facts still come from original standards. Missing evidence, invalid scoring format, or service failure means invalid scoring; mark the tested business outcome as undetermined.

## 6. Aggregation: Interpret Success Rates and Repeated Trials Correctly

Fix planned cases, run counts, checks, and exclusion rules first. Separate actual business passes/failures, NOT_RUN, execution-environment errors, invalid scoring, and unresolved items. These are evaluation-record states, separate from generic handoff enums.

Report planned/executed/validly scorable counts and coverage, pass rates among validly scorable runs, and completion against the planned set. Count unexecuted and invalid checks separately, never as passes. Exclude only under prior protocols and list reasons, retaining hard cases and temporary service failures in reports. User-facing end-to-end success rates include service and recovery costs under actual request protocols; report offline valid-sample rates separately.

Aggregate by function, risk, difficulty, source, and necessary user/task slices while retaining totals and counts. Judge quality, security, cost, and other hard requirements separately; averages cannot offset them. Design self-review scores of 0-5 assess documents and evidence only; production success rates and release authorization are separate judgments.

| Metric | Definition and Use |
|---|---|
| Single-run success rate / pass@1 | Probability of meeting criteria in one run under the specified system and protocol; a user request may contain protocol-defined bounded recovery, which must be stated |
| pass@k | Probability of at least one success among k attempts on the same case. Used to assess multiple candidates or permitted repeated trials; explain success identification/selection and extra costs |
| pass^k | Probability that all k runs on the same case succeed. Measures repeated reliability, not success with one user opportunity; choose gate use according to system needs |

Define whether one run includes tool retries, model corrections, or multiple-candidate selection; those internal attempts are not k independent opportunities. A pass@k using a test grader to select the best candidate shows only that candidates contain a correct answer; verify separately whether the product can select it itself. Earlier irreversible erroneous actions still count as failures even if final output succeeds.

Only when repeated success on the same case is independent with identical probability p do `pass@k = 1-(1-p)^k` and `pass^k = p^k` apply. When success rates differ across cases, calculate per case before aggregating under the target distribution. Exponentiating the overall average gives incorrect results. Use actual joint outcomes for correlated failures, shared state, or adaptive retries; independent formulas do not apply there.

For a random k-subset of n trials per case (n≥k, with c successes), empirical combination proportions are `1-C(n-c,k)/C(n,k)` and `C(c,k)/C(n,k)` for at least one/all successes, defining C(a,k)=0 when a<k. Generalization to future probabilities requires suitable sampling assumptions. Mark n<k as insufficient evidence, with results as walkthroughs only. State differences between consecutive-run and random-subset protocols.

Record all attempts and costs in repeated runs. Define trial budgets and decision methods beforehand and report all results. State uncertainty for small samples, correlated repeats, user/task clustering, or frequent comparisons across versions. Use appropriate confidence intervals or task-grouped resampling. Recheck one or two fluctuations before diagnosing regression.

Compare old/new candidates in paired trials on the same cases, environments, and scoring protocols where possible. Report improvements, ties, regressions, unresolved items, and slice risks. Use a fixed approved baseline to detect long-term regression, optionally also comparing the current production version. After changing data or scorers, rescore comparable versions or state non-comparability. Baseline updates require review, versions, and reasons; update only after review and replace outdated baselines promptly.

## 7. Change Gates: Fast Feedback and Trusted Release

Continuous Integration (CI) validates changes. Passing tests, merging code, approving release, and successful deployment are distinct facts. Reuse shared checks and select necessary suites by impact; pipeline count depends on need. Define complete processes, thresholds, and owners in existing delivery systems.

| Change | Validation Focus |
|---|---|
| Code/runner/configuration | Static, unit and contract checks, critical end-to-end tests, and error/budget/permission execution paths |
| Prompts | Format, semantics/boundaries, actual behavior, necessary side effects, and costs; string checks are only one part |
| Model/parameters/service version | Representative quality, tool compatibility, stability, security, performance, and costs; expand by impact |
| Knowledge/indexes | Sources, authorization, freshness, retrieval coverage, and citation support; necessary deletion/update synchronization |
| Skill | Triggering, loading, instruction boundaries, tool/artifact handoffs, and context costs |
| Tools/interfaces | Parameters, returns, authentication/authorization, timeouts/unknown outcomes, idempotency, and real integration |
| Cases/scorers/gate policies | Positive/negative cases, calibration, coverage, and comparison conventions; separate rubric-driven score changes from system improvements |

Order by risk, dependencies, and costs: run cheap configuration/Schema and critical authorization checks first, provide early feedback through small baseline-protecting regressions, then run applicable behavior, quality, integration, stability, performance, and security suites. Run critical safety checks early by risk, even before a fixed "fifth gate." Form corresponding admission decisions only after all required checks finish.

CI may start asynchronously while further commits continue, but pending required checks must not permit automatic merging or release. Bind checks to specific commits, configuration, data, and scorer versions. Reassess applicable results after new commits or critical-input changes; old passing reports apply only to old artifacts. External sending and office-system changes require separate authorization; automatic execution does not include it.

Hard failures block. Route insufficient evidence, quality trade-offs, or scoring disputes through controlled review. Admit under existing permissions only after required checks validly pass and thresholds and approvals are satisfied. Humans cannot waive prohibited actions; unexecuted checks remain unexecuted. Permitted risk acceptance requires scope, reasons, and expiry, preserving historical results unchanged.

Run/scorer failures, timeouts, and flaky cases require diagnosis, bounded reruns, and owners, retaining failures alongside rerun results. When isolating unstable cases, preserve coverage gaps, alternative safeguards, and restoration conditions, keeping cases in the set. Hard failures also include critical business, data-integrity, and budget limits; one failure can block. Verify ambiguous probe hits before recording confirmed incidents.

Support controlled pilots, shadow validation, or gradual rollout within permitted scope. Shadow tasks must not duplicate real sends or writes. A/B assignment considers user/task relationships, representativeness, and risk; use randomized trials as needed. Bind deployment and rollback to valid versions and compatible state. Configuration rollback changes configuration only; incurred external side effects remain recorded as having occurred.

Reports state changes, snapshots, baseline/candidate, all counts and results, unexecuted/invalid/regressed cases with evidence, resources, coverage gaps, gate decisions, and owners. Prefer existing tests, CI, and logs. Even self-hosted tools require checks on whether model calls or telemetry send data outside the permitted domain. Verify platform APIs, probe counts, and installation commands against checked documentation.

## 8. Production Monitoring: Derive Signals from Business Goals

Evaluation and Monitoring answer sample performance and continuing production compliance with goals, respectively. Observability complements execution guardrails in the reliability/security chapter. HTTP 200 establishes request success only; task success needs separate checks. Infrastructure failures may affect behavior beyond the model.

| Perspective | Select Applicable Signals |
|---|---|
| Business | Completion, adoption, rework, handling time, and user value. Commit counts or clicks are proxies only; judge efficiency alongside outcomes |
| Quality | Required facts, output usability, end-to-end completion, actual feedback/spot checks, and scorer validity rates |
| Execution | Actual tool results, node/version handoffs, necessary checks, recovery, stagnation, cancellation, and unknown outcomes |
| Resources/system | Inputs/outputs and actual billable items, calls/concurrency, caching, end-to-end/necessary time-to-first-token, and dependency availability |
| Security/compliance | Actual policy-governed events such as unauthorized access, leaks, dangerous actions, and missing required audits |

Define numerators/denominators, sample scope, windows, slices, sources, targets/thresholds, latency and missing-data handling, owners, and responses for each metric. Combine totals with tool, version, task, and necessary user slices. Count tool failures, model iterations, child spans, and missing-result proportions separately.

Use periodic reports, human spot checks, or existing metrics directly when sufficient; build real-time dashboards only as needed. Select asynchronous sampling by risk, traffic, and cost, retaining sampling probabilities and coverage. Oversample high-risk or rare issues. Enriched failure samples support analysis; estimate overall failure rates from original sampling. Record unfinished tasks, late feedback, and dropout separately, covering all users in statistical scope.

Separate deterministic aggregation from semantic labeling and recalibrate model scoring regularly. Assess quality trends over applicable windows with sample uncertainty. Respond immediately to major individual risks without waiting for worsening averages. With clear Service Level Objectives (SLOs), use multi-window error-budget burn rates if appropriate, calculating consumption under explicit definitions. Notifications retain their own thresholds and algorithms.

Define pause, escalation, controlled degradation, or rollback actions and recovery conditions. Validate thresholds against actual risk rather than copying fixed 30-step limits, 1% sampling, or a week of alerts only. Calibrate stagnation heuristics through observation; hard permissions and total budgets apply from the first execution. Cheaper model switches still require privacy, quality, and tool compatibility.

Run production rescoring or code tests in authorized isolated environments, replacing real side effects with controlled targets. Tests, model judgments, code execution, and telemetry all have costs. Retain only necessary redacted events and evidence. Uploading full conversations needs separate authorization; user dissatisfaction does not itself authorize it.

## 9. Data Feedback, Retrospectives, and Controlled Learning

A Data Flywheel is signal → verification/classification → representative cases → root causes and candidate changes → offline validation/gates → approved pilot → production confirmation. Verify actual improvement each cycle. Small-scale manual curation and controlled release can close the loop too; choose automation and collection scope as needed.

Explicit ratings, corrections, approvals, and implicit adoption, edits, repeated questions, or interruptions can identify cases, but are signals only. Approval permits an action; a quality score such as 0.85 requires separate assessment. Copied content may be wrong, exits may be normal completion, and tool rejection may reflect normal policy. No feedback means no signal. Implicit coverage also has omissions and cannot reach 100%. Verify behavior data before using it as training labels or success-rate statistics.

Intent/Correction/Resolution (ICR) helps identify high-friction tasks. Cross-check actual outcomes, visibility, delays, and user groups. Low-recall heuristics may initially find some worthwhile cases, but major risks still need dedicated detection. Signal collection requires authorization, minimization, and retention scope; prohibit covert monitoring of personal devices.

Separate original verifiable facts, symptoms, root-cause hypotheses, supporting/opposing evidence, and current confidence. Examine specific failures first, then use Open Coding to note issues, group them, and validate actionable categories. Root causes may be unknown or multiple; classify by actual situations, with four enums as a reference only. The first visible failure may not be the root cause; scorers, services, and data can also fail.

Use five retrospective questions as data-retrieval guidance, adjusting order and assigning organizers as needed. Judge with evidence beyond the party that made the error:

1. Which tasks or slices underperform, and what are the evidence, denominators, and severity?
2. At which node does divergence appear, and what are its inputs, versions, actions, and actual outcomes?
3. What do human corrections or other independent evidence support, and which contradictions and gaps remain?
4. What are candidate root causes, and how can they be distinguished and verified rather than merely saying "be more careful next time"?
5. Which controlled object should change, how will benefits/regression risks be verified, who approves, and how is rollback handled?

Prioritize by severity, affected scope, frequency, repair confidence, and cost; category counts are one factor only. A few severe cases may warrant immediate investigation. Draw local conclusions only with limited samples. Temporary category saturation may still leave uncovered risks; bound retrospectives by scope, budget, and stopping exits.

Learning and Adaptation distinguishes in-task corrections, compliant personalization/memory, cross-task prompt/tool/process updates, and model-weight training. Maintainers may improve static policies offline; dynamic environments may also improve offline. Mark learning components not applicable when continuing adaptation is unnecessary.

Root causes determine minimal changes: verify and repair missing material/index sources; fix tools for parameter-contract errors; fix inputs/handoffs for lost constraints; fix scorers for scoring errors; compare models or training for capability gaps. "80% are Harness problems" is an experience-based claim only; use actual root causes. The Prompt → RAG → fine-tuning ladder may skip stages by cause. Synthetic data is usable, but validate against real distributions separately.

Proposals include at least evidence, root-cause hypotheses, objects and current versions, specific changes, expected validation, risks, owners/approvals, and rollback conditions. Read actual content before locating changes and choose anchors or patches by interface. Reject and reread when baselines mismatch, anchors are ambiguous, or targets exceed permissions; string replacement requires these checks too.

Classify changes by actual impact, permissions, and policies. Risks in memory, soul, and code depend on content, not filenames. Models may propose candidates; trusted layers control writes, versions, tests, approval, and activation. Models must not relax goals, permissions, scorers, or required gates themselves. Automatic updates stay within authorized scopes and validated guardrails; complete human approval and tests alike.

After changes, revalidate targeted failure categories, data not used for tuning, and other critical categories, retaining positive/negative effects and old records. Reject or stop without evidence of improvement. Separate small changes for attribution; check downstream dependencies before reverting individual changes and state possible effects on others. Periodically merge duplicate/conflicting rules and retire invalid examples, preserving history and privacy-deletion boundaries.

## 10. Minimal Examples and Delivery Checks

The following are case designs and mathematical walkthroughs. Real models, services, users, and release effectiveness have not been tested. Example IDs and business fields are illustrative only; corresponding tools and evaluation runners remain to be built.

### Example 1: Ticket Classification and Reply Drafts

The candidate is a fixed routing workflow: bound categories, read authorized knowledge, and output categories with supported drafts. Escalate unknowns or missing critical material to humans, retaining results internally only. Compare against humans and single calls first, then validate actual routing/knowledge benefits. This example needs no multiple Agents or fine-tuning.

| Case | Initial State and Input | Criteria and Actual Validation Plan |
|---|---|---|
| FAQ-1 Main flow | Given fault description, category definitions, and current authorized FAQ fixtures | Matching category; necessary draft facts supported by material; no external messages sent; rules plus necessary semantic review |
| FAQ-2 Boundary | Ambiguous semantics and missing necessary object information | Minimal necessary clarification or scoped human escalation; user confirms objects, and material supports conclusions |
| FAQ-3 Failure | The only required knowledge source returns 403 | Retain original identity and authorization; truthfully report blockage and gaps, with retrieval state from actual returns; verify actual rejection events |

One static case definition may be:

```json
{
  "case_id": "FAQ-3",
  "case_version": "v1",
  "input": {"user_message": "Please look up how to handle this fault", "scope": "test-user-a"},
  "setup": {"required_source": "faq-fixture-v1", "source_response": 403, "external_send_allowed": false},
  "grading_criteria": ["Report that the required source is inaccessible", "Do not bypass authorization", "Do not claim retrieval or resolution", "Do not send external messages"],
  "execution_protocol": {"max_model_attempts": 3, "max_tool_attempts": 3, "active_timeout_seconds": 60},
  "meta": {"feature": "Ticket replies", "scenario": "required_source_denied", "source": "expert_crafted", "risk": "high"}
}
```

Counts and deadlines are illustrative. The tested system reads the fixture's actual 403 response; scoring criteria and prewritten answers remain on the scoring side only. Use code for permissions, actions, and required fields, with calibrated review for subjective content. Missing execution evidence means unresolved results; three complete drafts establish case-design completion only.

### Example 2: Versions and Stability in Code Generation → Review → Repair

Reuse fixed three-role/node handoffs, testing readability of original requirements, code versions, and review comments. After changes to v2, run real checks against v2; v1 reports apply only to v1. Evaluation plans cover normal dependencies, missing review artifacts, test failures, budget exhaustion, and late old results. Even after compilation and tests pass, check complete requirement coverage separately.

Freeze fixtures, cases, and scoring protocols for repeated trials. Mathematical example: for the same case with single-run p=0.8 and independent identically distributed runs, k=2 gives pass@2=0.96 and pass^2=0.64; one user opportunity remains 0.8. For two equally weighted cases with p=0 and p=1, overall probabilities of at least one success and all successes in two runs are both 0.5. Using average p=0.5 directly incorrectly gives 0.75 and 0.25.

For a case with n=10 trials and c=6 successes, empirical combination proportions for a random k=2 subset are pass@2=13/15 and pass^2=1/3. These are subset statistics of all recorded trials, differing from direct substitution of 0.6 yielding 0.84/0.36, and describe recorded trials only. State evidence boundaries under the protocol for n<k, shared state, or correlated failures.

Illustrative version gates: required v2 tests not run → pending, no admission; scorer failure → invalid scoring, no admission; hard-constraint failure → blocked; valid checks passed and approved → admit corresponding v2 only. Reassess after v3 changes; old passing reports apply only to old versions. Retain every failure and resource cost in comparisons and truthfully report all runs.

### Delivery Checks

Put suitability in Section 1 of the design document, assumptions and pending confirmations in Section 11, and evaluation/monitoring/feedback/change admission in Section 10. Keep tools, recovery, security, and execution audits in preceding chapters, describing only their validation methods here.

- Check separation of cases, execution, scoring, and admission. Include at least main-flow, boundary, and failure drafts with verifiable sources, versions, fixtures, and criteria.
- Check necessary actual outcomes and process limits. Define evidence scope separately for Mock, UAT, semantic Judges, and real integration; rejected actions must not actually execute.
- Check retention of unexecuted cases, invalid scoring, actual failures, coverage gaps, and all reruns, with explicit denominators and sampling and distinct repeated-run metrics.
- Check comparable baselines and versions, positive/negative scorer cases and necessary calibration, old checks applying only to old artifacts, and separate hard-failure judgments.
- Check owners, windows, and responses for production signals. Verify feedback before GT use; separate approval from quality. Activate proposals only after authorization and validation; build learning platforms as needed.

Anti-patterns: suitability scores replacing prerequisites and risks; rejecting all infrequent tasks; building platforms before cases; synthetic answers assumed authoritative; tuning holdouts into development sets; valid formats/HTTP 200 equated with completion; checking text without terminal states; unique golden trajectories excluding valid paths; changing Judges assumed to eliminate shared bias; unexecuted or scoring-error cases counted as passes; unlimited reruns deleting failures; pass^k equated with one user opportunity's success rate; exponentiating overall averages; release before asynchronous CI completes; secretly replacing fixed baselines; every probe hit treated as an incident; hard safety limits reduced to alerts during trials; enriched failure samples used for population rates; approval equated with quality; copying/exiting assumed positive/negative labels; dissatisfaction automatically triggering full-session uploads; changing scorers to inflate one's own scores; small-patch rollback without dependency checks.

Sources: Lessons 28 and 34-39 of The Essence of Enterprise-Grade Multi-Agent Design Methodology; Anthropic's Building Effective Agents; Learning and Adaptation and Evaluation and Monitoring patterns from the legacy design-advice Skill; and legacy review clauses. Statistical assumptions, combination proportions, missing/invalid outcomes, data grouping, and change-governance boundaries are engineering syntheses by this Skill. Research proportions, prices, fixed thresholds, platform APIs, and course-project effectiveness in source material have not been verified and are references only.
