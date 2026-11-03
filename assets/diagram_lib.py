import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Ellipse, Rectangle, FancyBboxPatch
import textwrap

NAVY = "#1f3a5f"
BLUE = "#2f6fa3"
LIGHT = "#eaf2f8"
GREY = "#444444"
RED = "#b03a2e"
GREEN = "#1e8449"


def new_fig(w, h, dpi=150):
    fig, ax = plt.subplots(figsize=(w / 100, h / 100), dpi=dpi)
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    ax.set_aspect("equal")
    return fig, ax


def actor(ax, x, y, label, scale=1.0):
    s = 14 * scale
    head_r = s * 0.6
    ax.add_patch(plt.Circle((x, y + s * 3.2), head_r, fill=False, ec=GREY, lw=1.8))
    ax.plot([x, x], [y + s * 2.6, y + s * 1.0], color=GREY, lw=1.8)
    ax.plot([x - s * 1.1, x + s * 1.1], [y + s * 2.1, y + s * 2.1], color=GREY, lw=1.8)
    ax.plot([x, x - s * 1.0], [y + s * 1.0, y - s * 0.6], color=GREY, lw=1.8)
    ax.plot([x, x + s * 1.0], [y + s * 1.0, y - s * 0.6], color=GREY, lw=1.8)
    ax.text(x, y - s * 1.4, label, ha="center", va="top", fontsize=9.5, color="black", weight="bold")


def usecase(ax, x, y, label, w=150, h=46, fc=LIGHT, ec=NAVY, fontsize=9, lw=1.4):
    e = Ellipse((x, y), w, h, fc=fc, ec=ec, lw=lw, zorder=3)
    ax.add_patch(e)
    wrapped = textwrap.fill(label, width=18)
    ax.text(x, y, wrapped, ha="center", va="center", fontsize=fontsize, zorder=4, color="black")
    return e


def boundary(ax, x, y, w, h, label):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=8",
                          fc="white", ec=NAVY, lw=1.6, zorder=1)
    ax.add_patch(box)
    ax.text(x + w / 2, y + h - 14, label, ha="center", va="top", fontsize=11, weight="bold", color=NAVY, zorder=2)


def association(ax, p1, p2, color=GREY):
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, lw=1.3, zorder=2)


def arrow(ax, p1, p2, style="-|>", color=GREY, dashed=False, lw=1.3, connectionstyle="arc3,rad=0.0"):
    ls = "dashed" if dashed else "solid"
    a = FancyArrowPatch(p1, p2, arrowstyle=style, color=color, lw=lw,
                         linestyle=ls, connectionstyle=connectionstyle,
                         mutation_scale=14, zorder=2)
    ax.add_patch(a)
    return a


def generalization(ax, child, parent, color=GREY):
    # hollow triangle pointing to parent (UML generalization)
    arrow(ax, child, parent, style="-|>", color=color, lw=1.3)


def label_mid(ax, p1, p2, text, dy=8, fontsize=8, italic=True, color="black"):
    mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
    ax.text(mx, my + dy, text, ha="center", va="bottom", fontsize=fontsize,
            style="italic" if italic else "normal", color=color,
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))


def classbox(ax, x, y, w, h, title, fields=None, methods=None, stereotype=None,
             title_fc="#dbe9f5", body_fc="white", ec=NAVY, fontsize=8.5, title_fontsize=9.5):
    """Top-left corner at (x, y) [matplotlib y grows up, so y is the TOP edge]."""
    fields = fields or []
    methods = methods or []
    title_h = 30 if not stereotype else 42
    box = Rectangle((x, y - h), w, h, fc=body_fc, ec=ec, lw=1.3, zorder=3)
    ax.add_patch(box)
    title_box = Rectangle((x, y - title_h), w, title_h, fc=title_fc, ec=ec, lw=1.3, zorder=4)
    ax.add_patch(title_box)
    ty = y - title_h / 2
    if stereotype:
        ax.text(x + w / 2, y - 12, stereotype, ha="center", va="center", fontsize=fontsize - 1,
                 style="italic", zorder=5)
        ax.text(x + w / 2, y - title_h + 12, title, ha="center", va="center",
                 fontsize=title_fontsize, weight="bold", zorder=5)
    else:
        ax.text(x + w / 2, ty, title, ha="center", va="center", fontsize=title_fontsize,
                 weight="bold", zorder=5)

    cur_y = y - title_h
    if fields:
        ax.plot([x, x + w], [cur_y, cur_y], color=ec, lw=1.0, zorder=4)
        for f in fields:
            cur_y -= 16
            ax.text(x + 8, cur_y + 4, f, ha="left", va="center", fontsize=fontsize, zorder=5, family="monospace")
        cur_y -= 6
    if methods:
        ax.plot([x, x + w], [cur_y, cur_y], color=ec, lw=1.0, zorder=4)
        for m in methods:
            cur_y -= 16
            ax.text(x + 8, cur_y + 4, m, ha="left", va="center", fontsize=fontsize, zorder=5, family="monospace")

    class Box:
        pass
    b = Box()
    b.x, b.y, b.w, b.h = x, y, w, h
    b.left = x
    b.right = x + w
    b.top = y
    b.bottom = y - h
    b.cx = x + w / 2
    b.cy = y - h / 2
    return b


