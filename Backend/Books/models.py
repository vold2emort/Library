from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=50)
    published_date = models.DateField()
    edition = models.CharField(max_length=20)
    author = models.ManyToManyField('Author')
    genre = models.ManyToManyField('Genre')
    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE, related_name='books')
    feature_image = models.ImageField(default='books/default-book.jpg', upload_to='books/', blank=True)
    summary = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Author(models.Model):
    name = models.CharField(max_length=50)    

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    

class Publisher(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    # username, first name, last name, username are already included (enforce them at registration level)
    phone_number = models.CharField(max_length=15, null=True, blank=True)   # needed later for contact (account recovery, notifications, etc.)
    address = models.TextField(null=True, blank=True)   # needed for physical book delivery if applicable
    profile_picture = models.ImageField(default='profiles/user-upload.jpg',  upload_to='profiles/', blank=True)
    bio = models.TextField(null=True, blank=True)
    
    ROLE_TYPES = [
        ('reader', 'Reader'),
        ('librarian', 'Librarian'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_TYPES, default='reader')
    # created_at = models.DateTimeField(auto_now_add=True)  # already included in AbstractUser as date_joined    
    last_modified = models.DateTimeField(auto_now=True)     # tracks last profile update time
    id = models.AutoField(primary_key=True)
    
    # needed fields for user preferences(wishlist)
    favorite_genres = models.ManyToManyField(Genre, blank=True)
    favorite_authors = models.ManyToManyField(Author, blank=True) # user can add favorite authors
    favorite_publishers = models.ManyToManyField(Publisher, blank=True) # user can add favorite publishers
    favorite_books = models.ManyToManyField(Book, blank=True, related_name='favorited_by_user')   # avoid clash with borrowed books relation
    
    # borrowed books tracking
    borrowed_books = models.ManyToManyField(Book, through='BorrowedBook', through_fields=['user', 'book'], # avoid clash with favorite books relation 
                                             blank=True, related_name='borrowed_by_user')   
    

class BorrowedBook(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    
    # only librarian/admin can issue books
    issued_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='issued_books')  # librarian who issued the book
    # track borrow and return dates
    borrow_date = models.DateField(auto_now_add=True)
    valid_until = models.DateField()  # due date for return
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.book.title} borrowed by {self.user.username}'
    

    class Meta:
        constraints = [     # to prevent a user from borrowing the same book twice before returning
            models.UniqueConstraint(
                fields= ['user', 'book', 'is_returned'],
                condition= models.Q(is_returned=False),  # only enforce uniqueness for active borrows (user can borrow same book again after returning)
                name='unique_active_borrow'
            )
        ]        
    ordering = ['-borrow_date']  # recent borrows first