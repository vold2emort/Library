import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_system.settings")
django.setup()

import threading
from Books.models import CustomUser, Book, BorrowedBook

def attempt_borrow(user, book_id):
    try:
        book = Book.objects.get(id=book_id)
        borrowed_book = BorrowedBook.objects.create(
            user=user,
            book=book,
            valid_until='2024-12-31'  # example due date
        )
        print(f"User {user.username} borrowed \t")
    except Exception as e:
        print(f"User {user.username} failed to borrow \t")


## assume book has only 1 stock available
book_id = 7
print("\nStarting concurrent borrow attempts...")
book = Book.objects.get(id=book_id)
print(f'Initial Book stock: {book.stock}\n')

users = CustomUser.objects.filter(is_active=True)[:5]  # get first 5 active users
# create threads for concurrent borrow attempts
threads = []
print(f"Race Started: {len(users)} users attempting to borrow book ID {book_id} concurrently.\n")
for user in users:
    t = threading.Thread(target=attempt_borrow, args=(user, book_id))
    threads.append(t)   # prepare all threads


[t.start() for t in threads]   # start all threads

[t.join() for t in threads]    # wait for all to finish

print("\nRace Ended.")
print(f'Final Book stock: {Book.objects.get(id=book_id).stock}')