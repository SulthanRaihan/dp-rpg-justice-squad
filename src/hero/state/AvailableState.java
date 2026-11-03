package hero.state;

// Healthy and idle, ready for action at full strength.
public class AvailableState implements HeroState {
    public String name() {
        return "Available";
    }
    public String describe() {
        return "Standing by at full strength.";
    }
    public boolean canAct() {
        return true;
    }
    public int powerPercent() {
        return 100;
    }
}
