---
description: Generate a sequence diagram of an endpoint or use case
argument-hint: "<endpoint or use case>"
---

Create a sequence diagram as a draw.io file, showing the calls made over time for one endpoint or use case.

Endpoint or use case: $ARGUMENTS

The plugin is installed at `${CLAUDE_PLUGIN_ROOT}`. Wherever the plugin's files mention the plugin root variable, use this path.

Read `${CLAUDE_PLUGIN_ROOT}/skills/drawio-diagram/SKILL.md` first and follow its full workflow, including the references it names and the mandatory validation step. It also covers not overwriting an existing diagram.

## Scope

- Find the entry point, then follow the calls in the order the code makes them.
- Ask a clarifying question only if the argument is missing, matches nothing, or matches several unrelated use cases. List the candidates found in the code. Without a way to ask, choose the most central candidate and state that in the summary.
- Write `docs/diagrams/<kebab-use-case>-sequence.drawio`.

## What to show

- Participants left to right in the order they are first called: actor or client, then services, then data stores and external systems.
- Participants at the level of a runtime component or major code layer, using layer colours. Do not give every helper function its own lifeline.
- Numbered messages using real routes, method names, or query intent, such as `1. POST /api/users` or `3. INSERT user`.
- Return messages as dashed lines, when they carry something meaningful.
- Self-calls only for steps that matter, such as hashing a password or signing a token.
- One or two important failure paths in `alt` frames, and asynchronous steps as dashed messages with a note in the legend.

Leave out logging, generic middleware and framework internals unless they change the outcome.

## Finish

Print a short summary:

- The file path and the validator result
- The sequence, in two or three lines, with its entry point
- Assumptions, and any step inferred rather than confirmed
- Anything skipped, such as failure paths left out

Then offer an SVG or PNG export, as described in step 6 of the skill.
