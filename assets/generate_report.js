const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
  Footer, AlignmentType, LevelFormat, TableOfContents, HeadingLevel,
  BorderStyle, WidthType, ShadingType, PageNumber, PageBreak, VerticalAlign,
} = require("docx");

const A = path.join(__dirname); // assets dir
const img = (name) => fs.readFileSync(path.join(A, name));

// ---------------------------------------------------------------- constants
const PAGE_W = 11906, PAGE_H = 16838; // A4
const MARGIN = 1440; // 1 inch
const CONTENT_W = PAGE_W - 2 * MARGIN; // 9026

const NAVY = "1F3A5F";
const GREY = "595959";

// ---------------------------------------------------------------- helpers
function h1(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(text)] });
}
function h2(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(text)] });
}
function h3(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun(text)] });
}
function p(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 160 },
    children: [new TextRun({ text, ...opts })],
  });
}
function pRuns(runs, opts = {}) {
  return new Paragraph({ spacing: { after: 160 }, ...opts, children: runs });
}
function bullet(text) {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    spacing: { after: 80 },
    children: [new TextRun(text)],
  });
}
function center(children, opts = {}) {
  return new Paragraph({ alignment: AlignmentType.CENTER, children, ...opts });
}

function pageBreak() {
  return new Paragraph({ children: [new PageBreak()] });
}

// Pre-measured intrinsic sizes (w,h in px) for each asset, captured during generation.
const SIZES = {
  "architecture_diagram.png": [1845, 1444],
  "usecase_diagram.png": [1789, 1444],
  "uml_strategy.png": [977, 653],
  "uml_factory.png": [1069, 584],
  "uml_observer.png": [1069, 676],
  "uml_decorator.png": [1069, 676],
  "uml_state.png": [1069, 699],
  "uml_command.png": [1127, 676],
  "uml_composite.png": [1069, 653],
  "uml_singleton.png": [977, 584],
  "shot1_recruit.png": [972, 274],
  "shot2_gear.png": [972, 202],
  "shot3_alert.png": [972, 220],
  "shot4_undo.png": [972, 328],
  "shot5_victory.png": [972, 238],
  "shot6_strategy.png": [972, 220],
  "shot7_state.png": [972, 346],
  "shot8_composite.png": [972, 508],
  "shot9_singleton.png": [972, 202],
  "nxu-logo.png": [154, 154],
};

function figure(name, maxW, caption) {
  const [iw, ih] = SIZES[name];
  const w = Math.min(maxW, iw);
  const hgt = Math.round(ih * (w / iw));
  const paras = [
    center([
      new ImageRun({
        type: "png",
        data: img(name),
        transformation: { width: w, height: hgt },
        altText: { title: name, description: caption || name, name },
      }),
    ], { spacing: { before: 120, after: caption ? 40 : 160 } }),
  ];
  if (caption) {
    paras.push(center([new TextRun({ text: caption, italics: true, size: 18, color: GREY })],
      { spacing: { after: 200 } }));
  }
  return paras;
}

function codeListing(title, code) {
  const lines = code.split("\n");
  const codeParas = lines.map((line) => new Paragraph({
    spacing: { after: 0 },
    children: [new TextRun({ text: line.length ? line : " ", font: "Consolas", size: 17 })],
  }));
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [CONTENT_W],
    rows: [
      new TableRow({
        children: [
          new TableCell({
            width: { size: CONTENT_W, type: WidthType.DXA },
            shading: { fill: "F2F2F2", type: ShadingType.CLEAR },
            margins: { top: 120, bottom: 120, left: 160, right: 160 },
            borders: borderSet("BFBFBF"),
            children: [
              new Paragraph({
                spacing: { after: 100 },
                children: [new TextRun({ text: title, bold: true, italics: true, size: 19 })],
              }),
              ...codeParas,
            ],
          }),
        ],
      }),
    ],
  });
}

function borderSet(color) {
  const b = { style: BorderStyle.SINGLE, size: 2, color };
  return { top: b, bottom: b, left: b, right: b };
}

function patternTableRow(pattern, problem, why, header = false) {
  const mk = (text) => new TableCell({
    width: { size: 0, type: WidthType.DXA },
    shading: header ? { fill: "DBE9F5", type: ShadingType.CLEAR } : undefined,
    margins: { top: 80, bottom: 80, left: 100, right: 100 },
    borders: borderSet("BFBFBF"),
    children: [new Paragraph({ children: [new TextRun({ text, bold: header, size: 19 })] })],
  });
  return new TableRow({ children: [mk(pattern), mk(problem), mk(why)] });
}

