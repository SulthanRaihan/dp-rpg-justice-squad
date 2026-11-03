package hero.decorator;

// Concrete component: the plain hero suit - no bonus, the base to wrap.
public class BasicGear implements Gear {
    public String description() {
        return "Suit";
    }
    public int powerBonus() {
        return 0;
    }
}
