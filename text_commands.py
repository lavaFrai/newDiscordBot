def info(text):
    print("[INFO]\t" + text)


def main():
    commands = {}

    def bot_text_command(func):
        info(f"Registered command {func.__name__.lower()}")
        commands[func.__name__] = func

    @bot_text_command
    def test(ctx):
        return "Test answer"

    return commands
