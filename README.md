# drawio-diagrams

A Claude Code plugin that reads the code in a repo and generates editable draw.io diagrams: architecture, flowcharts, entity-relationship diagrams and sequence diagrams. It works with any language or framework.

Diagrams are saved in the repo as plain `.drawio` files, so they can be reviewed, versioned and edited like any other file.

## Requirements

- [Claude Code](https://claude.com/claude-code)
- Python 3, for the diagram validator. No packages are needed.
- Optional: [draw.io desktop](https://github.com/jgraph/drawio-desktop/releases), for exporting images. Diagrams can be created without it, and opened at [app.diagrams.net](https://app.diagrams.net).

## Install

Run these inside Claude Code, replacing `YOUR-OWNER` with the GitHub account that hosts this plugin:

```
/plugin marketplace add YOUR-OWNER/drawio-diagrams
/plugin install drawio-diagrams@drawio-diagrams
```

On Claude Code 2.1.275 or later, this single command does both:

```
/plugin install drawio-diagrams --marketplace YOUR-OWNER/drawio-diagrams
```

A private repo requires GitHub access on each person's machine.

## Commands

Run these from the repo to be diagrammed.

| Command | Creates | Output |
|---|---|---|
| `/drawio-diagrams:architecture [path or module]` | System or component architecture | `architecture.drawio` |
| `/drawio-diagrams:flow <feature or endpoint>` | Flowchart of a feature or request | `<feature>-flow.drawio` |
| `/drawio-diagrams:erd [module or table group]` | Data model from schemas, ORM models or migrations | `erd.drawio` |
| `/drawio-diagrams:sequence <endpoint or use case>` | Calls over time between actors and services | `<use-case>-sequence.drawio` |
| `/drawio-diagrams:diagram <what to draw>` | Anything else, from a description | `<topic>.drawio` |

Examples:

```
/drawio-diagrams:architecture
/drawio-diagrams:architecture src/payments
/drawio-diagrams:flow user login
/drawio-diagrams:erd
/drawio-diagrams:sequence POST /api/orders
/drawio-diagrams:diagram which environment variables this app needs and which component uses each one
```

Plain requests also work, such as "draw the architecture of this repo".

## What you get

Diagrams go in `docs/diagrams/` in the repo being diagrammed:

```
docs/diagrams/architecture.drawio       # the diagram, editable in draw.io
docs/diagrams/architecture.drawio.svg   # optional export, also editable in draw.io
```

- **Validated:** every diagram goes through `scripts/validate_drawio.py` before it is reported as finished.
- **Traceable:** a footer on each diagram shows its title, repo name, git short SHA and date. The SHA ends in `-dirty` if the repo had uncommitted changes, and reads `no-git` outside a git repo.
- **Honest about gaps:** relationships inferred rather than seen in code are drawn dashed. The summary lists assumptions and anything skipped.
- **Safe to re-run:** an existing diagram is never overwritten without asking. The plugin offers a new name instead, such as `architecture-v2.drawio`.
- **Split when large:** each page holds about 25 nodes. Larger subjects are split across pages or diagrams.

## Export and embed

After each diagram, Claude offers to export it. To export by hand, run this from the repo being diagrammed, replacing `<plugin-path>` with the location of this plugin:

```bash
<plugin-path>/scripts/export.sh docs/diagrams/architecture.drawio svg
```

`svg` is the default, and `png` also works. Both images contain a copy of the diagram, including all of its pages, so draw.io can still edit them. The image itself shows only the first page.

If the image is newer than its source, the script skips it, because it may have been edited directly. Add `--force` to replace it.

To show an exported diagram in a README in the repo root:

```markdown
![Architecture](docs/diagrams/architecture.drawio.svg)
```

## Before you run it on private code

- **Secrets:** the plugin instructs Claude not to open `.env` files or key files, and to read only the variable names from templates such as `.env.example`. These are instructions rather than an enforced block, so don't rely on them alone for highly sensitive repos. Check the diagrams before sharing them.
- **Accuracy:** diagrams are drawn from reading the code, without running it. Check them against what you know, especially anything dashed or listed as an assumption.
- **Cost:** on small repos of 45 to 70 tracked files, each diagram took about 3 minutes and cost about $1 in Claude usage. Larger repos may cost more, so consider passing a scope.

## Troubleshooting

| Problem | Fix |
|---|---|
| Commands don't appear | Run `/plugin` to check that it's installed and enabled, then restart Claude Code. |
| `Unknown command: /architecture` | Use the full name, `/drawio-diagrams:architecture`. |
| `python3: command not found` | Install Python 3. On a Mac, run `xcode-select --install`. |
| "draw.io desktop was not found" | Export is optional, and the `.drawio` file is fine. Install draw.io desktop, or export from the app. To use a non-standard install location, set `DRAWIO_BIN` to its path. |
| Export says "Skipped" | The image is newer than its source. Add `--force` to replace it. |
| Layout looks cluttered | Ask Claude to adjust it, narrow the scope, or drag shapes in draw.io. The validator checks structure, not appearance. |
| Validator reports `root element must be <mxfile>` | Run it on the `.drawio` source rather than an exported image. |
| Many permission prompts | Approve repeated read-only commands for the session, or allow them in your settings. |

## Develop locally

To load the plugin from a checkout for one session, run this from the folder containing it:

```bash
claude --plugin-dir ./drawio-diagrams
```

To check your changes:

```bash
claude plugin validate ./drawio-diagrams
python3 ./drawio-diagrams/scripts/validate_drawio.py ./drawio-diagrams/skills/drawio-diagram/references/example.drawio
```

See [CHANGELOG.md](CHANGELOG.md) for release history.
