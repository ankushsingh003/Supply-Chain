# Qualitative Alpha: Supply Chain Monitoring with YOLO v11

Leveraging YOLO v11 to monitor supply chain activity (e.g., freight movement) to provide "Qualitative Alpha" for hedge fund style investment strategies.

## Features
- **YOLOv11 Detection**: High-speed detection of trucks, boats, trains, and cars.
- **Activity Index**: Real-time monitoring of logistical frequency.
- **Alpha Engine**: Trend analysis and financial signal generation.
- **Interactive Dashboard**: Streamlit-based visualization of supply chain velocity.

## Getting Started
1. Install dependencies: `pip install ultralytics opencv-python pandas streamlit plotly`
2. Run the dashboard: `streamlit run dashboard.py`

## Architecture
- `detector.py`: YOLOv11 integration.
- `tracker.py`: Real-time object tracking.
- `alpha_engine.py`: Financial signal logic.
- `dashboard.py`: Streamlit UI.
