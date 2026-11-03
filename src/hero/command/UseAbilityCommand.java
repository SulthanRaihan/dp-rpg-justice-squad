package hero.command;

import hero.core.Hero;
import hero.core.Villain;

// Hero unleashes a signature ability: a normal attack plus a flat bonus.
// Captures the villain's HP before so undo reverses the whole hit.

public class UseAbilityCommand implements Command {

    private static final int BONUS = 10;

    private final Hero hero;
    private final Villain target;
    private int villainHpBefore;

    public UseAbilityCommand(Hero hero, Villain target) {
        this.hero   = hero;
        this.target = target;
    }

    @Override
    public void execute() {
        villainHpBefore = target.getHp();
        int dmg = hero.attack(target) + BONUS;
        target.takeDamage(BONUS); // apply the bonus on top of the styled attack
        System.out.printf("  %s unleashes a SIGNATURE ABILITY on %s for %d! (%s HP: %d)%n",
            hero.getName(), target.getName(), dmg, target.getName(), target.getHp());
    }

    @Override
    public void undo() {
        target.takeDamage(target.getHp() - villainHpBefore); // negative = heal back
        System.out.printf("  [Undo] Ability cancelled -- %s HP restored to %d.%n",
            target.getName(), target.getHp());
    }

    @Override
    public String description() { return "Ability"; }
}
