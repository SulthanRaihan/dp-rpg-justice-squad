package hero.observer;

//OBSERVER PATTERN
public interface AlertObserver {

    /**
     * Called when a threat is broadcast to the city.
     *
     * @param location    where the villain appeared
     * @param dangerLevel 1..10 severity of the threat
     */
    void onThreat(String location, int dangerLevel);
}
