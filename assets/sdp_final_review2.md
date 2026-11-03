**Nanjing Xiaozhuang University**

**南京晓庄学院**

FINAL PROJECT REPORT

Software Design Pattern

![](media/image1.png){width="3.808226159230096in"
height="3.7916666666666665in"}

**Justice Squad**

**Superhero Battle**

*A Text-Based Java Console Game Demonstrating Eight Classic GoF Design
Patterns*

**苏睿涵 - Sulthan Syafiq Raihan**

Student No. L25020028 - Class IT-1

School of Information Engineering

June 2026

**Abstract**

Justice Squad: Superhero Battle is a text-based Java console game built
as the final project for the Software Design Pattern course. The brief
required a working program that demonstrates at least eight Gang-of-Four
design patterns in a way that can be read, run, and checked against the
actual source. Rather than writing eight disconnected toy examples, this
project ties every pattern into one coherent gameplay loop: a player
recruits a superhero, equips gear, responds to a city threat, and
battles a wave of villains turn by turn, with every action undoable and
every result tracked by a shared headquarters.

Eight patterns are demonstrated: Factory Method builds the right hero
subtype on recruitment; Strategy decides each hero\'s damage and
blocking math; Observer lets the city broadcast a threat to every
listener (hero and news) without knowing who is listening; Decorator
stacks gear upgrades on top of a base suit; State moves a hero between
Available, OnMission, Injured, and Retired purely from its HP; Command
wraps every battle action as an undoable object; Iterator lets the wave
of villains be walked one at a time without exposing how it is stored;
and Singleton guarantees a single shared HeroHQ tracking recruits and
victories across the session.

The system is implemented in plain Java (compiled for Java 8, built with
JDK 21) with no external libraries, console input via java.util.Scanner,
and two entry points: an interactive Game.java for playing the full
loop, and a scripted Main.java that demonstrates each pattern in
isolation for verification. The result is a small but complete
demonstration that each pattern earns its place by solving a concrete
problem in the game, rather than being bolted on for the sake of a
pattern count.

# Table of Contents {#table-of-contents .TOC-Heading}

