---
description: Generate a flowchart of a feature, endpoint or user flow
argument-hint: "<feature or endpoint>"
---

Create a flowchart as a draw.io file, tracing how the code handles one feature, request or user journey.

Feature or endpoint: $ARGUMENTS

The plugin is installed at `${CLAUDE_PLUGIN_ROOT}`. Wherever the plugin's files mention the plugin root variable, use this path.

Read `${CLAUDE_PLUGIN_ROOT}/skills/drawio-diagram/SKILL.md` first and follow its full workflow, including the references it names and the mandatory validation step. It also covers not overwriting an existing diagram.

## Scope

- Find where the feature starts, such as a route, handler, UI event, job or CLI command, and follow the calls from there.
- Ask a clarifying question only if the argument is missing, matches nothing, or matches several unrelated flows. List the candidates found in the code. Without a way to ask, choose the most central candidate and state that in the summary.
- Write `docs/diagrams/<kebab-feature>-flow.drawio`.

## What to show

- A start terminal, and an end terminal on every path.
- Steps named for what they do, not for function names, with the function or file in smaller text when useful.
- Decisions taken from real conditions in the code, with labelled branches such as `Yes` and `No`.
- Failure paths that the code actually handles, using the error style, such as validation errors and auth failures with their status codes.
- Swimlanes only when several roles or systems take part.

Leave out logging, generic middleware and framework internals unless they change the outcome.

## Finish

Print a short summary:

- The file path and the validator result
- The path traced, in two or three lines, with its entry point
- Assumptions, and any branch inferred rather than confirmed
- Anything skipped, such as calls not followed

Then offer an SVG or PNG export, as described in step 6 of the skill.
