# Contributing a skill

Skills here are served to every runsheet tenant's agents, so every change is
reviewed and merged by a person. No agent merges a pull request here.

1. Fork, then add or change `skills/<name>/SKILL.md`. Start with frontmatter:

   ```
   ---
   name: <name>
   description: <what it does, and when to use it>
   stack: <optional: go, loom-go, typescript, react-native, ...>
   ---
   ```

   Then concrete steps (commands, files to copy) and what to check.
   A variant for one stack goes beside it as `skills/<name>/<stack>.md`.
2. Keep it general: nothing about one tenant, no secrets, no private URLs.
3. Open a pull request saying what the skill fixes and how you tried it.

The validation check must pass and a code owner must approve before merge.
runsheet serves only what is merged to `main`.
