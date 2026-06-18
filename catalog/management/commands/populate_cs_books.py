from django.core.management.base import BaseCommand

from catalog.models import Book, BookCopy


CS_BOOKS = [
    {
        "title": "Introduction to Algorithms",
        "author": "Thomas H. Cormen et al.",
        "isbn": "9780262046305",
        "publisher": "MIT Press",
        "publication_year": 2022,
        "description": "Comprehensive algorithms textbook used in core CS courses.",
    },
    {
        "title": "Computer Networking: A Top-Down Approach",
        "author": "James F. Kurose & Keith W. Ross",
        "isbn": "9780136681557",
        "publisher": "Pearson",
        "publication_year": 2021,
        "description": "Networking fundamentals from application layer to physical layer.",
    },
    {
        "title": "Operating System Concepts",
        "author": "Abraham Silberschatz et al.",
        "isbn": "9781119800361",
        "publisher": "Wiley",
        "publication_year": 2021,
        "description": "Classic OS text covering processes, memory, and file systems.",
    },
    {
        "title": "Database System Concepts",
        "author": "Abraham Silberschatz et al.",
        "isbn": "9780078022159",
        "publisher": "McGraw-Hill",
        "publication_year": 2019,
        "description": "Relational databases, SQL, normalization, and transaction processing.",
    },
    {
        "title": "Artificial Intelligence: A Modern Approach",
        "author": "Stuart Russell & Peter Norvig",
        "isbn": "9780134610993",
        "publisher": "Pearson",
        "publication_year": 2020,
        "description": "Foundational AI covering search, logic, learning, and robotics.",
    },
    {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "isbn": "9780132350884",
        "publisher": "Prentice Hall",
        "publication_year": 2008,
        "description": "Best practices for writing readable, maintainable software.",
    },
    {
        "title": "The C Programming Language",
        "author": "Brian W. Kernighan & Dennis M. Ritchie",
        "isbn": "9780131103627",
        "publisher": "Prentice Hall",
        "publication_year": 1988,
        "description": "Definitive introduction to the C programming language.",
    },
    {
        "title": "Design Patterns: Elements of Reusable Object-Oriented Software",
        "author": "Erich Gamma et al.",
        "isbn": "9780201633610",
        "publisher": "Addison-Wesley",
        "publication_year": 1994,
        "description": "Gang of Four patterns for object-oriented design.",
    },
    {
        "title": "Compilers: Principles, Techniques, and Tools",
        "author": "Alfred V. Aho et al.",
        "isbn": "9780321486813",
        "publisher": "Pearson",
        "publication_year": 2006,
        "description": "Dragon book on lexical analysis, parsing, and code generation.",
    },
    {
        "title": "Computer Organization and Design",
        "author": "David A. Patterson & John L. Hennessy",
        "isbn": "9780128201091",
        "publisher": "Morgan Kaufmann",
        "publication_year": 2020,
        "description": "RISC-V edition covering hardware-software interface.",
    },
    {
        "title": "Structure and Interpretation of Computer Programs",
        "author": "Harold Abelson & Gerald Jay Sussman",
        "isbn": "9780262510875",
        "publisher": "MIT Press",
        "publication_year": 1996,
        "description": "SICP — programming paradigms using Scheme.",
    },
    {
        "title": "Code Complete",
        "author": "Steve McConnell",
        "isbn": "9780735619678",
        "publisher": "Microsoft Press",
        "publication_year": 2004,
        "description": "Practical handbook for software construction.",
    },
    {
        "title": "The Algorithm Design Manual",
        "author": "Steven S. Skiena",
        "isbn": "9783030542559",
        "publisher": "Springer",
        "publication_year": 2020,
        "description": "Algorithms with real-world applications and war stories.",
    },
    {
        "title": "Computer Science Illuminated",
        "author": "Nell Dale & John Lewis",
        "isbn": "9781284155617",
        "publisher": "Jones & Bartlett",
        "publication_year": 2017,
        "description": "Broad survey of computer science topics for undergraduates.",
    },
    {
        "title": "Head First Java",
        "author": "Kathy Sierra & Bert Bates",
        "isbn": "9780596009205",
        "publisher": "O'Reilly",
        "publication_year": 2005,
        "description": "Visual, beginner-friendly introduction to Java and OOP.",
    },
    {
        "title": "Python Crash Course",
        "author": "Eric Matthes",
        "isbn": "9781718501105",
        "publisher": "No Starch Press",
        "publication_year": 2023,
        "description": "Hands-on Python for projects, data, and web development.",
    },
    {
        "title": "Discrete Mathematics and Its Applications",
        "author": "Kenneth H. Rosen",
        "isbn": "9781259676512",
        "publisher": "McGraw-Hill",
        "publication_year": 2018,
        "description": "Logic, sets, graphs, and combinatorics for CS students.",
    },
    {
        "title": "Software Engineering",
        "author": "Ian Sommerville",
        "isbn": "9780137035151",
        "publisher": "Pearson",
        "publication_year": 2015,
        "description": "Processes, requirements, design, testing, and project management.",
    },
    {
        "title": "Computer Graphics: Principles and Practice",
        "author": "John F. Hughes et al.",
        "isbn": "9780321399526",
        "publisher": "Addison-Wesley",
        "publication_year": 2013,
        "description": "Rendering, modeling, and interactive graphics pipelines.",
    },
    {
        "title": "Cryptography and Network Security",
        "author": "William Stallings",
        "isbn": "9780138690176",
        "publisher": "Pearson",
        "publication_year": 2022,
        "description": "Symmetric/asymmetric crypto, protocols, and network security.",
    },
]


class Command(BaseCommand):
    help = "Populate the catalogue with 20 Computer Science textbooks."

    def add_arguments(self, parser):
        parser.add_argument(
            "--copies",
            type=int,
            default=2,
            help="Number of copies per book (default: 2).",
        )

    def handle(self, *args, **options):
        copies_per_book = options["copies"]
        created_books = 0
        created_copies = 0

        for index, data in enumerate(CS_BOOKS, start=1):
            book, book_created = Book.objects.get_or_create(
                isbn=data["isbn"],
                defaults={
                    **data,
                    "category": "Computer Science",
                },
            )
            if book_created:
                created_books += 1
            elif book.category != "Computer Science":
                book.category = "Computer Science"
                book.save(update_fields=["category"])

            for copy_num in range(1, copies_per_book + 1):
                copy_code = f"CS-{index:02d}-{copy_num}"
                _, copy_created = BookCopy.objects.get_or_create(
                    copy_code=copy_code,
                    defaults={
                        "book": book,
                        "shelf_location": f"CS-A{index:02d}",
                        "status": BookCopy.Status.AVAILABLE,
                    },
                )
                if copy_created:
                    created_copies += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. {len(CS_BOOKS)} CS books in catalogue "
                f"({created_books} new books, {created_copies} new copies)."
            )
        )
