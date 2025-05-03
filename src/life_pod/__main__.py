import sys
from .game import Cli
# from .game import Gui
from .guiapp import LifePodApp


def main():
    if len(sys.argv) > 1 and 'cli' in sys.argv:
        game = Cli()
        game.play()
    else:
        LifePodApp().run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit()