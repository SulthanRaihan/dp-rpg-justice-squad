from drawio_uml_lib import Diagram

RED_FILL, RED_STROKE = "#fdecea", "#b03a2e"
GREEN_FILL, GREEN_STROKE = "#eafaf1", "#1e8449"
ORANGE_FILL, ORANGE_STROKE = "#fdf3e6", "#b9770e"

# ============================================================== 1. STRATEGY
d = Diagram("Strategy", 820, 560)
iface = d.add_class(280, 40, 240, "CombatStyle", stereotype="interface",
                     methods=["+ name(): String", "+ attackDamage(p: int): int", "+ damageBlocked(i: int): int"])
agg = d.add_class(20, 240, 220, "AggressiveStyle",
                   methods=["+ name(): String", "+ attackDamage(p: int): int", "+ damageBlocked(i: int): int"])
de = d.add_class(290, 240, 220, "DefensiveStyle",
                  methods=["+ name(): String", "+ attackDamage(p: int): int", "+ damageBlocked(i: int): int"])
ta = d.add_class(560, 240, 220, "TacticalStyle",
                  methods=["+ name(): String", "+ attackDamage(p: int): int", "+ damageBlocked(i: int): int"])
hero = d.add_class(290, 420, 220, "Hero", fields=["- style: CombatStyle"], methods=["+ attack(t: Villain): int"])

d.edge(agg.id, iface.id, "realize", (0.3, 0), (0.2, 1))
d.edge(de.id, iface.id, "realize", (0.5, 0), (0.5, 1))
d.edge(ta.id, iface.id, "realize", (0.7, 0), (0.8, 1))
d.edge(hero.id, iface.id, "aggregation", (1, 0.5), (1, 0.5), route="orthogonal")
d.text(20, 500, 760, 30, "Figure 3a. Strategy - CombatStyle family used by Hero")
d.save("uml_strategy.drawio")

# ============================================================== 2. FACTORY METHOD
d = Diagram("Factory Method", 900, 480)
creator = d.add_class(330, 30, 260, "HeroFactory", stereotype="abstract",
                       methods=["+ recruit(name): Hero", "# createHero(name): Hero {abstract}", "# heroType(): String {abstract}"])
spd = d.add_class(40, 230, 230, "SpeedsterFactory", methods=["# createHero(name): Hero", "# heroType(): String"])
tnk = d.add_class(330, 230, 230, "TankFactory", methods=["# createHero(name): Hero", "# heroType(): String"])
mge = d.add_class(620, 230, 230, "MageFactory", methods=["# createHero(name): Hero", "# heroType(): String"])
hero = d.add_class(355, 390, 190, "Hero")

d.edge(spd.id, creator.id, "inherit", (0.5, 0), (0.15, 1))
d.edge(tnk.id, creator.id, "inherit", (0.5, 0), (0.5, 1))
d.edge(mge.id, creator.id, "inherit", (0.5, 0), (0.85, 1))
d.edge(creator.id, hero.id, "dependency", (1, 0.5), (1, 0.5), label="&#171;creates&#187;", route="orthogonal")
d.text(20, 450, 860, 30, "Figure 3b. Factory Method - HeroFactory and concrete creators")
d.save("uml_factory.drawio")

# ============================================================== 3. OBSERVER
d = Diagram("Observer", 900, 560)
subj_i = d.add_class(40, 30, 250, "ThreatSubject", stereotype="interface",
                      methods=["+ addObserver(o)", "+ removeObserver(o)"])
obs_i = d.add_class(420, 30, 260, "AlertObserver", stereotype="interface",
                     methods=["+ onThreat(loc, danger)"])
sys_ = d.add_class(40, 220, 250, "AlertSystem", fields=["- observers: List&lt;AlertObserver&gt;"],
                    methods=["+ broadcastThreat(loc, d)"])
hero = d.add_class(330, 400, 200, "Hero")
news = d.add_class(600, 400, 230, "NewsReporter")

d.edge(sys_.id, subj_i.id, "realize", (0.5, 0), (0.5, 1))
d.edge(hero.id, obs_i.id, "realize", (0.3, 0), (0.4, 1))
d.edge(news.id, obs_i.id, "realize", (0.6, 0), (0.7, 1))
d.edge(sys_.id, obs_i.id, "aggregation", (1, 0.3), (0, 0.8))
d.text(20, 500, 860, 30, "Figure 3c. Observer - AlertSystem notifies Hero and NewsReporter")
d.save("uml_observer.drawio")

# ============================================================== 4. DECORATOR
d = Diagram("Decorator", 900, 560)
gear_i = d.add_class(330, 30, 240, "Gear", stereotype="interface",
                      methods=["+ description(): String", "+ powerBonus(): int"])
basic = d.add_class(60, 220, 200, "BasicGear", methods=["+ description()", "+ powerBonus()"])
upg = d.add_class(330, 220, 240, "GearUpgrade", stereotype="abstract", fields=["# inner: Gear"])
cape = d.add_class(620, 150, 200, "CapeUpgrade")
shield = d.add_class(620, 240, 200, "ShieldUpgrade")
gadget = d.add_class(620, 330, 200, "GadgetUpgrade")

d.edge(basic.id, gear_i.id, "realize", (0.5, 0), (0.2, 1))
d.edge(upg.id, gear_i.id, "realize", (0.5, 0), (0.5, 1))
d.edge(cape.id, upg.id, "inherit", (0, 0.5), (1, 0.2))
d.edge(shield.id, upg.id, "inherit", (0, 0.5), (1, 0.5))
d.edge(gadget.id, upg.id, "inherit", (0, 0.5), (1, 0.8))
d.edge(upg.id, basic.id, "composition", (0, 0.5), (1, 0.5))
d.text(20, 480, 860, 30, "Figure 3d. Decorator - Gear wrapped by stacked upgrades")
d.save("uml_decorator.drawio")

