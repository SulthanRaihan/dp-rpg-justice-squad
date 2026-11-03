package hero.strategy;

// Balanced damage and a small block. Spellcasters / strategists.
public class TacticalStyle implements CombatStyle {
    public String name() {
        return "Tactical";
    }
    public int attackDamage(int rawPower) {
        return rawPower + 5;
    }
    public int damageBlocked(int incoming) {
        return incoming / 4;
    }
}
