from diagram_lib import *

def caption(ax, x, y, text):
    ax.text(x, y, text, ha="center", va="bottom", fontsize=9, color="#555555")

# ---------------------------------------------------------------- 1. STRATEGY
fig, ax = new_fig(820, 540)
iface = classbox(ax, 290, 520, 240, 100, "CombatStyle", stereotype="<<interface>>",
                  methods=["+name(): String", "+attackDamage(p): int", "+damageBlocked(d): int"])
agg = classbox(ax, 30, 340, 200, 88, "AggressiveStyle", methods=["+name(): String", "+attackDamage(p): int", "+damageBlocked(d): int"])
de = classbox(ax, 300, 340, 200, 88, "DefensiveStyle", methods=["+name(): String", "+attackDamage(p): int", "+damageBlocked(d): int"])
ta = classbox(ax, 570, 340, 220, 88, "TacticalStyle", methods=["+name(): String", "+attackDamage(p): int", "+damageBlocked(d): int"])
hero = classbox(ax, 290, 190, 240, 78, "Hero", fields=["-style: CombatStyle"], methods=["+attack(v): int"])

realization(ax, (agg.cx, agg.top), (iface.left + 30, iface.bottom))
realization(ax, (de.cx, de.top), (iface.cx, iface.bottom))
realization(ax, (ta.cx, ta.top), (iface.right - 30, iface.bottom))
aggregation(ax, (hero.cx, hero.top), (iface.cx, iface.bottom - 110))
caption(ax, 410, 20, "Figure 3a. Strategy - CombatStyle family used by Hero")
save(fig, "uml_strategy.png")

# ---------------------------------------------------------------- 2. FACTORY METHOD
fig, ax = new_fig(900, 480)
creator = classbox(ax, 330, 460, 260, 100, "HeroFactory", stereotype="<<abstract>>",
                    methods=["+recruit(name): Hero", "#createHero(name): Hero {abstract}", "#heroType(): String {abstract}"])
spd = classbox(ax, 40, 260, 230, 72, "SpeedsterFactory", methods=["#createHero(name): Hero", "#heroType(): String"])
tnk = classbox(ax, 330, 260, 230, 72, "TankFactory", methods=["#createHero(name): Hero", "#heroType(): String"])
mge = classbox(ax, 620, 260, 230, 72, "MageFactory", methods=["#createHero(name): Hero", "#heroType(): String"])
hero = classbox(ax, 350, 120, 190, 44, "Hero")

inheritance(ax, (spd.cx, spd.top), (creator.left + 35, creator.bottom))
inheritance(ax, (tnk.cx, tnk.top), (creator.cx, creator.bottom))
inheritance(ax, (mge.cx, mge.top), (creator.right - 35, creator.bottom))
dependency(ax, (creator.cx, creator.bottom - 150), (hero.cx, hero.top))
ax.text(creator.cx + 14, creator.bottom - 190, "<<creates>>", fontsize=8, style="italic")
caption(ax, 450, 20, "Figure 3b. Factory Method - HeroFactory and concrete creators")
save(fig, "uml_factory.png")

# ---------------------------------------------------------------- 3. OBSERVER
fig, ax = new_fig(900, 560)
subj_i = classbox(ax, 40, 540, 250, 84, "ThreatSubject", stereotype="<<interface>>",
                   methods=["+addObserver(o)", "+removeObserver(o)"])
obs_i = classbox(ax, 420, 540, 260, 68, "AlertObserver", stereotype="<<interface>>",
                  methods=["+onThreat(loc, danger)"])
sys_ = classbox(ax, 40, 380, 250, 78, "AlertSystem", fields=["-observers: List<AlertObserver>"],
                methods=["+broadcastThreat(loc, d)"])
hero = classbox(ax, 330, 240, 200, 44, "Hero")
news = classbox(ax, 600, 240, 230, 44, "NewsReporter")

realization(ax, (sys_.cx, sys_.top), (subj_i.cx, subj_i.bottom))
realization(ax, (hero.cx, hero.top), (obs_i.left + 60, obs_i.bottom))
realization(ax, (news.cx, news.top), (obs_i.right - 60, obs_i.bottom))
aggregation(ax, (sys_.right, sys_.top - 10), (obs_i.left, obs_i.cy - 230))
caption(ax, 450, 20, "Figure 3c. Observer - AlertSystem notifies Hero and NewsReporter")
save(fig, "uml_observer.png")

# ---------------------------------------------------------------- 4. DECORATOR
fig, ax = new_fig(900, 560)
gear_i = classbox(ax, 330, 540, 240, 84, "Gear", stereotype="<<interface>>",
                   methods=["+description(): String", "+powerBonus(): int"])
basic = classbox(ax, 60, 380, 200, 72, "BasicGear", methods=["+description()", "+powerBonus()"])
upg = classbox(ax, 330, 380, 240, 74, "GearUpgrade", stereotype="<<abstract>>", fields=["#inner: Gear"])
cape = classbox(ax, 620, 300, 200, 44, "CapeUpgrade")
shield = classbox(ax, 620, 220, 200, 44, "ShieldUpgrade")
gadget = classbox(ax, 620, 140, 200, 44, "GadgetUpgrade")

realization(ax, (basic.cx, basic.top), (gear_i.left + 40, gear_i.bottom))
realization(ax, (upg.cx, upg.top), (gear_i.cx, gear_i.bottom))
inheritance(ax, (cape.cx, cape.top), (upg.right - 10, upg.bottom + 5))
inheritance(ax, (shield.cx, shield.top), (upg.right, upg.cy))
inheritance(ax, (gadget.cx, gadget.top), (upg.right - 10, upg.bottom - 60))
composition(ax, (upg.left, upg.cy), (basic.right, basic.cy))
caption(ax, 450, 20, "Figure 3d. Decorator - Gear wrapped by stacked upgrades")
save(fig, "uml_decorator.png")

