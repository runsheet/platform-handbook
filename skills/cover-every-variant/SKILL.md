---
name: cover-every-variant
description: When a behaviour is keyed by a kind, platform, vendor, subject type, harness, role or actor, list every variant from the code's own source of truth and test each one or say why it is out. Use when adding or changing anything that says "per kind", "for each", or switches on a type.
---

# Cover every variant

Much of what a service does is keyed by something: a job kind, a deploy
platform, a vendor, the subject a request is for, the runtime a session
runs in, who is calling (a machine, a person, the platform itself). A
change tested for one variant is unproven for the rest, and the rest is
where it breaks.

1. **Find the list in code, never from memory.** The registry, the enum,
   the switch's cases, the table the router or scope check reads, the
   constructor every variant is made through. `grep` for it and name the
   file in the pull request.
2. **Write the list in the pull request**, one line per variant: tested
   (name the test), or out of scope and why.
3. **Test each variant that should behave the same** with a table test
   over the list itself, so a variant added later is covered without
   anyone remembering. Range over the registry; do not copy its entries
   into the test.
4. **Test one variant that must not get the behaviour**, so the boundary
   is pinned too.

An evaluator asks one question of any "per kind" change: which variants
did no test reach? If the answer is not in the pull request, find it
with the list from step 1 before passing.

Why this exists: a repository's declared hosts were read through a field
only one kind of job set. Plans were given the field when someone
noticed; deploys were not, so every deploy for a day was refused a host
its repository had declared. The same day the deploy kind's allowed
hosts were found short by two cloud hosts, one refusal at a time.
