# -------------------------------
# Personal Finance Tracker (No Libraries)
# -------------------------------

DATA_FILE = "finance_data.txt"

# Initialize file
def initialize_file():
    try:
        open(DATA_FILE, "x").write("Date,Type,Category,Amount,Description\n")
    except:
        pass  # File already exists

# Add a new transaction
def add_transaction():
    print("\n--- Add Transaction ---")
    date = input("Enter date (YYYY-MM-DD): ")
    t_type = input("Enter type (Income/Expense): ").strip().title()
    if t_type not in ["Income", "Expense"]:
        print("Invalid type! Please enter Income or Expense.")
        return
    category = input("Enter category (e.g., Food, Rent, Salary): ").strip().title()
    amount = input("Enter amount: ").strip()
    description = input("Enter short description: ").strip()

    line = f"{date},{t_type},{category},{amount},{description}\n"
    file = open(DATA_FILE, "a")
    file.write(line)
    file.close()

    print(f"✅ {t_type} of ₹{amount} added under '{category}'.")

# Display all transactions
def display_all():
    print("\n--- All Transactions ---")
    file = open(DATA_FILE, "r")
    lines = file.readlines()[1:]  # Skip header
    file.close()

    if not lines:
        print("No transactions available.")
        return

    for row in lines:
        data = row.strip().split(",")
        print(f"{data[0]} | {data[1]} | {data[2]} | ₹{data[3]} | {data[4]}")

# Generate monthly report
def monthly_report():
    print("\n--- Monthly Report ---")
    month = input("Enter month (YYYY-MM): ").strip()

    file = open(DATA_FILE, "r")
    lines = file.readlines()[1:]  # Skip header
    file.close()

    if not lines:
        print("No transactions to report.")
        return

    income_total = 0
    expense_total = 0
    category_expenses = {}

    for row in lines:
        data = row.strip().split(",")
        date, t_type, category, amount = data[0], data[1], data[2], float(data[3])

        if date.startswith(month):
            if t_type == "Income":
                income_total += amount
            elif t_type == "Expense":
                expense_total += amount
                if category not in category_expenses:
                    category_expenses[category] = 0
                category_expenses[category] += amount

    print(f"\n📅 Report for {month}")
    print("--------------------------------------")
    print(f"Total Income  : ₹{income_total:.2f}")
    print(f"Total Expense : ₹{expense_total:.2f}")
    print(f"Net Savings   : ₹{income_total - expense_total:.2f}")
    print("\n💸 Expense Breakdown by Category:")
    for cat in category_expenses:
        print(f"  {cat}: ₹{category_expenses[cat]:.2f}")
    print("--------------------------------------")

# Main menu
def menu():
    initialize_file()
    while True:
        print("\n========== Personal Finance Tracker ==========")
        print("1. Add Transaction")
        print("2. View All Transactions")
        print("3. Generate Monthly Report")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            add_transaction()
        elif choice == "2":
            display_all()
        elif choice == "3":
            monthly_report()
        elif choice == "4":
            print("👋 Exiting Personal Finance Tracker. Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

# Run the program
menu()