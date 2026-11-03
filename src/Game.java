import hero.command.*;
import hero.core.Hero;
import hero.core.Villain;
import hero.decorator.*;
import hero.factory.*;
import hero.iterator.VillainWave;
import hero.observer.*;
import hero.singleton.HeroHQ;

import java.util.Scanner;

public class Game {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("=================================================");
        System.out.println("      JUSTICE SQUAD - Superhero Battle");
        System.out.println("=================================================");
        System.out.println();

        // ── 1. Recruit a hero (Factory Method) ────────────────────────────────
        System.out.println("Choose your hero type:");
        System.out.println("  1) Speedster -- Aggressive (HP 80, hits hardest)");
        System.out.println("  2) Tank      -- Defensive  (HP 130, blocks half damage)");
        System.out.println("  3) Mage      -- Tactical   (HP 100, balanced)");
        System.out.print("Your choice [1-3]: ");

        HeroFactory factory;
        switch (readInt(sc)) {
            case 2:  factory = new TankFactory();  break;
            case 3:  factory = new MageFactory();  break;
            default: factory = new SpeedsterFactory(); break;
        }

        System.out.print("Name your hero: ");
        String heroName = sc.nextLine().trim();
        if (heroName.isEmpty()) heroName = "Nova";

        Hero hero = factory.recruit(heroName);
        HeroHQ.getInstance().recordRecruit();
        System.out.println();

        // 2. Equip gear (Decorator)
        System.out.println("Choose your gear:");
        System.out.println("  1) Suit only         (+0 power)");
        System.out.println("  2) Suit + Cape       (+3 power)");
        System.out.println("  3) Suit + Shield     (+5 power)");
        System.out.println("  4) Suit + Cape + Shield + Gadget (+12 power)");
        System.out.print("Your choice [1-4]: ");

        Gear gear;
        switch (readInt(sc)) {
            case 2:  gear = new CapeUpgrade(new BasicGear());
            break;
            case 3:  gear = new ShieldUpgrade(new BasicGear());
            break;
            case 4:  gear = new GadgetUpgrade(new ShieldUpgrade(new CapeUpgrade(new BasicGear())));
            break;
            default: gear = new BasicGear();
            break;
        }
        hero.setGear(gear);
        System.out.println("Gear equipped: " + gear.description() + " (+" + gear.powerBonus() + " power)");
        System.out.println();

        // 3. Observer: the city calls for help
        AlertSystem dispatch = new AlertSystem();
        dispatch.addObserver(hero);                      // Hero IS an observer
        dispatch.addObserver(new NewsReporter("CNN"));   // different reaction, same event
        dispatch.broadcastThreat("Downtown", 7);
        System.out.println();

        // 4. Fight a wave of villains (Iterator hides how the wave is stored)
        VillainWave wave = new VillainWave();
        wave.add(new Villain("Mr Beast", 60, 14));
        wave.add(new Villain("Dr. Octopus", 90, 18));

        CommandHistory history = new CommandHistory();
        hero.getContext().enterBattle();

        for (Villain villain : wave) {
            System.out.println("=================================================");
            System.out.println("  A villain appears: " + villain.getName()
                + " (HP " + villain.getHp() + ")");
            System.out.println("=================================================");

            while (!villain.isDefeated() && !hero.isDown()) {
                System.out.println();
                System.out.println(hero.status());
                System.out.printf("%s  HP %d%n", villain.getName(), villain.getHp());
                System.out.println("State: " + hero.getContext().describe());
                System.out.println();

                System.out.println("Actions:");
                System.out.println("  1) Attack  (standard hit)");
                System.out.println("  2) Defend  (recover HP, skip attack)");
                System.out.println("  3) Ability (signature move, extra damage)");
                System.out.println("  4) Undo    (free -- reverses last action)");
                System.out.println("  0) Retreat (quit)");
                System.out.print("Your choice: ");

                int choice = readInt(sc);
                System.out.println();

                switch (choice) {
                    case 0:
                        System.out.println("You retreat. The city still needs you...");
                        HeroHQ.getInstance().printReport();
                        sc.close();
                        return;
                    case 1:
                        history.execute(new AttackCommand(hero, villain));
                        break;
                    case 2:
                        history.execute(new DefendCommand(hero));
                        break;
                    case 3:
                        history.execute(new UseAbilityCommand(hero, villain));
                        break;
                    case 4:
                        history.undoLast();
                        continue; // undo doesn't trigger a counter-attack
                    default:
                        System.out.println("Invalid choice, try again.");
                        continue;
                }

                // Villain counter-attacks if still standing
                if (!villain.isDefeated()) {
                    villain.strike(hero);
                } else {
                    System.out.println();
                    System.out.println("  " + villain.getName() + " is DEFEATED!");
                    HeroHQ.getInstance().recordVictory();
                }
            }

            if (hero.isDown()) {
                System.out.println();
                System.out.println("  " + hero.getName() + " has fallen... Game over.");
                HeroHQ.getInstance().printReport();
                sc.close();
                return;
            }
        }

        // 5. Victory
        hero.getContext().leaveBattle();
        System.out.println();
        System.out.println("=================================================");
        System.out.println("  All villains defeated! The city is safe.");
        System.out.println("=================================================");
        HeroHQ.getInstance().printReport();
        sc.close();
    }

    private static int readInt(Scanner sc) {
        try {
            int v = sc.nextInt();
            sc.nextLine();
            return v;
        } catch (Exception e) {
            sc.nextLine();
            return -1;
        }
    }
}
