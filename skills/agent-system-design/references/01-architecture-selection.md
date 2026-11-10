# Architecture Selection

Use this reference in Step 2 of the main process. First determine whether a large language model is needed, then choose the control mode, and finally determine whether multiple Agents are necessary. Task complexity, step count, and tool count are only signals; assess the need for multiple Agents separately.

## Contents

1. First Rule Out Cases That Do Not Need an Agent
2. Assess Control Mode and Collaboration Structure Separately
3. Describe Requirements with C.U.P., Not Mechanical Scores
4. Choose Incrementally from the Simplest Viable Approach
5. When Splitting into Multiple Agents Is Worthwhile
6. Performance Constraints and Hybrid Architectures
7. Write a Reviewable Architecture Decision
8. Boundary Cases
9. Anti-Patterns and Sources

## 1. First Rule Out Cases That Do Not Need an Agent

Check the following table and prefer the simpler approach when a condition applies.

| Situation | Preferred Approach |
|---|---|
| Rules are clear, and ordinary code, SQL, or an existing system can meet the criteria | Use ordinary code, explain why, and end the Agent design process; Agent sections need not be filled in |
| All input material is available, and the task only requires classification, extraction, rewriting, or summarization | Try a single model call first; use code to retrieve material beforehand if needed |
| Steps, branches, and failure handling can be defined in advance | Use a fixed workflow, even when there are many steps |
| The original goal, evaluation criteria, or tool permissions are unclear | Clarify first; obtain missing information when it is insufficient, and use autonomous exploration only for genuine unknowns |
| Error consequences are unacceptable, and critical operations cannot be verified or intercepted | Retain human judgment and use the model only as an assistant; adding Agents cannot solve this problem |

A single call may include retrieval, examples, and structured output. A fixed workflow may include conditional branches, parallel steps, and bounded retries; execution remains controlled by code even with these capabilities.

## 2. Assess Control Mode and Collaboration Structure Separately

### Control Mode: Who Decides the Next Step

| Mode | Decision Criterion | Applicability Signals |
|---|---|---|
| Single call | The model generates a result once; code handles preprocessing and postprocessing | Sufficient inputs are available, and one processing step can meet the criteria |
| Fixed workflow (Workflow) | Paths, branching rules, and loop boundaries are defined in code in advance | Processing steps and exception paths can be listed clearly |
| Model-directed autonomous decisions (Agent) | The model selects its next action from observations and may revise its plan | The next step in search, diagnosis, or exploration is difficult to predetermine |

A model may classify the input and let code select a predefined branch; this can still be a workflow. A model may generate a plan once and let code execute it; this may also remain a workflow. The criterion is whether decisions continue to be made from feedback during execution.

### Collaboration Structure: One or Multiple Task Units

| Control Mode | Single Task Unit | Multiple Task Units |
|---|---|---|
| Fixed workflow | Call models or tools along a fixed path | Execute multiple task roles in a fixed sequence or in parallel, including multiple LLM Agents in a framework |
| Model-directed autonomous decisions | One Agent handles the task autonomously | Multiple Agents divide the work; overall orchestration and each Agent's internal execution may use different control modes |

This Skill retains the four common labels Prompt, Workflow, Single Agent, and Multi-Agent. They describe different dimensions: Workflow describes control mode, while Multi-Agent describes collaboration structure. Both can apply at the same time.

State both dimensions in the design document, for example, "Workflow: fixed sequence, 3 task roles" or "Single Agent: local autonomous decisions, with an outer workflow controlling execution." Define multiple model nodes in a fixed workflow through task contracts; configure planning, memory, and autonomous loops as needed.

Sources differ in how broadly they use the term Agent. This Skill permits describing multiple LLM Agents using framework terminology, but their autonomous decision boundaries must be stated. Autonomous collaboration capabilities depend on actual decision-making behavior; role names are only names.

## 3. Describe Requirements with C.U.P., Not Mechanical Scores

C.U.P. is an architecture-selection heuristic from the course: Complexity, Uncertainty, and Performance Constraints. It is a qualitative framework, not a score or threshold from which an architecture can be calculated directly.

| Dimension | Questions to Answer | Effect on Selection |
|---|---|---|
| Complexity C | Are inputs multi-turn, multimodal, or very long? Which tools and data are required? How many steps and dependencies are there? | Helps decide whether to process the task in steps; other dimensions are still needed to determine whether an Agent is necessary |
| Input uncertainty U | Do request types and input quality vary? Can the supported scope be restricted or inputs classified first? | Prefer clarification, preprocessing, or routing before increasing autonomy |
| Process uncertainty U | Can the next step be predefined? Must new evidence change the strategy? | The primary signal for deciding whether model-directed autonomous decisions are needed |
| Goal uncertainty U | What counts as completion? Can output quality be checked? | Define evaluation criteria first; clarify ambiguous goals, and assess Agent count separately |
| Performance constraints P | What are the limits for latency, per-run and total cost, call volume, and effective context budget? | Determines whether candidates are viable and must be considered during selection |

