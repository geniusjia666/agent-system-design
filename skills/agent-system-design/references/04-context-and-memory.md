# Context and Memory

Use this reference when designing the information environment in Step 3 of the main process, or when reviewing long tasks, multi-turn conversations, cross-session reuse, retrieval augmentation, and excessive context. First determine which information must be retained, where to obtain it, and when to update it; choose techniques afterward. Enable long-term memory as needed.

## Contents

1. Distinguish Context, Task State, Long-Term Memory, and Knowledge Sources
2. Design Effective Budgets and Startup Loading
3. Assemble Information on Demand Throughout the Lifecycle
4. Choose Pruning, Compaction, Notes, or Sub-Agents
5. Compact Safely and Recover Tasks
6. Design Long-Term Memory Admission and Governance
7. Choose Retrieval Methods and Evidence Rules for the Task
8. Prepare a Readable Information Environment for Agents
9. Two Minimal Design Examples
10. Delivery Checks, Validation, and Anti-Patterns

## 1. Distinguish Context, Task State, Long-Term Memory, and Knowledge Sources

Context Engineering selects the smallest sufficient set of high-signal information before each model call. Context Rot refers to possible declines in information recall or use accuracy in long contexts; the model may not reliably use everything that fits in its window.

| Information Layer | Purpose | Common Confusions |
|---|---|---|
| Current context | Instructions, user requests, necessary history, tool definitions, and results for this call | All application data; all information must remain resident |
| Session and task state (Session / State) | Current goals, parameters, progress, artifacts, pending actions, and remaining budget; persist as needed | Stable knowledge across tasks; assuming saved state guarantees exactly-once actions |
| Long-term memory (Memory) | Reuse confirmed preferences, decisions, facts, or experience across sessions | All chat history; instructions automatically having the highest priority |
| Authoritative knowledge and evidence | Current code, business data, formal documents, and verifiable operation records | Model summaries; assuming the previous answer is inherently trustworthy |

Long context expands information visible in this call; persistence handles saving and recovery; retrieval provides on-demand access; memory governance determines admission and correction. Each has a distinct role. Typical request-based LLMs see only the inputs supplied for each call, so the application must provide history, state, or read entry points.

For one-shot classification, task inputs and necessary examples suffice. Multi-turn clarification may need only session state; interrupted long tasks may need only task notes. Design long-term memory only when reuse across tasks is explicitly needed. When retrieving formal knowledge bases, save user memory separately only as needed.

## 2. Design Effective Budgets and Startup Loading

### Effective Budget

Record actual limits of the model and interface, reserving capacity for output and next actions. The budget includes system instructions, the current request, history, tool definitions, retrieval results, and interface-counted consumption of inputs such as images. Chat text is only one part.

```text
Input budget for this call = min(interface input limit, model context limit - reserved output) - safety margin
```

If the interface specifies separate input and output limits, handle them separately according to its actual counting rules. The safety margin covers estimation errors and expected growth. Prefer available token-counting interfaces or the corresponding tokenizer; rough character estimates are only for warnings with a margin.

Meet the needs of essential instructions, the current goal, hard constraints, and critical evidence first; allocate remaining budget to optional history and retrieval content. If insufficient budget remains, remove irrelevant inputs, read in segments, or choose long-task strategies. If even essential information cannot fit, narrow the task, switch to a suitable interface, or return blocked while preserving constraints in full.

Set soft triggers from task traces, information retention, latency, and cost; enforce hard limits before calls. There is no universal "40% inflection point" or optimal compaction ratio for all models. Long-context quality degradation is a risk, not a law that "each piece of information receives `1/N` attention." Verify pricing and latency against actual service rules; attention computation does not imply "the bill quadruples."

### Startup Loading (Bootstrap)

| Load First | Load on Demand or Not at All |
|---|---|
| Current goal, acceptance criteria, and trusted behavioral constraints | All conversation history, the full knowledge base, and all tool instructions |
| Necessary task state, original requirements, and dependency entry points | Unrelated project state, other users' profiles, or useless persona stories |
| Rules, indices, and a few representative examples needed by the current role | All boundary examples or all memory bodies |

Use clear sections to separate instructions, user requests, and reference data. Identity, user profiles, working rules, and memory indices are optional information categories that may use any storage medium; load the relevant content only for personalization or memory needs.

