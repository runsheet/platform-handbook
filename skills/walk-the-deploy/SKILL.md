---
name: walk-the-deploy
description: Check a change to .runsheet/deploy.yml, a deploy step, the deploy kind's egress or its credentials by walking every step as the session will run it, covering tools, hosts, credentials, limits and the probe. Use when writing or reviewing anything a deploy session executes, in any repository.
---

# Walk the deploy before it runs

A deploy file is only proven by a deploy. Until one has run end to end,
walk it by hand, step by step, and write down what each step needs.
Every line below has cost at least one failed deploy.

For **each step**, in order:

- **Tool.** Is the binary in the session's image, or installed by an
  earlier step into the session's home? Do not assume a cloud CLI is
  there.
- **Hosts.** Every host the command reaches, including the ones the
  tool chooses for you: a region's endpoint
  (`us-central1-run.googleapis.com`, not only `run.googleapis.com`), the
  registry, the download host, the API a wrapper calls first (service
  usage, secret manager). Run the command once with the tool's debug or
  HTTP log to see them. Each one is in the deploy kind's allowed hosts
  or in the repository's `.mesh/config.yml` under `egress: deploy:`.
  Wildcards are refused.
- **Credential.** Which entry of `credentials:` signs this step, and
  does the grant cover it: the federation target's purposes and kinds,
  the connection's limit, the role on the service account. See the
  `names-must-resolve` skill.
- **Vendor limits.** A Cloud Run tag plus the service name is at most
  46 characters, so tag with a short sha. A timeout shorter than the
  step's worst case fails the deploy, not the step.
- **What it leaves behind** if the next step fails: a migrated schema, a
  pushed image, a revision with no traffic. The order must be safe to
  stop at any point and safe to run again.

Then the whole file:

- **Schema before code**, and the migration is one the old revision
  still runs on.
- **No traffic until probed.** The new revision takes none until the
  probe has passed against the new revision itself, not the old one
  still serving.
- **The probe reaches the host it names** from the session, and what it
  checks is the service, not a CDN's cached page.
- **`on_failure`** says who looks and what they are told.
- **Parse it** with the platform's own parser or validation before
  merging; a file that does not parse never deploys.

After the change lands, **watch the first deploy to its end** and read
the session's log for `refused`. A deploy that "finished" is not a
deploy that shipped: check that a new revision is serving the commit.
If it was deployed by hand instead, record it (`deploys_record`), or the
repository stays blocked.

An evaluator fails a deploy change whose pull request does not list
each step's hosts and credential.

Why this exists: over two days one service's self-deploy failed, in
order, on the offer's shape, the federation grant's purpose, the
service-usage API, the secret manager, the region's Cloud Run endpoint,
and then the same endpoint again because the platform dropped the
repository's hosts for deploys. Each was found by running it and reading
the refusal, an hour apart.
