package hero.state;

// Badly hurt: still fights, but deals only 60% damage.
public class InjuredState implements HeroState {
    public String name() {
        return "Injured";
    }
    public String describe() {
        return "Wounded and bleeding - attacks are weaker.";
    }
    public boolean canAct() {
        return true;
    }
    public int powerPercent() {
        return 60;
    }
}
