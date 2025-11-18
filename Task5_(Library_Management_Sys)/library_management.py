"""
Simple Library Management System demonstrating core OOP concepts.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Book:
    """
    Represents a single book title in the library's catalogue.

    The class encapsulates the state (metadata, inventory counts) and behaviour
    (borrowing / returning) associated with a book.
    """

    book_id: str
    title: str
    author: str
    copies_total: int
    copies_available: int = field(init=False)

    def __post_init__(self) -> None:
        if self.copies_total < 1:
            raise ValueError("A book must have at least one copy.")
        self.copies_available = self.copies_total

    def is_available(self) -> bool:
        """Return True when at least one copy can be borrowed."""
        return self.copies_available > 0

    def checkout(self) -> None:
        """Reduce available copies by one when a member borrows the book."""
        if not self.is_available():
            raise RuntimeError(f"No copies of '{self.title}' are currently available.")
        self.copies_available -= 1

    def checkin(self) -> None:
        """Increase available copies when a member returns the book."""
        if self.copies_available >= self.copies_total:
            raise RuntimeError(f"All copies of '{self.title}' are already in the library.")
        self.copies_available += 1

    def __str__(self) -> str:  # pragma: no cover - convenience only
        return f"{self.title} by {self.author} ({self.copies_available}/{self.copies_total} available)"


@dataclass
class Member:
    """
    Represents a library member capable of borrowing books.

    Each member tracks the books currently borrowed to prevent duplicates and to
    keep the Library class slim.
    """

    member_id: str
    name: str
    borrowed_books: Dict[str, Book] = field(default_factory=dict)

    def borrow_book(self, book: Book) -> None:
        """Record that this member borrowed the provided book."""
        if book.book_id in self.borrowed_books:
            raise RuntimeError(f"{self.name} already borrowed '{book.title}'.")
        book.checkout()
        self.borrowed_books[book.book_id] = book

    def return_book(self, book_id: str) -> Book:
        """Return the borrowed book to the caller so the library can process it."""
        if book_id not in self.borrowed_books:
            raise KeyError(f"{self.name} has not borrowed a book with id '{book_id}'.")
        book = self.borrowed_books.pop(book_id)
        book.checkin()
        return book

    def list_borrowed_books(self) -> List[str]:
        """Provide a neat representation of currently borrowed books."""
        return [f"{book.title} ({book.book_id})" for book in self.borrowed_books.values()]


class Library:
    """
    High-level facade that coordinates books and members.

    Responsibilities:
    - Maintain catalog of `Book` objects.
    - Register members.
    - Facilitate lending, returning, and simple lookups.
    """

    def __init__(self) -> None:
        self._books: Dict[str, Book] = {}
        self._members: Dict[str, Member] = {}

    # --- catalog management -------------------------------------------------
    def add_book(self, book: Book) -> None:
        if book.book_id in self._books:
            raise KeyError(f"Book with id '{book.book_id}' already exists.")
        self._books[book.book_id] = book

    def find_book(self, book_id: str) -> Optional[Book]:
        return self._books.get(book_id)

    def search_books_by_title(self, keyword: str) -> List[Book]:
        keyword = keyword.lower()
        return [book for book in self._books.values() if keyword in book.title.lower()]

    # --- member management --------------------------------------------------
    def register_member(self, member: Member) -> None:
        if member.member_id in self._members:
            raise KeyError(f"Member with id '{member.member_id}' already exists.")
        self._members[member.member_id] = member

    def find_member(self, member_id: str) -> Optional[Member]:
        return self._members.get(member_id)

    # --- lending operations -------------------------------------------------
    def lend_book(self, book_id: str, member_id: str) -> None:
        book = self._require_book(book_id)
        member = self._require_member(member_id)
        member.borrow_book(book)

    def accept_return(self, book_id: str, member_id: str) -> None:
        member = self._require_member(member_id)
        member.return_book(book_id)

    # --- helpers ------------------------------------------------------------
    def inventory_report(self) -> List[str]:
        """Produce a readable snapshot of the current catalog."""
        report = []
        for book in sorted(self._books.values(), key=lambda b: b.title):
            status = f"{book.copies_available}/{book.copies_total}"
            report.append(f"{book.title} by {book.author} — {status} available")
        return report

    def member_report(self, member_id: str) -> List[str]:
        member = self._require_member(member_id)
        return member.list_borrowed_books()

    def _require_book(self, book_id: str) -> Book:
        book = self.find_book(book_id)
        if not book:
            raise KeyError(f"Book '{book_id}' not found.")
        return book

    def _require_member(self, member_id: str) -> Member:
        member = self.find_member(member_id)
        if not member:
            raise KeyError(f"Member '{member_id}' not found.")
        return member


def _demo() -> None:  # pragma: no cover - illustrative usage
    """Showcase basic behaviour without tying into any UI layer."""
    library = Library()

    # Populate catalogue
    library.add_book(Book("B001", "1984", "George Orwell", 3))
    library.add_book(Book("B002", "Clean Code", "Robert C. Martin", 2))

    # Register members
    alice = Member("M001", "Alice")
    bob = Member("M002", "Bob")
    library.register_member(alice)
    library.register_member(bob)

    # Borrow and return workflow
    library.lend_book("B001", "M001")
    library.lend_book("B002", "M002")
    library.accept_return("B001", "M001")

    print("Inventory:")
    for line in library.inventory_report():
        print(f"- {line}")

    print("\nAlice borrowed:", library.member_report("M001"))
    print("Bob borrowed:", library.member_report("M002"))


def run_cli() -> None:
    """Simple interactive interface driven by standard input."""
    library = Library()

    menu = """
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
"""

    actions = {
        "1": lambda: _cli_add_book(library),
        "2": lambda: _cli_register_member(library),
        "3": lambda: _cli_lend_book(library),
        "4": lambda: _cli_return_book(library),
        "5": lambda: _cli_show_inventory(library),
        "6": lambda: _cli_show_member_report(library),
        "7": lambda: _cli_search_books(library),
    }

    while True:
        print(menu)
        choice = input("Select an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if not action:
            print("Invalid choice, please try again.\n")
            continue
        try:
            action()
        except (KeyError, RuntimeError, ValueError) as exc:
            print(f"Error: {exc}\n")


def _cli_add_book(library: Library) -> None:
    book_id = input("Book id: ").strip()
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    copies = int(input("Number of copies: ").strip())
    library.add_book(Book(book_id, title, author, copies))
    print(f"Book '{title}' added.\n")


def _cli_register_member(library: Library) -> None:
    member_id = input("Member id: ").strip()
    name = input("Name: ").strip()
    library.register_member(Member(member_id, name))
    print(f"Member '{name}' registered.\n")


def _cli_lend_book(library: Library) -> None:
    book_id = input("Book id to lend: ").strip()
    member_id = input("Member id: ").strip()
    library.lend_book(book_id, member_id)
    print("Book lent successfully.\n")


def _cli_return_book(library: Library) -> None:
    book_id = input("Book id to return: ").strip()
    member_id = input("Member id: ").strip()
    library.accept_return(book_id, member_id)
    print("Book returned successfully.\n")


def _cli_show_inventory(library: Library) -> None:
    report = library.inventory_report()
    if not report:
        print("No books in inventory.\n")
        return
    print("Inventory:")
    for line in report:
        print(f"- {line}")
    print()


def _cli_show_member_report(library: Library) -> None:
    member_id = input("Member id: ").strip()
    borrowed = library.member_report(member_id)
    if not borrowed:
        print("Member has no borrowed books.\n")
        return
    print("Borrowed books:")
    for line in borrowed:
        print(f"- {line}")
    print()


def _cli_search_books(library: Library) -> None:
    keyword = input("Keyword: ").strip()
    results = library.search_books_by_title(keyword)
    if not results:
        print("No books match that keyword.\n")
        return
    print("Matches:")
    for book in results:
        print(f"- {book.title} by {book.author} ({book.copies_available}/{book.copies_total})")
    print()


if __name__ == "__main__":
    run_cli()