Navigation includes topics, purposes, trusted sources, necessary versions or times, and actual readable entry points. Indices also consume budget, so limit them to currently relevant items. Startup cost grows as file, Skill, or topic counts grow.

## 3. Assemble Information on Demand Throughout the Lifecycle

| Timing | Action | Required Boundaries |
|---|---|---|
| Start or resume a task | Load goals, hard constraints, the current request, and necessary state | Validate session, task, and access scope; distinguish old records from new instructions |
| Before every model call | Select relevant information, deduplicate, check budgets, and prune or compact if needed | Current requests take precedence over old summaries; preserve message-protocol integrity |
| After tool or retrieval results | Check actual status, relevance, size, sources, and continued-read entry points | Distinguish empty results, failures, truncation, and unknown outcomes; see the tool chapter for result formats |
| At milestones or before interruption | Save necessary progress, evidence, unresolved items, and remaining budget | Record only actual completions; external actions and state saving are separate transactions |
| At task end or memory admission | Assess cross-task reuse value and update under admission rules | Ordinary delivery does not need a memory Agent; report write failures truthfully |

Just-in-time Context retains lightweight references and reads bodies only when the task needs them. It differs from blind exploration and may coexist with prior retrieval. Prefetch stable material to reduce latency; read dynamic code and pages from current state. Both approaches can be combined.

For current code, files, configuration, or live business state, rely on actual reads; old notes are entry points only. Absence from an index, default search results, or summaries means only that the information has not yet been found. On finding a gap, try alternative terms or related entry points within authorization and budget; state insufficient evidence if it remains unavailable.

## 4. Choose Pruning, Compaction, Notes, or Sub-Agents

| Strategy | When to Prefer It | Retention and Costs |
|---|---|---|
| Pruning | Duplicate, obsolete, or already-used tool bodies consume space | Retain key facts, reread entry points, and evidence still needed for precise checks |
| Compaction | Extensive back-and-forth requires continuity with earlier history | Extract goals, constraints, decisions, unresolved items, and sources; incurs information loss and summary-call cost |
| Structured Note-taking | Iterative development, clear milestones, or continuation across contexts or restarts | Save progress and dependencies externally for later reads; synchronize with actual state |
| Independent sub-Agent context | Independent research or analysis requires extensive exploration, can hand off bounded artifacts, and simpler methods are insufficient | The main Agent keeps the plan; sub-Agents return conclusions, evidence, and gaps. Adds calls, aggregation, and coordination cost |

Remove redundancy first by default, then choose compaction or notes according to the task. Split Agents only when isolation has clear benefits. The three long-task strategies can be combined as needed; longer context calls for context management, while multiple Agents require separate justification.

Before pruning, extract still-useful IDs, numbers, sources, versions, and action states, retaining reread references. Preserve acceptance evidence according to its use, not message age. Repeated errors may be merged, but retain failed attempts and causes that affect later choices.

Prefer client-supported context-management mechanisms. When processing history yourself, protect tool calls, corresponding results, and other linked blocks according to the actual interface. Remove completed call groups as a whole or use interface-supported result placeholders. Handle calls and results as pairs; verify whether splitting by user turns is safe in the specific framework.

Sub-Agent inputs must include task goals, necessary original material, constraints, permissions, and budgets. Returns should include conclusions, sources, artifact references, and unresolved questions; summaries are only part of the return. Independent context isolates information only; design permission isolation separately. See the multi-agent chapter for complete dispatch, shared-state, and communication design.

## 5. Compact Safely and Recover Tasks

### Minimal Compaction Process

1. Select completed history segments suitable for compaction. Retain the current request, unfinished calls, and constraints that must remain verbatim.
2. Save evidence and records requiring precise traceability to authorized, readable locations first. If saving fails, retain the only copy and state that compaction is lossy.
3. Generate a structured summary, checking recall of key content before removing redundancy. Use a separate summary model or background service only as needed.
4. Check that the summary retains original goals, permissions, numbers, versions, action states, and unresolved items; assemble new context according to the message protocol.
5. Recheck that source state has not changed before replacement, and continue only after budget checks pass. On failure, retain usable state and retry, degrade, or return blocked within budget.

