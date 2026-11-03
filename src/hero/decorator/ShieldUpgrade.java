package hero.decorator;

// Decorator: a reinforced shield, +5 power.
public class ShieldUpgrade extends GearUpgrade {
    public ShieldUpgrade(Gear inner) { super(inner); }

    public String description() {
        return inner.description() + " + Shield";
    }
    public int powerBonus() {
        return inner.powerBonus() + 5;
    }
}
