---
name: match-the-other-side
description: A change that sends to or reads from another service (an internal API, a vendor such as GitHub, Cloudflare or Google Cloud, a webhook, a queue) takes the shape from that service's own contract or a captured answer, and is tested at real size and on the refusal. Use when touching a client, an adapter, a hook or any request or response struct.
---

# Match the other side

A repository's own tests agree with its own fakes. A fake written from
the same assumption as the code passes while production refuses.

1. **Take the shape from the other side.** For a service you own, its
   published contract and fixtures (an OpenAPI or JSON schema, a
   contract test, a `testdata` answer); for a vendor, its API reference
   or an answer you captured. Put the fixture in the test and decode it
   with the real struct or type. Never write the fixture by reading your
   own struct.
2. **When the contract does not say, ask.** A gap in another team's
   contract is an issue on their repository, not a guess. Say in the
   finish note that the shape is unconfirmed.
3. **Test the answer at its real size.** Lists grow: a vendor listing
   with several hundred entries, a suite with thousands of tests, a diff
   of a generated file. A read with a byte limit, a page size or a
   timeout gets a test with an answer past it.
4. **Test the refusal.** For each call, a test where the other side says
   no: what is recorded, what the person or session is told, and that it
   neither retries forever nor drops the work silently. A 4xx that names
   a field must reach whoever can fix the field.
5. **Regional and per-tenant hosts are different hosts.** A client that
   talks to `run.googleapis.com` in a test may talk to
   `us-central1-run.googleapis.com` in production. List the hosts a real
   call reaches (the tool's debug log shows them) and compare them with
   what the environment allows.
6. **Fake and real agree, or the fake is wrong.** When production
   refuses what the fake accepted, fix the fake in the same change.

An evaluator asks where each request or response shape came from. "The
test passes against our fake" fails the clause when nothing ties the
fake to the other side.

Why this exists, all from one week: a job API refused every deploy offer
with a 422 because one entry was sent as `{ref, host}` where the API
takes a ref or `{ref, purpose}`; a credential service could not list a
vendor's permission groups because it read at most 64 KB of any answer
and the list was larger; three deploys in a row were refused a cloud
host the session's CLI needed and nobody had listed.
