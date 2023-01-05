from commands import start

def main():
    try:
        scraper = start("config.yaml")
        scraper.run()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")

if __name__ == "__main__":
    main()