[1. Introduction [4](#introduction)](#introduction)

[1.1 Background [4](#background)](#background)

[1.2 Technology Stack [4](#technology-stack)](#technology-stack)

[1.3 Scope and Limitations
[4](#scope-and-limitations)](#scope-and-limitations)

[2. Design Analysis [5](#design-analysis)](#design-analysis)

[2.1 Pattern Selection Rationale
[5](#pattern-selection-rationale)](#pattern-selection-rationale)

[2.2 System Architecture
[6](#system-architecture)](#system-architecture)

[2.3 Use Case Analysis [6](#use-case-analysis)](#use-case-analysis)

[2.4 Class Design [7](#class-design)](#class-design)

[2.4.1 Strategy [7](#strategy)](#strategy)

[2.4.2 Factory Method [8](#factory-method)](#factory-method)

[2.4.3 Observer [8](#observer)](#observer)

[2.4.4 Decorator [8](#decorator)](#decorator)

[2.4.5 State [9](#state)](#state)

[2.4.6 Command [9](#command)](#command)

[2.4.7 Iterator [9](#iterator)](#iterator)

[2.4.8 Singleton [10](#singleton)](#singleton)

[3. Design Implementation
[11](#design-implementation)](#design-implementation)

[3.1 Factory Method [11](#factory-method-1)](#factory-method-1)

[3.2 Strategy [11](#strategy-1)](#strategy-1)

[3.3 Decorator [12](#decorator-1)](#decorator-1)

[3.4 Observer [13](#observer-1)](#observer-1)

[3.5 State [14](#state-1)](#state-1)

[3.6 Command [15](#command-1)](#command-1)

[3.7 Iterator [16](#iterator-1)](#iterator-1)

[3.8 Singleton [17](#singleton-1)](#singleton-1)

[3.9 Results [17](#results)](#results)

[4. Summary [19](#summary)](#summary)

[References [20](#references)](#references)

# 1. Introduction

## 1.1 Background

This report documents the final project for the \"Software Design
Pattern\" course, which required building a working Java program that
demonstrates a minimum of eight design patterns from the Gang-of-Four
catalogue, using Head First Design Patterns (2nd ed.) as the reference
text. Rather than writing isolated textbook snippets, the brief is
better satisfied by a single small system where each pattern solves a
real problem and the patterns visibly cooperate.

The chosen theme is Justice Squad: Superhero Battle, a text-based
console RPG. A player recruits a superhero from one of three archetypes,
equips stackable gear, watches the city broadcast a threat that the hero
and the news react to differently, and then fights a wave of villains
turn by turn , attacking, defending, using a signature ability, or
freely undoing the last action. Every recruit and victory is tallied by
a single shared headquarters for the whole session.

## 1.2 Technology Stack

The project deliberately stays inside plain Java with no external
dependencies, since the goal is to show pattern structure clearly rather
than to build a production system.

- Java language level 8 (compiled with release 8) for the runtime
  target; built with JDK 21.

- Console I/O only, via java.util.Scanner no GUI framework and no web
  layer.

- Two entry points: Game.java (interactive full game loop) and Main.java
  (scripted, one demo method per pattern, used to verify each pattern
  works in isolation).

- No persistence layer , the game state lives in memory for the duration
  of one run.

## 1.3 Scope and Limitations

A few boundaries were set deliberately, to keep the project focused on
demonstrating pattern structure rather than building a full game engine:

- No save/load system. Each run starts fresh; HeroHQ\'s counters live
  only for that JVM session.

- No graphics. The game is entirely text-based over the console, by
  design, it keeps every pattern\'s effect visible as printed text
  rather than hidden behind rendering code.

- Villains are scripted, not AI-driven. The focus is the hero-side
  pattern usage, not enemy behavior.

- Composite (Team/HeroMember) is not wired into the interactive
  Game.java loop, since the game follows one hero at a time; it is
  exercised through Main.java\'s scripted demo instead, shown in section
  3.7.

# 2. Design Analysis

This chapter explains how the eight required patterns were mapped onto
one coherent game, before any implementation detail. It moves from the
rationale behind each pattern choice, to the package architecture, the
use cases, and finally a class diagram for every pattern.

## 2.1 Pattern Selection Rationale

Every pattern below was chosen because it solves a specific problem that
the game already has, not the other way around. Table 1 lists the
problem each pattern addresses and why that pattern, rather than a
simpler if/switch, was the right fit.

*Table 1. Pattern Implementation -- Justice Squad Superhero Battle*

  ---------------------------------------------------------------------------------
  **Pattern**    **Problem in the Game**                 **Why This Pattern**
  -------------- --------------------------------------- --------------------------
  Factory Method Three hero archetypes (Speedster, Tank, Lets each concrete factory
                 Mage) each need a different             decide which Hero to
                 HP/power/style combination at           build, removing an
                 recruitment time.                       if/switch from the
                                                         recruiting flow.

  Strategy       Combat feel must differ per hero (hits  Encapsulates the
                 hard vs. blocks damage) without         damage/block formula so a
                 rewriting Hero for every style.         style can be swapped
                                                         without touching Hero.

  Observer       A single city threat must reach the     One broadcast, many
                 hero (who reacts) and the news (who     independent reactions,
                 reports), without AlertSystem knowing   adding a new reaction
                 either.                                 needs no change to the
                                                         subject.

  Decorator      Gear bonuses (Cape, Shield, Gadget)     Each upgrade wraps the
                 must stack in any combination without a previous Gear and adds its
                 subclass per combination.               own bonus, 3 upgrades give
                                                         8 possible combinations
                                                         from 3 classes.

  State          A hero\'s condition                     HeroContext recalculates
                 (Available/OnMission/Injured/Retired)   and delegates to the
                 must change automatically with HP, not  current HeroState object,
                 via scattered if-checks.                behavior changes without a
                                                         big switch in Game.java.

  Command        Every battle action must be undoable    Wrapping an action as a
                 without each action knowing about every Command object lets
                 other action.                           CommandHistory store and
                                                         reverse it generically via
                                                         execute()/undo().

  Iterator       The wave of villains must be walked one VillainWave implements
                 at a time without the client            Iterable so a custom
                 (Game.java) knowing whether it is       WaveIterator drives the
                 stored as a List, array, or something   client\'s for-each loop
                 else.                                   transparently, storage can
                                                         change without touching
                                                         Game.java.

  Singleton      Recruit/victory counters must be shared The
                 across the whole game session from one  Initialization-on-Demand
                 place.                                  Holder idiom guarantees
                                                         exactly one HeroHQ,
                                                         created lazily on first
                                                         access.
  ---------------------------------------------------------------------------------

## 2.2 System Architecture

The codebase is organised as one package per pattern under hero.\*, plus
a shared hero.core package holding the domain objects Hero and Villain.
Game.java and Main.java sit on top as the only two clients. Figure 1
traces the dependencies: the client depends on the four patterns it
orchestrates directly (Factory, Command, Iterator, Singleton), while
hero.core itself composes the four patterns that live inside every Hero
(Strategy, Decorator, State, Observer).

![](media/image2.png){width="6.107222222222222in"
height="3.641509186351706in"}

*Figure 1. Package Architecture -- Justice Squad Superhero Battle*

## 2.3 Use Case Analysis

A single actor, the Player, drives every use case in this game, there is
no second human role. Figure 2 shows the use cases and how they relate:
Battle Villain is a parent use case generalized by its three concrete
actions (Attack, Defend, Use Ability) plus Undo Action; responding to a
threat alert includes entering battle; and a battle turn includes the
villain\'s counter-attack, which the player does not directly trigger
but which always follows a surviving villain\'s turn.

![](media/image3.png){width="5.872794181977253in"
height="4.520833333333333in"}

*Figure 2. Use Case Diagram -- Justice Squad Superhero Battle*

## 2.4 Class Design

Each pattern\'s class structure is shown below as a standalone UML
diagram, using standard notation: a dashed arrow with a hollow head is
realization (implements), a solid arrow with a hollow head is
inheritance (extends), a filled diamond is composition, an open diamond
is aggregation, and a dashed arrow with an open head is a dependency.
Each diagram is referenced again in Chapter 3 alongside the code that
implements it.

### 2.4.1 Strategy

![](media/image4.png){width="5.307723097112861in"
height="3.2924529746281714in"}

*Figure 3a. Strategy -- CombatStyle family used by Hero*

### 2.4.2 Factory Method

![](media/image5.png){width="5.729166666666667in"
height="1.9270833333333333in"}

*Figure 3b. Factory Method -- HeroFactory and concrete creators*

### 2.4.3 Observer

![](media/image6.png){width="5.600788495188102in"
height="2.0416666666666665in"}

*Figure 3c. Observer -- AlertSystem notifies Hero and NewsReporter*

### 2.4.4 Decorator

![](media/image7.png){width="5.470526027996501in" height="2.46875in"}

*Figure 3d. Decorator -- Gear wrapped by stacked upgrades*

### 2.4.5 State

![](media/image8.png){width="5.576252187226597in"
height="1.885304024496938in"}

*Figure 3e. State -- HeroContext delegates to the current HeroState*

### 2.4.6 Command

![](media/image9.png){width="5.607393919510061in"
height="1.8958333333333333in"}

*Figure 3f. Command -- CommandHistory invokes undoable Commands*

### 2.4.7 Iterator

![](media/image10.png){width="5.161111111111111in"
height="3.187744969378828in"}

*Figure 3g. Iterator -- CommandHistory invokes undoable Commands*

### 2.4.8 Singleton

![](media/image11.png){width="2.56334208223972in"
height="3.7358497375328086in"}

*Figure 3h. Singleton -- HeroHQ via Initialization on Demand Holder*

# 3. Design Implementation

This chapter shows the code that realizes each pattern from Chapter 2,
and a screenshot proving it runs. Sections 3.1-3.8 show one pattern
each, referencing its class diagram from section 2.4. Section 3.9 closes
with the full interactive playthrough, tying every pattern together in
one continuous run.

## 3.1 Factory Method

HeroFactory (Figure 3b) declares recruit() as a template method that
calls the abstract factory method createHero(). Each concrete factory
below overrides createHero() to build a different Hero subtype with its
own HP, power, and CombatStyle , there is no if/switch anywhere in the
recruiting path.

+-----------------------------------------------------------------------+
| ***Listing 3.1 , HeroFactory.recruit() and SpeedsterFactory           |
| (src/hero/factory)***                                                 |
|                                                                       |
| public abstract class HeroFactory {                                   |
|                                                                       |
| public Hero recruit(String name) {                                    |
|                                                                       |
| Hero hero = createHero(name);                                         |
|                                                                       |
| System.out.printf(\"\[Recruit\] %s the %s joins the squad! (%s        |
| style)%n\",                                                           |
|                                                                       |
| name, heroType(), hero.getStyle().name());                            |
|                                                                       |
| return hero;                                                          |
|                                                                       |
| }                                                                     |
|                                                                       |
| protected abstract Hero createHero(String name);                      |
|                                                                       |
| protected abstract String heroType();                                 |
|                                                                       |
| }                                                                     |
|                                                                       |
| public class SpeedsterFactory extends HeroFactory {                   |
|                                                                       |
| protected Hero createHero(String name) { return new Hero(name, 80,    |
| 12, new AggressiveStyle()); }                                         |
|                                                                       |
| protected String heroType() { return \"Speedster\"; }                 |
|                                                                       |
| }                                                                     |
+=======================================================================+

In the screenshot above, choosing option 1 routes to SpeedsterFactory,
whose createHero() bakes in HP 80, base power 12, and AggressiveStyle,
TankFactory and MageFactory differ only in those three values and the
style object they pass in.

![](media/image12.png){width="5.85013779527559in"
height="2.2730369641294836in"}

*Figure 4. Game.java,- the player chooses a hero type and
SpeedsterFactory builds it.*

## 3.2 Strategy

CombatStyle (Figure 3a) is the common interface for every fighting
style. Hero holds one CombatStyle and delegates all damage math to it in
attack(), so swapping the style changes Hero\'s behaviour without
touching Hero\'s code.

+-----------------------------------------------------------------------+
| ***Listing 3.2 , CombatStyle and AggressiveStyle                      |
| (src/hero/strategy)***                                                |
|                                                                       |
| public interface CombatStyle {                                        |
|                                                                       |
| String name();                                                        |
|                                                                       |
| int attackDamage(int rawPower);                                       |
|                                                                       |
| int damageBlocked(int incoming);                                      |
|                                                                       |
| }                                                                     |
|                                                                       |
| public class AggressiveStyle implements CombatStyle {                 |
|                                                                       |
| public String name() { return \"Aggressive\"; }                       |
|                                                                       |
| public int attackDamage(int rawPower) { return rawPower + 8; }        |
|                                                                       |
| public int damageBlocked(int incoming) { return 0; }                  |
|                                                                       |
| }                                                                     |
+=======================================================================+

+-----------------------------------------------------------------------+
| ***Listing 3.3 , Hero.attack() delegating to the active CombatStyle   |
| (src/hero/core/Hero.java)***                                          |
|                                                                       |
| public int attack(Villain target) {                                   |
|                                                                       |
| int rawPower = basePower + gear.powerBonus(); // Decorator            |
| contributes here                                                      |
|                                                                       |
| int styled = style.attackDamage(rawPower); // Strategy decides the    |
| formula                                                               |
|                                                                       |
| int finalDmg = styled \* context.powerPercent() / 100; // State       |
| scales the result                                                     |
|                                                                       |
| target.takeDamage(finalDmg);                                          |
|                                                                       |
| return finalDmg;                                                      |
|                                                                       |
| }                                                                     |
+=======================================================================+

The same raw power of 12 produces three different results purely because
of which CombatStyle object is plugged in: Aggressive trades all
blocking for damage, Defensive blocks half of any hit, and Tactical sits
in between.

![](media/image13.png){width="5.75984251968504in"
height="1.1817793088363955in"}

![](media/image14.png){width="5.832929790026247in"
height="1.2485290901137358in"}

*Figure 5. AggressiveStyle source alongside the resulting attack damage
from a real battle turn.*

## 3.3 Decorator

Gear (Figure 3d) is the shared component interface. GearUpgrade is the
abstract decorator: it IS-A Gear and HAS-A Gear (the inner layer it
wraps), so each concrete upgrade only needs to add its own delta on top
of whatever it wraps.

+-----------------------------------------------------------------------+
| ***Listing 3.4 , GearUpgrade and CapeUpgrade (src/hero/decorator)***  |
|                                                                       |
| public abstract class GearUpgrade implements Gear {                   |
|                                                                       |
| protected final Gear inner;                                           |
|                                                                       |
| protected GearUpgrade(Gear inner) { this.inner = inner; }             |
|                                                                       |
| }                                                                     |
|                                                                       |
| public class CapeUpgrade extends GearUpgrade {                        |
|                                                                       |
| public CapeUpgrade(Gear inner) { super(inner); }                      |
|                                                                       |
| public String description() { return inner.description() + \" +       |
| Cape\"; }                                                             |
|                                                                       |
| public int powerBonus() { return inner.powerBonus() + 3; }            |
|                                                                       |
| }                                                                     |
+=======================================================================+

Option 4 builds new GadgetUpgrade(new ShieldUpgrade(new CapeUpgrade(new
BasicGear()))). Each layer calls inner.description() /
inner.powerBonus() first, then appends its own text and bonus , the +12
power shown above is 0 (BasicGear) + 3 (Cape) + 5 (Shield) + 4 (Gadget),
accumulated through the chain rather than hard-coded for that one
combination.

![](media/image15.png){width="5.681009405074366in"
height="1.713163823272091in"}

*Figure 6. Game.java - choosing the full stack: Suit + Cape + Shield +
Gadget.*

## 3.4 Observer

AlertSystem (Figure 3c) is the concrete subject. It holds a list of
AlertObserver and notifies every one of them with the same event; it has
no idea that one observer is a Hero and another is a NewsReporter.

+-----------------------------------------------------------------------+
| ***Listing 3.5 , AlertSystem.broadcastThreat()                        |
| (src/hero/observer/AlertSystem.java)***                               |
|                                                                       |
| public void broadcastThreat(String location, int dangerLevel) {       |
|                                                                       |
| System.out.printf(\" \[ALERT\] Threat at %s! Danger level %d.         |
| Dispatching\...%n\",                                                  |
|                                                                       |
| location, dangerLevel);                                               |
|                                                                       |
| for (AlertObserver o : observers) {                                   |
|                                                                       |
| o.onThreat(location, dangerLevel);                                    |
|                                                                       |
| }                                                                     |
|                                                                       |
| }                                                                     |
+=======================================================================+

+-----------------------------------------------------------------------+
| ***Listing 3.6 , Hero.onThreat() reacting to the same event           |
| (src/hero/core/Hero.java)***                                          |
|                                                                       |
| \@Override                                                            |
|                                                                       |
| public void onThreat(String location, int dangerLevel) {              |
|                                                                       |
| if (!context.canAct()) {                                              |
|                                                                       |
| System.out.printf(\" %s is %s and cannot respond.%n\", name,          |
| context.getStateName());                                              |
|                                                                       |
| return;                                                               |
|                                                                       |
| }                                                                     |
|                                                                       |
| System.out.printf(\" %s answers the call , heading to %s!%n\", name,  |
| location);                                                            |
|                                                                       |
| }                                                                     |
+=======================================================================+

Hero and NewsReporter both implement AlertObserver and both react to the
exact same onThreat() call , the hero heads to the scene while CNN
reports it as breaking news , with AlertSystem never branching on which
observer it is talking to.

![](media/image16.png){width="5.906175634295713in"
height="2.0225995188101487in"}

*Figure 7. Game.java,- one broadcastThreat() call, two independent
reactions.*

## 3.5 State

HeroContext (Figure 3e) is the state context, recalculating which
HeroState applies every time HP changes. AvailableState, OnMissionState,
InjuredState, and RetiredState each answer canAct() and powerPercent()
differently, so the same Hero genuinely behaves differently per state.

+-----------------------------------------------------------------------+
| ***Listing 3.7 , HeroContext.autoUpdate()                             |
| (src/hero/state/HeroContext.java)***                                  |
|                                                                       |
| public void autoUpdate() {                                            |
|                                                                       |
| int pct = hero.getHp() \* 100 / hero.getMaxHp(); // HP as a % of max  |
| HP                                                                    |
|                                                                       |
| if (hero.getHp() \<= 0) {                                             |
|                                                                       |
| setState(new RetiredState()); // dead -\> canAct() = false            |
|                                                                       |
| } else if (pct \< 30) {                                               |
|                                                                       |
| setState(new InjuredState()); // below 30% HP -\> powerPercent() = 60 |
|                                                                       |
| } else if (inBattle) {                                                |
|                                                                       |
| setState(new OnMissionState()); // healthy, fighting -\>              |
| powerPercent() = 100                                                  |
|                                                                       |
| } else {                                                              |
|                                                                       |
| setState(new AvailableState()); // healthy, not fighting -\>          |
| powerPercent() = 100                                                  |
|                                                                       |
| }                                                                     |
|                                                                       |
| }                                                                     |
+=======================================================================+

Every transition above is triggered automatically from inside
HeroContext after a takeDamage() or enterBattle() call , Game.java and
Main.java never assign a state directly, they only change HP and battle
status and let autoUpdate() decide.

powerPercent() here is the same multiplier consumed by Hero.attack() in
Listing 3.3 \-- an Injured hero\'s attacks are scaled down by exactly
this value, without Game.java ever touching that math directly.

![](media/image17.png){width="4.333938101487314in"
height="0.4792333770778653in"}

![](media/image18.png){width="5.629420384951881in"
height="0.634915791776028in"}

![](media/image19.png){width="5.898214129483814in"
height="0.965174978127734in"}

*Figure 8. Game.java - demoState() , Available to OnMission to Injured
to Retired, driven only by HP.*

## 3.6 Command

Command (Figure 3f) turns each battle action into an object with
execute() and undo(). AttackCommand below captures the villain\'s HP
before acting so undo() can restore it exactly; CommandHistory is the
invoker that runs commands and remembers them on a stack.

+-----------------------------------------------------------------------+
| ***Listing 3.8 , AttackCommand                                        |
| (src/hero/command/AttackCommand.java)***                              |
|                                                                       |
| public void execute() {                                               |
|                                                                       |
| villainHpBefore = target.getHp();                                     |
|                                                                       |
| int dmg = hero.attack(target);                                        |
|                                                                       |
| System.out.printf(\" %s attacks %s for %d damage! (%s HP: %d)%n\",    |
|                                                                       |
| hero.getName(), target.getName(), dmg, target.getName(),              |
| target.getHp());                                                      |
|                                                                       |
| }                                                                     |
|                                                                       |
| public void undo() {                                                  |
|                                                                       |
| target.takeDamage(target.getHp() - villainHpBefore); // negative =    |
| heal back                                                             |
|                                                                       |
| System.out.printf(\" \[Undo\] Attack cancelled , %s HP restored to    |
| %d.%n\",                                                              |
|                                                                       |
| target.getName(), target.getHp());                                    |
|                                                                       |
| }                                                                     |
+=======================================================================+

+-----------------------------------------------------------------------+
| ***Listing 3.9 , CommandHistory, the invoker                          |
| (src/hero/command/CommandHistory.java)***                             |
|                                                                       |
| public void execute(Command cmd) {                                    |
|                                                                       |
| cmd.execute();                                                        |
|                                                                       |
| history.push(cmd);                                                    |
|                                                                       |
| }                                                                     |
|                                                                       |
| public void undoLast() {                                              |
|                                                                       |
| Command cmd = history.pop();                                          |
|                                                                       |
| System.out.printf(\" Undoing: %s%n\", cmd.description());             |
|                                                                       |
| cmd.undo();                                                           |
|                                                                       |
| }                                                                     |
+=======================================================================+

CommandHistory only ever calls execute() and undo() , it has no idea
whether the command it is holding is an attack, a defend, or a signature
ability, which is what makes undo free to add for every future action
type.

![](media/image20.png){width="5.644244313210849in"
height="2.826499343832021in"}

*Figure 9. Game.java - option 4 undoes the previous attack and restores
the villain\'s HP.*

## 3.7 Iterator

VillainWave (Figure 3g) is the aggregate that hides how the wave of
villains is stored. Game.java only ever calls add() during setup and
then walks the wave with a plain Java for-each loop, which
Iterable\<Villain\> drives transparently to the custom WaveIterator
below.

+-----------------------------------------------------------------------+
| ***Listing 3.10 , VillainWave and WaveIterator (src/hero/iterator)*** |
|                                                                       |
| public class VillainWave implements Iterable\<Villain\> {             |
|                                                                       |
| private final List\<Villain\> villains = new ArrayList\<\>();         |
|                                                                       |
| public void add(Villain villain) { villains.add(villain); }           |
|                                                                       |
| \@Override                                                            |
|                                                                       |
| public Iterator\<Villain\> iterator() {                               |
|                                                                       |
| return new WaveIterator(villains);                                    |
|                                                                       |
| }                                                                     |
|                                                                       |
| }                                                                     |
|                                                                       |
| public class WaveIterator implements Iterator\<Villain\> {            |
|                                                                       |
| private final List\<Villain\> villains;                               |
|                                                                       |
| private int index = 0;                                                |
|                                                                       |
| \@Override                                                            |
|                                                                       |
| public boolean hasNext() { return index \< villains.size(); }         |
|                                                                       |
| \@Override                                                            |
|                                                                       |
| public Villain next() {                                               |
|                                                                       |
| if (!hasNext()) throw new NoSuchElementException(\"No more villains   |
| in this wave.\");                                                     |
|                                                                       |
| Villain villain = villains.get(index++);                              |
|                                                                       |
| System.out.printf(\" \[Iterator\] next villain in the wave: %s%n\",   |
| villain.getName());                                                   |
|                                                                       |
| return villain;                                                       |
|                                                                       |
| }                                                                     |
|                                                                       |
| }                                                                     |
+=======================================================================+

The print line inside next() was added purely to make the pattern
visible in the screenshot below exp- it is the only line in WaveIterator
that does not belong to the iterator contract itself, and it proves that
Game.java\'s for-each loop is actually walking a custom WaveIterator,
not a plain List iterator.

![](media/image21.png){width="6.268055555555556in"
height="1.4958333333333333in"}

*Figure 10. Game.java - the \"\[Iterator\] next villain in the wave\"
line fires every time the for-each loop moves to a new villain.*

## 3.8 Singleton

HeroHQ (Figure 3h) uses the Initialization-on-Demand Holder idiom: the
private static Holder class is only loaded by the JVM the first time
getInstance() runs, which makes the lazy creation thread-safe without
any synchronized block.

+-----------------------------------------------------------------------+
| ***Listing 3.11 , HeroHQ Singleton                                    |
| (src/hero/singleton/HeroHQ.java)***                                   |
|                                                                       |
| private HeroHQ() {}                                                   |
|                                                                       |
| private static class Holder {                                         |
|                                                                       |
| static final HeroHQ INSTANCE = new HeroHQ();                          |
|                                                                       |
| }                                                                     |
|                                                                       |
| public static HeroHQ getInstance() { return Holder.INSTANCE; }        |
+=======================================================================+

This screenshot is the closing report of a full game session:
recordRecruit() ran once during setup, recordVictory() ran twice (once
per defeated villain), and printReport() ran once at the very end \--
three calls to getInstance() from three completely different places in
Game.java, all updating the same HeroHQ. If this were not a singleton,
the counts would not line up.

![](media/image22.png){width="5.677876202974629in"
height="1.0939031058617672in"}

*Figure 11. Game.java - the closing HeroHQ report, accumulated from
three separate getInstance() calls across the session.*

## 3.9 Results

The screenshot below closes a full interactive run of Game.java: recruit
(3.1) to gear (3.3) to city alert (3.4) to a multi-turn battle that
includes an undo (3.6) to final victory. The State transition to
Available and the HeroHQ report are both visible in the same screenshot,
showing State and Singleton still working correctly at the very end of
the run.

![](media/image23.png){width="6.268055555555556in"
height="3.995138888888889in"}

*Figure 12. Game.java - final blow, state returns to Available, and
HeroHQ reports the session total.*

# 4. Summary

Justice Squad set out to prove that eight design patterns can share one
small system without feeling like eight disconnected exercises. Every
pattern in this report solves a problem the game actually has: Factory
Method removes a branch from recruiting, Strategy and Decorator both
contribute to the same damage formula from different angles, Observer
lets the city and the news react to one event independently, State keeps
a hero\'s condition consistent with its HP automatically, Command makes
every action undoable for free, Command makes every action undoable for
free, Iterator lets the villain wave be walked without exposing its
storage, and Singleton keeps one shared scoreboard for the whole
session.

Two design choices are worth calling out. First, Hero itself is the
meeting point of four patterns (Strategy, Decorator, State, Observer) at
once, which is what makes attack() in Listing 3.3 read as a short
pipeline rather than a wall of conditionals. Second, keeping Game.java
and Main.java separate let every pattern be demonstrated twice, once
inside the full playthrough, and once in isolation, which made it
straightforward to verify each pattern independently before trusting the
integrated game loop.

The scope was kept deliberately narrow: no persistence, no graphics, and
scripted rather than intelligent villains. Within that scope, the
project demonstrates a complete, runnable example of eight GoF patterns
cooperating in one coherent program, each one chosen because it was the
right tool for a real problem in the game rather than added to reach a
quota.

# 

# 

# 

# 

# 

# 

# 

# 

# 

# References

\[1\] E. Freeman and E. Robson, Head First Design Patterns, 2nd ed.
Sebastopol, CA: O\'Reilly Media, 2020.

\[2\] E. Gamma, R. Helm, R. Johnson, and J. Vlissides, Design Patterns:
Elements of Reusable Object-Oriented Software. Boston, MA:
Addison-Wesley, 1994.

\[3\] Oracle, \"Java Platform, Standard Edition Documentation,\" Oracle
Corporation. \[Online\]. Available:
https://docs.oracle.com/en/java/javase/
