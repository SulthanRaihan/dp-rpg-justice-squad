package hero.state;

// Knocked out (HP 0). Terminal: cannot act until revived.
public class RetiredState implements HeroState {
    public String  name() {
        return "Retired";
    }
    public String  describe() {
        return "Down for the count - out of the fight.";
    }
    public boolean canAct() {
        return false;
    }
    public int powerPercent() {
        return 0;
    }
}