function patternTable() {
  const colW = [1700, 3600, 3726];
  const rows = [
    ["Pattern", "Problem in the Game", "Why This Pattern", true],
    ["Factory Method", "Three hero archetypes (Speedster, Tank, Mage) each need a different HP/power/style combination at recruitment time.", "Lets each concrete factory decide which Hero to build, removing an if/switch from the recruiting flow."],
    ["Strategy", "Combat feel must differ per hero (hits hard vs. blocks damage) without rewriting Hero for every style.", "Encapsulates the damage/block formula so a style can be swapped without touching Hero."],
    ["Observer", "A single city threat must reach the hero (who reacts) and the news (who reports), without AlertSystem knowing either.", "One broadcast, many independent reactions -- adding a new reaction needs no change to the subject."],
    ["Decorator", "Gear bonuses (Cape, Shield, Gadget) must stack in any combination without a subclass per combination.", "Each upgrade wraps the previous Gear and adds its own bonus -- 3 upgrades give 8 possible combinations from 3 classes."],
    ["State", "A hero's condition (Available/OnMission/Injured/Retired) must change automatically with HP, not via scattered if-checks.", "HeroContext recalculates and delegates to the current HeroState object -- behavior changes without a big switch in Game.java."],
    ["Command", "Every battle action must be undoable without each action knowing about every other action.", "Wrapping an action as a Command object lets CommandHistory store and reverse it generically via execute()/undo()."],
    ["Composite", "A roster must support a lone hero or a nested league of teams, and awardXp() must reach all of them the same way.", "Team and HeroMember share one interface, so the caller never needs to know if it holds a leaf or a whole tree."],
    ["Singleton", "Recruit/victory counters must be shared across the whole game session from one place.", "The Initialization-on-Demand Holder idiom guarantees exactly one HeroHQ, created lazily on first access."],
  ];
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: colW,
    rows: rows.map((r, i) => patternTableRow(r[0], r[1], r[2], i === 0)),
  });
}

// ---------------------------------------------------------------- cover
const cover = [
  center([new TextRun({ text: "Nanjing Xiaozhuang University", bold: true, size: 28 })], { spacing: { before: 400, after: 40 } }),
  center([new TextRun({ text: "南京晓庄学院", bold: true, size: 28 })], { spacing: { after: 500 } }),
  center([new TextRun({ text: "FINAL PROJECT REPORT", bold: true, size: 24 })], { spacing: { after: 60 } }),
  center([new TextRun({ text: "Software Design Pattern", size: 24 })], { spacing: { after: 500 } }),
  ...figure("nxu-logo.png", 110),
  center([new TextRun({ text: "Justice Squad", bold: true, size: 56 })], { spacing: { before: 400, after: 80 } }),
  center([new TextRun({ text: "Superhero Battle", bold: true, size: 40 })], { spacing: { after: 200 } }),
  center([new TextRun({
    text: "A Text-Based Java Console Game Demonstrating Eight Classic GoF Design Patterns",
    italics: true, size: 22,
  })], { spacing: { after: 700 } }),
  center([new TextRun({ text: "苏睿涵 · Sulthan Syafiq Raihan", bold: true, size: 22 })], { spacing: { after: 40 } }),
  center([new TextRun({ text: "Student No. L25020028 · Class IT-1", size: 20 })], { spacing: { after: 40 } }),
  center([new TextRun({ text: "School of Information Engineering", size: 20 })], { spacing: { after: 40 } }),
  center([new TextRun({ text: "June 2026", size: 20 })], { spacing: { after: 40 } }),
  pageBreak(),
];

