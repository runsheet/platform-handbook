# runsheet platform handbook

The platform layer of runsheet's handbooks. Everything here reaches every
tenant, every project and every session, through runsheet's MCP
(`skills_list`, `skill_get`, `docs_search`, `docs_read`, and an MCP prompt
per skill).

Layers, most general first: **platform** (this repo) → **tenant** (an org's
handbook) → **project** handbook → the repo's own AGENTS.md. A more specific
layer overrides a general one by name, so a tenant can replace any skill here.

- `skills/<name>/SKILL.md` — one skill each: frontmatter (`name`,
  `description` with its trigger, optional `stack`) then steps and checks.
  Stack-scoped variants live beside it (`skills/<name>/<stack>.md`).
- `ways-of-working/` — rules every session's brief carries.
- `docs/` — how to use runsheet, written for tenants.

Nothing here is specific to runsheet the product; that lives in
`runsheet/handbook`. Agents propose changes as pull requests (the librarian
and the learning loops); people merge them.
