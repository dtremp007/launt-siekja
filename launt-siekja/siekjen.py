#!/Users/david/opt/anaconda3/bin/python
from commands import start, run_update
import os
import sys
import utils
from interface import CLInterface

def main():
    config_file = utils.resolve_path("config.yaml")
    user_settings_file = utils.resolve_path("user_settings.yaml")

    interface = CLInterface(user_settings_file)

    try:
        run_update()
        start(config_file, interface)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        interface.close()

if __name__ == "__main__":
    main()
