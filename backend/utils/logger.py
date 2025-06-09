import logging
import os

def setup_logger():
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(__file__), '../../sysdata/logs')
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, 'app.log')

    # Configure the logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",  # ✅ Added timestamp
        handlers=[
            logging.FileHandler(log_file),  # ✅ Logs to a file
            logging.StreamHandler()  # ✅ Also logs to console
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logger()

if __name__ == "__main__":
    logger.info("Logger is set up.")  # ✅ Test log
