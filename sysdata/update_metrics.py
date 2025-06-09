import sys
import os
import csv
import json
import time
import signal
import shutil
from datetime import datetime

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..', 'backend')))

try:
    from backend.metrics.metrics import get_gpu_usage, get_system_metrics, get_gpu_fps  # type: ignore
except ImportError as e:
    print(f"Error importing metrics module: {e}")
    sys.exit(1)

terminate = False

def update_metrics():
    global terminate
    try:
        # Gather metrics
        metrics = {
            "cpu_metrics": get_system_metrics(),
            "gpu_metrics": get_gpu_usage(),
            "fps": get_gpu_fps(),
            "timestamp": datetime.now().strftime("%H:%M:%S")  # ✅ Convert timestamp to readable format
        }

        # Save metrics to JSON file
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(data_dir, exist_ok=True)
        metrics_file_path = os.path.join(data_dir, 'metrics.json')

        with open(metrics_file_path, 'w') as file:
            json.dump(metrics, file, indent=4)

        # Append metrics to CSV log file
        logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        logs_file_path = os.path.join(logs_dir, 'logs.csv')

        file_exists = os.path.isfile(logs_file_path)
        with open(logs_file_path, 'a', newline='') as csvfile:
            fieldnames = [
                'timestamp', 'cpu_usage', 'cpu_count', 'cpu_user_time', 'cpu_system_time',
                'cpu_idle_time', 'cpu_temp', 'gpu_id', 'gpu_name', 'gpu_memory_total',
                'gpu_memory_used', 'gpu_util', 'gpu_temp', 'fps'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            
            for gpu in metrics['gpu_metrics']:
                writer.writerow({
                    'timestamp': metrics['timestamp'],
                    'cpu_usage': metrics['cpu_metrics']['cpu_usage'],
                    'cpu_count': metrics['cpu_metrics']['cpu_count'],
                    'cpu_user_time': metrics['cpu_metrics']['cpu_user_time'],
                    'cpu_system_time': metrics['cpu_metrics']['cpu_system_time'],
                    'cpu_idle_time': metrics['cpu_metrics']['cpu_idle_time'],
                    'cpu_temp': metrics['cpu_metrics']['cpu_temp'],
                    'gpu_id': gpu['gpu_id'],
                    'gpu_name': gpu['gpu_name'],
                    'gpu_memory_total': gpu['gpu_memory_total'],
                    'gpu_memory_used': gpu['gpu_memory_used'],
                    'gpu_util': gpu['gpu_util'],
                    'gpu_temp': gpu['gpu_temp'],
                    'fps': metrics['fps']
                })
    
    except Exception as e:
        print(f"Error updating metrics: {e}")

def terminate_metrics_collection(signum, frame):
    global terminate
    print("Terminating metrics collection...")
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    if os.path.exists(data_dir):
        shutil.rmtree(data_dir)
    terminate = True

if __name__ == "__main__":
    signal.signal(signal.SIGINT, terminate_metrics_collection)
    while not terminate:
        update_metrics()
        time.sleep(0.5)
