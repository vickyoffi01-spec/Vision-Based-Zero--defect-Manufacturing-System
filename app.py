"""Streamlit dashboard for genuine webcam-based bolt inspection."""

import time

import cv2
import pandas as pd
import streamlit as st

from database import InspectionDatabase
from inspection_service import CONFIDENCE_THRESHOLD, MODEL_PATH, InspectionService
from plc_simulator import PLCSimulator


st.set_page_config(page_title="Vision-Based Bolt Inspection", page_icon="B", layout="wide")
st.markdown("""
<style>
.stApp { background: #0b1117; color: #d8e2ea; }
.block-container { max-width: 1500px; padding-top: 2rem; }
.panel { background: #121b24; border: 1px solid #263847; padding: 1rem; border-radius: 6px; margin-bottom: 1rem; }
.label { color: #7fa1b8; font-size: .75rem; text-transform: uppercase; letter-spacing: .08em; }
.value { color: #f4f7f9; font-size: 1.1rem; font-weight: 600; }
.ok { color: #47d18c; } .warn { color: #ffb454; } .bad { color: #ff6b6b; }
</style>
""", unsafe_allow_html=True)


def panel_value(label: str, value: str, css: str = "value") -> str:
    return f'<div><div class="label">{label}</div><div class="{css}">{value}</div></div>'


if "service" not in st.session_state:
    st.session_state.service = InspectionService()
if "database" not in st.session_state:
    st.session_state.database = InspectionDatabase()
if "plc" not in st.session_state:
    st.session_state.plc = PLCSimulator()
if "running" not in st.session_state:
    st.session_state.running = False
if "current" not in st.session_state:
    st.session_state.current = {"product": "", "status": "WAITING FOR OBJECT", "class_name": "",
                                "confidence": None, "decision": "", "action": "",
                                "verification": "", "bbox": None}

service: InspectionService = st.session_state.service
database: InspectionDatabase = st.session_state.database
plc: PLCSimulator = st.session_state.plc

st.title("VISION-BASED BOLT MANUFACTURING INSPECTION")
st.caption("Real webcam frames | Genuine custom YOLO detections only | Virtual PLC simulation")
st.info("Virtual PLC Simulation Only")

camera_col, status_col = st.columns([2.1, 1])
with camera_col:
    st.subheader("CAMERA")
    start_col, stop_col = st.columns(2)
    with start_col:
        if st.button("START CAMERA", use_container_width=True):
            st.session_state.running = service.start_camera(0)
            if not st.session_state.running:
                st.error("Camera could not be opened.")
    with stop_col:
        if st.button("STOP CAMERA", use_container_width=True):
            st.session_state.running = False
            service.stop_camera()
    camera_status = "RUNNING" if st.session_state.running else "STOPPED"
    st.write(f"Camera status: **{camera_status}**")
    frame_placeholder = st.empty()
    st.caption("Bolt inspection area / ROI is outlined on the live frame.")

with status_col:
    st.subheader("AI MODEL STATUS")
    model_state = "LOADED" if service.model_loaded else "NOT LOADED"
    bolt_state = "READY" if service.model_loaded else "NOT FOUND"
    model_css = "ok" if service.model_loaded else "bad"
    st.markdown("<div class='panel'>" +
                panel_value("AI MODEL", model_state, model_css) +
                panel_value("BOLT MODEL", bolt_state, model_css) +
                panel_value("MODEL PATH", str(MODEL_PATH)) +
                panel_value("CONFIDENCE THRESHOLD", f"{CONFIDENCE_THRESHOLD:.2f}") +
                "</div>", unsafe_allow_html=True)
    if not service.model_loaded:
        st.warning("models/best.pt is required for bolt classification. No bolt decision will be made.")

st.subheader("CURRENT INSPECTION")
current = st.session_state.current
confidence = "N/A" if current.get("confidence") is None else f"{current['confidence']:.2%}"
inspection_html = "<div class='panel'><div style='display:grid;grid-template-columns:repeat(3,1fr);gap:1rem'>"
for label, value in [("PRODUCT", current.get("product") or "N/A"),
                     ("STATUS", current.get("status") or "N/A"),
                     ("CLASS", current.get("class_name") or "N/A"),
                     ("CONFIDENCE", confidence),
                     ("DECISION", current.get("decision") or "N/A"),
                     ("ACTION", current.get("action") or "N/A"),
                     ("VERIFICATION", current.get("verification") or "N/A")]:
    inspection_html += panel_value(label, str(value))
inspection_html += "</div></div>"
st.markdown(inspection_html, unsafe_allow_html=True)

st.subheader("KPI")
kpis = database.kpis()
kpi_cols = st.columns(4)
for column, label, value in zip(kpi_cols, ["TOTAL INSPECTED", "PASSED", "DEFECTIVE", "DEFECT RATE"],
                                [kpis["total_inspected"], kpis["passed"], kpis["defective"], f'{kpis["defect_rate"]:.1f}%']):
    with column:
        st.metric(label, value)

history_col, plc_col = st.columns([2, 1])
with history_col:
    st.subheader("INSPECTION HISTORY")
    history = database.history()
    if history:
        st.dataframe(pd.DataFrame(history), use_container_width=True, hide_index=True)
    else:
        st.caption("No genuine inspections recorded.")

with plc_col:
    st.subheader("VIRTUAL PLC")
    st.markdown("<div class='panel'>" +
                panel_value("PLC STATUS", plc.status, "ok" if plc.status == "READY" else "bad") +
                panel_value("LAST ACTION", plc.last_action) +
                panel_value("VERIFICATION", "VIRTUAL PLC ONLY") +
                "</div>", unsafe_allow_html=True)

if st.session_state.running:
    frame = service.read_frame()
    if frame is None:
        st.session_state.running = False
        service.stop_camera()
        st.error("The webcam stopped returning frames.")
    else:
        annotated, result, is_new = service.inspect(frame)
        st.session_state.current = result
        if is_new and result["status"] == "INSPECTED":
            plc.process_inspection(result)
            database.save(result)
        frame_placeholder.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), channels="RGB", use_container_width=True)
        time.sleep(0.05)
        st.rerun()
elif service.camera is None:
    frame_placeholder.info("Start the camera to view genuine webcam frames.")