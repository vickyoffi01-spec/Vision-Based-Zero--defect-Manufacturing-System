import numpy as np

from database import InspectionDatabase
from inspection_service import CONFIDENCE_THRESHOLD, MODEL_PATH, InspectionService
from plc_simulator import PLCSimulator


def test_missing_model_never_claims_bolt(tmp_path):
    service = InspectionService(tmp_path / "missing" / "best.pt")
    frame = np.zeros((240, 320, 3), dtype=np.uint8)
    _, result, is_new = service.inspect(frame)
    assert not service.model_loaded
    assert result["product"] == ""
    assert result["status"] == "WAITING FOR OBJECT"
    assert result["class_name"] == ""
    assert result["confidence"] is None
    assert not is_new


def test_database_starts_empty(tmp_path):
    database = InspectionDatabase(tmp_path / "inspections.db")
    assert database.kpis() == {"total_inspected": 0, "passed": 0, "defective": 0, "defect_rate": 0.0}
    assert database.history() == []


def test_plc_uses_only_bolt_decisions():
    plc = PLCSimulator()
    assert plc.process_inspection({"decision": "PASS"}) == {"status": "READY", "action": "CONTINUE_LINE"}
    assert plc.process_inspection({"decision": "DEFECT"}) == {"status": "REJECT", "action": "REJECT_BOLT"}


def test_configuration():
    assert str(MODEL_PATH).endswith("models\\best.pt") or str(MODEL_PATH).endswith("models/best.pt")
    assert CONFIDENCE_THRESHOLD == 0.50