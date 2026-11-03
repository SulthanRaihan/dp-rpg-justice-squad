package hero.core;

import hero.decorator.BasicGear;
import hero.decorator.Gear;
import hero.observer.AlertObserver;
import hero.state.HeroContext;
import hero.strategy.CombatStyle;

/**
 * Central domain object. Holds the hero's stats and ties together four patterns:
 *   - Strategy  : CombatStyle decides damage / blocking
 *   - Decorator : Gear adds stacked power bonuses
 *   - State     : HeroContext tracks Available/OnMission/Injured/Retired
 *   - Observer  : Hero IS an AlertObserver - it reacts to threat broadcasts
 */
public class Hero implements AlertObserver {

    private final String name;
    private int hp;
    private final int maxHp;
    private final int basePower;

    private CombatStyle style;          // Strategy
    private Gear gear;                  // Decorator root
    private final HeroContext context;  // State

    public Hero(String name, int hp, int basePower, CombatStyle style) {
        this.name      = name;
        this.hp        = hp;
        this.maxHp     = hp;
        this.basePower = basePower;
        this.style     = style;
        this.gear      = new BasicGear();
        this.context   = new HeroContext(this);
    }

    // ── combat ───────────────────────────────────────────────────────────────

    // Attack a villain. Damage = (base + gear) -> style -> scaled by state.
    public int attack(Villain target) {
        int rawPower  = basePower + gear.powerBonus();
        int styled    = style.attackDamage(rawPower);
        int finalDmg  = styled * context.powerPercent() / 100;
        target.takeDamage(finalDmg);
        return finalDmg;
    }

    // Take a hit. The combat style may block part of it. State recalculates.
    public void takeDamage(int incoming) {
        int blocked = style.damageBlocked(incoming);
        int actual  = Math.max(0, incoming - blocked);
        hp = Math.max(0, hp - actual);
        if (blocked > 0) {
            System.out.printf("  %s blocks %d (%s style), takes %d.%n",
                name, blocked, style.name(), actual);
        }
        context.autoUpdate();
    }

    public void heal(int amount) {
        hp = Math.min(maxHp, hp + amount);
        context.autoUpdate();
    }

    // undo support
    public void setHp(int value) {
        hp = Math.max(0, Math.min(maxHp, value));
        context.autoUpdate();
    }

    // composition setters
    public void setStyle(CombatStyle s) { this.style = s; }
    public void setGear(Gear g)         { this.gear  = g; }

    // Observer: react to a city threat
    @Override
    public void onThreat(String location, int dangerLevel) {
        if (!context.canAct()) {
            System.out.printf("  %s is %s and cannot respond.%n", name, context.getStateName());
            return;
        }
        System.out.printf("  %s answers the call -- heading to %s!%n", name, location);
    }

    // getters
    public String getName() {
        return name;
    }
    public int getHp() {
        return hp;
    }
    public int getMaxHp() {
        return maxHp;
    }
    public boolean isDown() {
        return hp <= 0;
    }
    public CombatStyle getStyle() {
        return style;
    }
    public Gear getGear() {
        return gear;
    }
    public HeroContext getContext() {
        return context;
    }

    public String status() {
        return String.format("%s  HP %d/%d  [%s style, gear: %s, state: %s]",
            name, hp, maxHp, style.name(), gear.description(), context.getStateName());
    }
}