The three uncertainty dimensions come from the course's discussion of "business entropy." This Skill uses them as qualitative questions, does not calculate entropy, and does not derive Agent count from Ashby's law.

| Requirement Characteristics | First Approach to Try | Conclusions That Do Not Follow Directly |
|---|---|---|
| Simple task with a clear path | Ordinary code or a single call | Add reflection, planning, or tools as needed |
| Many steps with a clear path | Fixed workflow | Step count is only a signal; assess multiple Agents separately |
| The next step must be decided from feedback | A single Agent or a local Agent within a workflow | Even with open-ended inputs, the execution path may remain fixed |
| Many dependencies and an uncertain path | Check the single Agent's bottlenecks before considering a split | Even with high C and high U, compare against a single Agent first |

## 4. Choose Incrementally from the Simplest Viable Approach

1. Use ordinary code or an existing system as the baseline. Stop adding complexity when it meets the requirements.
2. If language understanding or generation is needed, try a single call first. Check that inputs are complete and outputs can be validated.
3. If a single call is insufficient but fixed steps can be defined, choose a workflow; add only steps that address known failures.
4. If only one part requires exploration based on feedback, confine the autonomous Agent to that part and let code control the rest of the process.
5. Start autonomous tasks with one Agent by default. Consider multiple Agents only when there are specific reasons to split, as described in Section 5.
6. Check candidates against performance constraints and record benefits, costs, and unvalidated items. If constraints cannot be met, narrow the scope, degrade safely, or retain the manual process.

Without experimental results, an architecture may be proposed as a candidate, but the bottleneck pending validation and the smallest validation action must be stated. Describe design walkthroughs separately from measured performance.

## 5. When Splitting into Multiple Agents Is Worthwhile

Split to solve a specific problem that is difficult for one task unit to handle. The isolation needs below are only candidate reasons; compare against simpler approaches before splitting.

| Candidate Reason | Simpler Approach to Try First | Signals That a Split May Be Worthwhile |
|---|---|---|
| Different context or memory needs | On-demand retrieval, cleaning tool results, compaction, and structured notes | Subtasks require independent exploration, their details crowd out the main task's context, and they can communicate through artifact handoffs |
| Different tools or working methods | Tool grouping, on-demand loading, and Skill reuse | Simultaneously exposed tools or different instructions persistently cause incorrect selections or conflicts, and isolation can clearly improve this |
| Different permissions | Tool-layer permission controls and separation of reads from writes | Research, execution, and validation need different permission boundaries, and separate execution identities have practical value |
| Different concerns in generation and review | Prefer tests or deterministic validation; use another review call if needed | Independent review context and task contracts add value; the name "reviewer" is not a reason by itself |

Check whether subtasks can be completed independently, whether their inputs and outputs are clear, and whether handoffs may lose critical information. If subtasks depend closely on the same real-time state, consider a single Agent or an explicit shared-state workflow first.

Parallel execution and multiple Agents are different concepts. Code can call fixed, independent subtasks in parallel; consider splitting into Agents further only when role, context, or permission isolation is also needed.

When integrating the legacy coordinator's quick complexity assessment, retain only the principles "handle simple tasks directly, investigate cross-module tasks first, and parallelize independent problems." File and module counts only help estimate reading effort; decide whether to create Agents from isolation needs instead.

## 6. Performance Constraints and Hybrid Architectures

| Check | What to Record |
|---|---|
| Latency | The longest dependency chain, model and tool calls, validation, retries, and human waits; dependency-chain duration remains even after parallelization |
| Cost | Model inputs and outputs, tool fees, retries, and reviews across all branches; parallelization usually does not change total call cost |
| Context | Information and tool definitions actually needed at each step; calculate each load from its needs, not the total number of files |
| Controllability | What the model can decide autonomously, and which operations are constrained by code or require human review |

Estimate first, then measure with representative inputs. If explicit hard constraints exist and estimates exceed them, mark the approach infeasible. If measurements or constraints are missing, mark the relevant items as pending validation or to be confirmed; provide only measured values or explicitly labeled estimates.

If constraints cannot be met, options include restricting the supported scope, preparing material in advance, using a fixed workflow, enabling an Agent only locally, or handing the task to a human. Narrowing capability boundaries requires user confirmation and an explicit statement of unsupported cases.