def realization(ax, child_pt, parent_pt, color=GREY):
    """Dashed line, hollow triangle head (implements interface)."""
    arrow(ax, child_pt, parent_pt, style="-|>", dashed=True, color=color)


def inheritance(ax, child_pt, parent_pt, color=GREY):
    """Solid line, hollow triangle head (extends class)."""
    arrow(ax, child_pt, parent_pt, style="-|>", dashed=False, color=color)


def _diamond(ax, tip, direction, filled, color, size=9):
    import numpy as np
    dx, dy = direction
    norm = (dx ** 2 + dy ** 2) ** 0.5
    ux, uy = dx / norm, dy / norm
    px, py = -uy, ux
    p_tip = (tip[0], tip[1])
    p_back = (tip[0] + ux * size * 2, tip[1] + uy * size * 2)
    p_side1 = (tip[0] + ux * size, tip[1] + uy * size + py * size * 0.6 + px * size * 0.6)
    p_side2 = (tip[0] + ux * size, tip[1] + uy * size - py * size * 0.6 - px * size * 0.6)
    diamond = mpatches.Polygon([p_tip, p_side1, p_back, p_side2], closed=True,
                                fc=color if filled else "white", ec=color, lw=1.2, zorder=5)
    ax.add_patch(diamond)
    return p_back


def composition(ax, owner_pt, part_pt, color=GREY):
    """Solid line, filled diamond at owner side."""
    direction = (part_pt[0] - owner_pt[0], part_pt[1] - owner_pt[1])
    back = _diamond(ax, owner_pt, direction, filled=True, color=color)
    ax.plot([back[0], part_pt[0]], [back[1], part_pt[1]], color=color, lw=1.3, zorder=2)


def aggregation(ax, owner_pt, part_pt, color=GREY):
    """Solid line, open diamond at owner side."""
    direction = (part_pt[0] - owner_pt[0], part_pt[1] - owner_pt[1])
    back = _diamond(ax, owner_pt, direction, filled=False, color=color)
    ax.plot([back[0], part_pt[0]], [back[1], part_pt[1]], color=color, lw=1.3, zorder=2)


def dependency(ax, src_pt, dst_pt, color=GREY):
    """Dashed line, open arrow head (uses)."""
    arrow(ax, src_pt, dst_pt, style="->", dashed=True, color=color)


def package_box(ax, x, y, w, h, title, fc="#eaf2f8", ec=NAVY, fontsize=10.5):
    """UML package symbol: rectangle with a small tab on the top-left. Top-left corner at (x, y)."""
    tab_w, tab_h = min(110, w * 0.45), 18
    body = Rectangle((x, y - h), w, h - tab_h, fc=fc, ec=ec, lw=1.4, zorder=3)
    tab = Rectangle((x, y - tab_h), tab_w, tab_h, fc=fc, ec=ec, lw=1.4, zorder=3)
    ax.add_patch(body)
    ax.add_patch(tab)
    ax.text(x + w / 2, y - tab_h - (h - tab_h) / 2, title, ha="center", va="center",
            fontsize=fontsize, weight="bold", zorder=5)

    class Box:
        pass
    b = Box()
    b.x, b.y, b.w, b.h = x, y, w, h
    b.left, b.right = x, x + w
    b.top, b.bottom = y, y - h
    b.cx, b.cy = x + w / 2, y - h / 2
    return b


def save(fig, path):
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    print("saved", path)
