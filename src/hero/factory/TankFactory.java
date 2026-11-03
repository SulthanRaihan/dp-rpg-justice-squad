package hero.factory;

import hero.core.Hero;
import hero.strategy.DefensiveStyle;

// Concrete creator: a tough, slow Tank with Defensive style.
public class TankFactory extends HeroFactory {
    protected Hero createHero(String name) {
        return new Hero(name,130,8, new DefensiveStyle());
    }
    protected String heroType() {
        return "Tank";
    }
}
