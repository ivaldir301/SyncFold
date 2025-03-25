from loguru import logger
import datetime as dt
import sys

def configure_logger(log_file_path):
    logger.add(
        log_file_path,
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} - {level} - {message}",
        rotation="10 MB", 
        retention="7 days", 
        compression="zip"
    )

    logger.add(
        sys.stdout,
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} - {level} - {message}"
    )
    logger.info("Logger configured successfully.")
    return logger



# log_directory = "./logs/logs_today_v2.log"
# logger = configure_logger(log_directory)

# logger.info("Logging from the main module.")