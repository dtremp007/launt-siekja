#!/Users/david/opt/anaconda3/bin/python
from commands import start, run_update
import os
import sys
import utils

def main():
    try:
        run_update()
        scraper = start(utils.resolve_path("config.yaml"))
        scraper.run()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")

if __name__ == "__main__":
    main()
