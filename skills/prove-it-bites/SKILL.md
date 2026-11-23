---
name: prove-it-bites
description: Before finishing a fix or a feature, or passing one as an evaluator, show that its test fails without the change. Use whenever a change claims to fix a bug or add a behaviour and names a test as its proof.
---

# Prove the test bites

A test that passes with the change proves nothing until it has failed
without it. Do this once per behaviour the change claims, before you
finish (builder) or before you pass it (evaluator).

1. Save the code change, not the test: `git diff -- <code files> > fix.patch`
   (keep the patch outside the repository).
2. Put the code back as it was: `git checkout -- <code files>`.
3. Run only the new test. It must **fail**, and for the reason the change
   fixes.
4. Re-apply the change (`git apply fix.patch`) and run the test again. It
   must pass.

The test command is the repository's own, for example:

```sh
go test ./pkg/ -run 'TestTheNewOne' -count=1     # Go
npx vitest run path/to/the.test.ts -t 'the new one'   # TypeScript
pytest path/to/test_file.py -k the_new_one       # Python
```

Never `git stash`: the stash stack is shared across worktrees. For a
committed change, revert the code file with `git checkout <base> -- file`
and restore it with `git checkout HEAD -- file`.

Read the failure. It counts only when the message is the bug: "deploy
offer egress empty, want the repository's hosts" bites; a compile error,
a nil fixture or a timeout does not.

Say what you saw in the finish note or the verdict: the test's name, the
failing line without the change, and that it passes with it. An evaluator
that could not make the test fail fails the clause and says which
assertion never ran.

When there is no test to bite, the change is not proven. Write the test
first. The exceptions are a pure rename, a comment and generated output.

Why this exists: a repository's declared egress hosts reached build jobs
and were dropped for every deploy. The egress tests were green all along
because none of them exercised a deploy.
