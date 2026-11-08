---
name: drawio-diagram
description: This skill should be used when the user asks to "create a diagram", "draw the architecture", "make a flowchart", "generate an ERD", "draw a sequence diagram", "diagram this codebase", "visualize this repo", "map the data model", or "create a .drawio file", or otherwise wants a draw.io, architecture, flow, entity-relationship or sequence diagram of a codebase, in any language or framework.
---

# draw.io Diagrams From Code

Generate editable, uncompressed draw.io files that reflect what the code actually does. Write the XML directly; no draw.io connector or desktop app is needed to create a diagram.

## Workflow

Follow these steps in order.

### 1. Analyse

Read `${CLAUDE_PLUGIN_ROOT}/skills/drawio-diagram/references/repo-analysis.md` and apply it to the requested scope.

- Base every node and edge on evidence in the repo. Note the files each one came from while working.
- Never read `.env` files or other secrets. Never open `.env.example` or similar templates with the Read tool; extract only the variable names, using the command in `repo-analysis.md`.
- Never put credentials, tokens or private URLs in a label.
- Ask one clarifying question only when the scope is genuinely ambiguous.

### 2. Choose the diagram type

| Request is about | Type | Default file name |
|---|---|---|
| Components, services, layers, deployment | Architecture | `architecture` |
| A feature, request path, user journey, decisions | Flow | `<feature>-flow` |
| Tables, models, relationships | ERD | `erd` |
| Calls over time between actors and services | Sequence | `<use-case>-sequence` |
| Anything else | Closest fit, or free-form | `<topic>` |

### 3. Plan nodes and edges

Before writing XML, list the nodes, their layer or group, and the edges with short labels.

- Keep each page to about 25 nodes. Beyond that, split into multiple pages or diagrams. Legend and footer cells do not count.
- Merge incidental detail into node labels rather than adding nodes and edges.
- Draw a relationship that was inferred rather than seen in code as a dashed edge, and mention it in the final summary.
- Assign each node a position following `${CLAUDE_PLUGIN_ROOT}/skills/drawio-diagram/references/layout.md`.

### 4. Write the XML

Collect the footer values, resolve the output path (see below), then write the file.

- Follow `${CLAUDE_PLUGIN_ROOT}/skills/drawio-diagram/references/drawio-xml.md` for structure and escaping.
- Follow `${CLAUDE_PLUGIN_ROOT}/skills/drawio-diagram/references/styles.md` for shapes and colours.
- Use `${CLAUDE_PLUGIN_ROOT}/skills/drawio-diagram/references/example.drawio` as the structural template.
- Add a title, a legend covering only what the diagram uses, and the footer.

### 5. Validate

This step is mandatory after every diagram is written or changed. Run the validator on the file:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate_drawio.py" docs/diagrams/<kebab-name>.drawio
```

- Run it as a single command, with nothing chained after it. `PASS` or `FAIL` is printed on the first line.
- Fix every `ERROR` and re-run until the validator exits with code 0. Never finish or report success while errors remain.
- Review every `WARN`. Fix genuine overlaps and hidden label text. Mention any warning left in place, and why, in the final summary.
- Then work through the checklist at the end of `drawio-xml.md`, which covers what the validator cannot see.

### 6. Report and offer export

Finish with a short summary: the file path, what the diagram shows, any assumptions, and what was left out.

Then offer an export, and run it only if the user accepts. Without a way to ask, skip it and print the command instead. Export only a file that passed validation:

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/export.sh" docs/diagrams/<kebab-name>.drawio svg
```

- Prefer `svg`, or use `png` when the user asks for it. Both stay fully editable in draw.io, but the image itself shows only the first page.
- If draw.io desktop is not installed, the script explains this and exits with code 0. Relay the message and treat the diagram as finished.
- If the export fails, report the error and treat the diagram as finished, because the `.drawio` file is unaffected.
- If the script skips the file because the image is newer than its source, ask before re-running with `--force`, because the image may have been edited directly.

After an SVG export, give the user this snippet for a README in the repo root:

```markdown
![<Diagram title>](docs/diagrams/<kebab-name>.drawio.svg)
```

## Output Convention

All paths are relative to the root of the repo being diagrammed.

- Write diagrams to `docs/diagrams/<kebab-name>.drawio`. Create the folder if needed.
- Write exports next to the source as `docs/diagrams/<kebab-name>.drawio.svg`. GitHub renders these in markdown and draw.io can still edit them.
- Never overwrite an existing diagram without asking. Ask whether to replace it or write the next free name, such as `architecture-v2.drawio`. Without a way to ask, write the next free name.

## Footer

Every page has a small footer in this form:

```
<diagram title> · <repo name> · <git short SHA> · <YYYY-MM-DD>
```

Collect the values from the root of the repo being diagrammed. Run each of these as a separate command, because combined shell lines trigger extra permission prompts:

```bash
git rev-parse --show-toplevel
git rev-parse --short HEAD
git status --porcelain
date +%F
```

- Use the last path segment of `--show-toplevel` as the repo name. If that command fails, use the current folder's name.
- Use `no-git` as the SHA outside a git repo or in a repo with no commits.
- Append `-dirty` to the SHA, as in `abc1234-dirty`, when `git status --porcelain` prints anything.

## Reference Files

Each of these lives in `${CLAUDE_PLUGIN_ROOT}/skills/drawio-diagram/references/`:

- **`repo-analysis.md`**: discovering stack, entry points and structure in any language
- **`drawio-xml.md`**: file format rules, escaping and the pre-finish checklist
- **`styles.md`**: shape and edge palette with one colour per layer
- **`layout.md`**: grid, spacing, containers and page-splitting rules
- **`example.drawio`**: small valid architecture sample

## Scripts

- **`${CLAUDE_PLUGIN_ROOT}/scripts/validate_drawio.py`**: structural checks on `.drawio` files, exiting with code 1 on errors
- **`${CLAUDE_PLUGIN_ROOT}/scripts/export.sh`**: optional export to an editable `.drawio.svg` or `.drawio.png`, using draw.io desktop
