# Library Management System

A simple object-oriented Library Management System implemented in Python. It models three core entities—`Book`, `Member`, and `Library`—and exposes both a programmatic API and an interactive command-line interface for managing books and members.

## Features

- Add books with inventory tracking (total vs available copies).
- Register members and track currently borrowed books per member.
- Lend and return books with validation for availability and duplicates.
- Search the catalog by title.
- Generate inventory and per-member reports.
- Interactive CLI menu to perform common operations without writing extra code.

## Project Structure

- `library_management.py`  
  Contains the full implementation:
  - `Book`: encapsulates book metadata, stock, and lending logic.
  - `Member`: tracks borrowed books for each member and enforces one-copy-per-member.
  - `Library`: orchestrates catalog and member registries plus lending/return flows.
  - `_demo()`: scripted sample showcasing typical usage.
  - `run_cli()`: entry point for the interactive command-line experience.

## Getting Started

### Prerequisites

- Python 3.9+ (uses `dataclasses` typing enhancements and `from __future__ import annotations`).

### Setup

1. Clone or download the repository.
2. Open a terminal in the project directory (`Task5_(Library_Management_Sys)`).

### Running the CLI

```bash
python library_management.py
```

You will see a menu similar to:

```
Library Management System
-------------------------
1. Add book
2. Register member
3. Lend book
4. Return book
5. Show inventory report
6. Show member report
7. Search books by title
0. Exit
```

Follow the prompts to manage books and members interactively.

## Programmatic Usage

```python
from library_management import Book, Member, Library

library = Library()
library.add_book(Book("B001", "Clean Code", "Robert C. Martin", 3))
library.register_member(Member("M001", "Alice"))
library.lend_book("B001", "M001")
print(library.member_report("M001"))
# ['Clean Code (B001)']
```

## Testing the Demo Scenario

To run the scripted demonstration instead of the CLI, import the module and call `_demo()`:

```python
from library_management import _demo
_demo()
```

This prints inventory status plus borrowed books for two sample members.

## Extending the Project

Potential enhancements:

- Persist data to files or a database.
- Implement due dates, fines, or reservation queues.
- Add authentication and role-based permissions.
- Build a web or GUI front-end on top of the `Library` API.

## License

This project is provided as-is for educational purposes. Feel free to adapt it for your own learning or applications.
