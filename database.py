"""SQLite persistence for genuine bolt inspections."""

import sqlite3
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_DATABASE_PATH = Path(__file__).with_name("inspections.db")


class InspectionDatabase:
    def __init__(self, path: Path = DEFAULT_DATABASE_PATH):
        self.path = Path(path)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS inspections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    inspected_at TEXT NOT NULL,
                    product TEXT NOT NULL,
                    status TEXT NOT NULL,
                    class_name TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    decision TEXT NOT NULL,
                    action TEXT NOT NULL,
                    bbox TEXT NOT NULL
                )
                """
            )

    def save(self, inspection: Dict[str, Any]) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO inspections
                (inspected_at, product, status, class_name, confidence, decision, action, bbox)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    inspection["inspected_at"],
                    inspection["product"],
                    inspection["status"],
                    inspection["class_name"],
                    inspection["confidence"],
                    inspection["decision"],
                    inspection["action"],
                    inspection["bbox"],
                ),
            )

    def history(self, limit: int = 100) -> List[Dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM inspections ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
        return [dict(row) for row in rows]

    def kpis(self) -> Dict[str, Any]:
        with self._connect() as connection:
            total, passed, defective = connection.execute(
                """
                SELECT COUNT(*),
                       SUM(CASE WHEN decision = 'PASS' THEN 1 ELSE 0 END),
                       SUM(CASE WHEN decision = 'DEFECT' THEN 1 ELSE 0 END)
                FROM inspections
                """
            ).fetchone()
        total = int(total or 0)
        passed = int(passed or 0)
        defective = int(defective or 0)
        return {
            "total_inspected": total,
            "passed": passed,
            "defective": defective,
            "defect_rate": (defective / total * 100.0) if total else 0.0,
        }