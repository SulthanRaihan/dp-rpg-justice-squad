package hero.strategy;

// Hits hard, blocks nothing. Glass-cannon fighters.
public class AggressiveStyle implements CombatStyle {
    public String name() {
        return "Aggressive";
    }
    public int attackDamage(int rawPower) {
        return rawPower + 8;
    }
    public int damageBlocked(int incoming) {
        return 0;
    }
}
