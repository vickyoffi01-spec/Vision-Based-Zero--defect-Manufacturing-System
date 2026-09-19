# Vision-Based Bolt Manufacturing Inspection

This application inspects **BOLTS ONLY** from a real webcam. It runs webcam frames through OpenCV, the custom YOLOv8 model, the bolt decision engine, a virtual PLC, and SQLite persistence before displaying the Streamlit dashboard.

## Model contract

The application loads only `models/best.pt` when that file exists. It uses a confidence threshold of `0.50` and accepts only these class IDs:

| ID | Class |
| --- | --- |
| 0 | `Good_Bolt` |
| 1 | `Thread_Defect` |
| 2 | `Head_Defect` |

Without `models/best.pt`, the dashboard reports `AI MODEL: NOT LOADED` and `BOLT MODEL: NOT FOUND`. A visible object is reported as `PRESENCE_ONLY` and never classified as a bolt or written to the database.

## Run

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open `http://localhost:8501`, then select **START CAMERA**. The database is `inspections.db` beside `app.py`. It starts empty and receives only genuine YOLO inspections. One record is created when a new detected object enters the inspection area; the same tracked object does not create duplicates.

The PLC is a simulation only. `Good_Bolt` continues the line; either defect class rejects the bolt.