
from database import get_connection, create_table
from datetime import date
import csv


def add_expense():
    description = input("Enter expense description: ").strip()
    category = input("Enter category: ").strip()

    try:
        amount = float(input("Enter amount: "))
        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        expense_date = input(
            "Enter date (YYYY-MM-DD), or press Enter for today: "
        ).strip()

        if not expense_date:
            expense_date = date.today().isoformat()

        # Validate the date
        date.fromisoformat(expense_date)

        if not description or not category:
            print("Description and category are required.")
            return

        with get_connection() as conn:
            conn.execute("""
                INSERT INTO expenses
                (description, category, amount, expense_date)
                VALUES (?, ?, ?, ?)
            """, (description, category, amount, expense_date))

        print("Expense added successfully!")

    except ValueError:
        print("Invalid amount or date. Please try again.")


def view_expenses():
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT id, description, category, amount, expense_date
            FROM expenses
            ORDER BY expense_date DESC, id DESC
        """).fetchall()

    if not rows:
        print("No expenses found.")
        return

    print("\nID | Description | Category | Amount | Date")
    print("-" * 65)

    for row in rows:
        print(
            f"{row[0]} | {row[1]} | {row[2]} | "
            f"{row[3]:.2f} | {row[4]}"
        )


def total_expenses():
    with get_connection() as conn:
        total = conn.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
        """).fetchone()[0]

    print(f"Total expenses: {total:.2f}")


def category_report():
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT category, SUM(amount), COUNT(*)
            FROM expenses
            GROUP BY category
            ORDER BY SUM(amount) DESC
        """).fetchall()

    print("\nCategory-wise Expense Report")

    if not rows:
        print("No expenses found.")
        return

    for category, amount, count in rows:
        print(
            f"{category}: {amount:.2f} "
            f"({count} transactions)"
        )


def filter_by_category():
    category = input("Enter category to search: ").strip()

    with get_connection() as conn:
        rows = conn.execute("""
            SELECT description, amount, expense_date
            FROM expenses
            WHERE LOWER(category) = LOWER(?)
            ORDER BY expense_date DESC
        """, (category,)).fetchall()

    if not rows:
        print("No expenses found for this category.")
        return

    for description, amount, expense_date in rows:
        print(f"{expense_date} | {description} | {amount:.2f}")


def export_to_csv():
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT id, description, category, amount, expense_date
            FROM expenses
            ORDER BY expense_date DESC
        """).fetchall()

    with open("expense_report.csv", "w", newline="",
              encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "ID", "Description", "Category",
            "Amount", "Date"
        ])
        writer.writerows(rows)

    print("Report exported to expense_report.csv")


def main():
    create_table()

    while True:
        print("\n===== EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Calculate Total Expenses")
        print("4. Category-wise Report")
        print("5. Filter by Category")
        print("6. Export Report to CSV")
        print("7. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                add_expense()
            elif choice == "2":
                view_expenses()
            elif choice == "3":
                total_expenses()
            elif choice == "4":
                category_report()
            elif choice == "5":
                filter_by_category()
            elif choice == "6":
                export_to_csv()
            elif choice == "7":
                print("Thank you for using Expense Tracker!")
                break
            else:
                print("Invalid choice. Select 1 to 7.")

        except Exception as error:
            print("An error occurred:", error)


if __name__ == "__main__":
    main()
