import logging
from src.batch_loader.migrator import Migrator


def main():
    migrator = Migrator()
    migrator.run()


logging.getLogger().setLevel(logging.INFO)
if __name__ == "__main__":
    main()
