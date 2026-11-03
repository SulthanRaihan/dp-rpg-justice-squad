"""Helper to build draw.io files using the native UML Class template
(swimlane title + stacked attribute/operation compartments)."""

NAVY = "#1f3a5f"
FILL = "#dae8fc"

class Diagram:
    def __init__(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height
        self.cells = []
        self._id = 0

    def nid(self, prefix="c"):
        self._id += 1
        return f"{prefix}{self._id}"

    def add_class(self, x, y, w, title, fields=None, methods=None, stereotype=None,
                  fill=FILL, stroke=NAVY, title_extra_h=0):
        fields = fields or []
        methods = methods or []
        cid = self.nid("cls")
        start_size = 26 + (16 if stereotype else 0) + title_extra_h
        value = title if not stereotype else f"&#171;{stereotype}&#187;&lt;br&gt;&lt;b&gt;{title}&lt;/b&gt;"
        self.cells.append(
            f'<mxCell id="{cid}" value="{value}" '
            f'style="swimlane;fontStyle=1;html=1;align=center;verticalAlign=top;'
            f'childLayout=stackLayout;horizontal=1;startSize={start_size};horizontalStack=0;'
            f'resizeParent=0;resizeParentMax=0;collapsible=0;swimlaneFillColor=#ffffff;'
            f'fillColor={fill};strokeColor={stroke};fontSize=12;" '
            f'vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" as="geometry" />'  # height set below
            f'</mxCell>'
        )
        cell_idx = len(self.cells) - 1
        body_h = start_size

        def add_compartment(lines):
            nonlocal body_h
            if not lines:
                return
            h = max(20, 16 * len(lines) + 8)
            text = "&#10;".join(lines)
            comp_id = self.nid("cmp")
            self.cells.append(
                f'<mxCell id="{comp_id}" value="{text}" '
                f'style="text;align=left;verticalAlign=top;spacingLeft=6;spacingTop=-6;'
                f'spacingBottom=-6;whiteSpace=wrap;overflow=hidden;fontSize=11;'
                f'fontFamily=Consolas;html=0;" vertex="1" parent="{cid}">'
                f'<mxGeometry y="{body_h}" width="{w}" height="{h}" as="geometry" />'
                f'</mxCell>'
            )
            body_h += h

        add_compartment(fields)
        add_compartment(methods)
        if not fields and not methods:
            body_h += 4  # tiny padding so empty classes aren't a bare title bar

        # patch the geometry height now that we know body_h
        self.cells[cell_idx] = self.cells[cell_idx].replace(
            'as="geometry" /></mxCell>',
            f'height="{body_h}" as="geometry" /></mxCell>'
        )

        box = type("Box", (), {})()
        box.id, box.x, box.y, box.w, box.h = cid, x, y, w, body_h
        box.left, box.right = x, x + w
        box.top, box.bottom = y, y + body_h  # NOTE: y grows downward here
        box.cx, box.cy = x + w / 2, y + body_h / 2
        return box

    def edge(self, src, dst, kind, exit_xy=None, entry_xy=None, label=None, label_pos=None, route=None):
        eid = self.nid("e")
        edge_style = "edgeStyle=orthogonalEdgeStyle;rounded=0;" if route == "orthogonal" else "edgeStyle=none;rounded=0;"
        common = "html=1;" + edge_style
        if kind == "realize":
            style = common + "dashed=1;endArrow=block;endFill=0;endSize=14;startArrow=none;"
        elif kind == "inherit":
            style = common + "endArrow=block;endFill=0;endSize=14;startArrow=none;"
        elif kind == "composition":
            style = common + "startArrow=diamondThin;startFill=1;endArrow=none;"
        elif kind == "aggregation":
            style = common + "startArrow=diamondThin;startFill=0;endArrow=none;"
        elif kind == "dependency":
            style = common + "dashed=1;endArrow=open;endFill=0;endSize=10;startArrow=none;"
        else:  # association
            style = common + "endArrow=none;startArrow=none;"
        if exit_xy:
            style += f"exitX={exit_xy[0]};exitY={exit_xy[1]};exitDx=0;exitDy=0;"
        if entry_xy:
            style += f"entryX={entry_xy[0]};entryY={entry_xy[1]};entryDx=0;entryDy=0;"
        val = f' value="{label}"' if label else ""
        if label and label_pos:
            style += f"labelBackgroundColor=#ffffff;"
        self.cells.append(
            f'<mxCell id="{eid}"{val} style="{style}" edge="1" parent="1" '
            f'source="{src}" target="{dst}">'
            f'<mxGeometry relative="1" as="geometry" />'
            f'</mxCell>'
        )

    def text(self, x, y, w, h, value, size=12, color="#555555", align="center"):
        tid = self.nid("t")
        self.cells.append(
            f'<mxCell id="{tid}" value="{value}" '
            f'style="text;html=1;align={align};verticalAlign=middle;fontColor={color};fontSize={size};" '
            f'vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />'
            f'</mxCell>'
        )

    def save(self, path):
        body = "\n        ".join(self.cells)
        xml = f"""<mxfile host="app.diagrams.net" modified="2026-06-23T00:00:00.000Z" agent="claude-code" version="24.0.0" type="device">
  <diagram name="{self.name}" id="{self.name.lower().replace(' ', '-')}">
    <mxGraphModel dx="1024" dy="700" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{self.width}" pageHeight="{self.height}" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        {body}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(xml)
        print("saved", path)
