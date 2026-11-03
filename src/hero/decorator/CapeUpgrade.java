package hero.decorator;

// Decorator: a flowing cape, +3 power.
public class CapeUpgrade extends GearUpgrade {
    public CapeUpgrade(Gear inner) {
        super(inner);
    }

    public String description() {
        return inner.description() + " + Cape";
    }
    public int powerBonus() {
        return inner.powerBonus() + 3;
    }
}
