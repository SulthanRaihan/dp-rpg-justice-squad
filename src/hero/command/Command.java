package hero.command;

// COMMAND PATTERN
public interface Command {
    void execute();
    void undo();
    String description();
}
