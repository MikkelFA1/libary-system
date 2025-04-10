# test_library_system.py

import unittest
import os
from library_system_fixed import Book, Member, Library

class TestLibrarySystem(unittest.TestCase):

    def setUp(self):
        self.test_books_file = "test_books.json"
        self.test_members_file = "test_members.json"
        self.library = Library(self.test_books_file, self.test_members_file)
        self.library.books = {}
        self.library.members = {}

    def tearDown(self):
        if os.path.exists(self.test_books_file):
            os.remove(self.test_books_file)
        if os.path.exists(self.test_members_file):
            os.remove(self.test_members_file)

    def test_add_book(self):
        print("\n📘 Test: Tilføj en bog til biblioteket")
        book = Book("B001", "Bog A – Tilføj", "Forfatter A", 3)
        self.library.add_book(book)
        self.assertIn("B001", self.library.books)

    def test_remove_book(self):
        print("\n🗑️ Test: Fjern en bog fra biblioteket")
        book = Book("B002", "Bog B – Skal Slettet", "Forfatter B", 1)
        self.library.add_book(book)
        self.library.remove_book("B002")
        self.assertNotIn("B002", self.library.books)

    def test_update_book(self):
        print("\n✏️ Test: Opdater en bogs titel og antal kopier")
        book = Book("B003", "Bog C – Før Opdatering", "Forfatter C", 2)
        self.library.add_book(book)
        self.library.update_book("B003", title="Bog C – Efter Opdatering", copies=5)
        updated = self.library.books["B003"]
        self.assertEqual(updated.title, "Bog C – Efter Opdatering")
        self.assertEqual(updated.copies, 5)

    def test_add_member(self):
        print("\n👤 Test: Tilføj et medlem til systemet")
        member = Member("M001", "Medlem A – Tilføj")
        self.library.add_member(member)
        self.assertIn("M001", self.library.members)

    def test_remove_member(self):
        print("\n🗑️ Test: Fjern et medlem fra systemet")
        member = Member("M002", "Medlem B – Skal Slettet")
        self.library.add_member(member)
        self.library.remove_member("M002")
        self.assertNotIn("M002", self.library.members)

    def test_update_member(self):
        print("\n✏️ Test: Opdater et medlems navn")
        member = Member("M003", "Medlem C – Før Opdatering")
        self.library.add_member(member)
        self.library.update_member("M003", name="Medlem C – Efter Opdatering")
        self.assertEqual(self.library.members["M003"].name, "Medlem C – Efter Opdatering")

    def test_issue_and_return_book(self):
        print("\n🔁 Test: Udlån og returnér en bog korrekt")
        book = Book("B004", "Bog D – Udlån/Returnering", "Forfatter D", 1)
        member = Member("M004", "Medlem D – Udlån")
        self.library.add_book(book)
        self.library.add_member(member)

        self.library.issue_book("B004", "M004")
        self.assertEqual(book.copies, 0)
        self.assertIn(book, member.borrowed_books)

        self.library.return_book("B004", "M004")
        self.assertEqual(book.copies, 1)
        self.assertNotIn(book, member.borrowed_books)

    def test_borrow_unavailable_book(self):
        print("\n❌ Test: Prøv at udlåne en bog med 0 kopier (skal fejle korrekt)")
        book = Book("B005", "Bog E – 0 kopier", "Forfatter E", 0)
        member = Member("M005", "Medlem E – Prøver at låne 0 kopier")
        self.library.add_book(book)
        self.library.add_member(member)

        self.library.issue_book("B005", "M005")
        self.assertNotIn(book, member.borrowed_books)
        self.assertEqual(book.copies, 0)

    def test_borrow_nonexistent_book_or_member(self):
        print("\n❌ Test: Ugyldigt ID – prøver at udlåne og returnere ikke-eksisterende bog og medlem")
        self.library.issue_book("B404", "M404")
        self.library.return_book("B404", "M404")

    def test_return_book_not_borrowed(self):
        print("\n❌ Test: Returnér en bog, der ikke er lånt")
        book = Book("B006", "Bog F – Ikke lånt", "Forfatter F", 1)
        member = Member("M006", "Medlem F – Returnerer uden at låne")
        self.library.add_book(book)
        self.library.add_member(member)

        self.library.return_book("B006", "M006")
        self.assertEqual(book.copies, 1)
        self.assertNotIn(book, member.borrowed_books)

    def test_polymorphism_display_info(self):
        print("\n🧬 Test: Polymorfi – display_info() findes i både Book og Member")
        book = Book("B007", "Bog G – Polymorfi", "Forfatter G", 2)
        member = Member("M007", "Medlem G – Polymorfi")
        self.assertTrue(callable(book.display_info))
        self.assertTrue(callable(member.display_info))

if __name__ == "__main__":
    unittest.main()