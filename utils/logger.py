from loguru import logger
import sys

def configure_logger(log_file_path: str) -> logger:
    """
    This function configures the loguru logger instance, that will be used throught the application.

    Args:
        log_file_path: str

    Returns:
        logger: logger
    """

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
