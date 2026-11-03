package hero.command;

import java.util.ArrayDeque;
import java.util.Deque;

// Invoker: runs commands and keeps a history stack for undo.
// It knows nothing about what each command does -- only execute() and undo().

public class CommandHistory {

    private final Deque<Command> history = new ArrayDeque<>();

    public void execute(Command cmd) {
        cmd.execute();
        history.push(cmd);
    }

    public void undoLast() {
        if (history.isEmpty()) {
            System.out.println("  Nothing to undo.");
            return;
        }
        Command cmd = history.pop();
        System.out.printf("  Undoing: %s%n", cmd.description());
        cmd.undo();
    }

    public boolean hasHistory() {
        return !history.isEmpty();
    }
}
