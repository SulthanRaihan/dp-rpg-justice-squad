package hero.state;

import hero.core.Hero;

/**
 * The STATE CONTEXT (like GumballMachine in Head First ch.10).
 * Holds the current HeroState and recalculates it from the hero's HP.
 */
public class HeroContext {

    private final Hero hero;
    private HeroState state;
    private boolean inBattle = false;

    public HeroContext(Hero hero) {
        this.hero  = hero;
        this.state = new AvailableState();
    }

    public void enterBattle() {
        inBattle = true;  autoUpdate();
    }
    public void leaveBattle() {
        inBattle = false; autoUpdate();
    }

    // Pick the right state from current HP. Transitions happen here.
    public void autoUpdate() {
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
    }

    public void setState(HeroState newState) {
        if (!newState.name().equals(state.name())) {
            System.out.printf("  >> %s is now %s%n", hero.getName(), newState.name());
        }
        this.state = newState;
    }

    public HeroState getState() {
        return state;
    }
    public String getStateName() {
        return state.name();
    }
    public String describe() {
        return state.describe();
    }
    public boolean canAct() {
        return state.canAct();
    }
    public int powerPercent() {
        return state.powerPercent();
    }
}
