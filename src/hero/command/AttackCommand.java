package hero.command;

import hero.core.Hero;
import hero.core.Villain;

// Hero attacks a villain. Captures the villain's HP before/after so undo
// restores exactly the damage that was actually dealt.

public class AttackCommand implements Command {

    private final Hero hero;
    private final Villain target;
    private int villainHpBefore;

    public AttackCommand(Hero hero, Villain target) {
        this.hero = hero;
        this.target = target;
    }

    @Override
    public void execute() {
        villainHpBefore = target.getHp();
        int dmg = hero.attack(target);
        System.out.printf("  %s attacks %s for %d damage! (%s HP: %d)%n",
            hero.getName(), target.getName(), dmg, target.getName(), target.getHp());
    }

    @Override
    public void undo() {
        target.takeDamage(target.getHp() - villainHpBefore); // negative = heal back
        System.out.printf("  [Undo] Attack cancelled -- %s HP restored to %d.%n",
            target.getName(), target.getHp());
    }

    @Override
    public String description() {
        return "Attack (" + hero.getStyle().name() + ")";
    }
}
