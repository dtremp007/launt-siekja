#!/Users/david/opt/anaconda3/bin/python
from commands import start, run_update
import os
import sys
import utils
from interface import CLInterface

def main():
    config_file = utils.resolve_path("config.yaml")
    interface = CLInterface()

    try:
        run_update()
        start(config_file, interface)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")

if __name__ == "__main__":
    main()
