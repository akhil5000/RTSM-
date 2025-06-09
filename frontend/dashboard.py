import streamlit as st
import subprocess
import os
import json
import time
import shutil
import pandas as pd
import matplotlib.pyplot as plt

st.title("System Metrics Dashboard")

# Initialize session state for process
if 'process' not in st.session_state:
    st.session_state.process = None

start_collection = st.checkbox('Start Metrics Collection')

# Add a simple checkbox
simple_checkbox = st.checkbox('Show Real-time Graphs')

if start_collection:
    if st.session_state.process is None:
        # Start the metrics collection script
        st.session_state.process = subprocess.Popen(["python", "../vscode3/sysdata/update_metrics.py"])
        st.write("Metrics collection started.")
        time.sleep(5)  # Increase the delay to allow more time for the JSON file to be generated
else:
    if st.session_state.process is not None:
        # Terminate the metrics collection script
        st.session_state.process.terminate()
        st.write("Metrics collection terminated.")
        st.session_state.process = None
        # Delete the data directory
        data_dir = os.path.join(os.path.dirname(__file__), '../sysdata/data')
        if os.path.exists(data_dir):
            shutil.rmtree(data_dir)

data_dir = os.path.join(os.path.dirname(__file__), '../sysdata/data')
metrics_file_path = os.path.join(data_dir, 'metrics.json')

if os.path.exists(metrics_file_path):
    st.write("Metrics file found.")
    
    # Create placeholders for the metrics
    cpu_usage_placeholder = st.empty()
    cpu_count_placeholder = st.empty()
    cpu_user_time_placeholder = st.empty()
    cpu_system_time_placeholder = st.empty()
    cpu_idle_time_placeholder = st.empty()
    cpu_temp_placeholder = st.empty()
    gpu_metrics_placeholder = st.empty()
    fps_placeholder = st.empty()

    while start_collection:
        with open(metrics_file_path, 'r') as file:
            metrics = json.load(file)
        
        # Update placeholders with the latest metrics
        cpu_usage_placeholder.text(f"CPU Usage: {metrics['cpu_metrics']['cpu_usage']}%")
        cpu_count_placeholder.text(f"CPU Count: {metrics['cpu_metrics']['cpu_count']}")
        cpu_user_time_placeholder.text(f"CPU User Time: {metrics['cpu_metrics']['cpu_user_time']}%")
        cpu_system_time_placeholder.text(f"CPU System Time: {metrics['cpu_metrics']['cpu_system_time']}%")
        cpu_idle_time_placeholder.text(f"CPU Idle Time: {metrics['cpu_metrics']['cpu_idle_time']}%")
        cpu_temp_placeholder.text(f"CPU Temperature: {metrics['cpu_metrics']['cpu_temp']}°C")
        
        gpu_metrics = metrics['gpu_metrics'][0]  # Assuming single GPU for simplicity
        gpu_metrics_placeholder.text(f"GPU {gpu_metrics['gpu_id']} - {gpu_metrics['gpu_name']}: {gpu_metrics['gpu_util']}% Utilization, {gpu_metrics['gpu_temp']}°C")
        
        fps_placeholder.text(f"FPS: {metrics['fps']}")
        
        time.sleep(2)  # Update every 2 seconds
        
        if not start_collection:
            st.session_state.process.terminate()
            st.write("Metrics collection terminated.")
            st.session_state.process = None
            # Delete the data directory
            if os.path.exists(data_dir):
                shutil.rmtree(data_dir)
            break
else:
    st.write("Metrics file not found. Please start the metrics collection.")

# Real-time graphs for GPU temperature, FPS, and CPU utilization
if simple_checkbox:
    logs_file_path = os.path.join(os.path.dirname(__file__), '../sysdata/logs/logs.csv')
    if os.path.exists(logs_file_path):
        df = pd.read_csv(logs_file_path)

        # Convert timestamp to datetime format
        #df['timestamp'] = pd.to_datetime(df['timestamp'])

        st.write("### **Real-time Graphs**")

        # GPU Temperature Graph
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df['timestamp'], df['gpu_temp'], label='GPU Temperature', color='red', linestyle='-')
        ax.set_xlabel('Timestamp')
        ax.set_ylabel('Temperature (°C)')
        ax.set_title('GPU Temperature Over Time')
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.6)
        fig.autofmt_xdate()  # Prevents x-axis label overlap
        st.pyplot(fig)

        # FPS Graph
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df['timestamp'], df['fps'], label='FPS', color='blue', linestyle='--')
        ax.set_xlabel('Timestamp')
        ax.set_ylabel('Frames Per Second')
        ax.set_title('FPS Over Time')
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.6)
        fig.autofmt_xdate()
        st.pyplot(fig)

        # CPU Utilization Graph
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df['timestamp'], df['cpu_usage'], label='CPU Utilization', color='green', linestyle='-.')
        ax.set_xlabel('Timestamp')
        ax.set_ylabel('CPU Usage (%)')
        ax.set_title('CPU Utilization Over Time')
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.6)
        fig.autofmt_xdate()
        st.pyplot(fig)

    else:
        st.write("Logs file not found.")
