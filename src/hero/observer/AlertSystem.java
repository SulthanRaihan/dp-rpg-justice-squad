package hero.observer;

import java.util.ArrayList;
import java.util.List;

public class AlertSystem implements ThreatSubject {

    private final List<AlertObserver> observers = new ArrayList<>();

    @Override
    public void addObserver(AlertObserver o) {
        observers.add(o);
    }
    @Override
    public void removeObserver(AlertObserver o) {
        observers.remove(o);
    }

    // Fire the alert. All observers react in their own way. 
    public void broadcastThreat(String location, int dangerLevel) {
        System.out.printf("  [ALERT] Threat at %s! Danger level %d. Dispatching...%n",
            location, dangerLevel);
        for (AlertObserver o : observers) {
            o.onThreat(location, dangerLevel);
        }
    }
}
