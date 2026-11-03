package hero.observer;

/**
 * The SUBJECT contract: anything that can register/unregister AlertObservers
 * and broadcast a threat to all of them.
 */
public interface ThreatSubject {
    void addObserver(AlertObserver observer);
    void removeObserver(AlertObserver observer);
}
