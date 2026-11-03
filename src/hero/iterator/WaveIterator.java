package hero.iterator;

import hero.core.Villain;
import java.util.List;
import java.util.Iterator;
import java.util.NoSuchElementException;

/** Concrete iterator: walks a villain list one step at a time, nothing more. */
public class WaveIterator implements Iterator<Villain> {

    private final List<Villain> villains;
    private int index = 0;

    public WaveIterator(List<Villain> villains) {
        this.villains = villains;
    }

    @Override
    public boolean hasNext() {
        return index < villains.size();
    }

    @Override
    public Villain next() {
        if (!hasNext()) throw new NoSuchElementException("No more villains in this wave.");
        Villain villain = villains.get(index++);
        System.out.printf("  [Iterator] next villain in the wave: %s%n", villain.getName());
        return villain;
    }
}
