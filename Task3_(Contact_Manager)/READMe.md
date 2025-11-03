# Contact Manager

Simple command-line Contact Management program implemented in Python.

## Purpose
This small script provides an interactive menu to add, search, and display contacts. It is intended as a beginner-friendly exercise to practice basic Python I/O, dictionaries, and control flow.

## Files
- `Contact_Manager.py` — The main script. Run this to start the interactive contact manager.
- `Read.md` — This README file.

## Features
- Add a contact (name + phone number)
- Search for a contact by name
- Display all contacts (sorted by name)
- Simple text-based menu and friendly messages

## Usage
1. Make sure you have Python 3 installed (tested on Python 3.6+).
2. From a terminal, run:

```powershell
python Contact_Manager.py
```

3. Follow the on-screen menu and prompts.

## Example session
(> means user input)

======= Contact Management System =======
1. Add Contact
2. Search Contact
3. Display All Contacts
4. Exit
Enter your choice (1-4): > 1
Enter contact name: > Alice
Enter phone number: > 123-456-7890
✅ Contact 'Alice' added successfully!

Enter your choice (1-4): > 3
📋 Contact List:
➡️ Alice: 123-456-7890

Enter your choice (1-4): > 2
Enter the name to search: > Alice
📞 Alice: 123-456-7890

Enter your choice (1-4): > 4
👋 Exiting Contact Management System. Goodbye!

## Notes & Limitations
- Contacts are stored in an in-memory Python dictionary (`contacts`) only for the duration of the program. Closing the program will lose any added contacts.
- Names are normalized using `.strip().title()` when adding/searching. Phone numbers are stored as-is.
- There is no validation on phone number format.

## Possible Improvements
- Persist contacts to a file (JSON, CSV) or a lightweight database (SQLite).
- Add edit/delete contact functionality.
- Improve phone number validation and allow multiple phone numbers per contact.
- Add command-line arguments to support non-interactive/batch usage.

## Requirements
- Python 3 (3.6+ recommended)

## License
This repository contains educational/demo code and can be used or modified freely.
