---
description: Generate any draw.io diagram from a free-form description
argument-hint: "<what to draw>"
---

Create a draw.io diagram of what the user describes.

Description: $ARGUMENTS

The plugin is installed at `${CLAUDE_PLUGIN_ROOT}`. Wherever the plugin's files mention the plugin root variable, use this path.

Read `${CLAUDE_PLUGIN_ROOT}/skills/drawio-diagram/SKILL.md` first and follow its full workflow, including the references it names and the mandatory validation step. It also covers not overwriting an existing diagram.

## Scope

- If the description is empty, ask what to draw. Without a way to ask, stop and say a description is needed.
- Ask a clarifying question only if the description could mean very different diagrams.
- If the description is about this repo, base the diagram on its code. If it is about something else, such as a process or proposed design, draw it as described and say that it did not come from the code.
- Choose the type that best fits, using the patterns in the references. For a type without one, such as a state machine or dependency graph, use plain shapes and connectors that follow the general style rules.
- Write `docs/diagrams/<kebab-topic>.drawio`, with a short name of two to four words taken from the description.

## Finish

Print a short summary:

- The file path and the validator result
- The diagram type chosen, and what it shows in two or three lines
- Whether it came from the code, the description, or both
- Assumptions, and anything inferred or left out

Then offer an SVG or PNG export, as described in step 6 of the skill.
