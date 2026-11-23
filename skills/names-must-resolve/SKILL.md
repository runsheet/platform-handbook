---
name: names-must-resolve
description: A config file or document that names something outside itself (a credential, a connection, a host, a permission id, a secret, an env var, a cloud resource, another file) must be shown to resolve, and carries no placeholder. Use when writing or reviewing .runsheet/*.yml, .mesh/*.yml, deploy, validate or CI config, or docs that give a name to use.
---

# Every name resolves

A file that parses is not a file that works. Config fails in production
on the names it points at, and the parser never looks.

**No placeholders.** `<account id>`, `TODO`, `example`, `your-…` in a
file that runs is a failed change, whatever the tests say. If you do not
have the real value, do not invent one and do not leave a marker: finish
saying exactly what a person must supply and where.

**For each name the change introduces or touches, show it exists.**

| the name | how to show it |
|---|---|
| a file path, a script, a make or npm target | it is in the tree at the base: `git ls-files`, `grep`, the package's scripts |
| an env var a step reads | something sets it: the file's own `env:`, the session, the service's config |
| a host a step reaches | it is in the job kind's allowed hosts, or in the repository's `.mesh/config.yml` `egress:` for that kind |
| a connection, federation target or secret | a person or the org's API confirms the name, in the tenant the job runs under, granted for the job's purpose |
| a vendor permission or resource id | copied from the vendor's own listing or from a file where it already works; say which |
| a cloud resource (service, job, bucket, secret) | named the same in the Terraform, the deploy file or the runbook that creates it |
| another repository's file or tool | read at that repository's default branch |

A name you cannot check from inside the session is a **person
checkpoint**: say so in the finish note and name the one command or
screen that checks it. Do not write prose that claims it exists.

**A scope must be one the vendor can grant.** Asking for a narrower
grant than the vendor offers reads well and can never be issued.

An evaluator fails a config change that names something no clause
proves. "The file parses" and "the docs describe it" are not proof.

Why this exists: one deploy file named a credential that had never
existed for ten days, then a pull request replaced it with a connection
of the same made-up name, `<account id>` in a resource, a permission by
a name the credential service could not resolve and a per-resource scope
the vendor does not offer. It passed evaluation. Another deploy file
tagged a revision with a 40-character sha that the cloud refuses.
