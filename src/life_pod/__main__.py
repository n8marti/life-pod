import sys
from .game import Cli
from .game import Gui


def main():
    if len(sys.argv) > 1 and 'cli' in sys.argv:
        game = Cli()
    else:
        game = Gui()
    game.play()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit()