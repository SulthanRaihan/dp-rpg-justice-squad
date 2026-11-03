import hero.command.*;
import hero.core.Hero;
import hero.core.Villain;
import hero.decorator.*;
import hero.factory.*;
import hero.iterator.VillainWave;
import hero.observer.*;
import hero.singleton.HeroHQ;
import hero.state.*;
import hero.strategy.*;

/**
 * Scripted demo runner -- one demo per pattern, no user input.
 * Run this to prove every pattern works without playing the full game.
 */
public class Main {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("  JUSTICE SQUAD -- Design Pattern Demos");
        System.out.println("=================================================");
        System.out.println();

        demoFactoryMethod();
        demoStrategy();
        demoDecorator();
        demoObserver();
        demoState();
        demoCommand();
        demoIterator();
        demoSingleton();
        demoIntegrated();
    }

    // ── Pattern 2: Factory Method ─────────────────────────────────────────────
    static void demoFactoryMethod() {
        printHeader(2, "Factory Method");
        System.out.println("Each factory subclass overrides createHero() -- no if/switch.");
        System.out.println();

        HeroFactory[] factories = { new SpeedsterFactory(), new TankFactory(), new MageFactory() };
        for (HeroFactory f : factories) {
            Hero h = f.recruit("Test");
            System.out.println("  -> " + h.status());
        }
        System.out.println();
    }

    // ── Pattern 1: Strategy ───────────────────────────────────────────────────
    static void demoStrategy() {
        printHeader(1, "Strategy");
        System.out.println("Same raw power, different damage per combat style.");
        System.out.println();

        CombatStyle[] styles = { new AggressiveStyle(), new DefensiveStyle(), new TacticalStyle() };
        int rawPower = 12;
        for (CombatStyle s : styles) {
            System.out.printf("  %-11s | attack from power %d = %d | blocks from 20 incoming = %d%n",
                s.name(), rawPower, s.attackDamage(rawPower), s.damageBlocked(20));
        }
        System.out.println();
    }

    // ── Pattern 4: Decorator ──────────────────────────────────────────────────
    static void demoDecorator() {
        printHeader(4, "Decorator");
        System.out.println("Stack gear upgrades -- each layer wraps the previous one.");
        System.out.println();

        Gear[] gears = {
            new BasicGear(),
            new CapeUpgrade(new BasicGear()),
            new ShieldUpgrade(new CapeUpgrade(new BasicGear())),
            new GadgetUpgrade(new ShieldUpgrade(new CapeUpgrade(new BasicGear())))
        };
        for (Gear g : gears) {
            System.out.printf("  %-32s  power: +%d%n", g.description(), g.powerBonus());
        }
        System.out.println();
    }

    // ── Pattern 3: Observer ───────────────────────────────────────────────────
    static void demoObserver() {
        printHeader(3, "Observer");
        System.out.println("One threat broadcast -- heroes respond AND the news reports it.");
        System.out.println();

        AlertSystem dispatch = new AlertSystem();
        dispatch.addObserver(new SpeedsterFactory().recruit("Bolt"));
        dispatch.addObserver(new TankFactory().recruit("Titan"));
        dispatch.addObserver(new NewsReporter("BBC"));
        System.out.println();

        dispatch.broadcastThreat("Harbor District", 9);
        System.out.println();
    }

    // ── Pattern 5: State ─────────────────────────────────────────────────────
    static void demoState() {
        printHeader(5, "State");
        System.out.println("Same hero, behavior changes with HP; transitions happen automatically.");
        System.out.println();

        Hero hero = new SpeedsterFactory().recruit("Flash");
        System.out.println("Start: " + hero.getContext().getStateName()
            + " (power " + hero.getContext().powerPercent() + "%)");

        hero.getContext().enterBattle();
        System.out.println("Enter battle -> " + hero.getContext().getStateName());

        System.out.println("Taking a big hit (down to low HP)...");
        hero.takeDamage(65); // 80 -> 15, below 30%
        System.out.println("  Now: " + hero.getContext().getStateName()
            + " (power " + hero.getContext().powerPercent() + "%)  HP " + hero.getHp());

        System.out.println("Taking a finishing blow...");
        hero.takeDamage(50);
        System.out.println("  Now: " + hero.getContext().getStateName()
            + " canAct=" + hero.getContext().canAct());
        System.out.println();
    }

    // ── Pattern 6: Command ────────────────────────────────────────────────────
    static void demoCommand() {
        printHeader(6, "Command");
        System.out.println("Actions are objects. CommandHistory keeps a stack for undo.");
        System.out.println();

        Hero hero = new MageFactory().recruit("Orin");
        Villain villain = new Villain("Goon", 100, 10);
        CommandHistory history = new CommandHistory();

        System.out.println("Villain HP before: " + villain.getHp());
        history.execute(new AttackCommand(hero, villain));
        System.out.println("Villain HP after attack: " + villain.getHp());

        System.out.println("Undo the attack:");
        history.undoLast();
        System.out.println("Villain HP after undo: " + villain.getHp());
        System.out.println();
    }

    // ── Pattern 7: Iterator ───────────────────────────────────────────────────
    static void demoIterator() {
        printHeader(7, "Iterator");
        System.out.println("VillainWave hides its storage -- the client only ever calls add() and");
        System.out.println("walks it with a for-each loop, never touching the underlying List.");
        System.out.println();

        VillainWave wave = new VillainWave();
        wave.add(new Villain("Slime", 40, 8));
        wave.add(new Villain("Goblin", 55, 11));
        wave.add(new Villain("Ogre", 70, 15));

        System.out.println("Walking the wave with a plain for-each loop:");
        for (Villain v : wave) {
            System.out.printf("  -> %s  HP %d%n", v.getName(), v.getHp());
        }
        System.out.println();
    }

    // ── Pattern 8: Singleton ──────────────────────────────────────────────────
    static void demoSingleton() {
        printHeader(8, "Singleton");
        System.out.println("getInstance() always returns the same headquarters.");
        System.out.println();

        HeroHQ a = HeroHQ.getInstance();
        HeroHQ b = HeroHQ.getInstance();
        System.out.println("  a == b : " + (a == b));
        a.printReport();
        System.out.println();
    }

    // ── Integrated demo ───────────────────────────────────────────────────────
    static void demoIntegrated() {
        printHeader(0, "Integrated -- all patterns in one battle");
        System.out.println();

        // Factory + Singleton
        Hero hero = new TankFactory().recruit("Aegis");
        HeroHQ.getInstance().recordRecruit();

        // Decorator
        Gear gear = new GadgetUpgrade(new ShieldUpgrade(new BasicGear()));
        hero.setGear(gear);
        System.out.println("Equipped: " + gear.description() + " (+" + gear.powerBonus() + " power)");
        System.out.println();

        // Observer
        AlertSystem dispatch = new AlertSystem();
        dispatch.addObserver(hero);
        dispatch.addObserver(new NewsReporter("CNN"));
        dispatch.broadcastThreat("City Hall", 8);
        System.out.println();

        // Iterator: pull the villain out of a wave instead of a bare variable
        VillainWave wave = new VillainWave();
        wave.add(new Villain("Overlord", 70, 22));
        Villain villain = wave.iterator().next();

        // Command + Strategy + State in a short fight
        CommandHistory history = new CommandHistory();
        hero.getContext().enterBattle();

        System.out.println("Turn 1 - Attack:");
        history.execute(new AttackCommand(hero, villain));
        villain.strike(hero);
        System.out.println("  " + hero.status());
        System.out.println();

        System.out.println("Turn 2 - Signature ability:");
        history.execute(new UseAbilityCommand(hero, villain));
        if (!villain.isDefeated()) villain.strike(hero);
        System.out.println("  " + hero.status());
        System.out.println();

        System.out.println("Undo last action:");
        history.undoLast();
        System.out.println();

        if (villain.isDefeated()) HeroHQ.getInstance().recordVictory();

        // Singleton report
        HeroHQ.getInstance().printReport();
        System.out.println();
    }

    // ── helper ────────────────────────────────────────────────────────────────
    static void printHeader(int num, String name) {
        System.out.println("=================================================");
        if (num > 0)
            System.out.printf("  Pattern %d: %s%n", num, name);
        else
            System.out.printf("  %s%n", name);
        System.out.println("=================================================");
    }
}
