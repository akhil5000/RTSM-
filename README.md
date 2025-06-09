System Metrics Dashboard 🖥️📊
A real-time monitoring dashboard that tracks CPU usage, GPU usage, FPS, and temperature. Built with Python, Streamlit, and psutil/GPUtil.

📌 Features
✅ Real-time CPU & GPU monitoring (Usage, Temperature, Utilization)
✅ Live FPS counter
✅ Automatic logging to JSON & CSV
✅ Interactive Streamlit Dashboard with real-time graphs
✅ Auto-starts data collection when the dashboard is launched

🚀 Installation & Setup

1️⃣ Install Dependencies
Run this in your terminal: pip install psutil GPUtil streamlit pandas matplotlib

2️⃣ Start the Dashboard
Simply run:
streamlit run frontend/dashboard.py

✅ Automatically starts system monitoring
✅ Opens a web UI for visualization

📊 How It Works
1️⃣ Backend (backend/) → Collects system metrics using psutil & GPUtil.
2️⃣ Sysdata (sysdata/) → Stores metrics in metrics.json & logs.csv.
3️⃣ Frontend (frontend/) → A Streamlit dashboard visualizing real-time data.

✅ The dashboard automatically starts & stops data collection.

📂 Project Structure

vscode3/
├── backend/               # Core logic for data collection
│   ├── metrics/           # System monitoring scripts
│   │   └── metrics.py     # CPU, GPU, FPS collection
│   ├── utils/             # Helper utilities
│   │   └── logger.py      # Logging system
│   └── monitor.py         # Runs the monitoring system
├── frontend/              # User interface (Streamlit)
│   └── dashboard.py       # Main dashboard
├── sysdata/               # Data storage
│   ├── data/              # JSON metric storage
│   ├── logs/              # CSV logs
│   └── update_metrics.py  # Background process for metrics
└── README.md              # Project documentation

📌 Data Storage & Logging
JSON File: sysdata/data/metrics.json → Stores the latest system stats.
CSV File: sysdata/logs/logs.csv → Keeps a history of system performance.
Log File: sysdata/logs/app.log → Debugging logs for tracking issues.

📈 Viewing Real-Time Graphs
1️⃣ Start the dashboard using:
streamlit run frontend/dashboard.py

2️⃣ Check "Show Real-time Graphs" checkbox.

3️⃣ View CPU Usage, GPU Temperature, and FPS trends.

🛑 Stopping the Metrics Collection
Option 1: From the Dashboard
Uncheck "Start Metrics Collection"
✅ The process will automatically stop & delete old data.
Option 2: Manually Kill the Process
If the process doesn't stop, run:
pkill -f update_metrics.py  # Linux/Mac
taskkill /IM python.exe /F  # Windows (If running as python.exe)

🐛 Debugging & Troubleshooting
1️⃣ Metrics Not Updating?
Check if update_metrics.py is running.
Restart by stopping and restarting the dashboard.
2️⃣ No GPU Data?
Make sure you have a dedicated GPU (like NVIDIA).
Try running: python -c "import GPUtil; print(GPUtil.getGPUs())"

If no output, GPUtil isn’t detecting your GPU.
3️⃣ Logs Not Updating?
Check the log file: 
cat sysdata/logs/app.log  # Linux/Mac
type sysdata/logs/app.log  # Windows

📜 License
This project is open-source and free to use.

💡 Future Improvements
🚀 Add network monitoring
🚀 Improve multi-GPU support
🚀 Add email alerts for overheating

🎉 Now You're Ready to Monitor Your System in Real-Time!
Run the dashboard and enjoy live performance tracking! 🚀📊