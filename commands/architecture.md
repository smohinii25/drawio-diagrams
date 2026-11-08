---
description: Generate a system architecture diagram of this repo
argument-hint: "[path or module]"
---

Create a system architecture diagram of the current repo as a draw.io file.

Scope: $ARGUMENTS

The plugin is installed at `${CLAUDE_PLUGIN_ROOT}`. Wherever the plugin's files mention the plugin root variable, use this path.

Read `${CLAUDE_PLUGIN_ROOT}/skills/drawio-diagram/SKILL.md` first and follow its full workflow, including the references it names and the mandatory validation step.

## Scope

- With no scope given, diagram the whole repo and write `docs/diagrams/architecture.drawio`.
- With a path or module name, diagram only that part, showing what it connects to as simple outside nodes. Write `docs/diagrams/architecture-<kebab-scope>.drawio`.
- If the scope matches nothing, or matches several unrelated places, ask which is meant. Without a way to ask, make the most reasonable choice and state it in the summary.

## What to show

- Runtime components: clients, services, workers, data stores, queues, and external systems.
- How they connect, labelled with the protocol or what flows, such as `HTTPS`, `SQL` or `publishes`.
- For a single-service repo, show its internal layers or modules in a container, plus everything it talks to.
- CI/CD only when asked for or central to how the system runs.

## Finish

Print a short summary:

- The file path and the validator result
- What the diagram shows, in two or three lines
- Assumptions, and anything inferred or drawn dashed
- Anything skipped or sampled

Then offer an SVG or PNG export, as described in step 6 of the skill.
