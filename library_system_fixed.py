# library_system.py
import json
import os

class Book:
    # Repræsenterer en bog i bibliotekssystemet.
    def __init__(self, book_id, title, author, copies):
        #Initialiserer en ny bog.

        #Args:
    #     book_id (str): Bogens unikke ID.
    #       title (str): Titel på bogen.
    #     author (str): Forfatter til bogen.
    #      copies (int): Antal tilgængelige kopier.
        self.book_id = book_id
        self.title = title
        self.author = author
        self.copies = copies

    def display_info(self):
        #Viser bogens information i konsollen.
        print(f"[Bog] ID: {self.book_id}\n     Titel: {self.title}\n     Forfatter: {self.author}\n     Kopier: {self.copies}\n")

    def is_available(self):
        #Returnerer True hvis mindst én kopi er tilgængelig
        return self.copies > 0

    def to_dict(self):
        #Konverterer bogen til en ordbog til brug for JSON-gemning.
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "copies": self.copies
        }

    @staticmethod
    def from_dict(data):
        #Opretter et Book-objekt ud fra en ordbog (typisk indlæst fra JSON).
        return Book(data["book_id"], data["title"], data["author"], data["copies"])


class User:
    #Abstrakt brugerklasse, som andre brugertyper arver fra.
    def display_info(self):
        #Skal implementeres af subklasser
        raise NotImplementedError("Denne metode skal implementeres af underklassen")


class Member(User):
    #Repræsenterer et medlem i bibliotekssystemet.
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = []

    def display_info(self):
        #Viser medlemmets oplysninger og lånte bøger.
        borrowed = ', '.join([book.title for book in self.borrowed_books]) or "Ingen"
        print(f"[Medlem] ID: {self.member_id}\n     Navn: {self.name}\n     Lånte bøger: {borrowed}\n")

    def borrow_book(self, book):
        #Forsøger at låne en bog hvis den er tilgængelig.
        if book.is_available():
            self.borrowed_books.append(book)
            book.copies -= 1
            print(f"{self.name} har lånt '{book.title}'")
        else:
            print(f"'{book.title}' er ikke tilgængelig")

    def return_book(self, book):
        #Returnerer en bog hvis den er lånt af medlemmet.
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.copies += 1
            print(f"{self.name} har returneret '{book.title}'")
        else:
            print(f"{self.name} har ikke lånt '{book.title}'")

    def to_dict(self):
        #Konverterer medlem til ordbog til brug for JSON-gemning.
        return {
            "member_id": self.member_id,
            "name": self.name
        }

    @staticmethod
    def from_dict(data):
        #Opretter et Member-objekt ud fra ordbog.
        return Member(data["member_id"], data["name"])


class Library:
    #Håndterer al funktionalitet i biblioteket – bøger, medlemmer, udlån m.m.
    def __init__(self, books_file="books.json", members_file="members.json"):
        self.books_file = books_file
        self.members_file = members_file
        self.books = self.load_books()
        self.members = self.load_members()

    def save_books(self):
        #Gemmer alle bøger til JSON-fil.
        with open(self.books_file, "w") as f:
            json.dump([book.to_dict() for book in self.books.values()], f, indent=4)

    def save_members(self):
        #Gemmer alle medlemmer til JSON-fil.
        with open(self.members_file, "w") as f:
            json.dump([member.to_dict() for member in self.members.values()], f, indent=4)

    def load_books(self):
        #Indlæser bøger fra JSON-fil.
        if not os.path.exists(self.books_file):
            return {}
        with open(self.books_file, "r") as f:
            data = json.load(f)
            return {book["book_id"]: Book.from_dict(book) for book in data}

    def load_members(self):
        #Indlæser medlemmer fra JSON-fil
        if not os.path.exists(self.members_file):
            return {}
        with open(self.members_file, "r") as f:
            data = json.load(f)
            return {member["member_id"]: Member.from_dict(member) for member in data}

    def add_book(self, book):
        #Tilføjer en bog til systemet.
        self.books[book.book_id] = book
        self.save_books()
        print(f"✅ Bogen '{book.title}' er blevet tilføjet.")

    def remove_book(self, book_id):
        #Fjerner en bog baseret på ID.
        if book_id in self.books:
            del self.books[book_id]
            self.save_books()
            print("🗑️ Bog er blevet fjernet.")
        else:
            print("❌ Bog ikke fundet.")

    def update_book(self, book_id, title=None, author=None, copies=None):
        #Opdaterer oplysninger om en eksisterende bog.
        book = self.books.get(book_id)
        if book:
            if title: book.title = title
            if author: book.author = author
            if copies is not None: book.copies = copies
            self.save_books()
            print("🔄 Bog opdateret.")
        else:
            print("❌ Bog ikke fundet.")

    def display_books(self):
        #Viser alle bøger i biblioteket.
        print("\n📚 Liste over bøger i biblioteket:")
        if not self.books:
            print("Ingen bøger i biblioteket.")
        for book in self.books.values():
            book.display_info()

    def add_member(self, member):
        #Tilføjer et medlem til systemet.
        self.members[member.member_id] = member
        self.save_members()
        print(f"✅ Medlem '{member.name}' er blevet tilføjet.")

    def remove_member(self, member_id):
        #Fjerner et medlem baseret på ID.
        if member_id in self.members:
            del self.members[member_id]
            self.save_members()
            print("🗑️ Medlem er blevet fjernet.")
        else:
            print("❌ Medlem ikke fundet.")

    def update_member(self, member_id, name=None):
        #Opdaterer medlemmets navn.
        member = self.members.get(member_id)
        if member:
            if name:
                member.name = name
            self.save_members()
            print("🔄 Medlem opdateret.")
        else:
            print("❌ Medlem ikke fundet.")

    def display_members(self):
        #Viser alle medlemmer i systemet.
        print("\n👥 Liste over medlemmer i systemet:")
        if not self.members:
            print("Ingen medlemmer i systemet.")
        for member in self.members.values():
            member.display_info()

    def issue_book(self, book_id, member_id):
        #Udlåner en bog til et medlem.
        book = self.books.get(book_id)
        member = self.members.get(member_id)
        if book and member:
            member.borrow_book(book)
            self.save_books()
            self.save_members()
        else:
            print("❌ Bog eller medlem ikke fundet.")

    def return_book(self, book_id, member_id):
        #Returnerer en bog fra et medlem.
        book = self.books.get(book_id)
        member = self.members.get(member_id)
        if book and member:
            member.return_book(book)
            self.save_books()
            self.save_members()
        else:
            print("❌ Bog eller medlem ikke fundet.")


