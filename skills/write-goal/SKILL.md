---
name: write-goal
description: Write a Mesh goal a person can read and a planner can build, with numbered promises, acceptance checks that say which promise they cover, a signal naming where it is read, a parity line, a budget equal to the appetite and cross-project dependencies explained. Use before setGoal or goal_set, when restating a goal, or when reviewing one.
---

# Write a goal

A goal is read by a person deciding whether it is worth the money, by a
reviewer looking for what it would miss, and by a planner turning it
into items. Write it for all three. Check `goals_list` with `status:
all` first: the goal may exist, be done, or overlap a sibling.

## The fields

- **Title**: what will be true, at most 60 characters. No ticket
  wording, no spec in the title.
- **Outcome**: `Promises:` then numbered promises, `P1 …; P2 …`. Each is
  a state a person can check after it ships ("skills_list lists every
  platform skill for a tenant with no handbook"), not a task ("add a
  platform layer"). Three to five promises; more means two goals.
- **For**: who benefits, by role.
- **Why**: the evidence, with the one or two numbers that matter and
  their date and source.
- **Scope**: the repositories and areas it touches.
- **Non-goals**: what it will not do, each naming the goal that owns it
  when one does.
- **Appetite**: the money and the item count, for example
  `$200, at most five items`. Set the **budget equal to the appetite**;
  a budget above it hides a goal that has outgrown its promise.
- **Acceptance checks**: one or more per promise. Each starts
  `(covers Pn)`, says what is run or read (a named test, a command, a
  read and its value) and what is expected. "Works", "is documented" and
  "is reviewed" are not checks. At least one check is observable in
  production after the deploy.
- **Signal**: the metric, its direction, and **where it is read**
  ("read from merged pull requests touching skills/", "read from
  health_flow's p50"). A signal nobody can read is no signal.
- **Statement**: notes for builders, and the two lines below.

## Two lines the statement always carries

- **Dependencies across projects, explained.** "Depends on
  <goal> (<project>): it provides <what this goal reads>." Name what
  happens if it is late. A dependency inside the project is set with
  `goal_set_depends_on` as well.
- **`Parity:`** what keeps working exactly as before, each with a way to
  check it. A goal that replaces or moves something lists every thing
  the old path did; a lost duty is the most common miss.

## Before you submit

1. Every promise has a check that says `(covers Pn)`, and every check
   covers a promise.
2. Read the outcome alone: could a person tell from production, without
   the code, that it is true?
3. The non-goals name the sibling goals; nothing is claimed twice.
4. Budget equals appetite.
5. The signal says where it is read.

## Example

> **Outcome:** Promises: P1 a tenant with no handbook lists every
> platform skill, labelled platform; P2 a project skill of the same name
> wins over a platform one.
>
> **Acceptance:** (covers P1) skills_list for a project in a tenant with
> no handbook: every platform skill is listed, layer platform. (covers
> P2) a project skill named like a platform one: skill_get answers the
> project's.
>
> **Signal:** platform skills read per week, up, read from the MCP
> server's skill_get log.
>
> **Statement:** Depends on the-tenant-handbook (runsheet/runsheet): it
> provides skills_list. Parity: tenant and project skills are served as
> before.
