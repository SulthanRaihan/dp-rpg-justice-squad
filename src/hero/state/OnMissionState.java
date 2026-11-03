package hero.state;

// Engaged in battle, healthy, fighting at full strength.
public class OnMissionState implements HeroState {
    public String  name() {
        return "OnMission";
    }
    public String  describe() {
        return "In the field, trading blows with a villain.";
    }
    public boolean canAct() {
        return true;
    }
    public int powerPercent() {
        return 100;
    }
}
