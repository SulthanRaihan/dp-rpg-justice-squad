package hero.factory;

import hero.core.Hero;
import hero.strategy.AggressiveStyle;

// Concrete creator: a fast, fragile Speedster with Aggressive style.
public class SpeedsterFactory extends HeroFactory {
    protected Hero createHero(String name) {
        return new Hero(name,80,12, new AggressiveStyle());
    }
    protected String heroType() {
        return "Speedster";
    }
}
