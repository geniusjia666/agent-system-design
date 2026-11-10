# Individual Agent Design

Use this reference in Step 3 of the main process and for single-agent internal loops in Step 4. Retain the architecture decision first, then define task units. This chapter lists multiple capabilities; select only those each node needs.

## Contents

1. Tailor Design Scope to the Architecture
2. Define Roles, Goals, and Operating Guidelines
3. Write Task Contracts and Acceptance Rules
4. Add Milestones and Progress Monitoring as Needed
5. Select Necessary Reasoning Approaches
6. Design an Execution Loop Driven by Real Feedback
7. Define Stop Conditions and Return Behavior
8. Define Tool and Context Interfaces
9. Two Design Examples
10. Delivery Checks, Anti-Patterns, and Sources

## 1. Tailor Design Scope to the Architecture

| Task Unit | Required Design in This Chapter | Add Only as Needed |
|---|---|---|
| Single model call | Inputs, output form, completion criteria, and failure return; explicitly specify one call and a bounded timeout | Persona stories, tool loops, milestones, and long-term memory |
| Model node in a fixed workflow | Node contract, required dependencies, acceptance, and failure destination; define retry limits if retries are used | Dynamic planning or an autonomous Agent identity |
| Autonomous single Agent | Responsibility boundaries, contract, reasoning approach, real-feedback loop, stop conditions, and tool/context interfaces | Every reasoning technique merely for completeness |
| Member of a multi-agent system | Apply the rules above according to its actual control mode, then explain why its responsibilities are separate | Packing the member's responsibilities, entire team orchestration, and shared state into this node |

A Task describes what must be delivered in this run; a role describes what the task unit is responsible for; the process describes who decides the next step. One role can execute multiple tasks, and one Agent can make multiple model calls.

## 2. Define Roles, Goals, and Operating Guidelines

Use Role, Goal, and Backstory as references for organizing prompts, filling them in as needed by each framework. Prefer operating guidelines over fictional background. If no background content is necessary, write "Not applicable"; describe only real experience.

| Item | How to Write It | What to Avoid |
|---|---|---|
| Role | Responsible domain, scope of work, and delivery recipient, such as "read-only incident investigator" | Replacing responsibilities with "top expert," or assuming a role name guarantees correct knowledge |
| General goal | How to choose among permitted actions, such as "verify evidence first; do not fill gaps with guesses" | Conflicts with the current task goal, output requirements, or permission restrictions |
| Operating guidelines | When to verify, when to clarify, how to handle uncertainty, and applicable business rules | Long persona stories, unsourced knowledge, and contradictory instructions |
| Capability boundaries | What may be read, produced, or modified, and what is prohibited | Merely saying "operate carefully," or replacing actual permission controls with prompts |

Distinguish a general goal from the current task goal: the former is a preference, while the latter is a concrete deliverable requirement. They must be compatible. Resolve definition conflicts first; humans determine hard constraints.

Fixed business steps, approvals, acceptance, and permission restrictions can and should be specified explicitly. "Let the model choose the path" applies only to authorized autonomous portions; still state operating rules clearly. Put task-specific and potentially conflicting procedures in the task contract, and keep reusable roles limited to general content.

## 3. Write Task Contracts and Acceptance Rules

First fill in the Agent definition table in the existing design document, reusing the same template.

| Contract Item | Required Explanation |
|---|---|
| Current goal | Deliverable, recipient, and supported scope; define the endpoint as a concrete result, replacing vague phrases such as "analyze deeply" |
| Inputs | The user's original goal and hard constraints, material sources and formats, and required dependencies; identify missing inputs that prevent starting |
| Outputs | Fields or document structure needed by the consumer, field meanings, required evidence, and artifact locations |
| Completion criteria | What counts as completion, who checks it, and what happens if checks fail |
| Stop conditions | At least a maximum round count or total time limit, plus timeouts for external calls; define returns when blocked or over limits |
| Prohibited actions | Specific bans on unauthorized reads/writes, goal changes, fabricated facts or tool results, and similar actions |

Choose output structure for the consumer: Markdown sections may suit human reports; define fields, types, and required items for system consumers. Use JSON for natural-language replies only as needed. A single task should use only the relevant parts of the multi-agent handoff contract.