// ---------------------------------------------------------------- abstract
const abstractSection = [
  center([new TextRun({ text: "Abstract", bold: true, size: 26 })], { spacing: { after: 200 } }),
  p("Justice Squad: Superhero Battle is a text-based Java console game built as the final project " +
    "for the Software Design Pattern course. The brief required a working program that demonstrates " +
    "at least eight Gang-of-Four design patterns in a way that can be read, run, and checked against " +
    "the actual source. Rather than writing eight disconnected toy examples, this project ties every " +
    "pattern into one coherent gameplay loop: a player recruits a superhero, equips gear, responds to a " +
    "city threat, and battles a wave of villains turn by turn, with every action undoable and every " +
    "result tracked by a shared headquarters."),
  p("Eight patterns are demonstrated: Factory Method builds the right hero subtype on recruitment; " +
    "Strategy decides each hero's damage and blocking math; Observer lets the city broadcast a threat " +
    "to every listener (hero and news) without knowing who is listening; Decorator stacks gear upgrades " +
    "on top of a base suit; State moves a hero between Available, OnMission, Injured, and Retired purely " +
    "from its HP; Command wraps every battle action as an undoable object; Composite lets a roster of " +
    "heroes and nested teams be awarded experience through one uniform call; and Singleton guarantees a " +
    "single shared HeroHQ tracking recruits and victories across the session."),
  p("The system is implemented in plain Java (compiled for Java 8, built with JDK 21) with no external " +
    "libraries, console input via java.util.Scanner, and two entry points: an interactive Game.java for " +
    "playing the full loop, and a scripted Main.java that demonstrates each pattern in isolation for " +
    "verification. The result is a small but complete demonstration that each pattern earns its place by " +
    "solving a concrete problem in the game, rather than being bolted on for the sake of a pattern count."),
  pageBreak(),
];

// ---------------------------------------------------------------- TOC
const tocSection = [
  center([new TextRun({ text: "Table of Contents", bold: true, size: 26 })], { spacing: { after: 300 } }),
  new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-3" }),
  pageBreak(),
];

// ---------------------------------------------------------------- 1. Introduction
const introduction = [
  h1("1. Introduction"),
  h2("1.1 Background"),
  p("This report documents the final project for the \"Software Design Pattern\" course, which required " +
    "building a working Java program that demonstrates a minimum of eight design patterns from the " +
    "Gang-of-Four catalogue, using Head First Design Patterns (2nd ed.) as the reference text. Rather than " +
    "writing isolated textbook snippets, the brief is better satisfied by a single small system where each " +
    "pattern solves a real problem and the patterns visibly cooperate."),
  p("The chosen theme is Justice Squad: Superhero Battle, a text-based console RPG. A player recruits a " +
    "superhero from one of three archetypes, equips stackable gear, watches the city broadcast a threat " +
    "that the hero and the news react to differently, and then fights a wave of villains turn by turn -- " +
    "attacking, defending, using a signature ability, or freely undoing the last action. Every recruit and " +
    "victory is tallied by a single shared headquarters for the whole session."),
  h2("1.2 Technology Stack"),
  p("The project deliberately stays inside plain Java with no external dependencies, since the goal is to " +
    "show pattern structure clearly rather than to build a production system."),
  bullet("Java language level 8 (compiled with --release 8) for the runtime target; built with JDK 21."),
  bullet("Console I/O only, via java.util.Scanner -- no GUI framework and no web layer."),
  bullet("Two entry points: Game.java (interactive full game loop) and Main.java (scripted, one demo " +
    "method per pattern, used to verify each pattern works in isolation)."),
  bullet("No persistence layer -- the game state lives in memory for the duration of one run."),
  h2("1.3 Scope and Limitations"),
  p("A few boundaries were set deliberately, to keep the project focused on demonstrating pattern " +
    "structure rather than building a full game engine:"),
  bullet("No save/load system. Each run starts fresh; HeroHQ's counters live only for that JVM session."),
  bullet("No graphics. The game is entirely text-based over the console, by design -- it keeps every " +
    "pattern's effect visible as printed text rather than hidden behind rendering code."),
  bullet("Villains are scripted, not AI-driven. The focus is the hero-side pattern usage, not enemy " +
    "behaviour."),
  bullet("Composite (Team/HeroMember) is not wired into the interactive Game.java loop, since the game " +
    "follows one hero at a time; it is exercised through Main.java's scripted demo instead, shown in " +
    "section 3.7."),
  pageBreak(),
];

