import os


def main():
    # Command
    cmd = """osascript -e '
    set Message to "You have a new message!"
    display dialog Message
    '
    """

    # Execute
    os.system(cmd)


if __name__ == "__main__":
    main()
