import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User
from circulation.models import Loan
from catalog.models import BookCopy

def run_seed():
    print("Seeding users and loans...")

    departments = ["Computer Science", "Information Technology", "Cybersecurity", "Software Engineering"]
    first_names = ["John", "Jane", "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy", "Mallory", "Peggy", "Sybil", "Trent", "Victor", "Walter", "Sam", "Olivia", "Liam", "Emma", "Noah", "Ava"]
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson"]

    # 1. Create Librarians
    librarians = []
    for i in range(1, 4):
        matric = f"LIB{i:03d}"
        if not User.objects.filter(matric_no=matric).exists():
            lib = User.objects.create_user(
                matric_no=matric,
                password="password123",
                first_name=random.choice(first_names),
                last_name=random.choice(last_names),
                email=f"lib{i}@lautech.edu.ng",
                department="Library Services",
                role=User.Role.LIBRARIAN,
                is_staff=True
            )
            librarians.append(lib)
        else:
            librarians.append(User.objects.get(matric_no=matric))
    print(f"Created {len(librarians)} Librarians.")

    # 2. Create Students
    students = []
    for i in range(1, 51):
        year = random.choice([2019, 2020, 2021, 2022, 2023])
        matric = f"{year}CS{i:03d}"
        if not User.objects.filter(matric_no=matric).exists():
            student = User.objects.create_user(
                matric_no=matric,
                password="password123",
                first_name=random.choice(first_names),
                last_name=random.choice(last_names),
                email=f"student{i}@lautech.edu.ng",
                department=random.choice(departments),
                role=User.Role.MEMBER,
                biometric_enrolled=random.choice([True, True, False])  # 2/3 chance of being enrolled
            )
            students.append(student)
        else:
            students.append(User.objects.get(matric_no=matric))
    print(f"Created {len(students)} Students.")

    # 3. Create Loans
    # Get all available book copies
    available_copies = list(BookCopy.objects.filter(status=BookCopy.Status.AVAILABLE))
    if not available_copies:
        print("No available book copies to create loans. Please run seed_books.py first.")
        return

    now = timezone.now()
    loans_created = 0

    # Let's create about 60 loans (some returned, some active, some overdue)
    for _ in range(60):
        if not available_copies:
            break
        
        copy = random.choice(available_copies)
        available_copies.remove(copy)
        
        student = random.choice(students)
        librarian = random.choice(librarians)
        
        loan_type = random.choice(["returned", "active", "overdue"])
        
        if loan_type == "returned":
            borrowed_date = now - timedelta(days=random.randint(20, 60))
            due_date = borrowed_date + timedelta(days=14)
            returned_date = borrowed_date + timedelta(days=random.randint(1, 15))
            
            Loan.objects.create(
                borrower=student,
                book_copy=copy,
                issued_by=librarian,
                borrowed_at=borrowed_date,
                due_at=due_date,
                returned_at=returned_date
            )
            # Book remains available
            
        elif loan_type == "active":
            borrowed_date = now - timedelta(days=random.randint(1, 10))
            due_date = borrowed_date + timedelta(days=14)
            
            Loan.objects.create(
                borrower=student,
                book_copy=copy,
                issued_by=librarian,
                borrowed_at=borrowed_date,
                due_at=due_date
            )
            # Update book status
            copy.status = BookCopy.Status.ON_LOAN
            copy.save()
            
        elif loan_type == "overdue":
            borrowed_date = now - timedelta(days=random.randint(15, 30))
            due_date = borrowed_date + timedelta(days=14)
            
            Loan.objects.create(
                borrower=student,
                book_copy=copy,
                issued_by=librarian,
                borrowed_at=borrowed_date,
                due_at=due_date
            )
            # Update book status
            copy.status = BookCopy.Status.ON_LOAN
            copy.save()
            
        loans_created += 1

    print(f"Created {loans_created} loan records (Returned, Active, Overdue).")
    print("Done! You can now log in with e.g. matric 'LIB001' (password: password123) to view the librarian dashboard.")

if __name__ == '__main__':
    run_seed()
