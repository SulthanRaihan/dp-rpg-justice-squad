package hero.factory;

import hero.core.Hero;
import hero.strategy.TacticalStyle;

// Concrete creator: a balanced Mage with Tactical style.
public class MageFactory extends HeroFactory {
    protected Hero createHero(String name) {
        return new Hero(name,100,10, new TacticalStyle());
    }
    protected String heroType() {
        return "Mage";
    }
}