| Summary or Progress-Note Field | Content |
|---|---|
| Goals and constraints | Current task, success criteria, and user-confirmed boundaries; mark old goals separately as historical |
| Facts and decisions | Confirmed conclusions, evidence, and necessary times or versions; distinguish observations, user statements, and judgments pending validation |
| Progress and artifacts | Actual completed work, passed checks, artifact locations, and consumed or remaining task budget |
| Unresolved items | Unresolved questions, blockers, failures affecting later strategy, next steps, and dependencies |
| Action status | Not yet executed, executing, confirmed complete, failed, or outcome unknown; approval scope and current confirmation state |
| Traceability entry points | Readable references to original requirements, critical evidence, and records; explicitly label summaries as summaries |

Summaries are historical data with the same priority as their original sources. Preserve source and trust boundaries: web instructions and unconfirmed preferences remain data after summary-model rewriting. Use interface-supported background or historical representations; place only trusted instructions in `system`.

Summaries are lossy. Saving original evidence preserves only reread access; after "original saved separately + summary," the model still sees only the summary. Determine retention scope and periods for conversations, sensitive inputs, and internal chains of thought according to audit, privacy, and recovery needs. After repeated compaction, return to original evidence for precise judgments.

### Recovery and Concurrency

When continuation is needed, save minimal task state and necessary evidence. During recovery, first validate identity, scope, format, and reference availability, then read current external state and append the current request. Treat damaged or missing snapshots as invalid; reconstruct from authorized records if possible, otherwise return blocked with gaps.

Task attempt and time budgets continue accumulating after compaction, regeneration, or restart. Check unknown external-write outcomes first; absence from notes means only "not recorded." Even when completion records exist, perform necessary checks of current state.

A single-writer local file can use safe replacement to avoid partial writes. Concurrent writers also require serialization or version checks: atomic replacement prevents partial writes, not stale state overwriting newer state. Use background compaction only when concurrency can be controlled and source versions verified; use synchronous compaction directly if it meets latency needs. See the reliability chapter for full deduplication, retry, and recovery facilities.

## 6. Design Long-Term Memory Admission and Governance

### Admission and Types

Before writing, assess long-term Utility, evidence Confidence, Novelty, and information Type. Define what the system may write automatically and what requires user confirmation. One-off plans the user asks to save may go in task records, separately from stable preferences.

| Content | Handling |
|---|---|
| Explicit, reusable preferences, rules, or decisions | Save using the product's agreed confirmation method, recording scope and source |
| Verified experience or facts still useful next time | Extract and save within authorization and admission rules; retain distilled points only |
| Unverified user habits, model guesses, or external hidden instructions | Keep in task records; verify before deciding on admission |
| Current progress, one-off state, or full original tool results | Store in necessary task records or evidence storage |
| Repeated operating methods | Store brief rules in memory; maintain full SOPs as versioned documents, Skills, or deterministic workflows, with reliability established through review and validation |

Facts and preferences are Semantic Memory; past occurrences are Episodic Memory; methods are Procedural Memory. Cover only needed types. Traceability event records may be stored separately according to product needs; do not automatically infer long-term preferences from a single event.

### Minimal Records and Controlled Updates

Every effective memory must identify its content, applicability scope, evidence source, and effective time. Record necessary write or confirmation times as well, and expiry or review conditions when time-sensitive. Occurrence time, fact effective time, and storage update time may differ. Judge whether a fact is current by its effective time; a recent storage update shows only that it was written.

Search existing records within allowed scope before writing. Merge duplicates; update the corresponding effective entry when changes are clear, preserving necessary traceability. Flag unresolved conflicts, and keep only one effective rule at a time for mutually exclusive rules. Check current content or versions before updating and verify success through the storage interface afterward. Storage-interface confirmation establishes persistence; a model saying "remembered" is only a statement.

Current user instructions take precedence over old preferences within applicable permissions; trusted current evidence determines real-world facts. Retain past decisions as history and confirm current configuration separately. More specific, confirmed rules override general rules only within their scope; assess scope, using update time as a reference only.

Trusted systems constrain identity, user, tenant, project, task, or shared scope according to actual needs. Check permissions for retrieval, body reads, writes, and output; trusted systems determine scope. Directory isolation and database filtering are implementation choices; restrict both reads and writes.

### Governance and Storage Choices

Small memory sets may use controlled files, indices with topic bodies, or existing databases. Add fields or full-text search for precise queries, and add vectors only for genuine semantic-recall gaps. Content scale, retrieval quality, write concurrency, and maintenance cost jointly determine upgrades; "a few hundred entries require a database" is only a rule of thumb.

