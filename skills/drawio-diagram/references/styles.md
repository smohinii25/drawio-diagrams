# Styles

Use the same colour for the same kind of element across all diagrams. Change a colour or line style only when it means something different, and name it in the legend.

## Layer colours

Use these in architecture diagrams, and wherever else nodes represent a layer.

| Layer | Examples | `fillColor` | `strokeColor` |
|---|---|---|---|
| Frontend / client | Web app, mobile app, CLI, browser | `#dae8fc` | `#6c8ebf` |
| Backend / service | API, worker, cron job, function | `#d5e8d4` | `#82b366` |
| Data store | SQL or NoSQL database, cache, object storage | `#e1d5e7` | `#9673a6` |
| Queue / events | Message queue, event bus, stream | `#fff2cc` | `#d6b656` |
| External | Third-party API, SaaS, identity provider | `#ffe6cc` | `#d79b00` |
| Infrastructure | CI/CD, load balancer, CDN, gateway | `#eeeeee` | `#666666` |

## Node shapes

Append the layer colours to each style.

| Element | Style | Size |
|---|---|---|
| Component | `rounded=1;whiteSpace=wrap;html=1;` | 140×60 |
| Data store | `shape=cylinder3;boundedLbl=1;size=12;whiteSpace=wrap;html=1;` | 140×80 |
| Queue / events | `rounded=1;arcSize=50;whiteSpace=wrap;html=1;` | 140×60 |
| Person / actor | `shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;` | 30×60 |

## Flow elements

| Element | Style | `fillColor` / `strokeColor` | Size |
|---|---|---|---|
| Start / end | `rounded=1;arcSize=50;whiteSpace=wrap;html=1;` | `#d5e8d4` / `#82b366` | 120×40 |
| Step | `rounded=1;whiteSpace=wrap;html=1;` | `#dae8fc` / `#6c8ebf` | 140×60 |
| Decision | `rhombus;whiteSpace=wrap;html=1;` | `#fff2cc` / `#d6b656` | 160×100 |
| Error | `rounded=1;whiteSpace=wrap;html=1;` | `#f8cecc` / `#b85450` | 140×60 |

Keep decision text to about four words so it fits inside the diamond.

## ERD tables

Each table is a container with one child row per column. Use the data store colours on the table.

```xml
<mxCell id="t-article" value="Article" style="swimlane;fontStyle=1;childLayout=stackLayout;horizontalStack=0;resizeParent=1;resizeParentMax=0;startSize=30;collapsible=0;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
  <mxGeometry x="400" y="40" width="200" height="108" as="geometry"/>
</mxCell>
<mxCell id="t-article-id" value="PK id: Int" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;html=1;portConstraint=eastwest;fontStyle=1;" vertex="1" parent="t-article">
  <mxGeometry y="30" width="200" height="26" as="geometry"/>
</mxCell>
<mxCell id="t-article-author" value="FK authorId: Int" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;html=1;portConstraint=eastwest;fontStyle=2;" vertex="1" parent="t-article">
  <mxGeometry y="56" width="200" height="26" as="geometry"/>
</mxCell>
```

- Set row `y = 30 + index × 26`, and table `height = 30 + rows × 26`. Tables are the one exception to the 20px grid.
- Mark key columns in the text: `PK id: Int` in bold (`fontStyle=1`), `FK authorId: Int` in italic (`fontStyle=2`), and unique columns with `(UQ)`.

Connect the foreign-key row (source) to the primary-key row (target), with no label. The row ids make each line meet the table at the right column.