// ---------------------------------------------------------------- 2. Design Analysis
const designAnalysis = [
  h1("2. Design Analysis"),
  p("This chapter explains how the eight required patterns were mapped onto one coherent game, before " +
    "any implementation detail. It moves from the rationale behind each pattern choice, to the package " +
    "architecture, the use cases, and finally a class diagram for every pattern."),
  h2("2.1 Pattern Selection Rationale"),
  p("Every pattern below was chosen because it solves a specific problem that the game already has, not " +
    "the other way around. Table 1 lists the problem each pattern addresses and why that pattern -- rather " +
    "than a simpler if/switch -- was the right fit."),
  patternTable(),
  p("", { spacing: { after: 100 } }),
  h2("2.2 System Architecture"),
  p("The codebase is organised as one package per pattern under hero.*, plus a shared hero.core package " +
    "holding the domain objects Hero and Villain. Game.java and Main.java sit on top as the only two " +
    "clients. Figure 1 traces the dependencies: the client depends on the four patterns it orchestrates " +
    "directly (Factory, Command, Composite, Singleton), while hero.core itself composes the four patterns " +
    "that live inside every Hero (Strategy, Decorator, State, Observer)."),
  ...figure("architecture_diagram.png", 520),
  h2("2.3 Use Case Analysis"),
  p("A single actor, the Player, drives every use case in this game -- there is no second human role. " +
    "Figure 2 shows the use cases and how they relate: Battle Villain is a parent use case generalised by " +
    "its three concrete actions (Attack, Defend, Use Ability) plus Undo Action; responding to a threat " +
    "alert includes entering battle; and a battle turn includes the villain's counter-attack, which the " +
    "player does not directly trigger but which always follows a surviving villain's turn."),
  ...figure("usecase_diagram.png", 540),
  h2("2.4 Class Design"),
  p("Each pattern's class structure is shown below as a standalone UML diagram, using standard notation: " +
    "a dashed arrow with a hollow head is realization (implements), a solid arrow with a hollow head is " +
    "inheritance (extends), a filled diamond is composition, an open diamond is aggregation, and a dashed " +
    "arrow with an open head is a dependency. Each diagram is referenced again in Chapter 3 alongside the " +
    "code that implements it."),
  h3("2.4.1 Strategy"),
  ...figure("uml_strategy.png", 480),
  h3("2.4.2 Factory Method"),
  ...figure("uml_factory.png", 480),
  h3("2.4.3 Observer"),
  ...figure("uml_observer.png", 480),
  h3("2.4.4 Decorator"),
  ...figure("uml_decorator.png", 480),
  h3("2.4.5 State"),
  ...figure("uml_state.png", 480),
  h3("2.4.6 Command"),
  ...figure("uml_command.png", 480),
  h3("2.4.7 Composite"),
  ...figure("uml_composite.png", 480),
  h3("2.4.8 Singleton"),
  ...figure("uml_singleton.png", 420),
  pageBreak(),
];

// ---------------------------------------------------------------- 3. Design Implementation
function patternSection(num, title, intro, listings, figName, figW, figCaption, closing) {
  const out = [h2(`3.${num} ${title}`)];
  if (intro) out.push(...(Array.isArray(intro) ? intro : [intro]));
  listings.forEach((l) => { out.push(l); out.push(p("")); });
  if (closing) out.push(...(Array.isArray(closing) ? closing : [closing]));
  out.push(...figure(figName, figW, figCaption));
  return out;
}

