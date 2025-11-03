contacts = {}   # Dictionary to store contacts

def add_contact():
    name = input("Enter contact name: ").strip().title()
    phone = input("Enter phone number: ").strip()
    if name in contacts:
        print(f"⚠️ Contact '{name}' already exists.")
    else:
        contacts[name] = phone
        print(f"✅ Contact '{name}' added successfully!")

def search_contact():
    name = input("Enter the name to search: ").strip().title()
    if name in contacts:
        print(f"📞 {name}: {contacts[name]}")
    else:
        print(f"❌ No contact found with the name '{name}'.")

def display_contacts():
    if contacts:
        print("\n📋 Contact List:")
        for name, phone in sorted(contacts.items()):
            print(f"➡️ {name}: {phone}")
    else:
        print("No contacts available.")

def menu():
    while True:
        print("\n======= Contact Management System =======")
        print("1. Add Contact")
        print("2. Search Contact")
        print("3. Display All Contacts")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            add_contact()
        elif choice == '2':
            search_contact()
        elif choice == '3':
            display_contacts()
        elif choice == '4':
            print("👋 Exiting Contact Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    menu()