def show_menu():
        #Viser hovedmenuen for brugeren
    print("==============================")
    print("📚 Velkommen til Biblioteket 📚")
    print("==============================")
    print("0. ❓ Hjælp / Forklaring af muligheder")
    print("1. ➕ Tilføj bog")
    print("2. 📖 Vis bøger")
    print("3. ✏️ Opdater bog")
    print("4. ❌ Fjern bog")
    print("5. 👤 Tilføj medlem")
    print("6. 👥 Vis medlemmer")
    print("7. ✏️ Opdater medlem")
    print("8. ❌ Fjern medlem")
    print("9. 📚 Udlån bog")
    print("10. 🔁 Returnér bog")
    print("11. 🚪 Afslut")

def handle_choice(choice, lib):
#
#   Håndterer brugerens valg i menuen.
#
#Args:
#    choice (str): Brugerens valg.
#    lib (Library): Instans af bibliotekssystemet.
# 
# Returns:
#     bool: True hvis programmet skal fortsætte, False ellers.
#
    if choice == '0':
        print("""
📘 Hjælpemenu:
0 - Vis denne hjælpemenu
1 - Tilføj en ny bog til biblioteket
2 - Vis alle tilgængelige bøger
3 - Rediger oplysninger om en eksisterende bog
4 - Fjern en bog fra biblioteket
5 - Tilføj et nyt medlem til bibliotekssystemet
6 - Vis alle registrerede medlemmer
7 - Rediger oplysninger om et medlem
8 - Fjern et medlem fra systemet
9 - Udlån en bog til et medlem
10 - Returnér en bog fra et medlem
11 - Afslut programmet
""")
    elif choice == '1':
        print("-- Tilføj ny bog --")
        book_id = input("Bog ID: ")
        title = input("Titel: ")
        author = input("Forfatter: ")
        try:
            copies = int(input("Antal kopier: "))
        except ValueError:
            print("❌ Ugyldigt antal kopier.")
            return True
        lib.add_book(Book(book_id, title, author, copies))
    elif choice == '2':
        lib.display_books()
    elif choice == '3':
        print("-- Opdater bog --")
        book_id = input("Bog ID: ")
        title = input("Ny titel (Enter for at springe over): ")
        author = input("Ny forfatter (Enter for at springe over): ")
        copies = input("Nyt antal kopier (Enter for at springe over): ")
        lib.update_book(book_id, title or None, author or None, int(copies) if copies else None)
    elif choice == '4':
        print("-- Fjern bog --")
        book_id = input("Bog ID: ")
        lib.remove_book(book_id)
    elif choice == '5':
        print("-- Tilføj medlem --")
        member_id = input("Medlems ID: ")
        name = input("Navn: ")
        lib.add_member(Member(member_id, name))
    elif choice == '6':
        lib.display_members()
    elif choice == '7':
        print("-- Opdater medlem --")
        member_id = input("Medlems ID: ")
        name = input("Nyt navn: ")
        lib.update_member(member_id, name)
    elif choice == '8':
        print("-- Fjern medlem --")
        member_id = input("Medlems ID: ")
        lib.remove_member(member_id)
    elif choice == '9':
        print("-- Udlån bog --")
        book_id = input("Bog ID: ")
        member_id = input("Medlems ID: ")
        lib.issue_book(book_id, member_id)
    elif choice == '10':
        print("-- Returnér bog --")
        book_id = input("Bog ID: ")
        member_id = input("Medlems ID: ")
        lib.return_book(book_id, member_id)
    elif choice == '11':
        print("Tak fordi du brugte bibliotekssystemet. Farvel! 👋")
        return False
    else:
        print("❗ Ugyldigt valg. Prøv igen.")
    return True

def run_library_system():
    #Starter bibliotekssystemets hovedloop.
    lib = Library()
    running = True
    while running:
        show_menu()
        choice = input("Indtast et valg (0-11): ")
        running = handle_choice(choice, lib)

#Programstart
if __name__ == "__main__":
    print("""
🌟 VELKOMMEN TIL BIBLIOTEKSSYSTEMET 🌟
Du kan vælge, hvordan du vil starte:
  1. Klassisk menu med alle muligheder
  2. Step-by-step guide for begyndere (kommer snart)
""")
    mode = input("Vælg 1 og tryk Enter: ")
    run_library_system()
