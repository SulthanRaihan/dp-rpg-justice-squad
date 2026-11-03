package hero.iterator;

import hero.core.Villain;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

//ITERATOR PATTERN
public class VillainWave implements Iterable<Villain> {

    private final List<Villain> villains = new ArrayList<>();

    public void add(Villain villain) {
        villains.add(villain);
    }

    public int size() {
        return villains.size();
    }

    @Override
    public Iterator<Villain> iterator() {
        return new WaveIterator(villains);
    }
}