Complex artifacts may be saved and passed by reference, but specify how recipients can read them. Claim "the file has been generated" only when an accessible artifact exists.

### Turn Criteria into Checks

| Check Category | Examples | Checking Mechanism |
|---|---|---|
| Format and structure | Required fields, enums, length limits, and mandatory Markdown sections | Host code, JSON Schema, Pydantic, or document checks |
| Business requirements and facts | Categories belong to the allowed set, conclusions agree with citations, and changes pass required tests | Business rules, tests, and source checks; use an agreed model review or human reviewer when fully automatic judgment is unavailable |
| Deliverable usability | Files exist and are readable, and downstream systems can parse outputs | Actual read validation by the host or recipient |

Field descriptions help the model understand quality requirements; separate checks enforce those requirements. Passing a Schema establishes only that its declared structural constraints pass. Factual correctness, business-goal completion, and system-operation success require separate checks.

Define criteria and reviewers for subjective requirements. A model's claim that it "meets the requirements" is only a signal; the checking party performs acceptance separately. Prefer direct rules or tests where possible; simple tasks do not need a review Agent.

## 4. Add Milestones and Progress Monitoring as Needed

Goal setting and monitoring support long tasks, multi-stage delivery, or tasks where deviations must be detected. Simple tasks need only completion criteria.

1. Break the goal into acceptable artifacts, with each milestone representing a stage deliverable. Keep micro-actions such as "think once, search once, click once" inside milestones.
2. Define inputs, deliverables, and checking criteria for each milestone. Mark it complete only after checks pass.
3. Record completed work, current work, remaining work, and blockers. Base progress on artifacts and check results; call counts serve only budget accounting.
4. If the work deviates, search or processing strategies may change, but goals, acceptance criteria, and permissions remain unchanged. Ask the user to confirm any necessary change to those boundaries.

Let the existing host handle monitoring; create additional roles, dashboards, or scorers only as needed. Execution records need only support current-task recovery, acceptance, and later diagnosis. See the evaluation chapter for detailed monitoring design.

## 5. Select Necessary Reasoning Approaches

| Approach | When to Use It | Design Boundaries |
|---|---|---|
| Direct answer | Sufficient inputs and a simple result; one processing step is a candidate for meeting the criteria | Complete in one step, without a loop |
| Step-by-step reasoning (Chain-of-Thought) | Multi-step analysis, calculations, or constraint derivation from available material | Preserve supporting evidence and necessary calculations; internal chains of thought need not be disclosed |
| Alternating reasoning and action (ReAct) | External evidence is needed, and the next step depends on actual tool feedback | The host executes tools; observations come from real results |
| Plan then execute | Multi-step tasks have dependencies and require milestones to be established first | Revise only when feedback invalidates the plan; leave the full planning pattern to the orchestration chapter |
| Compare multiple candidates (Tree-of-Thought) | Evaluation criteria are clear, and comparing approaches may add value | Define candidate count and budget; enable according to criteria and expected benefit |
| Feedback-based correction (Self-Correction) | Tests, validation, or review identify specific errors | Correct with error feedback and bounded attempts; validate whether corrections improve results |

Choose according to task needs. Combine Chain-of-Thought, ReAct, Tree-of-Thought, and Self-Correction only as needed; scores do not depend on the number combined. Read actual material when facts need confirmation.

Auditable records consist of input evidence, tool requests and actual results, key decision summaries, artifacts, and check results. Internal reasoning need not be retained. Explain conclusions externally as needed; disclosing chains of thought is not a design or acceptance requirement.

Use intermediate storage only when it has practical value for saving artifacts, checking nodes, or recovering tasks; storage tools serve only these business needs.

## 6. Design an Execution Loop Driven by Real Feedback

ReAct's key is "decide the next step from real observations"; text labels are only one implementation. Use the following logic independently of specific framework APIs:

