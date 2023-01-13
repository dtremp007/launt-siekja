def parse_args(interface):
    parser = argparse.ArgumentParser(
                    prog = 'launt-siekja',
                    description = 'Scrape websites and export data',
    )
    parser.add_argument("-w", "--website", help="The website to scrape.")
    parser.add_argument("-f", "--format", help="The format to export the data in.")
    args = parser.parse_args()
    for arg in vars(args):
        value = getattr(args, arg)
        if value is not None:
            interface.add_value(arg, value)
    return interface
