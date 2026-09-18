"""
AUTONOMOUS CLOSED-LOOP ZERO-DEFECT MANUFACTURING COMMAND CENTER
================================================================
Principal Computer Vision & Industry 4.0 Systems Architecture
Single-File Production-Grade Streamlit & OpenCV Application

Author: Principal Computer Vision Architect
Stack: Streamlit, OpenCV, NumPy
Styling: Tesla/SpaceX Gigafactory Dark Cyberpunk Theme
"""

import time
import json
import math
import random
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional

import streamlit as st
import cv2
import numpy as np

# ==============================================================================
# 1. STREAMLIT CONFIGURATION & INDUSTRIAL CYBERPUNK CSS
# ==============================================================================
st.set_page_config(
    page_title="APEX-IV | Zero-Defect Command Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

CYBERPUNK_CSS = """
<style>
/* Root industrial dark cyberpunk variables */
:root {
    --bg-primary: #07090e;
    --bg-card: #0d121c;
    --bg-card-hover: #131b2a;
    --border-cyber: #1e293b;
    --neon-green: #00FF66;
    --neon-red: #FF0033;
    --neon-cyan: #00E5FF;
    --neon-amber: #FFB800;
    --text-primary: #f1f5f9;
    --text-muted: #64748b;
}

/* Base Body and Streamlit Container Overrides */
html, body, [class*="css"] {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace !important;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: #090d15 !important;
    border-right: 1px solid #1e293b !important;
}

/* Industrial Header Banner */
.cyber-header {
    background: linear-gradient(90deg, #09101d 0%, #0d1627 50%, #09101d 100%);
    border: 1px solid #1e2d44;
    border-left: 4px solid var(--neon-cyan);
    border-radius: 6px;
    padding: 12px 20px;
    margin-bottom: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 20px rgba(0, 229, 255, 0.08);
}
.cyber-title {
    font-size: 1.35rem;
    font-weight: 800;
    letter-spacing: 2px;
    color: #ffffff;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 12px;
}
.cyber-badge-live {
    background: rgba(0, 255, 102, 0.12);
    border: 1px solid var(--neon-green);
    color: var(--neon-green);
    font-size: 0.72rem;
    padding: 3px 10px;
    border-radius: 4px;
    font-weight: 700;
    letter-spacing: 1.5px;
    animation: pulse-green 2s infinite ease-in-out;
}

/* KPI Card Grid */
.kpi-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 12px;
}
.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border-cyber);
    border-radius: 6px;
    padding: 12px 14px;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 3px;
    height: 100%;
}
.kpi-card.total::before { background: var(--neon-cyan); }
.kpi-card.pass::before { background: var(--neon-green); }
.kpi-card.reject::before { background: var(--neon-red); }
.kpi-card.yield::before { background: var(--neon-amber); }

.kpi-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--text-muted);
    margin-bottom: 2px;
}
.kpi-value {
    font-size: 1.65rem;
    font-weight: 900;
    letter-spacing: 1px;
    font-family: 'JetBrains Mono', monospace;
}
.val-cyan { color: var(--neon-cyan); text-shadow: 0 0 10px rgba(0, 229, 255, 0.3); }
.val-green { color: var(--neon-green); text-shadow: 0 0 10px rgba(0, 255, 102, 0.3); }
.val-red { color: var(--neon-red); text-shadow: 0 0 10px rgba(255, 0, 51, 0.3); }
.val-amber { color: var(--neon-amber); text-shadow: 0 0 10px rgba(255, 184, 0, 0.3); }

/* Flashing Ejector Actuator Badges */
@keyframes flash-red {
    0%, 100% { background: rgba(255, 0, 51, 0.95); box-shadow: 0 0 25px #FF0033; }
    50% { background: rgba(139, 0, 0, 0.4); box-shadow: 0 0 5px #8B0000; }
}
@keyframes pulse-green {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.55; }
}
.ejector-badge-active {
    animation: flash-red 0.65s infinite ease-in-out;
    color: #ffffff;
    padding: 12px 14px;
    border-radius: 6px;
    font-weight: 900;
    font-size: 0.88rem;
    letter-spacing: 1.8px;
    text-align: center;
    border: 1px solid #ff4d6d;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    text-transform: uppercase;
}
.ejector-badge-idle {
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid #1e293b;
    color: #475569;
    padding: 10px 14px;
    border-radius: 6px;
    font-weight: 700;
    font-size: 0.78rem;
    letter-spacing: 1.5px;
    text-align: center;
    margin-bottom: 12px;
    text-transform: uppercase;
}

/* Terminal Console for PLC Telemetry */
.plc-terminal {
    background-color: #05070a;
    border: 1px solid #1e293b;
    border-left: 3px solid var(--neon-cyan);
    border-radius: 6px;
    padding: 10px 12px;
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    font-size: 0.72rem;
    color: #38bdf8;
    max-height: 280px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-all;
    line-height: 1.35;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.8);
}

/* Telemetry Parameter Meters */
.param-pill {
    display: flex;
    justify-content: space-between;
    background: #090e17;
    border: 1px solid #1a2536;
    border-radius: 4px;
    padding: 6px 10px;
    margin-bottom: 6px;
    font-size: 0.75rem;
}
.param-label { color: #94a3b8; }
.param-val-shift { color: var(--neon-amber); font-weight: 700; }
.param-val-norm { color: var(--neon-green); font-weight: 700; }

/* Edge Telemetry HUD Box */
.hud-telemetry {
    background: rgba(13, 18, 28, 0.85);
    border: 1px solid #1e293b;
    border-radius: 4px;
    padding: 8px 12px;
    margin-top: 8px;
    display: flex;
    justify-content: space-between;
    font-size: 0.75rem;
    color: #94a3b8;
}
</style>
"""
st.markdown(CYBERPUNK_CSS, unsafe_allow_html=True)


# ==============================================================================
# 2. AUDIO SYNTHESIS MODULE (HTML5 Web Audio API Alert Tone)
# ==============================================================================
def trigger_html5_audio_alert():
    """
    Renders an inline HTML5 Web Audio API synthesizer that produces a crisp,
    two-tone industrial reject siren/beep without requiring external sound files.
    """
    audio_js = """
    <script>
    (function() {
        try {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (!AudioContext) return;
            const ctx = new AudioContext();
            
            // Tone 1: High frequency burst
            const osc1 = ctx.createOscillator();
            const gain1 = ctx.createGain();
            osc1.type = 'sawtooth';
            osc1.frequency.setValueAtTime(880, ctx.currentTime);
            osc1.frequency.exponentialRampToValueAtTime(440, ctx.currentTime + 0.12);
            gain1.gain.setValueAtTime(0.25, ctx.currentTime);
            gain1.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.12);
            osc1.connect(gain1);
            gain1.connect(ctx.destination);
            osc1.start(ctx.currentTime);
            osc1.stop(ctx.currentTime + 0.12);

            // Tone 2: Low warning harmonic
            const osc2 = ctx.createOscillator();
            const gain2 = ctx.createGain();
            osc2.type = 'square';
            osc2.frequency.setValueAtTime(330, ctx.currentTime + 0.13);
            osc2.frequency.exponentialRampToValueAtTime(220, ctx.currentTime + 0.28);
            gain2.gain.setValueAtTime(0.3, ctx.currentTime + 0.13);
            gain2.gain.exponentialRampToValueAtTime(0.005, ctx.currentTime + 0.28);
            osc2.connect(gain2);
            gain2.connect(ctx.destination);
            osc2.start(ctx.currentTime + 0.13);
            osc2.stop(ctx.currentTime + 0.28);
        } catch(e) {
            console.error("Audio trigger inhibited:", e);
        }
    })();
    </script>
    """
    if hasattr(st, "html"):
        st.html(audio_js)
    else:
        st.components.v1.html(audio_js, height=0, width=0)


# ==============================================================================
# 3. PROCEDURAL SYNTHETIC IMAGE GENERATORS (ZERO EXTERNAL HARDWARE REQUIRED)
# ==============================================================================
class SyntheticDefectGenerator:
    """
    Industry-grade procedural synthesis of industrial manufactured goods.
    Generates dynamic conveyor belt video frames for both Smartphone OLED modules
    and Water Bottle Blow-Molding bottles, seamlessly simulating real defects.
    """

    @staticmethod
    def create_smartphone_frame(defect_type: Optional[str] = None, angle_shift: float = 0.0) -> np.ndarray:
        """
        Synthesizes a realistic 640x480 frame containing a smartphone on an industrial
        conveyor track with metallic anodized chassis, display glass, glare gradient,
        and procedurally rendered defects.
        """
        # Conveyor background texture
        frame = np.full((480, 640, 3), 18, dtype=np.uint8)
        # Add conveyor guide rails and metallic texture
        cv2.rectangle(frame, (0, 40), (640, 60), (32, 38, 48), -1)
        cv2.rectangle(frame, (0, 420), (640, 440), (32, 38, 48), -1)
        for x in range(0, 640, 40):
            cv2.line(frame, (x, 60), (x, 420), (22, 28, 36), 1)

        # Phone Geometry
        center_x, center_y = 320, 240
        phone_w, phone_h = 220, 340
        x1, y1 = center_x - phone_w // 2, center_y - phone_h // 2
        x2, y2 = center_x + phone_w // 2, center_y + phone_h // 2

        # Draw chassis (Matte titanium bezel)
        cv2.rectangle(frame, (x1 - 6, y1 - 6), (x2 + 6, y2 + 6), (65, 75, 88), -1)
        cv2.rectangle(frame, (x1 - 6, y1 - 6), (x2 + 6, y2 + 6), (110, 120, 135), 2)

        # OLED Display surface (Deep Obsidian Glass)
        disp_roi = np.full((phone_h, phone_w, 3), 26, dtype=np.uint8)

        # Ambient screen glare / light reflection gradient (suppressed by CLAHE in inspection)
        disp_roi_int = disp_roi.astype(np.int16)
        for gy in range(phone_h):
            intensity = int(18 * math.sin((gy / phone_h) * math.pi + 0.3))
            disp_roi_int[gy, :, :] = np.clip(disp_roi_int[gy, :, :] + intensity, 0, 255)
        disp_roi = disp_roi_int.astype(np.uint8)

        # Pristine OLED glass substrate (uniform specular surface)
        # Smooth reflection gradient is processed by CLAHE during QA inspection

        # Synthesize defects if requested
        if defect_type == "SPIDER_CRACK":
            # Procedural recursive branching spider crack
            start_x = random.randint(phone_w // 4, 3 * phone_w // 4)
            start_y = random.randint(phone_h // 4, 3 * phone_h // 4)
            cv2.circle(disp_roi, (start_x, start_y), 4, (240, 245, 255), -1)

            # Radiating crack fractures
            for _ in range(6):
                curr_x, curr_y = start_x, start_y
                angle = random.uniform(0, 2 * math.pi)
                length = random.randint(30, 85)
                for step in range(length):
                    angle += random.uniform(-0.35, 0.35)
                    curr_x = int(curr_x + math.cos(angle) * 1.5)
                    curr_y = int(curr_y + math.sin(angle) * 1.5)
                    if 0 <= curr_x < phone_w and 0 <= curr_y < phone_h:
                        disp_roi[curr_y, curr_x] = (235, 240, 255)
                        if step % 8 == 0 and random.random() > 0.4:
                            # Secondary hairline fracture branch
                            sub_x, sub_y = curr_x, curr_y
                            sub_ang = angle + random.choice([-0.8, 0.8])
                            for _ in range(random.randint(10, 25)):
                                sub_x += int(math.cos(sub_ang) * 1.5)
                                sub_y += int(math.sin(sub_ang) * 1.5)
                                if 0 <= sub_x < phone_w and 0 <= sub_y < phone_h:
                                    disp_roi[sub_y, sub_x] = (210, 220, 245)

        elif defect_type == "HAIRLINE_SCRATCH":
            # Fine micro-scratches
            for _ in range(random.randint(2, 4)):
                sx = random.randint(20, phone_w - 40)
                sy = random.randint(30, phone_h - 60)
                ex = sx + random.randint(25, 70)
                ey = sy + random.randint(10, 45)
                # Curve stroke
                pts = np.array([
                    [sx, sy],
                    [sx + (ex - sx) // 2 + random.randint(-8, 8), sy + (ey - sy) // 2 + random.randint(-6, 6)],
                    [ex, ey]
                ], np.int32)
                cv2.polylines(disp_roi, [pts], False, (215, 225, 235), 1, cv2.LINE_AA)

        elif defect_type == "FOREIGN_SMUDGE":
            # Low-contrast foreign particulate smudge / cluster
            cx = random.randint(phone_w // 3, 2 * phone_w // 3)
            cy = random.randint(phone_h // 3, 2 * phone_h // 3)
            for _ in range(40):
                rx = int(np.random.normal(cx, 12))
                ry = int(np.random.normal(cy, 12))
                if 0 <= rx < phone_w and 0 <= ry < phone_h:
                    smudge_val = np.clip(disp_roi[ry, rx].astype(np.int16) + random.randint(55, 110), 0, 255).astype(np.uint8)
                    disp_roi[ry, rx] = smudge_val

        elif defect_type == "BEZEL_DENT":
            # Deformed dent on chassis edge
            dent_y = center_y + random.randint(-60, 60)
            cv2.ellipse(frame, (x1 - 6, dent_y), (8, 14), 0, 0, 360, (25, 30, 38), -1)
            cv2.ellipse(frame, (x1 - 6, dent_y), (9, 15), 0, 0, 360, (180, 195, 210), 1)

        # Place display ROI onto frame
        frame[y1:y2, x1:x2] = disp_roi

        # Industrial alignment fiducial marks on conveyor
        cv2.drawMarker(frame, (center_x, y1 - 25), (0, 229, 255), cv2.MARKER_CROSS, 14, 1)
        cv2.drawMarker(frame, (center_x, y2 + 25), (0, 229, 255), cv2.MARKER_CROSS, 14, 1)

        return frame

    @staticmethod
    def create_water_bottle_frame(defect_type: Optional[str] = None) -> np.ndarray:
        """
        Synthesizes a realistic 640x480 frame containing a 1L water bottle on a
        high-speed blow-molding bottling conveyor line.
        """
        # Conveyor backdrop
        frame = np.full((480, 640, 3), 16, dtype=np.uint8)
        # Stainless steel conveyor guides
        cv2.rectangle(frame, (80, 0), (100, 480), (35, 45, 58), -1)
        cv2.rectangle(frame, (540, 0), (560, 480), (35, 45, 58), -1)
        for y in range(0, 480, 30):
            cv2.line(frame, (100, y), (540, y), (24, 30, 40), 1)

        center_x, center_y = 320, 240
        b_width = 130
        b_height = 340
        x1 = center_x - b_width // 2
        y1 = center_y - b_height // 2
        x2 = center_x + b_width // 2
        y2 = center_y + b_height // 2

        # 1. Bottle Body (Translucent PET plastic with lighting highlights)
        # Bottle shoulder curve
        shoulder_y = y1 + 75
        body_poly = np.array([
            [center_x - 30, y1 + 35],   # neck left
            [center_x - 30, shoulder_y - 20],
            [x1, shoulder_y],           # shoulder left
            [x1, y2 - 15],              # base left
            [x1 + 20, y2],              # base curve
            [x2 - 20, y2],              # base curve
            [x2, y2 - 15],              # base right
            [x2, shoulder_y],           # shoulder right
            [center_x + 30, shoulder_y - 20],
            [center_x + 30, y1 + 35],   # neck right
        ], np.int32)

        cv2.fillPoly(frame, [body_poly], (52, 70, 85))
        cv2.polylines(frame, [body_poly], True, (85, 110, 130), 2)

        # Water fill volume inside PET container
        water_poly = np.array([
            [x1 + 4, shoulder_y + 10],
            [x1 + 4, y2 - 12],
            [x2 - 4, y2 - 12],
            [x2 - 4, shoulder_y + 10]
        ], np.int32)
        cv2.fillPoly(frame, [water_poly], (68, 95, 120))

        # Structural ribbing rings on body (translucent PET reflections)
        for ry in range(shoulder_y + 40, y2 - 30, 35):
            cv2.line(frame, (x1 + 12, ry), (x2 - 12, ry), (75, 105, 130), 1)

        # 2. Cap Zone (Upper 1/3)
        cap_w = 44
        cap_h = 26
        cap_center_x = center_x
        cap_center_y = y1 + 20

        # Check for cap tilt defect
        tilt_angle = 0.0
        if defect_type == "CAP_TILT":
            tilt_angle = random.choice([-16.0, -22.0, 18.0, 24.0])
            cap_center_y += random.randint(2, 6)
            cap_center_x += random.randint(-4, 4)

        # Render cap with rotation
        rect = ((float(cap_center_x), float(cap_center_y)), (float(cap_w), float(cap_h)), tilt_angle)
        box = cv2.boxPoints(rect)
        box = np.int32(box)
        # Cap color: Industrial High-Vis Blue with knurling lines
        cv2.fillPoly(frame, [box], (220, 110, 20))  # BGR Deep Cyan/Blue
        cv2.polylines(frame, [box], True, (255, 160, 50), 2)

        # Safety Tamper Band below cap
        band_y = y1 + 33
        if defect_type != "CAP_TILT":
            cv2.rectangle(frame, (center_x - 24, band_y), (center_x + 24, band_y + 5), (45, 65, 110), -1)
        else:
            # Broken / ruptured seal band
            cv2.rectangle(frame, (center_x - 20, band_y + 3), (center_x - 5, band_y + 7), (45, 65, 110), -1)
            cv2.rectangle(frame, (center_x + 8, band_y + 5), (center_x + 22, band_y + 9), (45, 65, 110), -1)

        # 3. Sidewall Defect or Marker Contamination
        if defect_type == "SIDEWALL_DENT":
            dent_center_y = center_y + random.randint(10, 60)
            dent_x = center_x - 36 if random.random() > 0.5 else center_x + 36
            # Punch an asymmetric dent / buckling into the bottle wall
            cv2.ellipse(frame, (dent_x, dent_center_y), (18, 14), 0, 0, 360, (25, 32, 40), -1)
            cv2.ellipse(frame, (dent_x, dent_center_y), (20, 16), 0, 0, 360, (140, 175, 210), 2)
            cv2.ellipse(frame, (dent_x, dent_center_y), (10, 8), 0, 0, 360, (18, 24, 30), -1)

        elif defect_type == "BODY_CONTAMINATION":
            # Chemical marker spot / foreign particulate smudge
            spot_x = center_x + random.randint(-28, 28)
            spot_y = center_y + random.randint(0, 80)
            cv2.circle(frame, (spot_x, spot_y), random.randint(7, 12), (15, 20, 25), -1)
            cv2.circle(frame, (spot_x + 4, spot_y + 3), random.randint(4, 7), (25, 30, 35), -1)
            cv2.line(frame, (spot_x - 10, spot_y - 8), (spot_x + 8, spot_y + 10), (10, 15, 20), 3)

        return frame


# ==============================================================================
# 4. COMPUTER VISION INSPECTION PIPELINES (PROFILES A & B)
# ==============================================================================
class EdgeInspectionCore:
    """
    Core CV Edge Telemetry Engine implementing advanced frequency-domain,
    morphological, and orientation analysis on production units.
    """

    @staticmethod
    def inspect_smartphone_display(
        frame: np.ndarray, sensitivity_pct: int
    ) -> Tuple[str, str, int, np.ndarray, List[Dict[str, Any]], Dict[str, np.ndarray]]:
        """
        Profile A Pipeline:
        1. Extract Display Region of Interest (ROI).
        2. Convert to Grayscale + CLAHE for glare & specular suppression.
        3. High-frequency directional Canny edge detection + Laplacian variance.
        4. Morphological dilation to bridge hairline cracks.
        5. Area & contour severity estimation against dynamic sensitivity threshold.
        """
        h, w, _ = frame.shape
        # Dynamic or centered ROI: Phone display screen core (inside titanium bezel)
        rx1, ry1 = int(w * 0.35), int(h * 0.18)
        rx2, ry2 = int(w * 0.65), int(h * 0.82)
        roi = frame[ry1:ry2, rx1:rx2].copy()

        # Step 1: Grayscale conversion
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # Step 2: CLAHE (Contrast Limited Adaptive Histogram Equalization)
        # Suppresses glare and enhances local micro-contrast
        clahe = cv2.createCLAHE(clipLimit=3.5, tileGridSize=(8, 8))
        clahe_img = clahe.apply(gray)

        # Step 3: Directional Canny Edge Detection
        # Sensitivity scales thresholds inversely
        lower_canny = max(20, int(50 * (1.0 - sensitivity_pct / 130.0)))
        upper_canny = max(50, int(130 * (1.0 - sensitivity_pct / 130.0)))
        canny_edges = cv2.Canny(clahe_img, lower_canny, upper_canny)

        # Step 4: Laplacian Variance for high-frequency hairline spikes
        lap = cv2.Laplacian(clahe_img, cv2.CV_64F, ksize=3)
        lap_abs = cv2.convertScaleAbs(lap)
        _, lap_thresh = cv2.threshold(lap_abs, max(25, int(45 * (1.0 - sensitivity_pct / 150.0))), 255, cv2.THRESH_BINARY)

        # Fuse edge detectors
        fused = cv2.bitwise_or(canny_edges, lap_thresh)

        # Step 5: Morphological Dilation
        morph_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        dilated = cv2.dilate(fused, morph_kernel, iterations=1)

        # Step 6: Contour Analysis
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        defect_detections = []
        total_defect_metric = 0

        for cnt in contours:
            area = cv2.contourArea(cnt)
            perimeter = cv2.arcLength(cnt, True)
            if perimeter > 18 or area > 12:
                bx, by, bw, bh = cv2.boundingRect(cnt)
                # Map back to global frame coordinates
                global_bx = rx1 + bx
                global_by = ry1 + by
                total_defect_metric += area + perimeter * 2.5
                defect_detections.append({
                    "box": (global_bx, global_by, bw, bh),
                    "area": area,
                    "perimeter": perimeter
                })

        # Dynamic sensitivity threshold check
        # Sensitivity 100% => triggers on threshold 15; 1% => triggers on threshold 250
        trigger_limit = (100 - sensitivity_pct) * 2.3 + 20
        severity = min(99, int((total_defect_metric / 180.0) * 100))

        stages = {
            "CLAHE Equalized": cv2.cvtColor(clahe_img, cv2.COLOR_GRAY2BGR),
            "Canny Edges": cv2.cvtColor(canny_edges, cv2.COLOR_GRAY2BGR),
            "Fused Morph Dilated": cv2.cvtColor(dilated, cv2.COLOR_GRAY2BGR)
        }

        if total_defect_metric > trigger_limit and len(defect_detections) > 0:
            verdict = "REJECT"
            # Discriminate failure mode
            if severity > 55 or len(defect_detections) > 5:
                failure_mode = "Spider_Glass_Crack"
            elif any(d["perimeter"] > 50 for d in defect_detections):
                failure_mode = "Display_Micro_Scratch"
            else:
                failure_mode = "Foreign_Particulates_Smudge"
        else:
            verdict = "PASS"
            failure_mode = "Display_Integrity_Nominal"
            severity = 0

        return verdict, failure_mode, severity, roi, defect_detections, stages

    @staticmethod
    def inspect_water_bottle(
        frame: np.ndarray, sensitivity_pct: int
    ) -> Tuple[str, str, int, np.ndarray, List[Dict[str, Any]], Dict[str, np.ndarray]]:
        """
        Profile B Pipeline:
        1. Aspect ratio & orientation analysis of Cap ROI (upper third).
        2. High-contrast thresholding across bottle cylinder body.
        3. Identifies Cap Tilt / Seal Misalignment, Sidewall Dent, and Marker Contamination.
        """
        h, w, _ = frame.shape
        bx1, by1 = int(w * 0.30), int(h * 0.12)
        bx2, by2 = int(w * 0.70), int(h * 0.88)
        roi = frame[by1:by2, bx1:bx2].copy()
        roi_h, roi_w, _ = roi.shape

        defect_detections = []
        verdict = "PASS"
        failure_mode = "Cap_And_Body_Nominal"
        severity = 0

        # --- A. UPPER THIRD CAP INSPECTION ---
        cap_cutoff_y = int(roi_h * 0.22)
        cap_zone = roi[0:cap_cutoff_y, :]
        
        # High-contrast thresholding on cap zone (isolate industrial blue polymer)
        _, cap_thresh = cv2.threshold(cap_zone[:, :, 0], 160, 255, cv2.THRESH_BINARY)
        cap_contours, _ = cv2.findContours(cap_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cap_tilt_detected = False
        cap_angle = 0.0

        for c in cap_contours:
            if cv2.contourArea(c) > 200:
                rect = cv2.minAreaRect(c)
                (rcx, rcy), (rw, rh), angle = rect
                # Normalize orientation
                if rw < rh:
                    rw, rh = rh, rw
                    angle += 90.0
                while angle > 45.0:
                    angle -= 90.0
                while angle < -45.0:
                    angle += 90.0

                # Sensitivity threshold for cap tilt: 1% => 22 deg, 100% => 3.5 deg
                allowed_tilt = max(3.5, 20.0 * (1.0 - sensitivity_pct / 100.0))
                if abs(angle) > allowed_tilt:
                    cap_tilt_detected = True
                    cap_angle = angle
                    cbx, cby, cbw, cbh = cv2.boundingRect(c)
                    defect_detections.append({
                        "box": (bx1 + cbx, by1 + cby, cbw, cbh),
                        "defect_type": "CAP_SEAL_BREACH",
                        "desc": f"Cap Tilt: {abs(angle):.1f}°"
                    })

        # --- B. LOWER TWO-THIRDS CYLINDER BODY INSPECTION ---
        body_zone = roi[cap_cutoff_y:, :]
        body_gray = cv2.cvtColor(body_zone, cv2.COLOR_BGR2GRAY)
        
        # Adaptive thresholding to detect sharp dark marker spots or indentation shadows
        adaptive = cv2.adaptiveThreshold(
            body_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 15, max(2, int(6 * (1.0 - sensitivity_pct / 120.0)))
        )

        # Ignore outer boundary margins
        adaptive[:, :15] = 0
        adaptive[:, -15:] = 0
        adaptive[-25:, :] = 0

        body_contours, _ = cv2.findContours(adaptive, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        body_defects_found = []

        for bc in body_contours:
            b_area = cv2.contourArea(bc)
            bx, by, bw, bh = cv2.boundingRect(bc)
            # Filter out cosmetic horizontal ribs (very thin) and vertical border edges
            if bh <= 5 and bw > 25:
                continue
            if bw <= 12 and bh > 25:
                continue
            if bh > 110:
                continue
            if b_area > max(20, int(60 * (1.0 - sensitivity_pct / 100.0))):
                body_defects_found.append((bx, by, bw, bh, b_area))
                defect_detections.append({
                    "box": (bx1 + bx, by1 + cap_cutoff_y + by, bw, bh),
                    "defect_type": "BODY_DENT_OR_MARK",
                    "desc": f"Anomaly Area: {int(b_area)}px"
                })

        stages = {
            "Cap Thresholding": cv2.cvtColor(cap_thresh, cv2.COLOR_GRAY2BGR),
            "Body Adaptive Scan": cv2.cvtColor(adaptive, cv2.COLOR_GRAY2BGR)
        }

        if cap_tilt_detected:
            verdict = "REJECT"
            failure_mode = "Cap_Torque_Displacement"
            severity = min(98, int(abs(cap_angle) * 4.2))
        elif len(body_defects_found) > 0:
            verdict = "REJECT"
            total_body_area = sum(d[4] for d in body_defects_found)
            severity = min(95, int(total_body_area * 0.8))
            if any(d[2] > 25 or d[3] > 25 for d in body_defects_found):
                failure_mode = "Sidewall_Dent_Buckling"
            else:
                failure_mode = "Body_Contamination_Marker"
        else:
            verdict = "PASS"
            failure_mode = "Bottle_Geometry_Compliant"
            severity = 0

        return verdict, failure_mode, severity, roi, defect_detections, stages


# ==============================================================================
# 5. CYBERPUNK HUD OVERLAY & RETICLE RENDERER
# ==============================================================================
class CyberHudRenderer:
    """
    Renders high-tech aerospace/industrial reticles, targeting brackets,
    and telemetry tags onto OpenCV frames.
    """

    @staticmethod
    def draw_hud(
        frame: np.ndarray,
        verdict: str,
        failure_mode: str,
        severity: int,
        fps: float,
        latency_ms: float,
        profile_name: str,
        defect_boxes: List[Dict[str, Any]]
    ) -> np.ndarray:
        hud = frame.copy()
        h, w, _ = hud.shape

        # Colors in BGR
        NEON_GREEN = (102, 255, 0)
        NEON_RED = (51, 0, 255)
        NEON_CYAN = (255, 229, 0)
        DARK_BG = (14, 18, 24)

        theme_color = NEON_RED if verdict == "REJECT" else NEON_GREEN

        # 1. Corner Cyber HUD Brackets
        bracket_len = 28
        thickness = 2
        # Top-Left
        cv2.line(hud, (15, 15), (15 + bracket_len, 15), NEON_CYAN, thickness)
        cv2.line(hud, (15, 15), (15, 15 + bracket_len), NEON_CYAN, thickness)
        # Top-Right
        cv2.line(hud, (w - 15, 15), (w - 15 - bracket_len, 15), NEON_CYAN, thickness)
        cv2.line(hud, (w - 15, 15), (w - 15, 15 + bracket_len), NEON_CYAN, thickness)
        # Bottom-Left
        cv2.line(hud, (15, h - 15), (15 + bracket_len, h - 15), NEON_CYAN, thickness)
        cv2.line(hud, (15, h - 15), (15, h - 15 - bracket_len), NEON_CYAN, thickness)
        # Bottom-Right
        cv2.line(hud, (w - 15, h - 15), (w - 15 - bracket_len, h - 15), NEON_CYAN, thickness)
        cv2.line(hud, (w - 15, h - 15), (w - 15, h - 15 - bracket_len), NEON_CYAN, thickness)

        # 2. Top Telemetry Banner
        cv2.rectangle(hud, (20, 20), (320, 48), DARK_BG, -1)
        cv2.rectangle(hud, (20, 20), (320, 48), (40, 55, 75), 1)
        fps_text = f"FPS: {fps:4.1f} | EDGE LATENCY: {latency_ms:4.1f}ms"
        cv2.putText(hud, fps_text, (28, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.42, NEON_CYAN, 1, cv2.LINE_AA)

        # 3. Target Reticle Crosshairs in Center
        cx, cy = w // 2, h // 2
        cv2.line(hud, (cx - 16, cy), (cx + 16, cy), (60, 80, 100), 1)
        cv2.line(hud, (cx, cy - 16), (cx, cy + 16), (60, 80, 100), 1)
        cv2.circle(hud, (cx, cy), 28, (45, 60, 80), 1)

        # 4. Draw Defect Bounding Boxes & Telemetry Labels
        if verdict == "REJECT":
            for d in defect_boxes:
                bx, by, bw, bh = d["box"]
                # Neon-red bounding reticle with corner accents
                cv2.rectangle(hud, (bx, by), (bx + bw, by + bh), NEON_RED, 2)
                corner_size = min(10, min(bw, bh) // 2)
                # Outer reticle corners
                cv2.line(hud, (bx - 3, by - 3), (bx - 3 + corner_size, by - 3), (255, 255, 255), 2)
                cv2.line(hud, (bx - 3, by - 3), (bx - 3, by - 3 + corner_size), (255, 255, 255), 2)
                cv2.line(hud, (bx + bw + 3, by + bh + 3), (bx + bw + 3 - corner_size, by + bh + 3), (255, 255, 255), 2)
                cv2.line(hud, (bx + bw + 3, by + bh + 3), (bx + bw + 3, by + bh + 3 - corner_size), (255, 255, 255), 2)

                # Defect Label Callout Tag
                tag_text = f"DEFECT: {failure_mode.upper()} | SEV: {severity}%"
                cv2.rectangle(hud, (bx, max(0, by - 22)), (bx + len(tag_text) * 7 + 8, max(22, by)), DARK_BG, -1)
                cv2.rectangle(hud, (bx, max(0, by - 22)), (bx + len(tag_text) * 7 + 8, max(22, by)), NEON_RED, 1)
                cv2.putText(hud, tag_text, (bx + 4, max(14, by - 6)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, NEON_RED, 1, cv2.LINE_AA)
        else:
            # PASS Reticle: Centered clean green frame
            cv2.rectangle(hud, (int(w * 0.28), int(h * 0.14)), (int(w * 0.72), int(h * 0.86)), NEON_GREEN, 1)

        # 5. Bottom Main Status Reticle Bar
        status_bar_y = h - 45
        cv2.rectangle(hud, (20, status_bar_y), (w - 20, status_bar_y + 30), DARK_BG, -1)
        cv2.rectangle(hud, (20, status_bar_y), (w - 20, status_bar_y + 30), theme_color, 1)

        status_str = f"VERDICT: {verdict} | PROFILE: {profile_name} | FAULT: {failure_mode.upper()}"
        cv2.putText(hud, status_str, (32, status_bar_y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.44, theme_color, 1, cv2.LINE_AA)

        return hud


# ==============================================================================
# 6. SIMULATED PLC TELEMETRY PAYLOAD GENERATOR
# ==============================================================================
class VirtualPlcEngine:
    """
    Industry 4.0 Closed-Loop Actuator & Telemetry Dispatcher.
    Generates exact JSON payloads dispatched to edge PLCs and pneumatic ejectors.
    """

    @staticmethod
    def dispatch_payload(profile_key: str, verdict: str, failure_mode: str, severity: int) -> Dict[str, Any]:
        """
        Builds the closed-loop telemetry payload matching exact industrial specifications.
        """
        timestamp_iso = datetime.utcnow().isoformat() + "Z"

        if profile_key == "smartphone":
            if verdict == "REJECT":
                payload = {
                    "timestamp": timestamp_iso,
                    "station_id": "LINE_01_OLED_BONDING",
                    "sku": "Smartphone_Display_Unit",
                    "verdict": "REJECT",
                    "failure_mode": failure_mode if failure_mode != "Display_Integrity_Nominal" else "Glass_Substrate_Fracture",
                    "severity_index": f"{severity}%",
                    "actuator": "Pneumatic_Reject_Piston_FIRED",
                    "closed_loop_feedback": {
                        "lamination_pressure_offset": f"-{round(7.0 + severity * 0.03, 1)}%",
                        "thermal_platen_temp": f"+{round(2.5 + severity * 0.015, 1)}C",
                        "conveyor_speed_limit": f"{max(60, 95 - int(severity * 0.3))}%"
                    }
                }
            else:
                payload = {
                    "timestamp": timestamp_iso,
                    "station_id": "LINE_01_OLED_BONDING",
                    "sku": "Smartphone_Display_Unit",
                    "verdict": "PASS",
                    "failure_mode": "NONE",
                    "severity_index": "0%",
                    "actuator": "CONVEYOR_ADVANCE_NOMINAL",
                    "closed_loop_feedback": {
                        "lamination_pressure_offset": "0.0%",
                        "thermal_platen_temp": "NOMINAL (145.0C)",
                        "conveyor_speed_limit": "100%"
                    }
                }
        else:
            # Water Bottle Profile
            if verdict == "REJECT":
                payload = {
                    "timestamp": timestamp_iso,
                    "station_id": "LINE_04_BLOW_MOLD_CAPPING",
                    "sku": "FMCG_Water_Bottle_1L",
                    "verdict": "REJECT",
                    "failure_mode": failure_mode if failure_mode != "Cap_And_Body_Nominal" else "Cap_Torque_Displacement",
                    "severity_index": f"{severity}%",
                    "actuator": "Rotary_Sorter_Eject_FIRED",
                    "closed_loop_feedback": {
                        "capper_spindle_torque": f"+{round(0.35 + severity * 0.002, 2)}Nm",
                        "blow_pressure": f"+{round(0.20 + severity * 0.001, 2)}bar",
                        "mold_chiller_temp": f"-{round(1.0 + severity * 0.01, 1)}C"
                    }
                }
            else:
                payload = {
                    "timestamp": timestamp_iso,
                    "station_id": "LINE_04_BLOW_MOLD_CAPPING",
                    "sku": "FMCG_Water_Bottle_1L",
                    "verdict": "PASS",
                    "failure_mode": "NONE",
                    "severity_index": "0%",
                    "actuator": "PACKAGING_TRANSFER_STANDBY",
                    "closed_loop_feedback": {
                        "capper_spindle_torque": "NOMINAL (2.40Nm)",
                        "blow_pressure": "NOMINAL (38.5bar)",
                        "mold_chiller_temp": "NOMINAL (12.0C)"
                    }
                }

        return payload


# ==============================================================================
# 7. STREAMLIT APPLICATION STATE INITIALIZATION
# ==============================================================================
def init_session_state():
    if "total_inspected" not in st.session_state:
        st.session_state.total_inspected = 0
    if "passed_count" not in st.session_state:
        st.session_state.passed_count = 0
    if "rejected_count" not in st.session_state:
        st.session_state.rejected_count = 0
    if "plc_logs" not in st.session_state:
        st.session_state.plc_logs = []
    if "last_verdict" not in st.session_state:
        st.session_state.last_verdict = "STANDBY"
    if "last_failure_mode" not in st.session_state:
        st.session_state.last_failure_mode = "NONE"
    if "last_payload" not in st.session_state:
        st.session_state.last_payload = {}
    if "ejector_active" not in st.session_state:
        st.session_state.ejector_active = False
    if "sim_tick" not in st.session_state:
        st.session_state.sim_tick = 0
    if "force_defect_trigger" not in st.session_state:
        st.session_state.force_defect_trigger = False

init_session_state()


# ==============================================================================
# 8. SIDEBAR CONTROL PANEL
# ==============================================================================
with st.sidebar:
    st.markdown("""
    <div style="border-bottom: 1px solid #1e293b; padding-bottom: 8px; margin-bottom: 12px;">
        <span style="color: #00E5FF; font-weight: 800; font-size: 1.05rem; letter-spacing: 1px;">⚙️ STATION CONTROLLER</span>
    </div>
    """, unsafe_allow_html=True)

    # Profile Switcher
    profile_selection = st.selectbox(
        "ACTIVE SKU PROFILE",
        options=[
            "📱 Smartphone Screen & Chassis QA",
            "🍼 Water Bottle Blow-Molding QA"
        ],
        index=0
    )
    is_smartphone = "Smartphone" in profile_selection
    profile_key = "smartphone" if is_smartphone else "water_bottle"
    profile_label = "LINE_01: OLED DISPLAY" if is_smartphone else "LINE_04: BLOW MOLD"

    # Defect Sensitivity Slider
    st.markdown("<br>", unsafe_allow_html=True)
    sensitivity = st.slider(
        "DEFECT SENSITIVITY THRESHOLD",
        min_value=1,
        max_value=100,
        value=50,
        help="Higher values trigger rejection on microscopic hairline flaws; lower values require larger macroscopic fissures."
    )

    # Video Source Selector
    st.markdown("<br>", unsafe_allow_html=True)
    source_type = st.selectbox(
        "VIDEO STREAM SOURCE",
        options=["Demo Simulation Loop", "Live Camera (Index 0)", "Live Camera (Index 1)"],
        index=0
    )

    # Simulation Defect Frequency (For Demo Simulation Loop)
    if source_type == "Demo Simulation Loop":
        defect_prob = st.slider(
            "SIMULATED DEFECT PROBABILITY (%)",
            min_value=0,
            max_value=100,
            value=35,
            help="Chance of procedural defects (scratches, cracks, tilt, dents) entering the inspection cell."
        )

    # Manual Fault Injection Button (Hackathon Demo Super Weapon)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚨 INJECT SIMULATED DEFECT NOW", use_container_width=True):
        st.session_state.force_defect_trigger = True
        st.toast("⚡ FORCED DEFECT INJECTED INTO INFEED CONVEYOR!", icon="⚠️")

    # Audio Mute Toggle
    audio_enabled = st.checkbox("🔊 Enable HTML5 Audio Sirens", value=True)

    # Stage Previews Toggle
    show_cv_stages = st.checkbox("🔬 Show CV Algorithm Stages", value=False)

    # Reset Counters Button
    st.markdown("<hr style='border-color: #1e293b;'>", unsafe_allow_html=True)
    if st.button("🔄 RESET TELEMETRY COUNTERS", use_container_width=True):
        st.session_state.total_inspected = 0
        st.session_state.passed_count = 0
        st.session_state.rejected_count = 0
        st.session_state.plc_logs = []
        st.session_state.ejector_active = False
        st.rerun()


# ==============================================================================
# 9. MAIN COMMAND CENTER DASHBOARD (3 COLUMNS)
# ==============================================================================

# Header
st.markdown(f"""
<div class="cyber-header">
    <div class="cyber-title">
        <span>⚡ APEX-IV AUTONOMOUS ZERO-DEFECT COMMAND CENTER</span>
    </div>
    <div style="display: flex; gap: 12px; align-items: center;">
        <span style="color: #94a3b8; font-size: 0.8rem; letter-spacing: 1px;">PLC BUS: <strong style="color: #00FF66;">CONNECTED</strong></span>
        <span class="cyber-badge-live">● REAL-TIME ACTIVE</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 3-Column Layout
col_feed, col_kpi, col_plc = st.columns([1.35, 0.85, 1.1])

# Dynamic Placeholders for streaming updates
with col_feed:
    st.markdown("<div style='color: #00E5FF; font-size: 0.8rem; letter-spacing: 1.5px; margin-bottom: 6px;'>📡 EDGE VISION STREAM & RETICLE HUD</div>", unsafe_allow_html=True)
    video_placeholder = st.empty()
    stages_placeholder = st.empty()

with col_kpi:
    st.markdown("<div style='color: #00E5FF; font-size: 0.8rem; letter-spacing: 1.5px; margin-bottom: 6px;'>📊 REAL-TIME PRODUCTION ANALYTICS</div>", unsafe_allow_html=True)
    kpi_placeholder = st.empty()

with col_plc:
    st.markdown("<div style='color: #00E5FF; font-size: 0.8rem; letter-spacing: 1.5px; margin-bottom: 6px;'>🤖 VIRTUAL PLC & CLOSED-LOOP ACTUATORS</div>", unsafe_allow_html=True)
    actuator_placeholder = st.empty()
    feedback_placeholder = st.empty()
    terminal_placeholder = st.empty()

audio_placeholder = st.empty()


# ==============================================================================
# 10. FRAME ACQUISITION & PROCESSING CORE
# ==============================================================================
def acquire_frame(source: str, is_phone: bool, force_defect: bool, sim_defect_pct: int) -> Tuple[np.ndarray, Optional[str]]:
    """Acquires a frame either from live camera or the synthetic procedural simulator."""
    defect_type = None

    if source.startswith("Live Camera"):
        cam_idx = 0 if "0" in source else 1
        cap = cv2.VideoCapture(cam_idx)
        ret, cam_frame = cap.read()
        cap.release()
        if ret and cam_frame is not None:
            return cv2.resize(cam_frame, (640, 480)), None
        # Fallback to simulator if camera unavailable
        source = "Demo Simulation Loop"

    # Procedural Simulation Engine
    if is_phone:
        possible_defects = ["SPIDER_CRACK", "HAIRLINE_SCRATCH", "FOREIGN_SMUDGE", "BEZEL_DENT"]
        if force_defect or (random.randint(1, 100) <= sim_defect_pct):
            defect_type = random.choice(possible_defects)
        frame = SyntheticDefectGenerator.create_smartphone_frame(defect_type=defect_type)
    else:
        possible_defects = ["CAP_TILT", "SIDEWALL_DENT", "BODY_CONTAMINATION"]
        if force_defect or (random.randint(1, 100) <= sim_defect_pct):
            defect_type = random.choice(possible_defects)
        frame = SyntheticDefectGenerator.create_water_bottle_frame(defect_type=defect_type)

    return frame, defect_type


# ==============================================================================
# 11. STREAMING INSPECTION CYCLE
# ==============================================================================
# Acquire Frame
start_proc_time = time.time()
sim_defect_rate = defect_prob if source_type == "Demo Simulation Loop" else 0
raw_frame, synthetic_defect_injected = acquire_frame(
    source_type, is_smartphone, st.session_state.force_defect_trigger, sim_defect_rate
)
st.session_state.force_defect_trigger = False  # Consume trigger

# Run Selected Inspection Pipeline
if is_smartphone:
    verdict, failure_mode, severity, roi, defect_boxes, cv_stages = (
        EdgeInspectionCore.inspect_smartphone_display(raw_frame, sensitivity)
    )
else:
    verdict, failure_mode, severity, roi, defect_boxes, cv_stages = (
        EdgeInspectionCore.inspect_water_bottle(raw_frame, sensitivity)
    )

proc_latency_ms = (time.time() - start_proc_time) * 1000.0
# Add synthetic edge variance to reflect real embedded inference time ~12-16ms
edge_latency_ms = max(11.4, round(proc_latency_ms + random.uniform(11.2, 14.8), 1))
calc_fps = round(1000.0 / (edge_latency_ms + 1e-5), 1)

# Update Analytics Counters
st.session_state.total_inspected += 1
if verdict == "PASS":
    st.session_state.passed_count += 1
    st.session_state.ejector_active = False
else:
    st.session_state.rejected_count += 1
    st.session_state.ejector_active = True

# First-Pass Yield (FPY %)
fpy = (
    (st.session_state.passed_count / st.session_state.total_inspected) * 100.0
    if st.session_state.total_inspected > 0
    else 100.0
)

# Dispatch Simulated PLC Telemetry Payload
plc_payload = VirtualPlcEngine.dispatch_payload(profile_key, verdict, failure_mode, severity)
st.session_state.last_payload = plc_payload
st.session_state.last_verdict = verdict
st.session_state.last_failure_mode = failure_mode

# Append to live terminal log
log_entry = f"[{datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]}] {plc_payload['station_id']} -> VERDICT: {verdict} | ACTUATOR: {plc_payload['actuator']}\n"
st.session_state.plc_logs.insert(0, log_entry)
if len(st.session_state.plc_logs) > 30:
    st.session_state.plc_logs.pop()

# Render Cyber HUD Over Frame
hud_frame = CyberHudRenderer.draw_hud(
    raw_frame,
    verdict=verdict,
    failure_mode=failure_mode,
    severity=severity,
    fps=calc_fps,
    latency_ms=edge_latency_ms,
    profile_name=profile_label,
    defect_boxes=defect_boxes
)

# ==============================================================================
# 12. UI COMPONENT RENDERING
# ==============================================================================

# Column 1: Video Feed & Stages
with video_placeholder.container():
    # Convert BGR to RGB for Streamlit
    frame_rgb = cv2.cvtColor(hud_frame, cv2.COLOR_BGR2RGB)
    st.image(frame_rgb, channels="RGB", use_container_width=True)
    
    status_glow = "color: #FF0033; text-shadow: 0 0 10px rgba(255, 0, 51, 0.4);" if verdict == "REJECT" else "color: #00FF66; text-shadow: 0 0 10px rgba(0, 255, 102, 0.4);"
    st.markdown(f"""
    <div class="hud-telemetry">
        <span>INSPECTION STATE: <strong style="{status_glow}">{verdict}</strong></span>
        <span>OPTICAL DEFECT SEVERITY: <strong style="{status_glow}">{severity}%</strong></span>
    </div>
    """, unsafe_allow_html=True)

if show_cv_stages:
    with stages_placeholder.container():
        st.markdown("<div style='color: #00E5FF; font-size: 0.72rem; letter-spacing: 1px; margin-top: 8px;'>CV PIPELINE FILTER STAGES:</div>", unsafe_allow_html=True)
        stage_cols = st.columns(len(cv_stages))
        for idx, (s_name, s_img) in enumerate(cv_stages.items()):
            with stage_cols[idx]:
                st.caption(s_name)
                st.image(cv2.cvtColor(s_img, cv2.COLOR_BGR2RGB), use_container_width=True)

# Column 2: Real-Time KPI Analytics
with kpi_placeholder.container():
    fpy_class = "val-green" if fpy >= 95.0 else ("val-amber" if fpy >= 85.0 else "val-red")
    
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card total">
            <div class="kpi-label">TOTAL UNITS INSPECTED</div>
            <div class="kpi-value val-cyan">{st.session_state.total_inspected:,}</div>
        </div>
        <div class="kpi-card pass">
            <div class="kpi-label">PASSED UNITS (ZERO-DEFECT)</div>
            <div class="kpi-value val-green">{st.session_state.passed_count:,}</div>
        </div>
        <div class="kpi-card reject">
            <div class="kpi-label">REJECTED UNITS (DISCARDED)</div>
            <div class="kpi-value val-red">{st.session_state.rejected_count:,}</div>
        </div>
        <div class="kpi-card yield">
            <div class="kpi-label">FIRST-PASS YIELD (FPY)</div>
            <div class="kpi-value {fpy_class}">{fpy:5.1f}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Industrial Quality Benchmark Widget
    target_fpy = 98.5
    fpy_delta = fpy - target_fpy
    delta_color = "var(--neon-green)" if fpy_delta >= 0 else "var(--neon-red)"
    st.markdown(f"""
    <div style="background: #090e17; border: 1px solid #1a2536; border-radius: 6px; padding: 10px; font-size: 0.72rem;">
        <div style="color: #94a3b8; margin-bottom: 4px;">INDUSTRY 4.0 BENCHMARK: <strong>SIX-SIGMA 98.5%</strong></div>
        <div style="color: {delta_color}; font-weight: 700;">DELTA VS TARGET: {fpy_delta:+.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

# Column 3: Virtual PLC & Closed-Loop Actuator
with actuator_placeholder.container():
    if st.session_state.ejector_active:
        if is_smartphone:
            badge_text = "⚠️ PNEUMATIC EJECTOR ACTUATED"
        else:
            badge_text = "⚠️ ROTARY SORTER EJECT FIRED"
        st.markdown(f"""
        <div class="ejector-badge-active">
            {badge_text}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="ejector-badge-idle">
            ACTUATOR: ARMED / STANDBY
        </div>
        """, unsafe_allow_html=True)

with feedback_placeholder.container():
    st.markdown("<div style='color: #94a3b8; font-size: 0.72rem; letter-spacing: 1px; margin-bottom: 4px;'>CLOSED-LOOP SELF-HEALING OFFSETS:</div>", unsafe_allow_html=True)
    feedback_dict = plc_payload.get("closed_loop_feedback", {})
    for param_name, param_val in feedback_dict.items():
        is_shifted = "-" in param_val or "+" in param_val
        val_class = "param-val-shift" if is_shifted else "param-val-norm"
        cleaned_label = param_name.replace("_", " ").upper()
        st.markdown(f"""
        <div class="param-pill">
            <span class="param-label">{cleaned_label}</span>
            <span class="{val_class}">{param_val}</span>
        </div>
        """, unsafe_allow_html=True)

with terminal_placeholder.container():
    st.markdown("<div style='color: #00E5FF; font-size: 0.72rem; letter-spacing: 1px; margin-top: 8px; margin-bottom: 4px;'>PLC TELEMETRY STREAM TERMINAL:</div>", unsafe_allow_html=True)
    latest_json_str = json.dumps(plc_payload, indent=2)
    st.markdown(f"""
    <div class="plc-terminal">
// DISPATCHED TO EDGE GATEWAY MQTT/OPC-UA
{latest_json_str}
    </div>
    """, unsafe_allow_html=True)

# Trigger Audio Siren if Rejected
if verdict == "REJECT" and audio_enabled:
    with audio_placeholder.container():
        trigger_html5_audio_alert()

# ==============================================================================
# 13. STREAMLIT CONTINUOUS RUNTIME CONTROLLER
# ==============================================================================
st.markdown("<br>", unsafe_allow_html=True)
ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1, 1, 2])

with ctrl_col1:
    auto_run = st.toggle("⚡ Continuous Autonomous Inspection Loop", value=True)

with ctrl_col2:
    loop_delay = st.slider("Conveyor Scan Interval (s)", min_value=0.2, max_value=2.5, value=0.8, step=0.1)

with ctrl_col3:
    if st.button("⏩ Step Single Cycle (Manual Trigger)", use_container_width=True):
        st.rerun()

# Auto-refresh loop when continuous mode is active
if auto_run:
    time.sleep(loop_delay)
    st.rerun()
