---
name: change-a-shared-number
description: Before changing a default, cap, timeout, budget, resource size, shard count, retry limit or any constant more than one thing reads, measure first, say what else reads it and what you expect, run the whole suite, and measure after. Use when a diff changes a number rather than logic.
---

# Change a shared number on purpose

A one-line change to a number is the cheapest diff to write and has
broken main, the merge queue and the build machines more than once.
Treat it as an experiment with a prediction.

1. **Measure before.** The figure the number is meant to move, from
   production or the machine it runs on, with the date: a duration from
   a log, a count from a health read, a load from the host. No
   measurement, no change.
2. **Find every reader.** `grep` the constant and the config key. A
   resource size on a job is also what each lane reserves from the
   machine's budget and the pod's hard limit. A timeout is also the
   longest a lease is held. Write the readers down.
3. **Write the prediction in the commit**: "lanes open within a minute;
   load stays under 96". A prediction you cannot write means you do not
   yet know what the number does.
4. **Run everything, not a filter.** A default or cap is read by tests
   that do not name it. Run the repository's whole suite, end to end
   included, and gate the merge on its exit code, never on a tail of its
   output.
5. **Change one number at a time**, and leave the old value and the date
   in the comment beside it.
6. **Measure after, at the same place, and say so.** If the prediction
   was wrong, put the number back first and work out why second.

For a number on a machine (a node's capacity, a floor, a limit): know
what stops it running away before you raise it, and watch the host for
the first half hour.

An evaluator fails a changed default with no before-figure and no named
readers.

Why this exists: validation pods were raised from 4 CPUs to 6 to make
shards faster; each lane reserves that from the machine's 80, so lanes
queued 15 to 25 minutes instead. The next night the machine's budget was
raised from 80 to 160 on the belief that reservations far exceeded use;
load went to 157 on 96 cores and the host gate tripped for an hour.
Earlier, a filtered test run on a changed constant turned main red.
