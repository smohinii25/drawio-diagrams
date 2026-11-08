---
description: Generate an entity-relationship diagram of the data model
argument-hint: "[module or table group]"
---

Create an entity-relationship diagram as a draw.io file, from the data model defined in this repo.

Scope: $ARGUMENTS

The plugin is installed at `${CLAUDE_PLUGIN_ROOT}`. Wherever the plugin's files mention the plugin root variable, use this path.

Read `${CLAUDE_PLUGIN_ROOT}/skills/drawio-diagram/SKILL.md` first and follow its full workflow, including the references it names and the mandatory validation step. It also covers not overwriting an existing diagram.

## Scope

- With no scope given, cover the whole data model and write `docs/diagrams/erd.drawio`.
- With a module or table group, cover those tables, plus any table they reference shown with its primary key only. Write `docs/diagrams/erd-<kebab-scope>.drawio`.
- Ask a clarifying question only if the repo has several unrelated databases and no scope was given. Without a way to ask, use the main database and name the others in the summary.
- If the repo defines no data model, say so and do not create a file.

## Sources

Use the most authoritative source available, in this order:

1. A declared schema, such as `schema.prisma`, `schema.rb`, `structure.sql` or a schema dump
2. ORM models, entities or annotations
3. Migrations, applied in order to work out the final state

If sources disagree, follow the first one in this list and mention the difference in the summary. Read schema definitions only, not seed data or fixtures.

## What to show

- One table per entity, using its real table or model name, with its columns and types.
- `PK`, `FK` and `(UQ)` markers on every key column.
- For tables with more than about 12 columns, show keys and important columns, ending with a row such as `… 14 more`.
- Every relationship from a declared foreign key or ORM relation, as a crow's-foot edge from row to row, with each end set by the schema's nullability and uniqueness.
- Join tables for many-to-many relations, including implicit ones that the ORM creates, marked `(implicit)` in the title.
- A relationship inferred only from a name such as `user_id`, with no declared constraint, as a dashed edge with `dashed=1;`.

If there are more than about 25 tables, split by domain into separate pages.

## Finish

Print a short summary:

- The file path and the validator result
- Which source was used, with the table and relationship counts
- Assumptions, and any relationship inferred rather than declared
- Anything skipped, such as columns hidden or tables left out

Then offer an SVG or PNG export, as described in step 6 of the skill.
