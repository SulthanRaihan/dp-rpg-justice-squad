package hero.decorator;

// DECORATOR PATTERN
public interface Gear {

    // Description of every layer (e.g. "Suit + Cape + Shield").
    String description();

    // Total power added to the hero's raw attack power.
    int powerBonus();
}
