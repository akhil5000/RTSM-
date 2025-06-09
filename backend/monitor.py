from .metrics.metrics import get_gpu_usage, get_system_metrics, get_gpu_fps # type: ignore
try:
    from .utils.logger import logger
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

# Function to monitor system metrics and log the information
def monitor_system():
    logger.info("Monitoring system...")
    
    try:
        gpu_usage = get_gpu_usage()  # Get GPU usage
        system_metrics = get_system_metrics()  # Get system metrics
        gpu_fps = get_gpu_fps()  # Get GPU frames per second

        logger.info(f"GPU Usage: {gpu_usage}")  # Log GPU usage
        logger.info(f"System Metrics: {system_metrics}")  # Log system metrics
        logger.info(f"GPU FPS: {gpu_fps}")  # Log GPU FPS
        logger.info(f"CPU Temperature: {system_metrics.get('cpu_temp', 'N/A')}")  # Log CPU temperature

    except Exception as e:
        logger.error(f"Error collecting metrics: {e}")

# Main entry point of the script
if __name__ == "__main__":
    monitor_system()
