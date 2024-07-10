import logging

# Configure standard logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Ensure logs are output to the console
        logging.FileHandler("app.log"),
    ],
)

# Get a logger
logger = logging.getLogger(__name__)

# Debug statement to verify logging configuration
logger.info("Logging is configured correctly")
