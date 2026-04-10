# pyright: reportMissingImports=false
"""Simple PyQt prototype for the Pet Adoption Management System.

This UI matches the naming and menu functionality described in `Names.txt`
and `Python_Backend.txt`. It is intentionally a front-end scaffold and is
not connected to the database/backend yet.
"""

from __future__ import annotations

import sys

try:
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
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Pet Adoption Management System - PyQt Prototype")
        self.resize(1050, 760)

        self.pets = [
            {"pet_id": 1, "name": "Milo", "species": "Dog", "age": 3, "available": True},
            {"pet_id": 2, "name": "Luna", "species": "Cat", "age": 2, "available": False},
            {"pet_id": 3, "name": "Coco", "species": "Rabbit", "age": 1, "available": True},
        ]
        self.applications = [
            {
                "application_id": 101,
                "user_id": 1,
                "pet_id": 1,
                "status": "Pending",
                "submitted_at": "2026-04-10 10:00",
                "notes": "Lives near a dog park",
            },
            {
                "application_id": 102,
                "user_id": 2,
                "pet_id": 2,
                "status": "Approved",
                "submitted_at": "2026-04-09 14:30",
                "notes": "Previous cat owner",
            },
        ]

        self._build_ui()
        self.view_all_pets()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        title = QLabel("Pet Adoption Management System")
        title.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 8px;")
        subtitle = QLabel(
            "PyQt front-end scaffold based on the backend menu and table/column names in this repository."
        )
        subtitle.setWordWrap(True)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addWidget(self._create_actions_group())
        layout.addWidget(self._create_submit_group())
        layout.addWidget(self._create_search_group())
        layout.addWidget(self._create_status_group())

        self.status_label = QLabel("Prototype loaded. Backend wiring is not implemented yet.")
        self.status_label.setStyleSheet("padding: 8px; background: #eef6ff; border: 1px solid #cfe2ff;")
        layout.addWidget(self.status_label)

        self.results_table = QTableWidget()
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setMinimumHeight(260)
        layout.addWidget(self.results_table)

    def _create_actions_group(self) -> QGroupBox:
        group = QGroupBox("Quick Actions")
        grid = QGridLayout(group)

        buttons = [
            ("View all pets", self.view_all_pets),
            ("View available pets", self.view_available_pets),
            ("View all applications", self.view_all_applications),
            ("Count applications per pet", self.count_applications_per_pet),
            ("View approved applications", self.view_approved_applications),
        ]

        for index, (label, handler) in enumerate(buttons):
            button = QPushButton(label)
            button.clicked.connect(handler)
            grid.addWidget(button, index // 2, index % 2)

        return group

    def _create_submit_group(self) -> QGroupBox:
        group = QGroupBox("Submit Adoption Application")
        form = QFormLayout(group)

        self.user_id_input = QLineEdit()
        self.user_id_input.setPlaceholderText("Enter user_id")
        self.pet_id_input = QLineEdit()
        self.pet_id_input.setPlaceholderText("Enter pet_id")
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Optional notes")
        self.notes_input.setMaximumHeight(90)

        submit_button = QPushButton("Submit application")
        submit_button.clicked.connect(self.submit_application)

        form.addRow("user_id", self.user_id_input)
        form.addRow("pet_id", self.pet_id_input)
        form.addRow("notes", self.notes_input)
        form.addRow(submit_button)

        return group

    def _create_search_group(self) -> QGroupBox:
        group = QGroupBox("Search Applications")
        form = QFormLayout(group)

        self.search_pet_id_input = QLineEdit()
        self.search_pet_id_input.setPlaceholderText("View applications by pet ID")
        self.search_user_id_input = QLineEdit()
        self.search_user_id_input.setPlaceholderText("View applications by user ID")

        pet_button = QPushButton("Search by pet")
        pet_button.clicked.connect(self.view_applications_by_pet)
        user_button = QPushButton("Search by user")
        user_button.clicked.connect(self.view_applications_by_user)

        form.addRow("pet_id", self.search_pet_id_input)
        form.addRow(pet_button)
        form.addRow("user_id", self.search_user_id_input)
        form.addRow(user_button)

        return group

    def _create_status_group(self) -> QGroupBox:
        group = QGroupBox("Update Application Status")
        form = QFormLayout(group)

        self.application_id_input = QLineEdit()
        self.application_id_input.setPlaceholderText("Enter application_id")
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Pending", "Approved", "Rejected", "Withdrawn"])

        update_button = QPushButton("Update status")
        update_button.clicked.connect(self.update_application_status)

        form.addRow("application_id", self.application_id_input)
        form.addRow("status", self.status_combo)
        form.addRow(update_button)

        return group

    def view_all_pets(self) -> None:
        self._show_rows(self.pets, ["pet_id", "name", "species", "age", "available"])
        self._set_status("Previewing `view_all_pets()`.")

    def view_available_pets(self) -> None:
        rows = [pet for pet in self.pets if pet["available"]]
        self._show_rows(rows, ["pet_id", "name", "species", "age", "available"])
        self._set_status("Previewing `view_available_pets()`.")

    def submit_application(self) -> None:
        payload = {
            "user_id": self.user_id_input.text().strip(),
            "pet_id": self.pet_id_input.text().strip(),
            "status": "Pending",
            "notes": self.notes_input.toPlainText().strip(),
        }
        self._show_rows([payload], ["user_id", "pet_id", "status", "notes"])
        self._set_status("Prototype only: this will later call `submit_application()` from the backend.")

    def view_all_applications(self) -> None:
        self._show_rows(
            self.applications,
            ["application_id", "user_id", "pet_id", "status", "submitted_at", "notes"],
        )
        self._set_status("Previewing `view_all_applications()`.")

    def view_applications_by_pet(self) -> None:
        pet_id_text = self.search_pet_id_input.text().strip()
        rows = [app for app in self.applications if str(app["pet_id"]) == pet_id_text]
        self._show_rows(rows, ["application_id", "user_id", "pet_id", "status", "submitted_at", "notes"])
        self._set_status(f"Previewing `view_applications_by_pet()` for pet_id = {pet_id_text or 'N/A'}.")

    def view_applications_by_user(self) -> None:
        user_id_text = self.search_user_id_input.text().strip()
        rows = [app for app in self.applications if str(app["user_id"]) == user_id_text]
        self._show_rows(rows, ["application_id", "user_id", "pet_id", "status", "submitted_at", "notes"])
        self._set_status(f"Previewing `view_applications_by_user()` for user_id = {user_id_text or 'N/A'}.")

    def update_application_status(self) -> None:
        application_id_text = self.application_id_input.text().strip()
        new_status = self.status_combo.currentText()

        for application in self.applications:
            if str(application["application_id"]) == application_id_text:
                application["status"] = new_status
                if new_status == "Approved":
                    for pet in self.pets:
                        if pet["pet_id"] == application["pet_id"]:
                            pet["available"] = False
                break

        preview = [{"application_id": application_id_text, "status": new_status}]
        self._show_rows(preview, ["application_id", "status"])
        self._set_status("Prototype only: this will later call `update_application_status()` in the backend.")

    def count_applications_per_pet(self) -> None:
        rows = []
        for pet in self.pets:
            count = sum(1 for app in self.applications if app["pet_id"] == pet["pet_id"])
            rows.append(
                {
                    "pet_id": pet["pet_id"],
                    "pet_name": pet["name"],
                    "application_count": count,
                }
            )

        self._show_rows(rows, ["pet_id", "pet_name", "application_count"])
        self._set_status("Previewing `count_applications_per_pet()`.")

    def view_approved_applications(self) -> None:
        rows = [app for app in self.applications if app["status"] == "Approved"]
        self._show_rows(rows, ["application_id", "user_id", "pet_id", "status", "submitted_at", "notes"])
        self._set_status("Previewing `view_approved_applications()`.")

    def _set_status(self, message: str) -> None:
        self.status_label.setText(f"{message} Backend connection is not wired up yet.")

    def _show_rows(self, rows: list[dict], columns: list[str]) -> None:
        self.results_table.clear()
        self.results_table.setColumnCount(len(columns))
        self.results_table.setHorizontalHeaderLabels(columns)
        self.results_table.setRowCount(len(rows))

        for row_index, row in enumerate(rows):
            for column_index, column_name in enumerate(columns):
                value = row.get(column_name, "")
                self.results_table.setItem(row_index, column_index, QTableWidgetItem(str(value)))

        self.results_table.resizeColumnsToContents()


def main() -> None:
    app = QApplication(sys.argv)
    window = PetAdoptionWindow()
    window.show()

    if hasattr(app, "exec"):
        sys.exit(app.exec())
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
