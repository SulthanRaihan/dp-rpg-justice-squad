package hero.command;

import hero.core.Hero;

// Hero braces and recovers some HP instead of attacking.
// Stores HP before so undo restores it exactly.

public class DefendCommand implements Command {

    private static final int RECOVER = 12;

    private final Hero hero;
    private int hpBefore;

    public DefendCommand(Hero hero) {
        this.hero = hero;
    }

    @Override
    public void execute() {
        hpBefore = hero.getHp();
        hero.heal(RECOVER);
        System.out.printf("  %s braces and recovers HP (now %d/%d).%n",
            hero.getName(), hero.getHp(), hero.getMaxHp());
    }

    @Override
    public void undo() {
        hero.setHp(hpBefore);
        System.out.printf("  [Undo] Defend cancelled - %s HP back to %d.%n",
            hero.getName(), hero.getHp());
    }

    @Override
    public String description() { return "Defend"; }
}
