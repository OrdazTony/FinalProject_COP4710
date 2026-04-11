# pyright: reportMissingImports=false
"""Simple PyQt frontend for the Pet Adoption Management System.

This desktop UI uses the sample schema/data in the repository and gives a
simple way to preview Queries 1 through 8.
"""

from __future__ import annotations

import sys

try:
    from PyQt5.QtGui import QIntValidator
    from PyQt5.QtWidgets import (
        QApplication,
        QComboBox,
        QFormLayout,
        QGridLayout,
        QGroupBox,
        QLabel,
        QLineEdit,
        QMainWindow,
        QPushButton,
        QTableWidget,
        QTableWidgetItem,
        QTextEdit,
        QVBoxLayout,
        QWidget,
    )
except ImportError:
    from PyQt6.QtGui import QIntValidator  # type: ignore
    from PyQt6.QtWidgets import (  # type: ignore
        QApplication,
        QComboBox,
        QFormLayout,
        QGridLayout,
        QGroupBox,
        QLabel,
        QLineEdit,
        QMainWindow,
        QPushButton,
        QTableWidget,
        QTableWidgetItem,
        QTextEdit,
        QVBoxLayout,
        QWidget,
    )


class PetAdoptionWindow(QMainWindow):
    QUERY_TEXT = {
        "view_all_pets": "SELECT pet_id, name, species, age, available\nFROM Pet\nORDER BY pet_id;",
        "view_available_pets": "SELECT pet_id, name, species, age, available\nFROM Pet\nWHERE available = TRUE\nORDER BY pet_id;",
        "count_applications_per_pet": "SELECT p.pet_id, p.name AS pet_name, COUNT(a.application_id) AS application_count\nFROM Pet p\nLEFT JOIN AdoptionApplication a ON p.pet_id = a.pet_id\nGROUP BY p.pet_id, p.name\nORDER BY p.pet_id;",
        "view_approved_applications": "SELECT application_id, user_id, pet_id, status, submitted_at, notes\nFROM AdoptionApplication\nWHERE status = 'Approved'\nORDER BY application_id;",
        "view_all_applications": "SELECT application_id, user_id, pet_id, status, submitted_at, notes\nFROM AdoptionApplication\nORDER BY application_id;",
        "view_applications_by_pet": "SELECT application_id, user_id, pet_id, status, submitted_at, notes\nFROM AdoptionApplication\nWHERE pet_id = 101\nORDER BY application_id;",
        "view_applications_by_user": "SELECT application_id, user_id, pet_id, status, submitted_at, notes\nFROM AdoptionApplication\nWHERE user_id = 1\nORDER BY application_id;",
        "view_named_applications": "SELECT a.application_id, u.name AS user_name, p.name AS pet_name, a.status, a.submitted_at, a.notes\nFROM AdoptionApplication a\nJOIN UserTable u ON a.user_id = u.user_id\nJOIN Pet p ON a.pet_id = p.pet_id\nORDER BY a.application_id;",
        "submit_application": "INSERT INTO AdoptionApplication (user_id, pet_id, status, submitted_at, notes)\nVALUES (<user_id>, <pet_id>, 'Pending', CURRENT_TIMESTAMP, <notes>);",
        "update_application_status": "UPDATE AdoptionApplication\nSET status = <new_status>\nWHERE application_id = <application_id>;",
    }

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Pet Adoption Management System - PyQt Frontend")
        self.resize(1100, 850)

        self.int_validator = QIntValidator(1, 999999, self)

        self.users = [
            {"user_id": 1, "name": "Alice Johnson", "email": "alice@example.com"},
            {"user_id": 2, "name": "Brian Lee", "email": "brian@example.com"},
            {"user_id": 3, "name": "Carla Mendes", "email": "carla@example.com"},
            {"user_id": 4, "name": "David Smith", "email": "david@example.com"},
        ]
        self.pets = [
            {"pet_id": 101, "name": "Buddy", "species": "Dog", "age": 3, "available": True},
            {"pet_id": 102, "name": "Mittens", "species": "Cat", "age": 2, "available": True},
            {"pet_id": 103, "name": "Rocky", "species": "Dog", "age": 7, "available": False},
            {"pet_id": 104, "name": "Coco", "species": "Bird", "age": 0, "available": True},
            {"pet_id": 105, "name": "Luna", "species": "Cat", "age": 12, "available": True},
        ]
        self.applications = [
            {
                "application_id": 1,
                "user_id": 1,
                "pet_id": 101,
                "status": "Pending",
                "submitted_at": "2026-04-01 10:30:00",
                "notes": "Looking for a family dog",
            },
            {
                "application_id": 2,
                "user_id": 2,
                "pet_id": 102,
                "status": "Approved",
                "submitted_at": "2026-04-02 14:00:00",
                "notes": "Has experience with cats",
            },
            {
                "application_id": 3,
                "user_id": 3,
                "pet_id": 103,
                "status": "Rejected",
                "submitted_at": "2026-04-03 09:15:00",
                "notes": None,
            },
            {
                "application_id": 4,
                "user_id": 1,
                "pet_id": 105,
                "status": "Withdrawn",
                "submitted_at": "2026-04-04 16:45:00",
                "notes": "Moved to a smaller apartment",
            },
            {
                "application_id": 5,
                "user_id": 4,
                "pet_id": 101,
                "status": "Pending",
                "submitted_at": "2026-04-05 11:20:00",
                "notes": None,
            },
        ]

        self._sync_pet_availability()
        self._build_ui()
        self.view_all_pets()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        title = QLabel("Pet Adoption Management System")
        title.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 8px;")
        subtitle = QLabel(
            "Simple PyQt frontend based on the sample pet adoption schema and saved Queries 1-8."
        )
        subtitle.setWordWrap(True)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        schema_label = QLabel(
            "<b>UserTable</b>: user_id, name, email<br>"
            "<b>Pet</b>: pet_id, name, species, age, available<br>"
            "<b>AdoptionApplication</b>: application_id, user_id, pet_id, status, submitted_at, notes"
        )
        schema_label.setWordWrap(True)
        layout.addWidget(schema_label)

        layout.addWidget(self._create_actions_group())
        layout.addWidget(self._create_submit_group())

        self.status_label = QLabel("Loaded with the sample pet adoption data. Backend wiring is not implemented yet.")
        self.status_label.setStyleSheet("padding: 8px; background: #eef6ff; border: 1px solid #cfe2ff;")
        layout.addWidget(self.status_label)

        self.query_title_label = QLabel("Select one of the eight queries.")
        self.query_title_label.setStyleSheet("font-weight: bold; margin-top: 6px;")
        layout.addWidget(self.query_title_label)

        self.query_preview = QTextEdit()
        self.query_preview.setReadOnly(True)
        self.query_preview.setMaximumHeight(130)
        self.query_preview.setStyleSheet("font-family: Menlo, Consolas, monospace;")
        layout.addWidget(self.query_preview)

        self.results_table = QTableWidget()
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setMinimumHeight(260)
        layout.addWidget(self.results_table)

    def _create_actions_group(self) -> QGroupBox:
        group = QGroupBox("Queries 1-8")
        grid = QGridLayout(group)

        buttons = [
            ("Query 1 · All pets", self.view_all_pets),
            ("Query 2 · Available pets", self.view_available_pets),
            ("Query 3 · Count per pet", self.count_applications_per_pet),
            ("Query 4 · Approved apps", self.view_approved_applications),
            ("Query 5 · All apps", self.view_all_applications),
            ("Query 6 · Apps for pet 101", self.run_query_6_sample),
            ("Query 7 · Apps for user 1", self.run_query_7_sample),
            ("Query 8 · Names view", self.view_named_applications),
        ]

        for index, (label, handler) in enumerate(buttons):
            button = QPushButton(label)
            button.clicked.connect(handler)
            grid.addWidget(button, index // 2, index % 2)

        return group

    def _create_submit_group(self) -> QGroupBox:
        group = QGroupBox("New Adoption Application")
        form = QFormLayout(group)

        self.user_combo = QComboBox()
        for user in self.users:
            self.user_combo.addItem(f"{user['user_id']} - {user['name']}", user["user_id"])

        self.pet_combo = QComboBox()
        self._refresh_pet_combo()

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Optional notes")
        self.notes_input.setMaximumHeight(80)

        submit_button = QPushButton("Submit application")
        submit_button.clicked.connect(self.submit_application)

        form.addRow("user", self.user_combo)
        form.addRow("available pet", self.pet_combo)
        form.addRow("notes", self.notes_input)
        form.addRow(submit_button)

        return group

    def _sync_pet_availability(self) -> None:
        approved_pet_ids = {
            app["pet_id"] for app in self.applications if app["status"] == "Approved"
        }
        for pet in self.pets:
            pet["available"] = pet["pet_id"] not in approved_pet_ids

    def _refresh_pet_combo(self) -> None:
        self._sync_pet_availability()
        self.pet_combo.clear()
        available_pets = [pet for pet in self.pets if pet["available"]]

        if not available_pets:
            self.pet_combo.addItem("No available pets", None)
            return

        for pet in available_pets:
            self.pet_combo.addItem(f"{pet['pet_id']} - {pet['name']} ({pet['species']})", pet["pet_id"])

    def view_all_pets(self) -> None:
        self._sync_pet_availability()
        self._show_rows(self.pets, ["pet_id", "name", "species", "age", "available"])
        self._set_context("Showing all pets from the sample data.", "view_all_pets")

    def view_available_pets(self) -> None:
        self._sync_pet_availability()
        rows = [pet for pet in self.pets if pet["available"]]
        self._show_rows(rows, ["pet_id", "name", "species", "age", "available"])
        self._set_context("Showing only pets that are currently available.", "view_available_pets")

    def count_applications_per_pet(self) -> None:
        rows = []
        for pet in self.pets:
            rows.append(
                {
                    "pet_id": pet["pet_id"],
                    "pet_name": pet["name"],
                    "application_count": sum(1 for app in self.applications if app["pet_id"] == pet["pet_id"]),
                }
            )
        self._show_rows(rows, ["pet_id", "pet_name", "application_count"])
        self._set_context("Showing the number of applications for each pet.", "count_applications_per_pet")

    def view_approved_applications(self) -> None:
        rows = [app for app in self.applications if app["status"] == "Approved"]
        self._show_rows(rows, ["application_id", "user_id", "pet_id", "status", "submitted_at", "notes"])
        self._set_context("Showing approved adoption applications only.", "view_approved_applications")

    def view_all_applications(self) -> None:
        self._show_rows(self.applications, ["application_id", "user_id", "pet_id", "status", "submitted_at", "notes"])
        self._set_context("Showing all adoption applications.", "view_all_applications")

    def run_query_6_sample(self) -> None:
        rows = [app for app in self.applications if app["pet_id"] == 101]
        self._show_rows(rows, ["application_id", "user_id", "pet_id", "status", "submitted_at", "notes"])
        self._set_context("Showing Query 6 for pet_id = 101.", "view_applications_by_pet")

    def run_query_7_sample(self) -> None:
        rows = [app for app in self.applications if app["user_id"] == 1]
        self._show_rows(rows, ["application_id", "user_id", "pet_id", "status", "submitted_at", "notes"])
        self._set_context("Showing Query 7 for user_id = 1.", "view_applications_by_user")

    def view_named_applications(self) -> None:
        rows = []
        for application in self.applications:
            user_name = next((user["name"] for user in self.users if user["user_id"] == application["user_id"]), "Unknown user")
            pet_name = next((pet["name"] for pet in self.pets if pet["pet_id"] == application["pet_id"]), "Unknown pet")
            rows.append(
                {
                    "application_id": application["application_id"],
                    "user_name": user_name,
                    "pet_name": pet_name,
                    "status": application["status"],
                    "submitted_at": application["submitted_at"],
                    "notes": application["notes"],
                }
            )
        self._show_rows(rows, ["application_id", "user_name", "pet_name", "status", "submitted_at", "notes"])
        self._set_context("Showing each application with the user and pet names.", "view_named_applications")

    def submit_application(self) -> None:
        user_id = self.user_combo.currentData()
        pet_id = self.pet_combo.currentData()
        notes = self.notes_input.toPlainText().strip() or None

        self.query_title_label.setText("New adoption application")
        self.query_preview.setPlainText(self.QUERY_TEXT["submit_application"])

        if user_id is None or pet_id is None:
            self._show_notice("Please choose an available pet to continue.")
            return

        next_id = max(app["application_id"] for app in self.applications) + 1
        new_application = {
            "application_id": next_id,
            "user_id": user_id,
            "pet_id": pet_id,
            "status": "Pending",
            "submitted_at": "CURRENT_TIMESTAMP",
            "notes": notes,
        }

        self.applications.append(new_application)
        self.notes_input.clear()
        self._show_rows(
            [new_application],
            ["application_id", "user_id", "pet_id", "status", "submitted_at", "notes"],
        )
        self._set_status(f"Application {next_id} was submitted successfully.")

    def _set_context(self, message: str, query_key: str) -> None:
        self._set_status(message)
        self.query_title_label.setText(query_key.replace("_", " ").title())
        self.query_preview.setPlainText(self.QUERY_TEXT.get(query_key, ""))

    def _set_status(self, message: str) -> None:
        self.status_label.setText(f"{message} This frontend uses the sample data and is not connected to the live backend.")

    def _show_notice(self, message: str) -> None:
        self._show_rows([{"notice": message}], ["notice"])

    def _show_rows(self, rows: list[dict], columns: list[str]) -> None:
        self.results_table.clear()
        self.results_table.setColumnCount(len(columns))
        self.results_table.setHorizontalHeaderLabels(columns)
        self.results_table.setRowCount(len(rows))

        for row_index, row in enumerate(rows):
            for column_index, column_name in enumerate(columns):
                value = row.get(column_name, "")
                self.results_table.setItem(row_index, column_index, QTableWidgetItem(self._format_value(value)))

        self.results_table.resizeColumnsToContents()

    def _format_value(self, value: object) -> str:
        if value is None or value == "":
            return "NULL"
        if isinstance(value, bool):
            return "true" if value else "false"
        return str(value)


def main() -> None:
    app = QApplication(sys.argv)
    window = PetAdoptionWindow()
    window.show()

    if hasattr(app, "exec"):
        sys.exit(app.exec())
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
