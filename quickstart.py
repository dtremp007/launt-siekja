import argparse

def parse_args():
    parser = argparse.ArgumentParser(
                    prog = 'launt-siekja',
                    description = 'Scrape websites and export data',
    )
    parser.add_argument("-w", "--website", help="The website to scrape.")
    parser.add_argument("-f", "--format", default="Google Sheets", help="The format to export the data in. Default: Google Sheets")
    args = parser.parse_args()
    for arg in vars(args):
        # interface.add_value(arg, getattr(args, arg))
        print(getattr(args, arg))
    return args.website


parse_args()
