# runsheet: the target work model (draft, 28 Nov 2026)

Status: agreed direction from Chris (28 Nov), refined with Codex. To land in the handbook as the
overview and its six chapters. It replaces the ADR/TRD maze; old ADRs are marked superseded,
never renumbered or deleted.

## 1. Work model

| runsheet | means | Jira |
|---|---|---|
| Initiative | a body of outcomes, may span projects | Epic (or portfolio level) |
| Goal | one outcome in **one project**, across any of that project's repos | Story, Task or Bug |
| Item | one change that can land by itself (one PR per repo it touches), about a day of work | Sub-task |
| Sub-item | a checklist step inside an item, done by a subagent | checklist on the sub-task |
| Pitch | an idea a person approves, defers or rejects; approval makes delivery work | discovery idea |

- A goal keeps outcome, for, why, scope, appetite, acceptance checks, non-goals, signal. Templates:
  Story, Bug, Maintenance, Investigation (no invented user for platform work).
- A goal is linked to one project. Anything outside the project is a **dependency on another
  goal**, naming the contract/version or milestone it needs, not the whole upstream goal.
- A goal **declares its switches**: feature flags (temporary, with an owner, safe default and a
  cleanup item) and kill switches (may outlive the goal).
- runsheet stays authoritative for claims, leases, evidence, cost, retries, merges, deploys and
  rollout. Jira mirrors; a Jira status never authorises a merge.

## 2. Execution: one item, one Mesh job

1. **Coordinator session** takes the item, plans its sub-items and runs builder **subagents**
   (code, tests, docs, fixtures), then integrates their work.
2. **Self-check in the same session**: the node's suites via run_suite plus the /verify self-review
   (#7872). The coordinator fixes what it finds before finishing.
3. **Independent evaluation**: a separate, cheaper session, preferably another model (Codex
   judging Claude, or the reverse). It judges acceptance against the diff and the signed suite
   results. It never edits code.
4. **Resume with findings**: the evaluator's findings go back to **the same coordinator session**
   (resumed, or a new session handed the transcript and its saved progress), not to a fresh
   builder. One deterministic rejection needs changed inputs before it is evaluated again; an
   unchanged head is never re-judged.
5. **Security review** stays independent and never edits.
6. The coordinator checkpoints after each sub-item so a lost lease loses one sub-item, not the item.

## 3. Integration

- An item **lands when green**, behind its goal's flag where the change is user-visible
  (trunk-based dark launch). No long-lived goal branch; a goal **manifest** pins each repo's
  revision and its dependencies; each item has its own worktree, restacked when one below it moves.
- What a flag cannot hide (schema, wire format) uses **expand → migrate → contract** and tolerates
  version skew. Merge order is not deploy order.
- Validation is of the exact candidate tree on current main. Speculation across goals is allowed
  but bounded; a result a predecessor's failure invalidates is **stale evidence** and is re-run,
  never blamed on the other goal. Unrelated goals are never batched into one pass/fail validation.
- A head is validated before it is evaluated, whoever produced it (goal
  a-rebased-head-is-validated-before-it-is-evaluated).

## 4. Release

- A goal **ships** when its acceptance passes in production and its flag is turned on (by rollout
  rule or a person, per the project's promotion setting). Its last item retires temporary flags.
- Releases are stored, signed and deployed by digest (live since 28 Nov: v0.0.1 onward).

## 5. Policy and config

- **How a repo is built, validated, released and deployed lives in runsheet** (Chris, 17 Nov; goal
  a-repo-is-tagged-with-templates-that-say-how-it-is-built): versioned **templates** (go-loom-service,
  shell-console, nextjs-cloudflare, expo-app, astro-site, docs, cloud-run, cloudflare-pages,
  cloudflare-worker); a repo is one or more **components** (folders) tagged with templates, with
  overrides, set in the console or over MCP. A node is handed the combined spec in its job and reads
  no file. Every component follows the latest template; a new version is tried on every tagged
  component's main head first and held if any is red.
- Changing a template, tag or override that touches **deploy steps or egress needs an org admin**,
  with a reason, recorded. Protected paths follow the same rule: a change can never weaken the policy
  judging it (ADR 021 kept); GitHub rulesets stay where GitHub enforces them.
- The **handbook** holds knowledge: guidance, agent roles, skills, decisions, served over MCP with
  versions and provenance, never instructions fetched mid-job.
- A repo keeps only what a local build needs (build scripts, lockfiles, migrations, tests) and
  `.mesh/product.yml`. The spec digest is recorded on every piece of evidence; the combined spec can be
  exported for offline use. The repo files go once templates are live (goal
  a-repos-build-files-leave-the-repo).

## 6. Records and training data

Every job writes a **replayable record**, so we can train our own models later:

- inputs: brief, goal/item fields, bundle digest, skills and their versions, base and head commits,
  tool list, model and harness;
- the session: messages, tool calls and results, subagent transcripts, checkpoints;
- outputs: diff, finish, suite results (signed), evaluation verdict, findings, cause class, the
  resume-with-findings correction and its result, security findings, merge and deploy outcome,
  cost and time;
- **provenance on every record**: which model and harness produced it, which person.

Export rule (Chris, 21 Nov; Anthropic's terms): records are kept for every producer, but **only
records whose producer is on the org's allowlist** (Codex/OpenAI, people) are exported for
training, opted-in tenants only, platform faults excluded. Claude-produced content is kept for
replay and audit but never exported for training. The best-labelled pairs come from
evaluator findings → coordinator correction → green.

## 7. Docs

- One product overview and six living chapters (work model, execution and evidence, integration,
  release, policy and config, operations), each with an owner, its invariants and links to the
  tests that prove them.
- ADRs only for durable commitments that cross projects, or security, identity, storage and
  protocol decisions. Cross-project contracts stay generated fixtures.
- Migration: inventory by full filename, map each decision to its chapter, mark superseded; most
  critical chapters first.

## Order of work

1. Land this design (overview + chapters) in the handbook; pause gate goals that build the old
   chain-mixing model.
2. Execution fixes: ready means claimable; head validated before evaluation; no re-judging an
   unchanged head; one live-goal limit applied in one place.
3. Coordinator + subagents + resume-with-findings, with job records (section 6).
4. Prove the model on one goal: two repos, three items (compatible producer, consumer behind a
   disabled flag, rollout + cleanup), landing while another goal lands alongside.
5. Finish templates (items 6–8), then remove the repo files; then the Jira adapter.

## Open questions

- Can a Mesh lease be resumed with findings, or is it a new session handed the transcript?
- Which model evaluates which: Codex for Claude-built items, Claude for Codex-built?
- How big may an item get before it must split (lines changed, sub-items, lease time)?
