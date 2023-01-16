#!/Users/david/opt/anaconda3/bin/python
from commands import start, run_update
import os
import sys
import utils
from interface import CLInterface

def set_project_root():
    """
    Sets the working directory to the root of this project.
    This allows me to use relative paths throughout the project.
    """
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

def main():
    config_file = utils.resolve_path("config.yaml")
    user_settings_file = utils.resolve_path("user_settings.yaml")

    interface = CLInterface(user_settings_file)

    try:
        run_update()
        start(config_file, interface)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    # except Exception as e:
    #     print(e)
    finally:
        interface.close()

if __name__ == "__main__":
    main()
