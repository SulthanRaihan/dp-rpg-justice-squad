package hero.strategy;

public interface CombatStyle {

    // Label shown in status (e.g. "Aggressive").
    String name();

    // Turn the hero's raw power into outgoing damage.
    int attackDamage(int rawPower);

    // How much incoming damage this style blocks (0 = none).
    int damageBlocked(int incoming);
}
