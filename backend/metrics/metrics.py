import time
import GPUtil
import psutil

# GPU Metrics
def get_gpu_usage():
    gpus = GPUtil.getGPUs()
    gpu_usage = []
    for gpu in gpus:
        gpu_usage.append({
            'gpu_id': gpu.id,
            'gpu_name': gpu.name,
            'gpu_memory_total': gpu.memoryTotal,
            'gpu_memory_used': gpu.memoryUsed,
            'gpu_util': gpu.load * 100,  # ✅ Fixed GPU utilization calculation
            'gpu_temp': gpu.temperature
        })
    return gpu_usage

# System Metrics
def get_system_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()
    cpu_times = psutil.cpu_times_percent(interval=1, percpu=False)
    
    # Get CPU temperature (Handle Windows Compatibility)
    cpu_temp = None
    try:
        temps = psutil.sensors_temperatures()
        if temps and 'coretemp' in temps:
            cpu_temp = temps['coretemp'][0].current
    except (AttributeError, KeyError):
        cpu_temp = None  # ✅ Fixed Windows compatibility

    system_metrics = {
        'cpu_usage': cpu_usage,
        'cpu_count': cpu_count,
        'cpu_user_time': cpu_times.user,
        'cpu_system_time': cpu_times.system,
        'cpu_idle_time': cpu_times.idle,
        'cpu_temp': cpu_temp
    }
    
    return system_metrics

# FPS Metrics
class FPS:
    def __init__(self):
        self.start_time = None
        self.frame_count = 0

    def start(self):
        self.start_time = time.time()
        self.frame_count = 0

    def update(self):
        self.frame_count += 1

    def get_fps(self):
        if self.start_time is None:
            return 0
        elapsed_time = time.time() - self.start_time
        return self.frame_count / elapsed_time if elapsed_time > 0 else 0

def get_gpu_fps():
    fps = FPS()
    fps.start()
    time.sleep(1)  # Simulate a delay to gather GPU load
    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        if gpu.load > 0:  # Only update FPS if GPU load is greater than 0
            fps.update()
    return fps.get_fps()

if __name__ == "__main__":
    print("GPU Usage:", get_gpu_usage())
    print("System Metrics:", get_system_metrics())
    print("GPU FPS:", get_gpu_fps())