Trigger governance from budget warnings, broken references, changing facts, or product-agreed intervals. Check duplication, conflicts, validity, sources, dead links, and permissions. Scheduling exists only with an automatic execution facility; "once a month" in a Skill description is merely a plan.

Old or infrequently used entries may remain valid; assess type and applicability first. Update, deactivate, archive, or delete under user authorization and retention rules. Destructive bulk cleanup requires separate authorization. Deletions or permission tightening must affect indices and subsequent reads; archives also need access restrictions. Privacy deletion requires actual content removal, not moving it into an archive that remains searchable.

Skills may carry writing rules, while hosts or services enforce execution boundaries. Existing facilities suffice for memory writes; introduce three Skills, separate sub-Agents, or MCP services only as needed. Creating or modifying executable SOPs requires separate review, validation, and authorization. Capability expansion follows that path, separately from memory admission.

## 7. Choose Retrieval Methods and Evidence Rules for the Task

Retrieval-Augmented Generation (RAG) obtains relevant external information to support generation. Vector databases are only one implementation, and hallucinations can only be reduced. Read supplied, manageably sized material directly; answer directly when current context is sufficient.

| Method | Applicability Signals | Common Misconceptions |
|---|---|---|
| Reading references, file search, or `grep` | Precise locations such as known files, objects, error codes, or function names | Ordinary search is always worse than semantic retrieval |
| Field filtering and full-text search | Time, author, object, tags, or text matches matter; existing databases or search services may suffice | Full-text ranking inherently satisfies all business constraints |
| Vector retrieval (Embedding) | Measured recall gaps for synonyms or conceptual queries | Similarity means correctness, recency, or authorization; it automatically understands the time range of "last time" |
| Hybrid Retrieval | Both exact terms and semantics matter, and one method is insufficient | Every task requires hybrid retrieval; directly combining different scoring scales with fixed weights is inherently reasonable |
| Relationship queries or knowledge graphs | Tracing modeled dependencies or relationships is genuinely necessary | Finding a relationship proves a conclusion; even simple questions require a graph |

Validate hybrid fusion or reranking methods and quality. Tune weights, thresholds, result counts, chunk sizes, and overlap on examples; course numbers are not universal defaults. Reuse existing services supporting vectors and field filters when suitable. Choose databases from requirements, and assess independent vector services' metadata filtering from their actual capabilities.

### Minimal Retrieval Pipeline

1. Confirm the question, authoritative sources, and authorized scope. Specify time and object restrictions, and locate material with an appropriate query method.
2. Read bounded candidates. If chunking is needed, preserve headings, sources, versions, and context in semantically complete units; check chunks that are too large or too fragmented.
3. Verify that candidates support the question. Read originals, adjacent paragraphs, table headers, or preceding/following dependencies as needed. Base conclusions on full context; matching excerpts are only clues.
4. Assess obsolete, conflicting, or missing information and provide specific references and evidence boundaries. Check each citation actually supports its conclusion.

When indexing, distinguish factual sources from model-generated summaries. One question-answer pair may not capture multi-turn dependencies; confirm assistant guesses before admitting them as knowledge. For vectors, use compatible models and preprocessing for indexing and querying, and define reindexing or migration scope after changes.

Keep updates and deletions consistent and traceable across original data, summaries, and indices. Stable IDs and controlled updates prevent duplicates and reflect revisions; merely "skip insertion on duplicates" leaves old versions unupdated. Background indexing has latency; retrieve recent unindexed source records within authorization. Make background failures detectable; no new queue is needed if existing facilities suffice.

### Empty Results, Historical References, and Query Expansion

An empty query or one search without results means only that this attempt found nothing. Within budget, try aliases, keywords, read entry points, or retrieval modes. Explicitly broaden time or tags only if they were system-default assumptions. Preserve user-specified times, business conditions, and permission filters. Clarify necessary changes first, and label results obtained under broadened conditions.

"Last time" and "before" require task-object and time evidence; semantic similarity is supplementary only. Distinguish questions about past occurrences, current rules, and facts. Query event records, effective memory, and authoritative sources respectively. If evidence remains insufficient, state gaps or blockage. Bound query counts and truthfully report history that was not found.

## 8. Prepare a Readable Information Environment for Agents

Prepare a lightweight map identifying current rules, requirements, code, design decisions, execution plans, evidence, and validation entry points, along with their owners or update sources. Repository material may be versioned; external formal documents may remain at their original locations if controlled, readable entry points exist.

