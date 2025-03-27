from utils.logger import configure_logger
from syncronizer import SyncFold
import argparse
import time

def parse_passed_arguments():
    parser = argparse.ArgumentParser(description="Folder Synchronization Settings")
    parser.add_argument("--source_folder", help="Path to source folder")
    parser.add_argument("--replica_folder", help="Path to destiny folder")
    parser.add_argument("--interval", type=int, help="Synchronization interval format: (seconds)")
    parser.add_argument("--log_folder", help="Path to logs file")

    return parser.parse_args()

def main():
    args = parse_passed_arguments()

    source = args.source_folder
    destiny = args.replica_folder
    periodic_interval = args.interval
    log_folder_path = args.log_folder

    logger = configure_logger(log_folder_path)
    try:
        while True:
            synchronizer = SyncFold(source, destiny, logger)
            synchronizer.run_sincronization()
            time.sleep(periodic_interval)
    except KeyboardInterrupt:
        logger.info("Program stopped throught keyboard. Synchronization Stopped.")
    except Exception as e:
        logger.error(str(e))


if __name__ == "__main__":
    main()