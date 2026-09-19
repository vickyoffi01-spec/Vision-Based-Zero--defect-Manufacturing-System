"""Virtual PLC decision endpoint for genuine bolt inspections."""

from typing import Any, Dict


class PLCSimulator:
    def __init__(self):
        self.status = "READY"
        self.last_action = "WAITING"

    def process_inspection(self, inspection: Dict[str, Any]) -> Dict[str, str]:
        if inspection.get("decision") == "PASS":
            self.status = "READY"
            self.last_action = "CONTINUE_LINE"
        elif inspection.get("decision") == "DEFECT":
            self.status = "REJECT"
            self.last_action = "REJECT_BOLT"
        return {"status": self.status, "action": self.last_action}

    def reset(self) -> None:
        self.status = "READY"
        self.last_action = "WAITING"