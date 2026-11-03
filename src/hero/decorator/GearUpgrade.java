package hero.decorator;

public abstract class GearUpgrade implements Gear {
    protected final Gear inner;

    protected GearUpgrade(Gear inner) {
        this.inner = inner;
    }
}
