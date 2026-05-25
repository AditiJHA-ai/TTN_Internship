from datetime import datetime, timedelta
 
 
class Book:
    def __init__(self, isbn, title, author, year):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.is_available = True
 
    def __str__(self):
        status = "Available" if self.is_available else "Checked out"
        return f"[{self.isbn}] '{self.title}' by {self.author} ({self.year}) - {status}"
 
 
class Member:
    def __init__(self, member_id, name, email):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.borrowed_books = []
 
    def __str__(self):
        return f"Member #{self.member_id}: {self.name} ({self.email})"
 
 
class Loan:
    LOAN_DAYS = 14
 
    def __init__(self, book, member):
        self.book = book
        self.member = member
        self.borrow_date = datetime.now()
        self.due_date = self.borrow_date + timedelta(days=self.LOAN_DAYS)
        self.return_date = None
 
    def is_overdue(self):
        if self.return_date:
            return self.return_date > self.due_date
        return datetime.now() > self.due_date
 
    def __str__(self):
        returned = f"Returned: {self.return_date.strftime('%Y-%m-%d')}" if self.return_date else "Not returned"
        overdue = " [OVERDUE]" if self.is_overdue() else ""
        return (
            f"Loan: '{self.book.title}' -> {self.member.name} | "
            f"Due: {self.due_date.strftime('%Y-%m-%d')} | {returned}{overdue}"
        )
 
 
class Library:
    def __init__(self, name):
        self.name = name
        self._books = {}       # isbn -> Book
        self._members = {}     # member_id -> Member
        self._loans = []
 
    def add_book(self, book):
        if book.isbn in self._books:
            raise ValueError(f"Book with ISBN {book.isbn} already exists.")
        self._books[book.isbn] = book
        print(f"Added book: {book.title}")
 
    def register_member(self, member):
        if member.member_id in self._members:
            raise ValueError(f"Member ID {member.member_id} already exists.")
        self._members[member.member_id] = member
        print(f"Registered member: {member.name}")
 
    def borrow_book(self, isbn, member_id):
        if isbn not in self._books:
            raise KeyError(f"Book with ISBN {isbn} not found.")
        if member_id not in self._members:
            raise KeyError(f"Member ID {member_id} not found.")
 
        book = self._books[isbn]
        member = self._members[member_id]
 
        if not book.is_available:
            raise PermissionError(f"'{book.title}' is not available.")
 
        book.is_available = False
        loan = Loan(book, member)
        member.borrowed_books.append(isbn)
        self._loans.append(loan)
        print(f"{member.name} borrowed '{book.title}'. Due: {loan.due_date.strftime('%Y-%m-%d')}")
 
    def return_book(self, isbn, member_id):
        if isbn not in self._books:
            raise KeyError(f"Book with ISBN {isbn} not found.")
        if member_id not in self._members:
            raise KeyError(f"Member ID {member_id} not found.")
 
        book = self._books[isbn]
        member = self._members[member_id]
 
        active_loan = next(
            (l for l in self._loans if l.book.isbn == isbn and l.member.member_id == member_id and not l.return_date),
            None
        )
        if not active_loan:
            raise LookupError(f"No active loan found for '{book.title}' and member '{member.name}'.")
 
        active_loan.return_date = datetime.now()
        book.is_available = True
        member.borrowed_books.remove(isbn)
        overdue_msg = " (OVERDUE)" if active_loan.is_overdue() else ""
        print(f"{member.name} returned '{book.title}'{overdue_msg}.")
 
    def search_books(self, query):
        query = query.lower()
        results = [b for b in self._books.values()
                   if query in b.title.lower() or query in b.author.lower()]
        return results
 
    def list_all_books(self):
        if not self._books:
            print("No books in the library.")
            return
        for book in self._books.values():
            print(f"  {book}")
 
    def list_active_loans(self):
        active = [l for l in self._loans if not l.return_date]
        if not active:
            print("No active loans.")
            return
        for loan in active:
            print(f"  {loan}")
 
 
if __name__ == "__main__":
    lib = Library("City Library")
 
    # Add books
    lib.add_book(Book("978-0-13-468599-1", "Clean Code", "Robert C. Martin", 2008))
    lib.add_book(Book("978-0-20-161622-4", "The Pragmatic Programmer", "Hunt & Thomas", 1999))
    lib.add_book(Book("978-0-59-651798-1", "Fluent Python", "Luciano Ramalho", 2015))
 
    # Register members
    lib.register_member(Member(1, "Alice", "alice@example.com"))
    lib.register_member(Member(2, "Bob", "bob@example.com"))
 
    print("\n--- All Books ---")
    lib.list_all_books()
 
    # Borrow and return
    lib.borrow_book("978-0-13-468599-1", 1)
    lib.borrow_book("978-0-59-651798-1", 2)
 
    print("\n--- Active Loans ---")
    lib.list_active_loans()
 
    lib.return_book("978-0-13-468599-1", 1)
 
    print("\n--- Books After Return ---")
    lib.list_all_books()
 
    # Search
    print("\n--- Search: 'python' ---")
    results = lib.search_books("python")
    for b in results:
        print(f"  {b}")
 
    # Error handling demo
    print("\n--- Error Handling Demo ---")
    try:
        lib.borrow_book("978-0-59-51798-1", 999)
    except KeyError as e:
        print(f"Caught error: {e}")
