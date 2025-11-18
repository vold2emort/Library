from django.db import transaction
from django.db.models import F  # for atomic field updates
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from .models import Book, BorrowedBook


def safe_borrow(user, book_id):
    """ Service to safely borrow a book with concurrency control """
    try:
        with transaction.atomic():  # ensure atomicity
            # Lock the book record for this transaction to prevent race conditions
            book = Book.objects.select_for_update().get(id=book_id)
            if book.stock < 1:
                raise ValidationError("Book is out of stock.")
            
            book.stock = F('stock') - 1  # atomic decrement
            book.save()

            borrowed_book = BorrowedBook.objects.create(
                user=user,
                book=book,
                valid_until= date.today() + timedelta(days=14)  # due date according to policy
            )

            return borrowed_book
    except Book.DoesNotExist:
        raise ValidationError("Book does not exist.")


def return_book(borrowed_book_id):
    # Service to handle book return with concurrency control
    with transaction.atomic(): # ensure atomicity         
        # lock the borrowed book record
        borrowed_book = BorrowedBook.objects.select_for_update().get(id=borrowed_book_id)
        if borrowed_book.is_returned:
            raise ValidationError("Book is already returned.")

        borrowed_book.is_returned = True
        borrowed_book.return_date = date.today()
        borrowed_book.save()

        Book.objects.filter(id=borrowed_book.book.id).update(stock=F('stock') + 1)  # atomic increment on book stock
        
        return borrowed_book




'''
Why services over signals here?
- Signals can lead to hidden side effects and make the flow harder to trace.
- Services provide explicit control over transaction boundaries and error handling.
- Easier to test and maintain business logic in services than in signals.

- Signals cannot handle concurrency because:
    They do not lock database rows
    They run outside the API control flow
    They can be triggered unexpectedly (admin panel, shell, tests)
    They cause inconsistent business logic execution under concurrent requests.

->> Signals cannot prevent real-world race conditions
    
'''
    

