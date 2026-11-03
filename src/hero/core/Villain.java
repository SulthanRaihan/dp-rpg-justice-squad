package hero.core;

public class Villain {

    private final String name;
    private int hp;
    private final int power;

    public Villain(String name, int hp, int power) {
        this.name  = name;
        this.hp    = hp;
        this.power = power;
    }

    /** Counter-attack a hero. */
    public int strike(Hero target) {
        System.out.printf("  %s strikes %s for %d!%n", name, target.getName(), power);
        target.takeDamage(power);
        return power;
    }

    public void takeDamage(int amount) {
        hp = Math.max(0, hp - amount);
    }

    public String getName() {
        return name;
    }
    public int getHp() {
        return hp;
    }
    public boolean isDefeated() {
        return hp <= 0;
    }
}
