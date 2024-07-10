from app.config.logging_config import logger


def log_message(level: str, event: str, **kwargs):
    """
    Log a message with the given level and event.

    Args:
        level (str): The log level (e.g., "info", "error").
        event (str): The event description.
        **kwargs: Additional key-value pairs to include in the log.
    """

    logging_string = f"{event} {kwargs}"

    # make log using logger
    logger.info(logging_string)
