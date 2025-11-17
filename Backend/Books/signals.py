from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver



@receiver(pre_save, sender='Books.BorrowedBook')    
def book_borrow_return(sender, instance, **kwargs):
    borrowed_book = instance
    bookObj = borrowed_book.book
    if instance._state.adding:  # new instance being created
        if not borrowed_book.is_returned and bookObj.is_available:  # on new borrow
            bookObj.stock -= 1
            bookObj.save()
        else: # trying to borrow when no stock available
            raise ValueError("Book is not available for borrowing.")

    else:   # on update
        old_instance = sender.objects.get(pk=borrowed_book.pk)
        if not old_instance.is_returned and borrowed_book.is_returned: # status changed from False to True
            bookObj.stock += 1      # avoid double incrementing stock if already returned (comparing old and new status)
            bookObj.save()  # save the updated stock   

    ''' Signal to adjust book stock on borrow/return of books 
        must be called before saving BorrowedBook instance to have correct stock update
    '''

