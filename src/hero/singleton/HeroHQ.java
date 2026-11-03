package hero.singleton;

// SINGLETON PATTERN
public class HeroHQ {

    private int heroesRecruited  = 0;
    private int villainsDefeated = 0;

    // SINGLETON: private constructor + holder

    // Singleton - can't be built from outside
    private HeroHQ() {
    }
    // The one way to get it:
    public static HeroHQ getInstance() {
        return Holder.INSTANCE;
    }

    private static class Holder {
        static final HeroHQ INSTANCE = new HeroHQ();
    }

    // API

    public void recordRecruit() {
        heroesRecruited++;
    }
    public void recordVictory() {
        villainsDefeated++;
    }

    public int getHeroesRecruited() {
        return heroesRecruited;
    }
    public int getVillainsDefeated() {
        return villainsDefeated;
    }

    public void printReport() {
        System.out.printf("[HeroHQ] Report -- heroes recruited: %d | villains defeated: %d%n",
            heroesRecruited, villainsDefeated);
    }
}