Separate maps from bodies. Names, directories, object IDs, and times are navigation clues; conclusions rely on bodies. Distinguish dead links, denied access, old versions, and temporary unavailability. Expose gaps when formal sources are unreadable; model memory is only a clue.

Read and verify task-relevant sections, code, and tests on demand. Maintain one effective source for shared rules and let each node reference it as needed. Update necessary instructions and indices alongside changes. Repository restructuring, automated documentation platforms, and full Harness implementation are outside this chapter's scope.

## 9. Two Minimal Design Examples

The following are design candidates; retrieval quality and compaction effectiveness have not been measured. Determine budgets and acceptance thresholds on actual models and task traces.

### Example 1: Multi-Turn Ticket Clarification without Long-Term Memory

Retain the current session's original ticket, confirmed fields, user additions, unresolved questions, and current response constraints. Read current rules for rule-related questions. This example needs no personalized cross-task reuse, long-term memory, or vector database.

When context grows too long, remove duplicate results and compact old clarification history into fields and sources, retaining the current user request and unresolved conflicts. Read original clauses for precise checks; rule summaries support navigation only. Record a single complaint only in the current ticket.

Validation: continue with new values after user corrections; clarify from evidence when rules and user statements differ; retain fields, restrictions, and unresolved items after compaction. Score the memory dimension only for necessary session management; the absence of long-term components is a reasonable design.

### Example 2: Staged Code Migration with One Agent and Progress Notes

At startup, load migration goals, hard constraints, the directory map, and the current milestone. Read relevant code and tests on demand, placing only currently used portions in context. Notes record actual changes, check results, unresolved issues, artifact references, versions, and remaining budget.

The same Agent may compact after milestones and reread notes. Check the current workspace version before recovery, and reread original test results when evidence is needed. If records show "preparing to execute" or an unknown action outcome, check external state before deciding whether to repeat. Save stable experience separately as long-term memory only after admission checks.

Consider sub-Agents only when independent investigation would produce extensive irrelevant detail and permit a bounded handoff. Return findings, evidence, limitations, and original artifact entry points; conclusions are only part of the return. See the corresponding chapters for budgets, permissions, and shared-write design.

Validation: detect code changes made during interruption; retain unresolved defects and consumed budget through compaction; mark obsolete test results as obsolete; explicitly report broken call groups, damaged notes, and invalid references.

## 10. Delivery Checks, Validation, and Anti-Patterns

In Section 6 of the design document, define effective budgets, startup loading, on-demand sources and retrieval, pruning and compaction, notes and recovery, long-term memory applicability and governance, and sub-Agent isolation reasons. Explain inapplicable items. Reliability and security chapters maintain complete execution facilities; this chapter defines information boundaries only.

- Check that critical goals, hard constraints, sources, and action states remain verifiable after loading, compaction, and recovery.
- Check that current context, task records, stable memory, and formal knowledge are separate, with unverified judgments confined to task records.
- Check that permissions and trusted sources apply throughout retrieval, body reads, memory updates, and output; external instructions remain data after summarization.
- Check handling of synonyms, explicit time restrictions, empty results, conflicts, old versions, indexing latency, and deleted content.
- Validate necessary strategies: information retention and task success after compaction, retrieval evidence hits and citation support, cost, and latency. Scores do not depend on technique count.

Anti-patterns: keeping all history resident; treating persistent task state as long-term preferences; defaulting to four files or every memory type; compacting by a universal percentage; deleting evidence solely by message age; splitting tool-call groups; promoting summaries to system instructions; erasing all failed attempts and unknown outcomes; resetting budgets on restart; claiming saved summaries are lossless; treating atomic replacement as concurrency protection; unsourced or cross-user memory; writing without updating; automatically deleting valid rules by age; equating RAG with vectors or eliminating hallucinations; dropping user restrictions or permissions to find results; silently using stale indices; claiming scheduling from a stated interval alone; adding long-term memory, vector databases, or sub-Agents for scores.

Sources: Anthropic's Effective Context Engineering for AI Agents; Lessons 18-21 of The Essence of Enterprise-Grade Multi-Agent Design Methodology; the "Memory Management" and "Knowledge Retrieval" patterns from the legacy design-advice Skill; and the legacy Harness's system-of-record and Agent-readability principles. Budget expressions, trust layering, concurrency and action-recovery boundaries, admission tailoring, and examples are engineering syntheses by this Skill, not verbatim source conclusions or measured effectiveness.