const implementation = [
  h1("3. Design Implementation"),
  p("This chapter shows the code that realises each pattern from Chapter 2, and a screenshot proving it " +
    "runs. Sections 3.1-3.8 show one pattern each, referencing its class diagram from section 2.4. Section " +
    "3.9 closes with the full interactive playthrough, tying every pattern together in one continuous run."),

  ...patternSection(1, "Factory Method",
    p("HeroFactory (Figure 3b) declares recruit() as a template method that calls the abstract factory " +
      "method createHero(). Each concrete factory below overrides createHero() to build a different Hero " +
      "subtype with its own HP, power, and CombatStyle -- there is no if/switch anywhere in the recruiting " +
      "path."),
    [codeListing("Listing 3.1 -- HeroFactory.recruit() and SpeedsterFactory (src/hero/factory)",
`public abstract class HeroFactory {
    public Hero recruit(String name) {
        Hero hero = createHero(name);
        System.out.printf("[Recruit] %s the %s joins the squad! (%s style)%n",
            name, heroType(), hero.getStyle().name());
        return hero;
    }
    protected abstract Hero createHero(String name);
    protected abstract String heroType();
}

public class SpeedsterFactory extends HeroFactory {
    protected Hero   createHero(String name) { return new Hero(name, 80, 12, new AggressiveStyle()); }
    protected String heroType()              { return "Speedster"; }
}`)],
    "shot1_recruit.png", 480,
    "Figure 4. Game.java -- the player chooses a hero type and SpeedsterFactory builds it.",
    p("In the screenshot above, choosing option 1 routes to SpeedsterFactory, whose createHero() bakes in " +
      "HP 80, base power 12, and AggressiveStyle -- TankFactory and MageFactory differ only in those three " +
      "values and the style object they pass in.")),

  ...patternSection(2, "Strategy",
    p("CombatStyle (Figure 3a) is the common interface for every fighting style. Hero holds one CombatStyle " +
      "and delegates all damage math to it in attack(), so swapping the style changes Hero's behaviour " +
      "without touching Hero's code."),
    [codeListing("Listing 3.2 -- CombatStyle and AggressiveStyle (src/hero/strategy)",
`public interface CombatStyle {
    String name();
    int attackDamage(int rawPower);
    int damageBlocked(int incoming);
}

public class AggressiveStyle implements CombatStyle {
    public String name()                   { return "Aggressive"; }
    public int attackDamage(int rawPower)  { return rawPower + 8; }
    public int damageBlocked(int incoming) { return 0; }
}`),
     codeListing("Listing 3.3 -- Hero.attack() delegating to the active CombatStyle (src/hero/core/Hero.java)",
`public int attack(Villain target) {
    int rawPower  = basePower + gear.powerBonus();   // Decorator contributes here
    int styled    = style.attackDamage(rawPower);    // Strategy decides the formula
    int finalDmg  = styled * context.powerPercent() / 100; // State scales the result
    target.takeDamage(finalDmg);
    return finalDmg;
}`)],
    "shot6_strategy.png", 480,
    "Figure 5. Main.java demoStrategy() -- identical raw power, three different outcomes.",
    p("The same raw power of 12 produces three different results purely because of which CombatStyle " +
      "object is plugged in: Aggressive trades all blocking for damage, Defensive blocks half of any hit, " +
      "and Tactical sits in between.")),

  ...patternSection(3, "Decorator",
    p("Gear (Figure 3d) is the shared component interface. GearUpgrade is the abstract decorator: it IS-A " +
      "Gear and HAS-A Gear (the inner layer it wraps), so each concrete upgrade only needs to add its own " +
      "delta on top of whatever it wraps."),
    [codeListing("Listing 3.4 -- GearUpgrade and CapeUpgrade (src/hero/decorator)",
`public abstract class GearUpgrade implements Gear {
    protected final Gear inner;
    protected GearUpgrade(Gear inner) { this.inner = inner; }
}

public class CapeUpgrade extends GearUpgrade {
    public CapeUpgrade(Gear inner) { super(inner); }
    public String description() { return inner.description() + " + Cape"; }
    public int powerBonus()     { return inner.powerBonus() + 3; }
}`)],
    "shot2_gear.png", 480,
    "Figure 6. Game.java -- choosing the full stack: Suit + Cape + Shield + Gadget.",
    p("Option 4 builds new GadgetUpgrade(new ShieldUpgrade(new CapeUpgrade(new BasicGear()))). Each layer " +
      "calls inner.description() / inner.powerBonus() first, then appends its own text and bonus -- the " +
      "+12 power shown above is 0 (BasicGear) + 3 (Cape) + 5 (Shield) + 4 (Gadget), accumulated through the " +
      "chain rather than hard-coded for that one combination.")),

  ...patternSection(4, "Observer",
    p("AlertSystem (Figure 3c) is the concrete subject. It holds a list of AlertObserver and notifies every " +
      "one of them with the same event; it has no idea that one observer is a Hero and another is a " +
      "NewsReporter."),
    [codeListing("Listing 3.5 -- AlertSystem.broadcastThreat() (src/hero/observer/AlertSystem.java)",
`public void broadcastThreat(String location, int dangerLevel) {
    System.out.printf("  [ALERT] Threat at %s! Danger level %d. Dispatching...%n",
        location, dangerLevel);
    for (AlertObserver o : observers) {
        o.onThreat(location, dangerLevel);
    }
}`),
     codeListing("Listing 3.6 -- Hero.onThreat() reacting to the same event (src/hero/core/Hero.java)",
`@Override
public void onThreat(String location, int dangerLevel) {
    if (!context.canAct()) {
        System.out.printf("  %s is %s and cannot respond.%n", name, context.getStateName());
        return;
    }
    System.out.printf("  %s answers the call -- heading to %s!%n", name, location);
}`)],
    "shot3_alert.png", 480,
    "Figure 7. Game.java -- one broadcastThreat() call, two independent reactions.",
    p("Hero and NewsReporter both implement AlertObserver and both react to the exact same onThreat() call " +
      "-- the hero heads to the scene while CNN reports it as breaking news -- with AlertSystem never " +
      "branching on which observer it is talking to.")),

  ...patternSection(5, "State",
    p("HeroContext (Figure 3e) is the state context, recalculating which HeroState applies every time HP " +
      "changes. AvailableState, OnMissionState, InjuredState, and RetiredState each answer canAct() and " +
      "powerPercent() differently, so the same Hero genuinely behaves differently per state."),
    [codeListing("Listing 3.7 -- HeroContext.autoUpdate() (src/hero/state/HeroContext.java)",
`public void autoUpdate() {
    int pct = hero.getHp() * 100 / hero.getMaxHp();
    if (hero.getHp() <= 0) {
        setState(new RetiredState());
    } else if (pct < 30) {
        setState(new InjuredState());
    } else if (inBattle) {
        setState(new OnMissionState());
    } else {
        setState(new AvailableState());
    }
}`)],
    "shot7_state.png", 480,
    "Figure 8. Main.java demoState() -- Available to OnMission to Injured to Retired, driven only by HP.",
    p("Every transition above is triggered automatically from inside HeroContext after a takeDamage() or " +
      "enterBattle() call -- Game.java and Main.java never assign a state directly, they only change HP " +
      "and battle status and let autoUpdate() decide.")),

  ...patternSection(6, "Command",
    p("Command (Figure 3f) turns each battle action into an object with execute() and undo(). " +
      "AttackCommand below captures the villain's HP before acting so undo() can restore it exactly; " +
      "CommandHistory is the invoker that runs commands and remembers them on a stack."),
    [codeListing("Listing 3.8 -- AttackCommand (src/hero/command/AttackCommand.java)",
`public void execute() {
    villainHpBefore = target.getHp();
    int dmg = hero.attack(target);
    System.out.printf("  %s attacks %s for %d damage! (%s HP: %d)%n",
        hero.getName(), target.getName(), dmg, target.getName(), target.getHp());
}

public void undo() {
    target.takeDamage(target.getHp() - villainHpBefore); // negative = heal back
    System.out.printf("  [Undo] Attack cancelled -- %s HP restored to %d.%n",
        target.getName(), target.getHp());
}`),
     codeListing("Listing 3.9 -- CommandHistory, the invoker (src/hero/command/CommandHistory.java)",
`public void execute(Command cmd) {
    cmd.execute();
    history.push(cmd);
}

public void undoLast() {
    Command cmd = history.pop();
    System.out.printf("  Undoing: %s%n", cmd.description());
    cmd.undo();
}`)],
    "shot4_undo.png", 480,
    "Figure 9. Game.java -- option 4 undoes the previous attack and restores the villain's HP.",
    p("CommandHistory only ever calls execute() and undo() -- it has no idea whether the command it is " +
      "holding is an attack, a defend, or a signature ability, which is what makes undo free to add for " +
      "every future action type.")),

  ...patternSection(7, "Composite",
    p("RosterComponent (Figure 3g) is the shared interface for a single hero (HeroMember, the leaf) and a " +
      "group (Team, the composite). Calling awardXp() on a Team forwards the call to every member, " +
      "including nested Teams, so the caller never needs to know the shape of the tree it is holding."),
    [codeListing("Listing 3.10 -- Team.awardXp(), recursing into nested teams (src/hero/composite/Team.java)",
`public void awardXp(int amount) {
    System.out.printf("  [Team] \\"%s\\" awarding %d XP to all members:%n", name, amount);
    for (RosterComponent m : members) m.awardXp(amount);
}`)],
    "shot8_composite.png", 480,
    "Figure 10. Main.java demoComposite() -- a league of two nested teams plus a lone hero.",
    p("\"Justice League\" contains \"Team Alpha\" and \"Team Beta\" as well as a hero added directly at the top " +
      "level. One awardXp(50) call reaches all four heroes regardless of how deep they are nested, because " +
      "every level just forwards the call to its own members.")),

  ...patternSection(8, "Singleton",
    p("HeroHQ (Figure 3h) uses the Initialization-on-Demand Holder idiom: the private static Holder class " +
      "is only loaded by the JVM the first time getInstance() runs, which makes the lazy creation " +
      "thread-safe without any synchronized block."),
    [codeListing("Listing 3.11 -- HeroHQ Singleton (src/hero/singleton/HeroHQ.java)",
`private HeroHQ() {}

private static class Holder {
    static final HeroHQ INSTANCE = new HeroHQ();
}

public static HeroHQ getInstance() { return Holder.INSTANCE; }`)],
    "shot9_singleton.png", 480,
    "Figure 11. Main.java demoSingleton() -- two references obtained separately are the same object.",
    p("a == b prints true because both calls to getInstance() return the same Holder.INSTANCE -- every " +
      "recordRecruit() and recordVictory() call anywhere in the game updates that one shared object.")),

  h2("3.9 Results"),
  p("The screenshot below closes a full interactive run of Game.java: recruit (3.1) to gear (3.3) to city " +
    "alert (3.4) to a multi-turn battle that includes an undo (3.6) to final victory. The State transition " +
    "to Available and the HeroHQ report are both visible in the same screenshot, showing State and " +
    "Singleton still working correctly at the very end of the run."),
  ...figure("shot5_victory.png", 480,
    "Figure 12. Game.java -- final blow, state returns to Available, and HeroHQ reports the session total."),
  pageBreak(),
];

