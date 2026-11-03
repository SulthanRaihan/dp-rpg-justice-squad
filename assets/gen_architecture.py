from diagram_lib import *

fig, ax = new_fig(1100, 760)

# Row 1: entry points
game = package_box(ax, 380, 740, 340, 70, "Game.java / Main.java\n(Client / Entry Point)", fc="#fdf3e6", ec="#b9770e")

# Row 2: orchestration-level patterns used directly by the client
factory = package_box(ax, 40, 600, 220, 70, "hero.factory")
command = package_box(ax, 300, 600, 220, 70, "hero.command")
composite = package_box(ax, 560, 600, 220, 70, "hero.composite")
singleton = package_box(ax, 820, 600, 220, 70, "hero.singleton")

# Row 3: shared domain core
core = package_box(ax, 380, 440, 340, 80, "hero.core\n(Hero, Villain)", fc="#eafaf1", ec=GREEN)

# Row 4: patterns composed inside Hero
strategy = package_box(ax, 40, 280, 220, 70, "hero.strategy")
decorator = package_box(ax, 300, 280, 220, 70, "hero.decorator")
state = package_box(ax, 560, 280, 220, 70, "hero.state")
observer = package_box(ax, 820, 280, 220, 70, "hero.observer")

# arrows: Game.java depends on the 4 orchestration packages
for pkg in [factory, command, composite, singleton]:
    dependency(ax, (game.cx, game.bottom), (pkg.cx, pkg.top))

# arrows: orchestration packages operate on hero.core
for pkg in [factory, command, composite]:
    dependency(ax, (pkg.cx, pkg.bottom), (core.cx + (pkg.cx - core.cx) * 0.25, core.top))
# singleton does not touch core directly (it only counts events) -> dashed dependency from Game instead
dependency(ax, (singleton.left, singleton.bottom), (game.right - 10, game.bottom + 4))

# arrows: hero.core composes the 4 internal patterns
for pkg in [strategy, decorator, state, observer]:
    composition(ax, (core.cx + (pkg.cx - core.cx) * 0.25, core.bottom), (pkg.cx, pkg.top))

ax.text(550, 30, "Figure 1. Package Architecture - Justice Squad Superhero Battle",
        ha="center", va="bottom", fontsize=10, color="#555555")

save(fig, "architecture_diagram.png")