A hybrid architecture is a "workflow backbone + local autonomous decisions." For example, a diagnosis task collects monitoring data and logs through fixed steps, then lets a single Agent choose supplementary checks within a time-limited, read-only scope. On timeout, return existing evidence to a human; a human decides high-risk remediation.

Hybrid is a combination approach, not a fifth tier beyond the four labels. Address latency, context, and safety issues separately; increasing Agent count does not resolve them.

## 7. Write a Reviewable Architecture Decision

Write the decision in Section 2 of the existing design document, reusing its fields and following the table below:

| Field | Required Content |
|---|---|
| Selected tier | Common labels, control mode, task roles or Agent count, and the specific location of autonomous decisions |
| Selection rationale | Evidence about paths, dependencies, or isolation tied to requirements; include only C.U.P. factors that affect the decision |
| Why not choose a simpler tier | Specific shortcomings of simpler candidates; if the simplest approach is already selected, write "No increase in complexity needed" |
| Performance-constraint check | User constraints, estimation or measurement evidence, and whether they are met; mark unknowns as to be confirmed or pending validation |
| Main risks | Actual risks, such as unsupported inputs, handoff losses, or autonomy exceeding its boundaries, and fallback directions |

Do not force every design to compare all combinations, list all 21 patterns, or select a framework. Just establish why the current approach is necessary relative to simpler candidates.

## 8. Boundary Cases

| Scenario and Prerequisites | Candidate Selection | Key Rationale |
|---|---|---|
| Calculate prices or validate required fields according to established rules | Ordinary code | No language understanding or generation task must be handled by a model |
| Text and category definitions are available; only classification is needed | Single call | One processing step is a candidate for meeting the criteria; reflection, planning, and multiple Agents are unnecessary |
| Classify tickets and answer fixed FAQs with clear categories and knowledge sources | Fixed routing workflow | Request content varies, but processing paths are defined; hand unknown categories to a human |
| The same customer-service assistant must query different systems over multiple turns and choose its next step from results | Single Agent, with external permission and escalation rules retained | Process uncertainty justifies autonomous decisions; the name "customer service" does not determine architecture |
| Generate, review, and refactor code in a fixed order | Fixed workflow with 3 task roles or LLM Agents | A fixed sequence may still use multiple Agents; refactoring must read both the original code and review comments |
| Extract and aggregate many independent documents using a fixed format | Parallel workflow | Many documents can be partitioned; introduce autonomous Agents or a coordinator only as needed |
| Cross-domain research with uncertain search paths and separate in-depth exploration | Multi-Agent candidate | Independent exploration and context isolation may add value; handoff quality and budget still need validation |

Example architecture decision for a code pipeline:

- Selected tier: Workflow; code orchestrates 3 task roles in a fixed sequence, with no autonomous planning loop.
- Selection rationale: generation, review, and refactoring have a known order; the review task uses independent inputs and evaluation criteria, with outputs handed off through contracts.
- Why not choose a simpler tier: requirements explicitly call for independent review and targeted changes, which a single generation call cannot deliver; whether quality exceeds a single call has not been measured.
- Performance-constraint check: at least 3 model calls, with validation and retries adding overhead; user budget is to be confirmed, and actual latency is pending measurement.
- Main risks: unreliable review comments or loss of original constraints during refactoring; retain the original goal, generated code, and review comments as refactoring inputs, then run executable validation on the result.

## 9. Anti-Patterns and Sources

- Choosing multiple Agents directly from "high complexity and high uncertainty" without checking specific single-agent bottlenecks.
- Adding free-form planning to an existing fixed process, expanding execution paths that could otherwise remain restricted.
- Adding Agents because inputs are open-ended or goals are vague, skipping clarification, routing, and evaluation-criteria design.
- Giving every step a persistent role, memory, and toolbox, or mechanically dispatching Agents by file count.
- Quietly dropping user requirements to reduce cost, or presenting estimates and scenario walkthroughs as measured results.
- Adding unnecessary patterns to appear complete, or assigning low design scores because tools or reflection are absent.

Main sources: Anthropic's Building Effective Agents; Google ADK's Sequential template workflow agent; Anthropic's Effective Context Engineering for AI Agents; Lessons 01, 04, 05, and 25 of The Essence of Enterprise-Grade Multi-Agent Design Methodology; and the legacy coordinator's quick complexity assessment.

The two-dimensional selection approach, candidate validation, and isolation assessment above are engineering syntheses by this Skill. The course's C.U.P. and "entropy" are qualitative references only. Its statements that "every Agent must make autonomous decisions" and that high C and high U directly imply multiple Agents apply only within the course's context; this Skill uses its own definitions.
