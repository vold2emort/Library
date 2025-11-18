from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from Books.models import Wishlist
import json


@receiver(user_logged_in)
def merge_wishlist_on_login(sender, request, **kwargs):     # no session used in JWT auth
    user = request.user
    wishlist_obj, created = Wishlist.objects.get_or_create(user=user)   # get if exists else create new
    # get wishlist data from forntend local storage
    wishlist = request.data.get('wishlist', '[]')
    json_wishlist = json.loads(wishlist) if isinstance(wishlist, str) else wishlist # only parse if it's a string    

    # for book in json_wishlist:        
    #     book_id = int(book.get('id'))   # work for both dict and Book instances
    #     wishlist_obj.books.add(book_id)  # add book to user's wishlist (duplicates automatically handled)

    [wishlist_obj.books.add(int(book.get('id'))) for book in json_wishlist] # add all books from local storage to user's wishlist
    wishlist_obj.save()     

    print(f"Merged {len(json_wishlist)} wishlist items into user {user.username}'s wishlist on login.")   



'''
Signals cannot handle concurrency because:
    They do not lock database rows
    They run outside the API control flow
    They can be triggered unexpectedly (admin panel, shell, tests)
    They cause inconsistent business logic execution under concurrent requests.


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

    Signal to adjust book stock on borrow/return of books 
    must be called before saving BorrowedBook instance to have correct stock update 


'''