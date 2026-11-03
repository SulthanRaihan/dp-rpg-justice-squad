package hero.strategy;

// Weaker punches, but soaks up half of incoming damage. Tanks.
public class DefensiveStyle implements CombatStyle {
    public String name() {
        return "Defensive";
    }
    public int attackDamage(int rawPower) {
        return rawPower + 2;
    }
    public int damageBlocked(int incoming) {
        return incoming / 2;
    }
}