# ============================================================== 5. STATE
d = Diagram("State", 900, 620)
state_i = d.add_class(320, 30, 260, "HeroState", stereotype="interface",
                       methods=["+ name(): String", "+ describe(): String", "+ canAct(): boolean", "+ powerPercent(): int"])
av = d.add_class(10, 250, 200, "AvailableState")
om = d.add_class(230, 250, 200, "OnMissionState")
inj = d.add_class(460, 250, 190, "InjuredState")
ret = d.add_class(670, 250, 200, "RetiredState")
ctx = d.add_class(280, 400, 300, "HeroContext",
                   fields=["- hero: Hero", "- state: HeroState", "- inBattle: boolean"],
                   methods=["+ enterBattle()", "+ leaveBattle()", "+ autoUpdate()", "+ setState(s)"])

d.edge(av.id, state_i.id, "realize", (0.5, 0), (0.1, 1))
d.edge(om.id, state_i.id, "realize", (0.5, 0), (0.35, 1))
d.edge(inj.id, state_i.id, "realize", (0.5, 0), (0.65, 1))
d.edge(ret.id, state_i.id, "realize", (0.5, 0), (0.9, 1))
d.edge(ctx.id, state_i.id, "composition", (0.5, 0), (0.5, 1))
d.text(20, 580, 860, 30, "Figure 3e. State - HeroContext delegates to the current HeroState")
d.save("uml_state.drawio")

# ============================================================== 6. COMMAND
d = Diagram("Command", 950, 560)
cmd_i = d.add_class(350, 30, 250, "Command", stereotype="interface",
                     methods=["+ execute()", "+ undo()", "+ description(): String"])
atk = d.add_class(60, 230, 210, "AttackCommand")
dfd = d.add_class(320, 230, 210, "DefendCommand")
abl = d.add_class(580, 230, 240, "UseAbilityCommand")
inv = d.add_class(320, 380, 260, "CommandHistory", fields=["- history: Deque&lt;Command&gt;"],
                   methods=["+ execute(cmd)", "+ undoLast()", "+ hasHistory(): boolean"])
recv = d.add_class(650, 380, 220, "Hero / Villain")

d.edge(atk.id, cmd_i.id, "realize", (0.5, 0), (0.2, 1))
d.edge(dfd.id, cmd_i.id, "realize", (0.5, 0), (0.5, 1))
d.edge(abl.id, cmd_i.id, "realize", (0.5, 0), (0.8, 1))
d.edge(inv.id, cmd_i.id, "aggregation", (0, 0.3), (0, 0.7), route="orthogonal")
d.edge(atk.id, recv.id, "dependency", (1, 0.7), (0, 0.3))
d.text(20, 500, 910, 30, "Figure 3f. Command - CommandHistory invokes undoable Commands")
d.save("uml_command.drawio")

# ============================================================== 7. ITERATOR
d = Diagram("Iterator", 900, 560)
iterable_i = d.add_class(40, 30, 260, "Iterable&lt;Villain&gt;", stereotype="interface",
                          methods=["+ iterator(): Iterator&lt;Villain&gt;"])
iterator_i = d.add_class(420, 30, 280, "Iterator&lt;Villain&gt;", stereotype="interface",
                          methods=["+ hasNext(): boolean", "+ next(): Villain"])
wave = d.add_class(40, 230, 260, "VillainWave", fields=["- villains: List&lt;Villain&gt;"],
                    methods=["+ add(v)", "+ size(): int", "+ iterator(): Iterator&lt;Villain&gt;"])
witer = d.add_class(420, 230, 280, "WaveIterator", fields=["- villains: List&lt;Villain&gt;", "- index: int"],
                     methods=["+ hasNext(): boolean", "+ next(): Villain"])
villain = d.add_class(440, 420, 200, "Villain")

d.edge(wave.id, iterable_i.id, "realize", (0.5, 0), (0.5, 1))
d.edge(witer.id, iterator_i.id, "realize", (0.5, 0), (0.5, 1))
d.edge(wave.id, witer.id, "dependency", (1, 0.3), (0, 0.3), label="&#171;creates&#187;")
d.edge(witer.id, villain.id, "association", (0.5, 1), (0.5, 0))
d.text(20, 500, 860, 30, "Figure 3g. Iterator - VillainWave hides storage behind a custom WaveIterator")
d.save("uml_iterator.drawio")

# ============================================================== 8. SINGLETON
d = Diagram("Singleton", 820, 460)
hq = d.add_class(250, 30, 320, "HeroHQ",
                  fields=["- heroesRecruited: int", "- villainsDefeated: int"],
                  methods=["- HeroHQ()", "+ static getInstance(): HeroHQ", "+ recordRecruit()",
                           "+ recordVictory()", "+ printReport()"])
holder = d.add_class(290, 270, 240, "Holder", stereotype="static", fields=["+ static INSTANCE: HeroHQ"])

d.edge(hq.id, holder.id, "composition", (0.5, 1), (0.5, 0), label="lazily creates")
d.text(20, 400, 780, 30, "Figure 3h. Singleton - HeroHQ via Initialization-on-Demand Holder")
d.save("uml_singleton.drawio")

print("All 8 UML class diagrams generated.")