# ---------------------------------------------------------------- 5. STATE
fig, ax = new_fig(900, 580)
state_i = classbox(ax, 320, 560, 260, 116, "HeroState", stereotype="<<interface>>",
                    methods=["+name(): String", "+describe(): String", "+canAct(): boolean", "+powerPercent(): int"])
av = classbox(ax, 10, 360, 200, 44, "AvailableState")
om = classbox(ax, 230, 360, 200, 44, "OnMissionState")
inj = classbox(ax, 460, 360, 190, 44, "InjuredState")
ret = classbox(ax, 670, 360, 200, 44, "RetiredState")
ctx = classbox(ax, 280, 200, 300, 126, "HeroContext", fields=["-hero: Hero", "-state: HeroState", "-inBattle: boolean"],
               methods=["+autoUpdate()", "+setState(s)"])

realization(ax, (av.cx, av.top), (state_i.left + 30, state_i.bottom))
realization(ax, (om.cx, om.top), (state_i.cx - 50, state_i.bottom))
realization(ax, (inj.cx, inj.top), (state_i.cx + 50, state_i.bottom))
realization(ax, (ret.cx, ret.top), (state_i.right - 30, state_i.bottom))
composition(ax, (ctx.cx, ctx.top), (state_i.cx, state_i.bottom - 160))
caption(ax, 450, 20, "Figure 3e. State - HeroContext delegates to the current HeroState")
save(fig, "uml_state.png")

# ---------------------------------------------------------------- 6. COMMAND
fig, ax = new_fig(950, 560)
cmd_i = classbox(ax, 350, 540, 250, 100, "Command", stereotype="<<interface>>",
                  methods=["+execute()", "+undo()", "+description(): String"])
atk = classbox(ax, 60, 350, 210, 44, "AttackCommand")
dfd = classbox(ax, 320, 350, 210, 44, "DefendCommand")
abl = classbox(ax, 580, 350, 240, 44, "UseAbilityCommand")
inv = classbox(ax, 320, 200, 260, 94, "CommandHistory", fields=["-history: Deque<Command>"],
               methods=["+execute(cmd)", "+undoLast()"])
recv = classbox(ax, 650, 200, 220, 44, "Hero / Villain")

realization(ax, (atk.cx, atk.top), (cmd_i.left + 50, cmd_i.bottom))
realization(ax, (dfd.cx, dfd.top), (cmd_i.cx, cmd_i.bottom))
realization(ax, (abl.cx, abl.top), (cmd_i.right - 50, cmd_i.bottom))
aggregation(ax, (inv.cx, inv.top), (cmd_i.cx - 60, cmd_i.bottom - 140))
dependency(ax, (atk.cx + 70, atk.bottom), (recv.left, recv.top - 10))
caption(ax, 470, 20, "Figure 3f. Command - CommandHistory invokes undoable Commands")
save(fig, "uml_command.png")

# ---------------------------------------------------------------- 7. COMPOSITE
fig, ax = new_fig(900, 540)
comp_i = classbox(ax, 320, 520, 260, 116, "RosterComponent", stereotype="<<interface>>",
                   methods=["+getName(): String", "+awardXp(amt)", "+getTotalXp(): int", "+print(indent)"])
leaf = classbox(ax, 70, 320, 230, 62, "HeroMember", fields=["-hero: Hero"])
team = classbox(ax, 480, 320, 270, 94, "Team", fields=["-members: List<RosterComponent>"],
                methods=["+add(c)", "+remove(c)"])

realization(ax, (leaf.cx, leaf.top), (comp_i.left + 50, comp_i.bottom))
realization(ax, (team.cx, team.top), (comp_i.right - 60, comp_i.bottom))
composition(ax, (team.right, team.cy), (team.right + 60, team.cy))
ax.plot([team.right + 60, team.right + 60], [team.cy, comp_i.bottom - 60], color=GREY, lw=1.3, zorder=2)
arrow(ax, (team.right + 60, comp_i.bottom - 60), (comp_i.right - 5, comp_i.bottom - 5), style="-|>", color=GREY,
      connectionstyle="arc3,rad=-0.3")
ax.text(team.right + 70, team.cy - 24, "0..*\n(recursive)", fontsize=7.5)
caption(ax, 450, 20, "Figure 3g. Composite - Team nests HeroMembers or other Teams")
save(fig, "uml_composite.png")

# ---------------------------------------------------------------- 8. SINGLETON
fig, ax = new_fig(820, 480)
hq = classbox(ax, 250, 460, 320, 158, "HeroHQ",
              fields=["-heroesRecruited: int", "-villainsDefeated: int"],
              methods=["-HeroHQ()", "+static getInstance(): HeroHQ", "+recordRecruit()", "+recordVictory()", "+printReport()"])
holder = classbox(ax, 290, 220, 240, 74, "Holder", stereotype="<<static>>", fields=["+static INSTANCE: HeroHQ"])

composition(ax, (hq.cx, hq.bottom), (holder.cx, holder.top))
ax.text(hq.cx + 14, hq.bottom - 16, "lazily creates", fontsize=8, style="italic")
caption(ax, 410, 20, "Figure 3h. Singleton - HeroHQ via Initialization-on-Demand Holder")
save(fig, "uml_singleton.png")

print("All class diagrams generated.")