1. The host reads the task contract, checks inputs and permissions, and initializes progress and this task's counters or deadline.
2. Before every model or tool call, check cancellation, blockers, and resource limits. Only the host adjusts budgets.
3. Using the original goal, necessary material, and actual historical results, the model proposes a tool request, a clarification question, or a candidate result.
4. The host first validates a tool request's name, parameters, and permissions, pausing for required approval. Do not execute the tool if validation or approval fails.
5. The host actually calls the tool and truthfully records success, empty results, errors, or timeouts. The model continues from real results; planned calls are only plans until executed.
6. Send candidate results to the agreed checking mechanism. Mark completion only on passing; otherwise, return specific issues to the model. Whether to generate again depends on remaining budget and error type.
7. Pause or end when clarification is needed or work cannot continue. Return existing results, gaps, and who must do what next.

Structured Tool Calling or Function Calling requests may separate model requests from actual execution. Text-based ReAct Stop Tokens are parsing mechanisms in some implementations; use them as needed, while the host separately validates permissions.

After "a tool request was generated," check whether the tool executed successfully. After "the tool returned success," check whether the task passed acceptance. Only actual results count as environment feedback; claim validation only after pages have actually been read or tests actually run.

## 7. Define Stop Conditions and Return Behavior

Distinguish the end of the current model output, task success, pausing, and fallback termination. `Final Answer` or a stop marker only means the model stopped generating for this call; check task completion separately.

| Trigger | Handling Rule |
|---|---|
| User cancellation, denial of permission, or denial of required approval | Stop new operations and explain why; restrictions remain effective |
| Total time limit or hard resource budget exhausted | Stop model and tool calls; the host returns existing artifacts and the termination reason, truthfully marking conclusions as incomplete |
| Candidate result passes all mandatory checks, with none of the hard stops above triggered | Mark success and return immediately, even if the final allowed round has just been used |
| Result fails the criteria and model rounds are exhausted | End and return completed portions and gaps; explain the blockage if nothing usable exists |
| Consecutive actions yield no new evidence, failures repeat, or key inputs are missing | Apply predefined correction, clarification, or stopping rules; this task's limits continue accumulating |
| Human information or confirmation is needed | Pause and submit the question; define waiting timeout and recovery, and record the task as incomplete while waiting |

Define what counts as a round. This Skill's examples count "one attempted model call" as one round. Final-answer generation, format correction, and regeneration all count toward the same task total. Give tool retries separate limits while also charging them to the task budget. If a framework counts differently, document the mapping during implementation.

Define at least a maximum round count or total time limit. Tool calls and other external waits also require bounded timeouts. The host enforces limits; a prompt's "try at most N times" only explains them. Determine budget values from the task and experiments; the course's 100 rounds are a demonstration value, not a default.

When structured returns are needed, reuse existing conventions: `SUCCESS` for success, `PARTIAL` for usable but incomplete results, and `BLOCKED` when work cannot continue. Use `remaining` for partial completion and `blockers` for blockage. Replies to people may express the same meanings in natural language; include fields as needed.

For a single Agent, this chapter only determines triggers and destinations. See the reliability chapter for full implementation of error classification, backoff retries, idempotency, and checkpoint recovery; reuse its state and recovery design here.

## 8. Define Tool and Context Interfaces

| Interface | What to Define at This Step | What to Expand Later |
|---|---|---|
| Tools | Required capabilities, when to call them, permitted read/write scope, approvals, and key evidence in results | Tool descriptions, parameters, misuse prevention, and MCP or Skill integration |
| Context | Original goal, hard constraints, required dependencies, latest actual results, and current progress | On-demand loading, pruning, compaction, and memory governance |
| Persistence | Whether artifacts or progress must be saved and who reads them afterward; write "None" when saving is unnecessary | Checkpoint recovery, version management, and shared-state mechanisms |

Retain only information relevant to the current task. Give each node only the history and tool definitions it needs. Enable memory as needed; reuse across tasks requires explicit needs and governance rules.

## 9. Two Design Examples

The following are design candidates. Their budgets are demonstration configurations, not empirically measured performance, and are provided for illustration only.

### Example 1: Classifying Customer-Service Tickets from Supplied Material