```xml
<mxCell id="rel-article-user" style="edgeStyle=entityRelationEdgeStyle;html=1;startArrow=ERzeroToMany;startFill=0;endArrow=ERmandOne;endFill=0;strokeColor=#666666;" edge="1" parent="1" source="t-article-author" target="t-user-id">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

| Each end means | Arrow value |
|---|---|
| Exactly one | `ERmandOne` |
| Zero or one | `ERzeroToOne` |
| One or many | `ERoneToMany` |
| Zero or many | `ERzeroToMany` |

Set each end from the schema. A nullable foreign key points at `ERzeroToOne` rather than `ERmandOne`.

## Sequence diagrams

Each participant is a lifeline with its layer colour. Position each message using a pixel offset from the top of its lifeline, with `exitDy` and `entryDy`.

```xml
<mxCell id="ll-api" value="API" style="shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;html=1;container=0;collapsible=0;size=40;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
  <mxGeometry x="280" y="60" width="140" height="440" as="geometry"/>
</mxCell>
<mxCell id="msg-1" value="1. POST /users" style="html=1;verticalAlign=bottom;endArrow=block;endFill=1;strokeColor=#666666;rounded=0;exitX=0.5;exitY=0;exitDx=0;exitDy=80;exitPerimeter=0;entryX=0.5;entryY=0;entryDx=0;entryDy=80;entryPerimeter=0;" edge="1" parent="1" source="ll-client" target="ll-api">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

- Set `exitDy` and `entryDy` to the same value on a message, increasing by 40 per message. Start at 80, with `size=40` for the header.
- All lifelines share one `y` and one `height`, which must extend at least 40 past the last message.
- For a return message, use `endArrow=open;endFill=0;dashed=1;`.
- For an error message, also use `strokeColor=#b85450;`.
- Number messages in order, as `1.`, `2.`, `3.`, in the label.

For a self-call, keep `source` and `target` the same and step `entryDy` 40 past `exitDy`. Use `align=left;spacingLeft=4;` in place of `verticalAlign=bottom;`. The waypoints are page coordinates, 60 right of the lifeline's centre, at `lifeline y + exitDy` and `lifeline y + entryDy`:

```xml
<mxCell id="msg-4" value="4. sign JWT" style="html=1;align=left;spacingLeft=4;endArrow=block;endFill=1;strokeColor=#666666;rounded=0;exitX=0.5;exitY=0;exitDx=0;exitDy=200;exitPerimeter=0;entryX=0.5;entryY=0;entryDx=0;entryDy=240;entryPerimeter=0;" edge="1" parent="1" source="ll-api" target="ll-api">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="410" y="260"/>
      <mxPoint x="410" y="300"/>
    </Array>
  </mxGeometry>
</mxCell>
```

For a conditional block, draw a frame around its messages and name the condition in `value`, such as `alt: invalid input`, with a `width` that fits it. Start the frame at least 100 left of the first lifeline's centre, so the title tab clears the line:

```
shape=umlFrame;whiteSpace=wrap;html=1;width=140;height=24;strokeColor=#999999;
```

## Edges

Use this base style for all connectors, except in diagram types that define their own:

```
edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=block;endFill=1;strokeColor=#666666;fontColor=#333333;labelBackgroundColor=default;
```

| Meaning | Add to base |
|---|---|
| Synchronous call | Nothing |
| Asynchronous or event | `dashed=1;` |
| Inferred, not seen in code | `dashed=1;strokeColor=#b85450;` |
| Yes / success branch | `fontColor=#2D7600;` |
| No / failure branch | `fontColor=#B20000;` |

Keep edge labels to one to three words that say what flows, such as `HTTPS`, `publishes` or `No`.

## Containers

```
swimlane;startSize=30;html=1;fontStyle=1;fillColor=#f9f9f9;strokeColor=#999999;
```

Use the same pale grey for every container unless the legend gives a tint a meaning.

## Text cells

| Use | Style |
|---|---|
| Title | `text;html=1;align=left;verticalAlign=middle;fontSize=18;fontStyle=1;whiteSpace=wrap;` |
| Legend swatch | `rounded=1;html=1;fontSize=10;` plus the layer colours |
| Legend text | `text;html=1;align=left;verticalAlign=middle;fontSize=10;fontColor=#666666;whiteSpace=wrap;` |
| Footer | `text;html=1;align=left;verticalAlign=middle;fontSize=10;fontColor=#666666;whiteSpace=wrap;` |
