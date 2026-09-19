"""Real webcam and custom YOLO bolt inspection service."""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import cv2
import numpy as np

try:
    from ultralytics import YOLO
except ImportError:
    YOLO = None


MODEL_PATH = Path(__file__).with_name("models") / "best.pt"
CONFIDENCE_THRESHOLD = 0.50
VALID_CLASSES = {0: "Good_Bolt", 1: "Thread_Defect", 2: "Head_Defect"}


class InspectionService:
    def __init__(self, model_path: Path = MODEL_PATH):
        self.model_path = Path(model_path)
        self.model = None
        self.camera: Optional[cv2.VideoCapture] = None
        self._tracked_bbox: Optional[Tuple[int, int, int, int]] = None
        self._presence_reference: Optional[np.ndarray] = None
        self.model_error = ""
        if self.model_path.exists() and YOLO is not None:
            try:
                self.model = YOLO(str(self.model_path))
            except Exception as error:
                self.model_error = str(error)

    @property
    def model_loaded(self) -> bool:
        return self.model is not None

    def start_camera(self, camera_index: int = 0) -> bool:
        self.stop_camera()
        self.camera = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        if not self.camera.isOpened():
            self.camera.release()
            self.camera = cv2.VideoCapture(camera_index)
        if not self.camera.isOpened():
            self.camera = None
            return False
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        return True

    def stop_camera(self) -> None:
        if self.camera is not None:
            self.camera.release()
            self.camera = None
        self._tracked_bbox = None
        self._presence_reference = None

    def read_frame(self) -> Optional[np.ndarray]:
        if self.camera is None or not self.camera.isOpened():
            return None
        success, frame = self.camera.read()
        return frame if success and frame is not None else None

    def inspect(self, frame: np.ndarray) -> Tuple[np.ndarray, Dict[str, Any], bool]:
        if self.model_loaded:
            annotated, result = self._inspect_with_yolo(frame)
        else:
            annotated, result = self._inspect_without_model(frame)

        present = result["status"] in {"INSPECTED", "OBJECT PRESENT"}
        is_new = present and self._tracked_bbox is None
        if present:
            self._tracked_bbox = result.get("bbox") or self._tracked_bbox or (0, 0, 0, 0)
        else:
            self._tracked_bbox = None
        return annotated, result, is_new

    def _inspect_with_yolo(self, frame: np.ndarray) -> Tuple[np.ndarray, Dict[str, Any]]:
        annotated = frame.copy()
        detections = []
        try:
            results = self.model.predict(frame, conf=CONFIDENCE_THRESHOLD, verbose=False)
            for result in results:
                names = result.names or {}
                for box in result.boxes:
                    class_id = int(box.cls[0].item())
                    confidence = float(box.conf[0].item())
                    class_name = str(names.get(class_id, ""))
                    if class_id not in VALID_CLASSES or class_name != VALID_CLASSES[class_id]:
                        continue
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int).tolist()
                    bbox = (x1, y1, x2 - x1, y2 - y1)
                    detections.append((confidence, class_name, bbox))
                    color = (0, 200, 0) if class_id == 0 else (0, 0, 255)
                    cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(annotated, f"{class_name} {confidence:.2%}",
                                (x1, max(22, y1 - 8)), cv2.FONT_HERSHEY_SIMPLEX,
                                0.65, color, 2)
        except Exception as error:
            self.model_error = str(error)
            detections = []

        if not detections:
            self._draw_roi(annotated, (255, 180, 0))
            return annotated, self._waiting_result("WAITING FOR OBJECT")

        confidence, class_name, bbox = max(detections, key=lambda item: item[0])
        is_good = class_name == "Good_Bolt"
        return annotated, {
            "inspected_at": datetime.now().isoformat(timespec="seconds"),
            "product": "BOLT",
            "status": "INSPECTED",
            "class_name": class_name,
            "confidence": confidence,
            "decision": "PASS" if is_good else "DEFECT",
            "action": "CONTINUE_LINE" if is_good else "REJECT_BOLT",
            "verification": "YOLO DETECTION VERIFIED",
            "bbox": bbox,
        }

    def _inspect_without_model(self, frame: np.ndarray) -> Tuple[np.ndarray, Dict[str, Any]]:
        annotated = frame.copy()
        roi = self._roi(frame)
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        if self._presence_reference is None:
            self._presence_reference = gray.copy()
        difference = cv2.absdiff(gray, self._presence_reference)
        present = float(np.mean(difference)) > 12.0 or float(np.std(gray)) > 28.0
        self._draw_roi(annotated, (0, 180, 255) if present else (130, 130, 130))
        if present:
            return annotated, self._waiting_result("OBJECT PRESENT")
        return annotated, self._waiting_result("WAITING FOR OBJECT")

    def _waiting_result(self, status: str) -> Dict[str, Any]:
        if self.model_loaded:
            return {"product": "UNKNOWN", "status": status, "class_name": "NONE",
                    "confidence": None, "decision": "PENDING_AI",
                    "action": "WAITING_FOR_AI_DETECTION",
                    "verification": "NO VALID BOLT DETECTION", "bbox": None}
        return {"product": "UNKNOWN" if status == "OBJECT PRESENT" else "",
                "status": status,
                "class_name": "PRESENCE_ONLY" if status == "OBJECT PRESENT" else "",
                "confidence": None,
                "decision": "PENDING_AI" if status == "OBJECT PRESENT" else "",
                "action": "WAITING_FOR_AI_MODEL" if status == "OBJECT PRESENT" else "",
                "verification": "MODEL REQUIRED FOR BOLT DECISION", "bbox": None}

    @staticmethod
    def _roi(frame: np.ndarray) -> np.ndarray:
        height, width = frame.shape[:2]
        roi_width, roi_height = int(width * 0.65), int(height * 0.75)
        x1, y1 = (width - roi_width) // 2, (height - roi_height) // 2
        return frame[y1:y1 + roi_height, x1:x1 + roi_width]

    @staticmethod
    def _draw_roi(frame: np.ndarray, color: Tuple[int, int, int]) -> None:
        height, width = frame.shape[:2]
        roi_width, roi_height = int(width * 0.65), int(height * 0.75)
        x1, y1 = (width - roi_width) // 2, (height - roi_height) // 2
        cv2.rectangle(frame, (x1, y1), (x1 + roi_width, y1 + roi_height), color, 2)

    def release(self) -> None:
        self.stop_camera()