# draw.io XML Format Rules

## File skeleton

Always write uncompressed XML. Each `<diagram>` holds an `<mxGraphModel>` element directly, never base64 text.

```xml
<mxfile host="drawio-diagrams" compressed="false">
  <diagram id="architecture" name="Architecture">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="20" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0" adaptiveColors="auto">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

- Cells `id="0"` and `id="1" parent="0"` are mandatory on every page and come first.
- Add one `<diagram>` per page, each with its own `id`, `name` and root cells.
- Set `pageWidth` and `pageHeight` large enough to hold the content.
- Do not write XML comments.

## Cell ids

- Keep ids unique within a page. Prefer unique across the whole file.
- Use short descriptive kebab-case ids, such as `svc-orders` or `edge-api-db`. Never reuse `0` or `1`.

## Vertices

A vertex has `vertex="1"`, a `parent`, and an `mxGeometry` with `x`, `y`, `width`, `height` and `as="geometry"`.

```xml
<mxCell id="svc-api" value="API Service" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="140" height="60" as="geometry"/>
</mxCell>
```

- Use `parent="1"` for top-level cells.
- A child's `x` and `y` are relative to the top-left corner of its container, including the title bar. Start children below the title: `y >= startSize + 20`.

## Edges

An edge has `edge="1"`, a `parent`, a `source`, a `target`, and a child `mxGeometry`. Never self-close an edge cell.

```xml
<mxCell id="edge-api-db" value="SQL" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;" edge="1" parent="1" source="svc-api" target="db-main">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

- `source` and `target` must name existing vertices on the same page.
- Set the edge `parent` to the innermost container holding both ends, or `1` when an end is at the top level.
- Do not add waypoints unless an edge would otherwise cross a shape.

## Edge label cells

To place extra text along an edge, such as a cardinality, add a child vertex of the edge. It uses relative geometry with no size, and `x` runs from -1 (source) to 1 (target).

```xml
<mxCell id="label-1" value="1..*" style="edgeLabel;resizable=0;html=1;align=left;verticalAlign=bottom;" vertex="1" connectable="0" parent="edge-api-db">
  <mxGeometry x="-1" relative="1" as="geometry"/>
</mxCell>
```

## Labels and escaping

Put `html=1` in every cell style. A `value` is decoded twice when `html=1` is set: once as XML, then once as HTML.

| Wanted on screen | Write in `value` |
|---|---|
| `A & B` | `A &amp; B` |
| `Say "hi"` | `Say &quot;hi&quot;` |
| `x > 0` | `x &gt; 0` |
| `List<User>` | `List&amp;lt;User&amp;gt;` |
| Bold word | `&lt;b&gt;Word&lt;/b&gt;` |
| Line break | `&lt;br&gt;` |

- Double-escape a literal `<`, including its closing `>`. Written as `List&lt;User&gt;`, the text renders as just `List`, because `<User>` is treated as an HTML tag. This affects generics, typed collections and placeholders such as `<id>`.
- Single-escape tags that are meant as formatting, such as `<b>` and `<br>`.
- Never write `\n` in a label. It renders literally.
- Use `fontStyle=1` for a fully bold label rather than `<b>` tags.

## Pre-finish checklist

The validator checks structure, but it cannot see these. Check them by reading the plan and coordinates:

- [ ] No edge passes through an unrelated shape, and no label sits on a border or another shape.
- [ ] Every node and edge is supported by the code, with inferred ones dashed.
- [ ] Each label's text fits its shape.
- [ ] Every page has a title, a legend covering what it uses, and a footer.
