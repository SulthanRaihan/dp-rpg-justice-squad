package hero.state;

//PATTERN STATE
public interface HeroState {

    // Short label shown in the UI (e.g. "Available").
    String name();

    // Flavor text shown to the player.
    String describe();

    // False = the hero cannot take a turn (e.g. Retired / knocked out).
    boolean canAct();

    // Damage dealt is scaled by this percent (Injured heroes hit weaker).
    int powerPercent();
}
