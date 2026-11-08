# Layout

Plain `.drawio` files have no layout pass and no obstacle-aware routing. draw.io draws an edge as a simple path between its ends, so it runs straight through any shape in the way. Prevent this through placement.

## Grid and spacing

- Place every `x`, `y`, `width` and `height` on a multiple of 20. Set `gridSize="20"`.
- Start a default layout at `x = 40`, with columns 200 apart and rows 120 apart.
- Keep at least 40 between sibling shapes.
- Leave at least 80 along an edge that carries a label, and a free column for labels longer than one word.
- Keep a child at least 20 from the sides and bottom of its container.

## Direction

Pick one direction per diagram.

| Diagram | Direction |
|---|---|
| Architecture | Top to bottom, one row per tier: clients, entry, services, data |
| Flow | Top to bottom; side branches go into the next column |
| Pipeline | Left to right, wrapping to a new row after about five steps |
| ERD | Most-referenced table in the middle, referencing tables around it |
| Sequence | Actors left to right; time runs top to bottom |

## Placement

- Put connected shapes in neighbouring cells. An edge crossing two or more cells means a shape is misplaced.
- Put a shape with many connections in the middle of what it connects.
- Put a service's own data store directly below it.
- Put shared queues and event buses in a row or bar of their own, never between a service and its own database.
- Keep shapes of one kind the same size.
- Avoid edges that overlap each other or pile labels on one side of a shape.
- Do not repeat one label across parallel edges. Label one of them, or none if the meaning is obvious.
- When a relationship applies to every member of a container, attach one edge to the container rather than one per member.

## ERD and sequence spacing

- **ERD:** Use tables 200 wide with a free 160 between neighbours (`x = 40, 400, 760`), and at most three in a row. Leave at least 60 between rows. Place a table that references another beside or under it.
- **Sequence:** Space lifelines 240 apart (`x = 40, 280, 520`), and shorten labels to fit. Keep to about 20 messages per diagram. Cover the main path plus one or two important failures, and split anything longer.

## Containers and swimlanes

- Group layers, modules and deployment zones in containers, with the members as children using `parent`.
- Do not fake containment by drawing a shape on top of a larger one.
- Keep external systems and actors outside implementation containers.
- Size a container to its children: `height >= startSize + 20 + content + 20`.
- Keep nesting to two levels at most.
- Keep edges from crossing a container's title text. Container titles are centred, so when an edge enters near the middle, add `align=left;spacingLeft=10;` to the container's style.
- A label sits at the middle of its edge by default, so on an edge entering a container it can land on the border. Move it along the edge with `x` on the edge's `mxGeometry`, from -1 (source) to 1 (target), as in `x="-0.4"`.
- For multi-role flows, stack flat horizontal swimlanes with `horizontal=0;` and give each role one row. Do not nest lanes inside a pool.

## Size limits

- Keep to about 25 nodes per page, excluding the title, legend and footer.
- Beyond that, split the content in one of two ways:
  - Add an overview page plus one page per module, in the same file.
  - Create separate diagrams, one per subsystem.
- Name each page after what it shows. Link pages by naming the related page in a label or note.

## Title, legend and footer

- Put the title at the top left, at about `y = 20`.
- Put the legend directly below the content, with one swatch per colour or text entry per line style used. Omit anything unused.
- Put the footer in the bottom row, below the legend, left aligned.
- Keep these cells clear of nodes and edges.
