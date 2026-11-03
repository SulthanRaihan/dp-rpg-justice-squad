package hero.observer;

/**
 * A CONCRETE OBSERVER that reacts to the SAME threat event as the heroes,
 * but does something completely different: it reports the news. Proves the
 * subject is decoupled from what its observers do.
 */
public class NewsReporter implements AlertObserver {

    private final String channel;

    public NewsReporter(String channel) {
        this.channel = channel;
    }

    @Override
    public void onThreat(String location, int dangerLevel) {
        System.out.printf("  [News-%s] BREAKING: villain spotted at %s (danger %d/10)!%n",
            channel, location, dangerLevel);
    }
}
