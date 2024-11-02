import json
from datetime import datetime


class Record:
    def __init__(self, date, amount, record_type, note):
        self.date = date
        self.amount = float(amount)
        self.type = record_type
        self.note = note

    def to_dict(self):
        return {
            'date': self.date,
            'amount': self.amount,
            'type': self.type,
            'note': self.note
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['date'], data['amount'], data['type'], data['note'])


class Ledger:
    def __init__(self, file_path='ledger.json'):
        self.records = []
        self.file_path = file_path
        self.load_records()

    def add_record(self, date, amount, record_type, note):
        new_record = Record(date, amount, record_type, note)
        self.records.append(new_record)
        self.save_records()

    def view_records(self):
        for record in self.records:
            print(f"Date: {record.date}, Amount: {record.amount}, Type: {record.type}, Note: {record.note}")

    def calculate_statistics(self):
        total_income = sum(record.amount for record in self.records if record.type == 'income')
        total_expense = sum(record.amount for record in self.records if record.type == 'expense')
        net_income = total_income - total_expense
        return total_income, total_expense, net_income

    def save_records(self):
        with open(self.file_path, 'w') as f:
            json.dump([r.to_dict() for r in self.records], f, indent=4)

    def load_records(self):
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                self.records = [Record.from_dict(item) for item in data]
        except FileNotFoundError:
            self.records = []


def main():
    ledger = Ledger()

    while True:
        print("\nPersonal Ledger")
        print("1. Add Record")
        print("2. View Records")
        print("3. Show Statistics")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            date = input("Enter date (YYYY-MM-DD): ")
            amount = input("Enter amount: ")
            record_type = input("Enter type (income/expense): ").lower()
            note = input("Enter note: ")
            ledger.add_record(date, amount, record_type, note)

        elif choice == '2':
            ledger.view_records()

        elif choice == '3':
            income, expense, net = ledger.calculate_statistics()
            print(f"Total Income: {income}")
            print(f"Total Expense: {expense}")
            print(f"Net Income: {net}")

        elif choice == '4':
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()