import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
)


class BudgetApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Aplicație de Buget Familial")
        self.setGeometry(300, 100, 600, 400)

        self.total_income = 0  # Venitul lunar total
        self.balance = 0  # Balanța curentă (după cheltuieli și venituri)

        # Widget principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal
        self.main_layout = QVBoxLayout()

        # Etichetă pentru venitul lunar inițial
        self.income_label = QLabel("Introduceți venitul lunar total:")
        self.main_layout.addWidget(self.income_label)

        # Input pentru venitul lunar
        self.income_input = QLineEdit()
        self.main_layout.addWidget(self.income_input)

        # Buton pentru setarea venitului lunar
        self.set_income_button = QPushButton("Setează venitul lunar")
        self.set_income_button.clicked.connect(self.set_income)
        self.main_layout.addWidget(self.set_income_button)

        # Etichetă pentru balanța curentă
        self.balance_label = QLabel(f"Balanța curentă: {self.balance} RON")
        self.main_layout.addWidget(self.balance_label)

        # Etichetă pentru banii rămași
        self.remaining_label = QLabel(f"Bani rămași pe lună: {self.balance} RON")
        self.main_layout.addWidget(self.remaining_label)

        # Form pentru adăugare venituri/cheltuieli
        self.form_layout = QFormLayout()

        self.amount_input = QLineEdit()
        self.category_input = QLineEdit()
        self.type_input = QLineEdit()  # Venit/Cheltuială
        self.form_layout.addRow("Sumă:", self.amount_input)
        self.form_layout.addRow("Categorie:", self.category_input)
        self.form_layout.addRow("Tip (Venit/Cheltuiala):", self.type_input)

        self.main_layout.addLayout(self.form_layout)

        # Buton pentru adăugare tranzacție
        self.add_button = QPushButton("Adaugă tranzacție")
        self.add_button.clicked.connect(self.add_transaction)
        self.main_layout.addWidget(self.add_button)

        # Tabel pentru istoricul tranzacțiilor
        self.transactions_table = QTableWidget()
        self.transactions_table.setColumnCount(3)
        self.transactions_table.setHorizontalHeaderLabels(["Sumă", "Categorie", "Tip"])
        self.main_layout.addWidget(self.transactions_table)

        self.central_widget.setLayout(self.main_layout)

    def set_income(self):
        """Setează venitul lunar și actualizează balanța."""
        try:
            self.total_income = float(self.income_input.text())
            self.balance = self.total_income
            self.update_balance_labels()
        except ValueError:
            self.income_label.setText("Introduceți un venit lunar valid!")

    def add_transaction(self):
        """Adaugă o tranzacție (venit/cheltuială) și actualizează balanța."""
        try:
            amount = float(self.amount_input.text())
            category = self.category_input.text()
            transaction_type = self.type_input.text().lower()

            # Actualizează balanța în funcție de tipul tranzacției
            if transaction_type == "venit":
                self.balance += amount
            elif transaction_type == "cheltuiala":
                self.balance -= amount
            else:
                return  # Dacă tipul nu este corect, nu face nimic

            # Actualizează eticheta balanței și a banilor rămași
            self.update_balance_labels()

            # Adaugă tranzacția în tabel
            row_position = self.transactions_table.rowCount()
            self.transactions_table.insertRow(row_position)
            self.transactions_table.setItem(row_position, 0, QTableWidgetItem(f"{amount} RON"))
            self.transactions_table.setItem(row_position, 1, QTableWidgetItem(category))
            self.transactions_table.setItem(row_position, 2, QTableWidgetItem(transaction_type.capitalize()))

            # Resetează câmpurile de input
            self.amount_input.clear()
            self.category_input.clear()
            self.type_input.clear()
        except ValueError:
            pass  # Dacă datele introduse nu sunt valide, ignoră tranzacția

    def update_balance_labels(self):
        """Actualizează etichetele pentru balanța curentă și banii rămași."""
        self.balance_label.setText(f"Balanța curentă: {self.balance:.2f} RON")
        self.remaining_label.setText(f"Bani rămași pe lună: {self.balance:.2f} RON")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = BudgetApp()
    window.show()

    sys.exit(app.exec())