// ---------------------------------------------------------------- 4. Summary
const summary = [
  h1("4. Summary"),
  p("Justice Squad set out to prove that eight design patterns can share one small system without feeling " +
    "like eight disconnected exercises. Every pattern in this report solves a problem the game actually " +
    "has: Factory Method removes a branch from recruiting, Strategy and Decorator both contribute to the " +
    "same damage formula from different angles, Observer lets the city and the news react to one event " +
    "independently, State keeps a hero's condition consistent with its HP automatically, Command makes " +
    "every action undoable for free, Composite lets a roster be awarded XP regardless of its shape, and " +
    "Singleton keeps one shared scoreboard for the whole session."),
  p("Two design choices are worth calling out. First, Hero itself is the meeting point of four patterns " +
    "(Strategy, Decorator, State, Observer) at once, which is what makes attack() in Listing 3.3 read as a " +
    "short pipeline rather than a wall of conditionals. Second, keeping Game.java and Main.java separate " +
    "let every pattern be demonstrated twice -- once inside the full playthrough, and once in isolation -- " +
    "which made it straightforward to verify each pattern independently before trusting the integrated " +
    "game loop."),
  p("The scope was kept deliberately narrow: no persistence, no graphics, and scripted rather than " +
    "intelligent villains. Within that scope, the project demonstrates a complete, runnable example of " +
    "eight GoF patterns cooperating in one coherent program, each one chosen because it was the right tool " +
    "for a real problem in the game rather than added to reach a quota."),
  h1("References"),
  p("[1] E. Freeman and E. Robson, Head First Design Patterns, 2nd ed. Sebastopol, CA: O'Reilly Media, 2020."),
  p("[2] E. Gamma, R. Helm, R. Johnson, and J. Vlissides, Design Patterns: Elements of Reusable " +
    "Object-Oriented Software. Boston, MA: Addison-Wesley, 1994."),
  p("[3] Oracle, \"Java Platform, Standard Edition Documentation,\" Oracle Corporation. [Online]. " +
    "Available: https://docs.oracle.com/en/java/javase/"),
];

// ---------------------------------------------------------------- build
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 30, bold: true, font: "Arial", color: NAVY },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Arial", color: NAVY },
        paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 23, bold: true, italics: true, font: "Arial", color: NAVY },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 } },
    ],
  },
  numbering: {
    config: [
      { reference: "bullets",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ],
  },
  sections: [{
    properties: {
      page: {
        size: { width: PAGE_W, height: PAGE_H },
        margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN },
      },
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ children: [PageNumber.CURRENT], size: 18 })],
        })],
      }),
    },
    children: [
      ...cover,
      ...abstractSection,
      ...tocSection,
      ...introduction,
      ...designAnalysis,
      ...implementation,
      ...summary,
    ],
  }],
});

Packer.toBuffer(doc).then((buffer) => {
  const out = path.join(__dirname, "..", "report", "SDP_Report_L25020028_JusticeSquad.docx");
  fs.writeFileSync(out, buffer);
  console.log("written:", out);
});
