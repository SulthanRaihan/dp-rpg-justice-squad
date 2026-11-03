package hero.factory;

import hero.core.Hero;

//FACTORY PATTERN
public abstract class HeroFactory {

    // Template method: recruit a hero. Calls the factory method internally.
    public Hero recruit(String name) {
        Hero hero = createHero(name);
        System.out.printf("[Recruit] %s the %s joins the squad! (%s style)%n",
            name, heroType(), hero.getStyle().name());
        return hero;
    }

    // Factory method - subclass decides which Hero (and style) to create.
    protected abstract Hero createHero(String name);

    // Short type label used in the recruit message.
    protected abstract String heroType();
}
