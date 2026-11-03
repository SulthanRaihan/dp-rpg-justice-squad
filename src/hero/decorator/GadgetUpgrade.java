package hero.decorator;

// Decorator: a high-tech gadget belt, +4 power.
public class GadgetUpgrade extends GearUpgrade {
    public GadgetUpgrade(Gear inner) {
        super(inner);
    }

    public String description() {
        return inner.description() + " + Gadget";
    }
    public int powerBonus() {
        return inner.powerBonus() + 4;
    }
}