| Item | Design |
|---|---|
| Control mode | Single model call, without an autonomous loop |
| Responsibilities and inputs | Receive the original ticket and supplied category definitions; classify only. Replying to the customer and modifying the ticket are outside the role's responsibilities |
| Output structure | `category` is an allowed business category or "Human judgment required"; `reason` is a brief classification rationale |
| Completion criteria | All required fields are present and the category is valid; evaluate actual classification accuracy on the evaluation set. Passing format checks establishes structural correctness only |
| Reasoning, tools, and memory | Direct classification or necessary step-by-step analysis; no tools, long-term memory, or persona story |
| Stopping and failure | Demonstration configuration: 1 model call with a 10-second timeout; hand format failures or timeouts to a human, retaining a total of 1 call |

Check classification correctness with the evaluation set, not model self-scoring. This example does not need reflection, tools, or progress monitoring; their absence is a reasonable design choice.

### Example 2: Read-Only Incident Investigation Agent

| Item | Design |
|---|---|
| Role and general goal | Read-only incident investigator; verify evidence first and retain uncertainty when confirmation is unavailable |
| Current goal | Investigate one error for a specified service, environment, and time range, producing confirmed facts, candidate causes, and next validation actions. A root cause may be found, or only candidates may remain |
| Inputs | Original error text, service and environment identifiers, time range, read-only material entry points, and permitted scope; clarify missing service or time range first |
| Output structure | `facts`, `hypotheses`, and `next_checks`; facts link to real sources, hypotheses are marked separately, and blockers or remaining work are filled in according to return status |
| Completion criteria | Consistent scope, complete required fields, facts matching actual sources, hypotheses distinguished from root causes, and concrete next actions. The host checks what existing rules can verify; semantic judgment follows the agreed review process |
| Reasoning and loop | ReAct; choose supplementary queries from actual log or document results. Investigation is read-only; service-configuration changes and repairs are outside permissions |
| Tools and context | Read-only log and document queries; retain the original goal, key results, and remaining gaps, using only session-local state |
| Stop configuration | Demonstration configuration: at most 6 model calls or 120 seconds, whichever is reached first limits further execution. External requests wait at most 15 seconds and must not exceed the remaining total time |
| No progress and blockers | Demonstration configuration: investigate the reason after 2 consecutive queries yield no new evidence; end if permitted alternative queries also cannot advance the task. Return blocked directly if permissions fail or required material does not exist |

Possible execution trace: round 1 reads logs; round 2 queries related documents because evidence is insufficient; round 3 submits a sourced report, passes the agreed checks, and ends. If the model still requests additional queries after round 6, the host stops model calls, does not start round 7, and returns existing facts and remaining work. If no usable result exists, return blocked.

## 10. Delivery Checks, Anti-Patterns, and Sources

Write responsibilities, inputs and outputs, completion criteria, reasoning approaches, and stop conditions into Section 4 of the design document; single-agent loops into Section 7; and tool and context interfaces into Sections 5 and 6 respectively. Reference the same definition of a constraint across chapters to maintain consistency.

- Check that each task has a concrete deliverable and does not mix general goals, task endpoints, and permissions.
- Check who verifies mandatory criteria and whether structural validation, model self-scoring, or stop labels are being treated as business success.
- Check that model calls, format correction, tool waits, and human waits are all governed by the defined limits.
- Check that blockage and limit exhaustion return actual gaps while retaining the original goal and necessary evidence.
- Check that selected capabilities are genuinely needed. Configure loops for fixed nodes only as needed; auditability rests on evidence and results, not disclosure of internal chains of thought.

Anti-patterns: vague expert personas; conflicts between Goal and Task; missing completion criteria; treating Schema success as factual correctness; fabricated tool observations; treating `Final Answer` as success; adding storage tools merely to fill reasoning rounds; resetting budgets through retries or replanning; adding every reasoning pattern to improve a score.

Sources: Anthropic's Building Effective Agents; Lessons 02, 07, 08, and 09 of The Essence of Enterprise-Grade Multi-Agent Design Methodology; and the "Goal Setting and Monitoring" and "Reasoning Techniques" patterns from the legacy design-advice Skill. Stop priorities, counting conventions, optional Backstory, and example budgets are engineering syntheses by this Skill, not verbatim source conclusions or empirically measured results.
